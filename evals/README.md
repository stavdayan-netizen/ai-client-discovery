# Evals: AI follow-up question generation

Evaluates the planned feature "propose 0 to 5 follow-up questions after the client fills in the
questionnaire". It does not call any API and needs no keys. Criteria, anchors and thresholds:
`rubric.md` (fixed before any run).

| Path | What it is |
|---|---|
| `cases/` | Six synthetic Hebrew questionnaires (the only thing a model sees, via `prompts/followups_v1.md`) |
| `labels/` | Hidden labels per case (expected gaps, acceptable targets, not-applicable items, limits) |
| `prompts/` | Generation prompt and grading prompt (versioned) |
| `rubric.md` | Hard checks, metrics, graded criteria with anchors, thresholds |
| `checks.py`, `report.py`, `run_evals.py`, `baseline.py` | Exact checks, scoring and report, CLI, simulated baseline |
| `runs/<run_id>/` | Saved inputs and raw outputs of one run (`run.json` records provenance) |
| `reports/<run_id>.md` | The readable report of that run |

Two kinds of run are kept strictly apart, and the labels are enforced by the code and by tests:

- `simulated-baseline`: a rule-based baseline, regenerated and checked in CI. Labelled **SIMULATED,
  not a model evaluation**.
- `claude-code-subagents`: a genuine model run orchestrated by hand through Claude Code subagents
  (see the run's `run.json` and report for the method and its limits). Labelled **REAL-MODEL**.

```bash
python -m evals.run_evals simulate          # regenerate the simulated baseline run and report
python -m evals.run_evals prepare RUN_ID    # write the model-visible generation prompts
python -m evals.run_evals prepare-grading RUN_ID
python -m evals.run_evals report RUN_ID     # re-score a saved run, write its report
python -m evals.run_evals check             # verify all stored runs and reports (used by CI)
```

Re-scoring saved outputs is deterministic. Generating new model outputs is not: a new generation is a
new run with its own id and report.
