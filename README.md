# AI Client Discovery

A small internal tool for an AI implementation consultancy. After an initial fit call, a team member creates a lead and sends a personalized Hebrew (RTL) discovery questionnaire. The lead fills it in (with autosave, draft and resume), answers a few AI-suggested follow-up questions, and submits. The team then reviews the answers, private notes and a draft AI analysis before the next discovery conversation.

This is a learning project. All data in it is synthetic.

## AiDO Lesson 9 - Assignment Overview

**Status (as of 2026-11-04).** Design, placement and project management are in place, and the first slices are built: the localhost-only application skeleton, the database schema, the questionnaire template (the 18 original questions) and a first AI Evaluation. There are no user-facing screens yet. Issues #1 and #2 are done; the Evaluation part of #8 is done (its browser-test part is still open); #3 to #7 and #9 are not started.

| Phase | Where to look |
|---|---|
| **Design** | [`SPEC.md`](SPEC.md) (what to build and why), [`architecture.md`](architecture.md) (components, data model, flows, decision log D-1 to D-27) |
| **Place** | [`architecture.md`](architecture.md), section 8 (where each part runs, limits, secrets, cost assumptions) and section 9 (security model and its limits). Planning only: nothing is deployed |
| **Manage** | [GitHub Project board](https://github.com/users/stavdayan-netizen/projects/1) (To do / In progress / Done); [Issues #1 to #9](https://github.com/stavdayan-netizen/ai-client-discovery/issues); merged Pull Requests [#10](https://github.com/stavdayan-netizen/ai-client-discovery/pull/10) (Issue #1), [#11](https://github.com/stavdayan-netizen/ai-client-discovery/pull/11) (Issue #2), [#12](https://github.com/stavdayan-netizen/ai-client-discovery/pull/12) (Issue #8, Evaluation part); rules in [`practice.md`](practice.md); [Issue template](.github/ISSUE_TEMPLATE/task.md) and [PR template](.github/pull_request_template.md); labels `phase:design`, `phase:place`, `phase:manage`, `phase:test-eval` |
| **Test/Eval** | Automated tests in [`tests/`](tests); GitHub Actions workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) ([runs](https://github.com/stavdayan-netizen/ai-client-discovery/actions)); real-model Evaluation report [`evals/reports/real-2026-11-04-claude-code.md`](evals/reports/real-2026-11-04-claude-code.md); criteria and thresholds [`evals/rubric.md`](evals/rubric.md); how it works [`evals/README.md`](evals/README.md) |

Every Issue was done on its own branch with its own Pull Request, with owner approval before each merge. The repository and the Project board are public, and all data in them is synthetic.

### Passing tests are not the same as passing the Evaluation

These are two different things, and they have different results:

- **Automated tests: passing.** 166 tests pass locally and in GitHub Actions, together with lint and an offline check that the stored Evaluation reports still match their data. They show that the code behaves as specified (localhost-only guard, database rules, questionnaire seed, Evaluation scoring and report labelling).
- **Real-model Evaluation: thresholds not all met.** A genuine model (Claude, run through Claude Code subagents, no API calls) generated follow-up questions for six synthetic Hebrew questionnaires, judged against criteria and thresholds fixed in advance. Result: hard checks 52 of 54 (**fail**), gap recall 0.88 (pass), precision 0.70 (pass), and the three graded criteria 1.17, 1.17 and 1.33 out of 2 against a 1.5 threshold (**fail**). The failures are recorded as measured, together with the owner's manual review of two cases and the limitations of the method. Six cases and one run are an illustration, not a quality guarantee.
- A separate **simulated** baseline (fixed rules, not a model) is labelled as such and says nothing about model quality.

### Important limits

**This application is not deployed and is not ready for real client data.** It runs on localhost only, has no authentication, and holds only fictional demo data. Authentication and role-based access are mandatory before any deployment or use with real client information (see [`architecture.md`](architecture.md), section 9.3).

## Planned stack

Python, FastAPI, SQLite, HTML, CSS and vanilla JavaScript. No Node.js or frontend frameworks. A deterministic mock AI provider is used first; a real AI provider and API-based Evals will be added only after explicit approval.

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
- Run the checks: `ruff check .`, `ruff format --check .`, `python -m pytest` and `python -m evals.run_evals check`. The same checks run in GitHub Actions on every Pull Request.

## Working on this project

Read `SPEC.md`, `architecture.md` and `practice.md` first. The development plan is nine GitHub Issues (see `architecture.md`, section 14), done one at a time, each with its own branch and Pull Request, merged only with owner approval.
