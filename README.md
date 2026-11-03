# AI Client Discovery

A small internal tool for an AI implementation consultancy. After an initial fit call, a team member creates a lead and sends a personalized Hebrew (RTL) discovery questionnaire. The lead fills it in (with autosave, draft and resume), answers a few AI-suggested follow-up questions, and submits. The team then reviews the answers, private notes and a draft AI analysis before the next discovery conversation.

This is a learning project for the AiDO Lesson 9 assignment. All data in it is synthetic.

## The four assignment phases

| Phase | What it covers | Where |
|---|---|---|
| **Design** | What we build and why | `SPEC.md`, `architecture.md` |
| **Place** | Where components run, limits, secrets, cost assumptions (plan only) | `architecture.md` (section 8) |
| **Manage** | GitHub repo, Project board, small Issues, a branch and PR per Issue | `practice.md`, GitHub Issues and Project |
| **Test/Eval** | Automated tests, simulated AI Evals, responsive checks, CI | `tests/`, `evals/`, `.github/workflows/ci.yml` (added in later Issues) |

## Status

Early development. The application skeleton, database schema and questionnaire seed exist (Issue #2); the screens come in later Issues. Architecture is approved for the local assignment MVP.

The development plan is nine GitHub Issues, done one at a time in order, each with its own branch and Pull Request (see `architecture.md`, section 14): documentation and setup; skeleton, database and questionnaire seed; admin dashboard, leads and links; respondent UI; autosave and progress tracking; mock AI follow-ups, submission and analysis; admin results, contacts and notes; automated tests, simulated Evals, responsive checks and CI; editable questionnaire template.

## Planned stack

Python, FastAPI, SQLite, HTML, CSS and vanilla JavaScript. No Node.js or frontend frameworks. A deterministic mock AI provider is used first; real AI and real-model Evals will be added only after explicit approval.

## Running locally

Requirements: Python 3.12. Nothing is deployed, and no paid service or live AI call is used.

```bash
python -m venv .venv
.venv\Scripts\activate           # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python -m app.seed               # creates data/app.db (git-ignored) with template v1 and fictional demo leads
python -m app                    # starts the server on http://127.0.0.1:8000
```

- `python -m app` is the supported launcher. It listens on localhost only and refuses to start on any other address. The application has **no authentication yet**, so it must never be exposed to a network (see `architecture.md`, sections 9.1 to 9.3).
- Optional settings (`HOST`, `PORT`, `DATABASE_PATH`, `AI_PROVIDER`) come from environment variables or a git-ignored `.env` file copied from `.env.example`. Only the `mock` AI provider exists.
- Run the checks: `ruff check .`, `ruff format --check .` and `python -m pytest`. The same checks run in GitHub Actions on every Pull Request.

## Out of scope

**Deployment is out of scope.** The app is designed to run locally only, bound to localhost, with no admin authentication and synthetic data only. Authentication and role-based access are mandatory before any deployment or use with real client data (see `architecture.md`, section 9.3).

## Working on this project

Read `SPEC.md`, `architecture.md` and `practice.md` first. Work proceeds one Issue, one branch, one Pull Request, with owner approval before merging.

- Issues and the board: GitHub Issues #1 to #9 in the private Project "AI Client Discovery" (To do / In progress / Done).
- New Issues use `.github/ISSUE_TEMPLATE/task.md`; Pull Requests use `.github/pull_request_template.md`.
- Phase labels: `phase:design`, `phase:place`, `phase:manage`, `phase:test-eval`.
