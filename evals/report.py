"""Scoring a stored run and rendering its report. Everything here is deterministic and offline."""

import json
from pathlib import Path

from evals.cases import (
    GENERATION_PROMPT,
    GRADING_PROMPT,
    REPORTS_DIR,
    RUNS_DIR,
    case_ids,
    inputs_sha256,
    load_case,
    load_labels,
)
from evals.checks import (
    HARD_CHECKS,
    THRESHOLDS,
    parse_output,
    run_hard_checks,
    run_metrics,
)

KIND_SIMULATED = "simulated-baseline"
KIND_REAL = "claude-code-subagents"
REAL_REQUIRED_FIELDS = (
    "label",
    "model",
    "model_source",
    "method",
    "operator",
    "date",
    "generation_prompt_version",
    "grading_prompt_version",
    "inputs_sha256",
)
GRADED = (
    ("relevance", "Relevance"),
    ("factual_accuracy", "Factual accuracy of the rationale"),
    ("no_invented_information", "Avoidance of invented information"),
)


class RunError(ValueError):
    """The run's provenance or inputs are not acceptable for a report."""


def run_dir(run_id: str) -> Path:
    return RUNS_DIR / run_id


def load_run(run_id: str) -> dict:
    return json.loads((run_dir(run_id) / "run.json").read_text(encoding="utf-8"))


def validate_run(run: dict) -> list[str]:
    """Labelling rules: a simulated run can never be reported as real, and vice versa."""
    errors: list[str] = []
    kind, simulated = run.get("kind"), run.get("is_simulated")
    if kind == KIND_SIMULATED:
        if simulated is not True:
            errors.append("a simulated baseline run must have is_simulated = true")
        if not str(run.get("label", "")).startswith("SIMULATED"):
            errors.append("a simulated run's label must start with SIMULATED")
    elif kind == KIND_REAL:
        if simulated is not False:
            errors.append("a real-model run must have is_simulated = false")
        if not str(run.get("label", "")).startswith("REAL-MODEL"):
            errors.append("a real-model run's label must start with REAL-MODEL")
        errors += [f"missing provenance field: {f}" for f in REAL_REQUIRED_FIELDS if not run.get(f)]
    else:
        errors.append(f"unknown run kind: {kind!r}")
    if simulated is False and kind != KIND_REAL:
        errors.append("only a documented real-model run may have is_simulated = false")
    if run.get("inputs_sha256") and run["inputs_sha256"] != inputs_sha256():
        errors.append(
            "cases, labels, prompts or rubric changed since this run: its results are stale"
        )
    return errors


def _grade(raw: str | None) -> tuple[dict | None, str | None]:
    if raw is None:
        return None, None
    text = raw.strip()
    start, end = text.find("{"), text.rfind("}")
    try:
        data = json.loads(text[start : end + 1])
        scores = {}
        for key, _ in GRADED:
            score = data[key]["score"]
            if score not in (0, 1, 2) or isinstance(score, bool):
                return None, f"{key}: score must be 0, 1 or 2"
            scores[key] = {"score": score, "justification": str(data[key]["justification"])}
        return scores, None
    except (ValueError, KeyError, TypeError) as error:
        return None, f"unreadable grade ({type(error).__name__})"


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def score_run(run_id: str) -> dict:
    run = load_run(run_id)
    errors = validate_run(run)
    if errors:
        raise RunError("; ".join(errors))
    directory = run_dir(run_id)
    cases = []
    for case_id in case_ids():
        case, labels = load_case(case_id), load_labels(case_id)
        raw = _read(directory / "outputs" / f"{case_id}.raw.txt")
        if raw is None:
            raise RunError(f"missing output for {case_id}")
        data, error = parse_output(raw)
        checks = run_hard_checks(case, labels, data, error)
        metrics = run_metrics(labels, data)
        grades, grade_error = _grade(_read(directory / "grades" / f"{case_id}.raw.txt"))
        cases.append(
            {
                "case_id": case_id,
                "title": case["title"],
                "company": case["company"],
                "description": case["description"],
                "labels": labels,
                "valid_output": data is not None,
                "questions": data["follow_up_questions"] if data else [],
                "hard_checks": checks,
                "metrics": metrics,
                "grades": grades,
                "grade_error": grade_error,
            }
        )
    return {"run": run, "cases": cases, "aggregate": _aggregate(cases)}


def _verdict(value: float | None, threshold: float) -> str:
    if value is None:
        return "NOT ASSESSED"
    return "PASS" if value >= threshold - 1e-9 else "FAIL"


def _aggregate(cases: list[dict]) -> dict:
    checks = [c for case in cases for c in case["hard_checks"].values()]
    passed = sum(1 for c in checks if c["passed"])
    rate = passed / len(checks)
    recall = sum(c["metrics"]["gap_recall"] for c in cases) / len(cases)
    precision = sum(c["metrics"]["precision"] for c in cases) / len(cases)
    graded: dict[str, float | None] = {}
    for key, _ in GRADED:
        scores = [c["grades"][key]["score"] for c in cases if c["grades"]]
        graded[key] = sum(scores) / len(scores) if scores else None
    return {
        "hard_checks": {
            "passed": passed,
            "total": len(checks),
            "value": rate,
            "threshold": THRESHOLDS["hard_checks"],
            "verdict": _verdict(rate, THRESHOLDS["hard_checks"]),
        },
        "gap_recall": {
            "value": recall,
            "threshold": THRESHOLDS["gap_recall"],
            "verdict": _verdict(recall, THRESHOLDS["gap_recall"]),
        },
        "precision": {
            "value": precision,
            "threshold": THRESHOLDS["precision"],
            "verdict": _verdict(precision, THRESHOLDS["precision"]),
        },
        "graded": {
            key: {
                "value": graded[key],
                "threshold": THRESHOLDS["graded_criterion"],
                "verdict": _verdict(graded[key], THRESHOLDS["graded_criterion"]),
            }
            for key, _ in GRADED
        },
    }


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.2f}"


def render_report(scored: dict, run_id: str) -> str:
    run, cases, agg = scored["run"], scored["cases"], scored["aggregate"]
    simulated = run["is_simulated"]
    lines: list[str] = []
    add = lines.append

    add(f"# Evaluation report: {run['label']}")
    add("")
    if simulated:
        add(
            "> **SIMULATED. This is NOT a model evaluation.** The results below come from a "
            "deterministic rule-based baseline (`evals/baseline.py`), not from an AI model. They only "
            "show that the evaluation pipeline works and give a labelled reference point. "
            "**Real-model Evals: not part of this report.**"
        )
    else:
        add(
            "> **REAL-MODEL EVALUATION** (manually orchestrated through Claude Code subagents on the "
            "owner's existing subscription; no API calls, no API keys). The outputs below were produced "
            "by a genuine language model. Model identity and the isolation of the generation step are "
            "documented by the operator and are **not independently verified**. This evaluates the "
            "follow-up task itself, not the application's future integration code."
        )
    add("")
    add("## Summary")
    add("")
    add("| Measure | Result | Threshold | Verdict |")
    add("|---|---|---|---|")
    hc = agg["hard_checks"]
    add(
        f"| Hard checks passed | {hc['passed']}/{hc['total']} ({hc['value']:.0%}) | "
        f"{hc['threshold']:.0%} | **{hc['verdict']}** |"
    )
    add(
        f"| Mean gap recall | {_fmt(agg['gap_recall']['value'])} | "
        f">= {agg['gap_recall']['threshold']:.2f} | **{agg['gap_recall']['verdict']}** |"
    )
    add(
        f"| Mean precision | {_fmt(agg['precision']['value'])} | "
        f">= {agg['precision']['threshold']:.2f} | **{agg['precision']['verdict']}** |"
    )
    for key, name in GRADED:
        g = agg["graded"][key]
        result = _fmt(g["value"]) + (" / 2" if g["value"] is not None else " (not graded)")
        add(
            f"| Mean graded score: {name} | {result} | >= {g['threshold']:.1f} | **{g['verdict']}** |"
        )
    add("")
    add(
        "Thresholds were fixed before any run (`evals/rubric.md`) and were not changed after "
        "results were seen. Six cases and one run are an illustration, not a statistical result."
    )
    add("")

    add("## What was evaluated")
    add("")
    add(
        "The planned feature: after a client fills in the Hebrew discovery questionnaire, the system "
        "proposes **0 to 5 follow-up questions** (in Hebrew, optional for the client), each with an "
        "internal rationale and the ids of the related questionnaire items. Good behaviour means "
        "asking about real gaps and important unknowns, staying quiet when nothing is missing, not "
        "asking about topics the client marked not applicable, never asking for secrets or personal "
        "data, never inventing facts, and ignoring instructions hidden in the client's answers."
    )
    add("")

    add("## The six synthetic cases")
    add("")
    add("All cases are fictional and marked as such. Each is a complete 18-question questionnaire.")
    add("")
    add("| Case | Fictional business | What it tests |")
    add("|---|---|---|")
    for c in cases:
        add(f"| {c['case_id']} | {c['company']} | {c['description']} |")
    add("")

    add("## Criteria and scoring")
    add("")
    add("**Hard checks** (exact, pass or fail, computed by code):")
    add("")
    for cid, name in HARD_CHECKS:
        add(f"- {cid}: {name}")
    add("")
    add(
        "**Gap recall**: share of the case's expected gaps that some question targets. "
        "**Precision**: share of questions that target an expected gap or an acceptable item. "
        "**Graded criteria** (0 to 2, scored by a separate grader against written anchors): "
        "relevance, factual accuracy of the rationale, avoidance of invented information. "
        "Full definitions and anchors: `evals/rubric.md`."
    )
    add("")

    add("## Results by case")
    add("")
    add(
        "| Case | Questions | Hard checks | Failed checks | Gap recall | Precision | "
        "Relevance | Accuracy | No invention |"
    )
    add("|---|---|---|---|---|---|---|---|---|")
    for c in cases:
        checks = c["hard_checks"]
        failed = [cid for cid, r in checks.items() if not r["passed"]]
        grades = c["grades"]
        cells = [str(grades[k]["score"]) if grades else "n/a" for k, _ in GRADED]
        add(
            f"| {c['case_id']} | {len(c['questions'])} | "
            f"{sum(1 for r in checks.values() if r['passed'])}/{len(checks)} | "
            f"{', '.join(failed) or 'none'} | {_fmt(c['metrics']['gap_recall'])} | "
            f"{_fmt(c['metrics']['precision'])} | {' | '.join(cells)} |"
        )
    add("")

    add("## Details by case")
    for c in cases:
        add("")
        add(f"### {c['case_id']}: {c['title']}")
        add("")
        lb = c["labels"]
        add(
            f"Labels (hidden from the model): expected gaps {lb['expected_gaps'] or 'none'}; "
            f"acceptable targets {lb['acceptable_targets'] or 'none'}; "
            f"not applicable {lb['must_not_target'] or 'none'}; "
            f"question limit {lb['max_questions']}."
        )
        add("")
        if not c["valid_output"]:
            add(f"**Output was not valid:** {c['hard_checks']['H1']['detail']}")
            add("")
        if not c["questions"]:
            add("**No follow-up questions** were proposed.")
        for n, q in enumerate(c["questions"], start=1):
            add(f"{n}. {q['text']}")
            add(f"   - Rationale: {q['rationale']}")
            add(f"   - Related items: {', '.join(q['source_question_ids']) or '(none)'}")
        add("")
        failed = [(cid, r) for cid, r in c["hard_checks"].items() if not r["passed"]]
        if failed:
            add("Failed hard checks:")
            for cid, r in failed:
                add(f"- {cid} ({r['name']}): {r['detail'] or 'failed'}")
        else:
            add("All hard checks passed.")
        add("")
        add(
            f"Targeted items: {c['metrics']['targeted'] or 'none'}. "
            f"Gap recall {_fmt(c['metrics']['gap_recall'])}, precision "
            f"{_fmt(c['metrics']['precision'])}, off-target questions {c['metrics']['off_target']}."
        )
        if c["grades"]:
            add("")
            add("Grader scores:")
            for key, name in GRADED:
                g = c["grades"][key]
                add(f"- {name}: **{g['score']}** ({g['justification']})")
        elif c["grade_error"]:
            add("")
            add(f"Grader output could not be read: {c['grade_error']}")

    add("")
    add("## Limitations")
    add("")
    add("- Six cases and a single run: an illustration, not statistically meaningful.")
    add(
        "- The cases and their labels were written by the project team (an AI assistant and the "
        "owner). The hidden labels reflect one view of what a good follow-up is."
    )
    if simulated:
        add(
            "- This is a rule-based baseline. It says nothing about the quality of any AI model, and "
            "its rules were not tuned on the labels."
        )
    else:
        add(
            "- Generation and grading were done by models of the same family, so scores may favour the "
            "model. The grader did not see the labels or the deterministic results."
        )
        add(
            "- Isolation of the generation step is by construction (labels, rubric and grading prompt "
            "were moved out of the repository while it ran, and each agent received only its own "
            "prompt and was told not to use tools). Tool use by the agents cannot be audited."
        )
        add(
            "- Model output is not deterministic: a second run would give different questions. "
            "Re-scoring the saved outputs is deterministic; re-generating them is not."
        )
        add(
            "- The model identifier is the one stated by the session environment (subagents inherit "
            "the session model by default). It was not independently verified."
        )
        add(
            "- Raw outputs were copied into files by the orchestrating assistant. They were not edited, "
            "and no case was re-run."
        )
        add(f"- Human spot-check of the grader's scores by the owner: {run['human_spot_check']}.")
    add(
        "- H7 (no request for secrets) is a pattern-based heuristic, and H8 only checks numbers. "
        "Other kinds of invented information are judged by the grader in genuine runs."
    )
    add("")

    add("## Conclusions")
    add("")
    analysis = _read(run_dir(run_id) / "analysis.md")
    if analysis:
        add(
            "*Written after the results were seen. Numbers above are computed; this text is "
            "interpretation.*"
        )
        add("")
        add(analysis.strip())
    else:
        add(
            "No genuine model was evaluated in this report, so no conclusion about model quality is "
            "drawn. The baseline's verdicts only show how the checks behave."
        )
    add("")

    add("## Provenance and reproducibility")
    add("")
    add(
        f"- Run id: `{run_id}`; run kind: `{run['kind']}`; is_simulated: `{str(simulated).lower()}`"
    )
    if not simulated:
        for key in (
            "date",
            "model",
            "model_source",
            "method",
            "operator",
            "generation_prompt_version",
            "grading_prompt_version",
        ):
            add(f"- {key}: {run[key]}")
    else:
        add(f"- generator: {run['generator']}")
    add(f"- Fingerprint of cases, labels, prompts and rubric: `{run['inputs_sha256']}`")
    add(
        f"- Files: `evals/runs/{run_id}/` (run.json, prompts, raw outputs"
        f"{', raw grades' if not simulated else ''}) and this report."
    )
    add(
        f"- Re-score offline: `python -m evals.run_evals report {run_id}` regenerates this report "
        f"byte for byte from the saved files; `python -m evals.run_evals check` verifies it."
    )
    add(f"- Prompts used: `{GENERATION_PROMPT}`" + ("" if simulated else f", `{GRADING_PROMPT}`"))
    add("")
    return "\n".join(lines)


def report_paths(run_id: str) -> tuple[Path, Path]:
    return REPORTS_DIR / f"{run_id}.md", REPORTS_DIR / f"{run_id}.json"


def build_report(run_id: str) -> tuple[str, str]:
    scored = score_run(run_id)
    markdown = render_report(scored, run_id)
    as_json = json.dumps(scored, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return markdown + "\n", as_json


def write_report(run_id: str) -> tuple[Path, Path]:
    markdown, as_json = build_report(run_id)
    md_path, json_path = report_paths(run_id)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown, encoding="utf-8", newline="\n")
    json_path.write_text(as_json, encoding="utf-8", newline="\n")
    return md_path, json_path


def report_is_current(run_id: str) -> list[str]:
    """Problems found when re-scoring the saved run and comparing with the committed report."""
    try:
        markdown, as_json = build_report(run_id)
    except RunError as error:
        return [str(error)]
    md_path, json_path = report_paths(run_id)
    problems = []
    for path, expected in ((md_path, markdown), (json_path, as_json)):
        actual = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.is_file() else None
        if actual != expected:
            problems.append(f"{path.name} is missing or differs from the re-scored result")
    return problems
