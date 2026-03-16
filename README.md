# Job Search Agent

An AI-powered career assistant that helps you find relevant job opportunities, tailor your resume, draft cover letters, prepare for interviews, and benchmark salaries — all grounded in your actual resume content.

---

## Contents

| File | Purpose |
|---|---|
| `YCH_PRADEEP_STARTEGY_2026.pdf` | Source resume (Pradeep YCH) |
| `system_prompt.md` | Agent system prompt defining role, capabilities, and behaviour rules |
| `agent.py` | Python CLI that runs the Job Search Agent interactively |
| `requirements.txt` | Python dependencies |

---

## Quick Start

### 1. Install dependencies

    pip install -r requirements.txt

### 2. Set your OpenAI API key

    export OPENAI_API_KEY=sk-...

### 3. Run the agent

    # Pre-loads the bundled resume automatically
    python agent.py

    # Provide a different resume PDF
    python agent.py --resume /path/to/your_resume.pdf

    # Start without a pre-loaded resume (agent will ask you to paste it)
    python agent.py --no-resume

### 4. Optional environment variables

| Variable | Default | Description |
|---|---|---|
| OPENAI_API_KEY | (required) | Your OpenAI API key |
| OPENAI_BASE_URL | OpenAI default | Override for local/custom endpoints |
| OPENAI_MODEL | gpt-4o | Model to use |

---

## Agent Capabilities

The agent can assist with six core tasks:

1. **Job Role Matching** - Suggests the most relevant roles with fit scores and evidence from your resume.
2. **Job Search Strategy** - Recommends platforms, company types, and target markets.
3. **Resume Tailoring** - Rewrites bullet points to match a specific job description (JD) with ATS optimisation.
4. **Cover Letter Drafting** - Writes a tailored cover letter aligned to a JD.
5. **Interview Preparation** - Generates likely questions with STAR-format answer guidance.
6. **Salary Benchmarking** - Provides salary ranges and negotiation advice by role and location.
