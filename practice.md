# AI Client Discovery - Development Practice

Status: Draft v0.1. These rules apply to all work on this project and are intended for Claude Code.

## 1. Read first

Before proposing or changing code, read **SPEC.md**, **practice.md**, and **architecture.md** (once created), plus the current GitHub Issue. If any file or issue does not exist yet, say so; do not fabricate its contents. Check repository state and the active branch before editing. `practice.md` is not automatically loaded by Claude Code; add a minimal `CLAUDE.md` pointing to these files **only after owner approval**.

## 2. Ticket loop - one issue, one branch, one PR

For every approved development ticket:

1. **Read** the GitHub Issue, restate the user-visible goal and acceptance criteria, and verify consistency with SPEC.md. Flag out-of-scope work.
2. **Plan** in 3-5 concise lines: approach, files affected, risks, and tests. **Pause for owner approval** before implementation.
3. **Branch** from current main (or approved base) with a branch name linked to the Issue, e.g. `12-autosave-draft`. Never implement a feature directly on main.
4. **Build** the smallest change that meets the Issue's acceptance criteria. Keep the implementation and dependencies minimal.
5. **Test/Eval**: add/run reproducible unit/integration tests for deterministic code changes. For changes to model prompts, tools, or behavior, run relevant AI Eval cases and compare with the recorded baseline; if real model calls are unavailable, state clearly that live Evals were **not run** and use explicit mocked/fixture-based checks only. Fix failures before proposing a merge.
6. **Docs**: update SPEC.md / architecture.md / test notes if a real decision or behavior changed, in the same PR. Record the reason and tradeoff for architectural decisions.
7. **Commit** only approved, reviewed files with an informative message including the Issue number, e.g. `Add draft autosave (#12)`.
8. **PR**: open a Pull Request referencing the Issue, summarizing the change, test results, Eval results/baseline if applicable, open risks, and reviewer checklist. **Do not merge without explicit owner approval.** A discovered unrelated bug becomes a separate Issue.

Do not assume that creating a PR, passing a check, or receiving a green badge grants merge approval.

## 3. GitHub project management

Use a single GitHub Project board with **To do**, **In progress**, **Done**. Every work item is a trackable GitHub Issue with: objective, context/why, in scope/out of scope, acceptance criteria ("Done when"), test plan, and owner/status where useful. Keep tasks small and demonstrable. Link PRs to Issues. The board is a planning artifact, not a substitute for Git history.

During the documentation-only setup stage, do **not** initialize Git, create repositories/issues/branches, write application code, or push anything unless the owner explicitly approves that stage.

## 4. User experience, content, and scope

- All user-facing UI: **Hebrew RTL**, including screen titles, buttons, validation messages, status labels, and questionnaire wording. Documentation/code can use English. **Mobile-first responsive design is mandatory for BOTH respondent and admin views; mobile must support all core features, not just display a shrunk desktop layout.**
- Preserve the 18 original questions and their grouping in the initial template; don't silently rewrite them. Maintain editable template versions and snapshots for sent instances.
- Use the approved **Turquoise / Coral / Sunshine** palette from SPEC.md meaningfully across the UI. Keep accessible contrast; don't use color as the sole status indicator.
- Before finishing any UI Issue, review at 320px, 375px, 768px and 1280px widths, checking RTL, touch targets, navigation, text wrapping, keyboard focus, validation, and absence of horizontal overflow. Test at least one representative respondent and admin mobile flow. Clearly distinguish automated checks from manual inspection.
- On phones, render repeatable stakeholder rows as stacked cards; make the admin dashboard and questionnaire editor mobile-usable; keep notes, save status and progress accessible. Do not depend on hover, drag-only interactions, or wide tables.
- Lead-facing views must **never** expose admin notes, other companies' data, internal reasoning, or AI reports.
- Keep users' own answers verbatim and separate from AI-created interpretations. Show uncertain points explicitly.
- Use simple, maintainable modules; avoid premature abstractions, full CRM features, and unsolicited additions.
- Never invent real business names, personal contact details, or client responses. Mark fictional demo fixtures as such.

## 5. Persistence, privacy, and AI cost rules

- Each keystroke updates local draft state immediately; backend saves must be debounced and acknowledged. Never call an LLM for autosave, progress bars, timestamps, or session tracking.
- Avoid save races, dropped writes, duplicate form submission, and duplicate AI runs; write regression tests for these cases.
- Track sessions and approximate active time without keylogging or invasive analytics.
- Keep credentials, access tokens, and personal data out of Git history and frontend bundles. Use `.env` only locally, always ignored by Git; publish `.env.example` with variable names only if needed.
- Do not commit client questionnaire responses, phone numbers, email addresses, or proprietary business information. Use fictional fixtures.
- Never provision or use a paid service, metered API, hosting plan, or production deployment without **upfront cost disclosure and explicit owner approval**. Prefer free local tools and mocked AI for CI.
- No live Anthropic/OpenAI API calls are authorized merely because a model name appears in docs. Ask before incurring model costs or transmitting actual client data.
- Treat questionnaire links as sensitive capabilities; plan authentication/authorization and expiration/revocation. An unguessable link is not administrator authentication.

## 6. Tests, evaluations, and evidence

- **Tests** assert deterministic outcomes: validation, template snapshot behavior, contact extraction rules, debounced saves, offline recovery behavior, progress percentages, session counting, note authorization, and final submission semantics.
- **Evals** assess AI follow-up quality and internal summary: relevancy, no repeated questions, no fabricated facts, limit of five, sensitivity handling, source-grounding and uncertainty. Some Eval checks can be exact (structured JSON, maximum count, tool choices), others use a documented rubric.
- Store representative synthetic cases in `evals/` and a repeatable evaluation script. A fake-model test is not evidence of real-model quality. Where possible, document real before/after performance and run/cost; never fabricate metrics.
- Use GitHub Actions to run **free, reproducible, network-independent code tests on PRs**. Never require secrets or charged AI calls in default CI.
- If checks fail, fix and rerun; never weaken or remove tests simply to show green status.

## 7. Architecture and deployment boundary

- Document component diagrams, flows, storage schema, request/response lifecycle, runtime placement, rate and size limits, security model, and decision rationale in `architecture.md`.
- The lesson asks for **Design, Place, Manage, Test/Eval**, not Deployment. Planning future hosting is appropriate; actually deploying to Railway or any cloud service is **out of scope** until separately approved.
- Avoid introducing infrastructure just for the assignment. A small local backend and local database are acceptable for the learning demo if the rationale is documented.

## 8. Communication and approval gates

Respond concisely with: work done, files changed, commands/tests run and actual results, unresolved items, the exact next proposed action. Prefer a short question only when a missing decision is truly blocking; otherwise make a conservative, documented proposal.

**Never without explicit owner approval**:
- Push to `main`, merge PRs, delete branches, or rewrite history.
- Add paid dependencies, make live AI calls, or deploy.
- Change original questionnaire language or approved product scope.
- Modify or delete production/real client data.
- Turn internal AI draft analysis into automatically sent client advice.

## 9. First session instructions

If starting from an empty folder, begin by reviewing these documents with the owner. Next propose a small `architecture.md`, a minimal repository structure, and a GitHub Issues/Project plan aligned with the four lesson phases. **Stop for owner approval before generating application code or interacting with GitHub.**
