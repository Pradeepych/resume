#!/usr/bin/env python3
"""
Job Search Agent — CLI interface.

Reads the system prompt from system_prompt.md and runs an interactive
conversation with an OpenAI-compatible chat model to assist with job searching.

Usage:
    python agent.py [--resume PATH_TO_RESUME_PDF]

Environment variables:
    OPENAI_API_KEY   – required; your OpenAI (or compatible) API key.
    OPENAI_BASE_URL  – optional; override the API base URL (e.g. for local models).
    OPENAI_MODEL     – optional; model name to use (default: gpt-4o).
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    sys.exit(
        "openai package not found. Install dependencies with:\n"
        "  pip install -r requirements.txt"
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_system_prompt(path: Path) -> str:
    """Load the agent system prompt from a markdown file."""
    if not path.exists():
        sys.exit(f"System prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def extract_resume_text(pdf_path: Path) -> str:
    """Extract plain text from a PDF resume file."""
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        text = extract_text(str(pdf_path))
        return text.strip()
    except ImportError:
        sys.exit(
            "pdfminer.six is required to read PDF files.\n"
            "Install dependencies with:  pip install -r requirements.txt"
        )
    except Exception as exc:
        sys.exit(f"Failed to read PDF '{pdf_path}': {exc}")


def build_client() -> OpenAI:
    """Create an OpenAI client from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "OPENAI_API_KEY environment variable is not set.\n"
            "Export it before running:  export OPENAI_API_KEY=sk-..."
        )
    kwargs: dict = {"api_key": api_key}
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


# ---------------------------------------------------------------------------
# Conversation loop
# ---------------------------------------------------------------------------

GREETING = (
    "Welcome to the Job Search Agent!\n"
    "Type your message and press Enter. Type 'quit' or 'exit' to stop.\n"
    + "-" * 60
)


def run_agent(system_prompt: str, resume_text: str | None, model: str) -> None:
    """Run the interactive CLI conversation."""
    client = build_client()

    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    # Pre-load the resume so the agent can reference it immediately.
    if resume_text:
        messages.append(
            {
                "role": "user",
                "content": (
                    "Here is my resume. Please parse it and confirm what you "
                    "have extracted.\n\n" + resume_text
                ),
            }
        )

    print(GREETING)

    # Prime the conversation with the opening assistant turn when a resume is
    # pre-loaded, so the user sees the extraction summary right away.
    if resume_text:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        assistant_msg = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})
        print(f"\nAssistant:\n{assistant_msg}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
        except Exception as exc:
            print(f"[Error communicating with API: {exc}]")
            continue

        assistant_msg = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})
        print(f"\nAssistant:\n{assistant_msg}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = Path(__file__).parent

    parser = argparse.ArgumentParser(
        description="Job Search Agent — AI-powered career assistant."
    )
    parser.add_argument(
        "--resume",
        type=Path,
        default=repo_root / "YCH_PRADEEP_STARTEGY_2026.pdf",
        help="Path to a PDF resume file (default: YCH_PRADEEP_STARTEGY_2026.pdf).",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Start without pre-loading a resume (agent will ask for one).",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "gpt-4o"),
        help="OpenAI model to use (default: gpt-4o).",
    )
    args = parser.parse_args()

    system_prompt = load_system_prompt(repo_root / "system_prompt.md")

    resume_text: str | None = None
    if not args.no_resume:
        resume_path: Path = args.resume
        if resume_path.exists():
            resume_text = extract_resume_text(resume_path)
        else:
            print(
                f"[Warning] Resume file not found at '{resume_path}'. "
                "Starting without pre-loaded resume."
            )

    run_agent(system_prompt, resume_text, args.model)


if __name__ == "__main__":
    main()
