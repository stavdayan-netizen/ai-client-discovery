# AI Client Discovery

A small internal tool for an AI implementation consultancy. After an initial fit call, a team member creates a lead and sends a personalized Hebrew (RTL) discovery questionnaire. The lead fills it in (with autosave, draft and resume), answers a few AI-suggested follow-up questions, and submits. The team then reviews the answers, private notes and a draft AI analysis before the next discovery conversation.

This is a learning project for the AiDO Lesson 9 assignment. All data in it is synthetic.

## The four assignment phases

| Phase | What it covers | Where |
|---|---|---|
| **Design** | What we build and why | `SPEC.md`, `architecture.md` |
| **Place** | Where components run, limits, secrets, cost assumptions (plan only) | `architecture.md` (section 8) |
| **Manage** | GitHub repo, Project board, small Issues, a branch and PR per Issue | `practice.md`, GitHub Issues and Project |
| **Test/Eval** | Automated tests, simulated AI Evals, responsive checks, CI | `tests/`, `evals/`, `.github/workflows/ci.yml` (added in later milestones) |

## Status

Planning and setup stage. No application code yet. Architecture is approved for the local assignment MVP.

## Planned stack

Python, FastAPI, SQLite, HTML, CSS and vanilla JavaScript. No Node.js or frontend frameworks. A deterministic mock AI provider is used first; real AI and real-model Evals will be added only after explicit approval.

## Out of scope

**Deployment is out of scope.** The app is designed to run locally only, bound to localhost, with no admin authentication and synthetic data only. Authentication and role-based access are mandatory before any deployment or use with real client data (see `architecture.md`, section 9.3).

## Working on this project

Read `SPEC.md`, `architecture.md` and `practice.md` first. Work proceeds one Issue, one branch, one Pull Request, with owner approval before merging.
