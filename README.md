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

Planning and setup stage. No application code yet. Architecture is approved for the local assignment MVP.

The development plan is nine GitHub Issues, done one at a time in order, each with its own branch and Pull Request (see `architecture.md`, section 14): documentation and setup; skeleton, database and questionnaire seed; admin dashboard, leads and links; respondent UI; autosave and progress tracking; mock AI follow-ups, submission and analysis; admin results, contacts and notes; automated tests, simulated Evals, responsive checks and CI; editable questionnaire template.

## Planned stack

Python, FastAPI, SQLite, HTML, CSS and vanilla JavaScript. No Node.js or frontend frameworks. A deterministic mock AI provider is used first; real AI and real-model Evals will be added only after explicit approval.

## Running locally

*Placeholder: the application does not exist yet. These instructions become real when Issue #2 (application skeleton) is merged.*

Planned shape (see `architecture.md`, section 8.1):

1. Install Python 3 (exact version to be pinned in Issue #2).
2. Create and activate a virtual environment, then install the dependencies: `pip install -r requirements.txt`.
3. Optionally copy `.env.example` to `.env` (git-ignored; names only, no secrets are needed).
4. Start the server on localhost only: `uvicorn app.main:app --host 127.0.0.1`.

Nothing is deployed, and no paid service or live AI call is used.

## Out of scope

**Deployment is out of scope.** The app is designed to run locally only, bound to localhost, with no admin authentication and synthetic data only. Authentication and role-based access are mandatory before any deployment or use with real client data (see `architecture.md`, section 9.3).

## Working on this project

Read `SPEC.md`, `architecture.md` and `practice.md` first. Work proceeds one Issue, one branch, one Pull Request, with owner approval before merging.

- Issues and the board: GitHub Issues #1 to #9 in the private Project "AI Client Discovery" (To do / In progress / Done).
- New Issues use `.github/ISSUE_TEMPLATE/task.md`; Pull Requests use `.github/pull_request_template.md`.
- Phase labels: `phase:design`, `phase:place`, `phase:manage`, `phase:test-eval`.
