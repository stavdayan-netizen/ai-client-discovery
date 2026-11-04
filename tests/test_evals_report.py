"""Labelling rules, reproducibility and the committed reports."""

import json
import shutil

import pytest

from evals import report as report_module
from evals.cases import RUNS_DIR, case_ids, inputs_sha256
from evals.checks import THRESHOLDS
from evals.report import (
    KIND_REAL,
    KIND_SIMULATED,
    RunError,
    build_report,
    report_is_current,
    validate_run,
)
from evals.run_evals import SIMULATED_RUN_ID, main, simulated_run_files


def real_run(**overrides):
    run = {
        "run_id": "r",
        "kind": KIND_REAL,
        "label": "REAL-MODEL (test)",
        "is_simulated": False,
        "model": "some-model",
        "model_source": "stated by the environment",
        "method": "subagents",
        "operator": "assistant",
        "date": "2026-01-01",
        "generation_prompt_version": "followups_v1",
        "grading_prompt_version": "grading_v1",
        "inputs_sha256": inputs_sha256(),
        "human_spot_check": "pending",
    }
    return {**run, **overrides}


def simulated_run(**overrides):
    run = {
        "kind": KIND_SIMULATED,
        "label": "SIMULATED baseline",
        "is_simulated": True,
        "inputs_sha256": inputs_sha256(),
    }
    return {**run, **overrides}


# ---- labelling rules: a simulated result can never be presented as real ----------------------


def test_valid_runs_pass_validation():
    assert validate_run(real_run()) == []
    assert validate_run(simulated_run()) == []


def test_a_simulated_run_cannot_be_marked_real():
    assert validate_run(simulated_run(is_simulated=False))
    assert validate_run(simulated_run(label="REAL-MODEL baseline"))


def test_only_a_documented_real_run_may_claim_is_simulated_false():
    assert validate_run(simulated_run(is_simulated=False, kind="something-else"))
    assert validate_run(real_run(kind="something-else"))


@pytest.mark.parametrize(
    "missing", ["model", "model_source", "method", "operator", "date", "inputs_sha256"]
)
def test_a_real_run_needs_its_provenance(missing):
    assert any(missing in e for e in validate_run(real_run(**{missing: ""})))


def test_a_real_run_cannot_be_labelled_simulated_or_flagged_simulated():
    assert validate_run(real_run(is_simulated=True))
    assert validate_run(real_run(label="SIMULATED baseline"))


def test_results_are_refused_when_cases_or_labels_changed_after_the_run():
    errors = validate_run(simulated_run(inputs_sha256="0" * 64))
    assert any("stale" in e for e in errors)


def test_report_generation_refuses_an_invalid_run(tmp_path, monkeypatch):
    run_dir = tmp_path / "runs" / "bad"
    (run_dir / "outputs").mkdir(parents=True)
    (run_dir / "run.json").write_text(
        json.dumps(simulated_run(is_simulated=False)), encoding="utf-8"
    )
    monkeypatch.setattr(report_module, "RUNS_DIR", tmp_path / "runs")
    with pytest.raises(RunError):
        build_report("bad")


def test_cli_refuses_to_write_a_mislabelled_report(tmp_path, monkeypatch, capsys):
    run_dir = tmp_path / "runs" / "bad"
    run_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text(json.dumps(real_run(model="")), encoding="utf-8")
    monkeypatch.setattr(report_module, "RUNS_DIR", tmp_path / "runs")
    assert main(["report", "bad"]) == 2
    assert "Refusing" in capsys.readouterr().err


# ---- the committed simulated baseline ---------------------------------------------------------


def test_simulated_baseline_is_clearly_labelled():
    markdown, as_json = build_report(SIMULATED_RUN_ID)
    assert markdown.startswith("# Evaluation report: SIMULATED")
    assert "NOT a model evaluation" in markdown
    assert "Real-model Evals: not part of this report" in markdown
    data = json.loads(as_json)
    assert data["run"]["is_simulated"] is True
    assert all(c["grades"] is None for c in data["cases"])
    assert all(g["verdict"] == "NOT ASSESSED" for g in data["aggregate"]["graded"].values())


def test_simulated_baseline_regenerates_exactly_as_committed():
    for relative, text in simulated_run_files().items():
        stored = (RUNS_DIR / SIMULATED_RUN_ID / relative).read_text(encoding="utf-8")
        assert stored.replace("\r\n", "\n") == text


def test_every_committed_run_rescores_to_its_committed_report():
    runs = [p.name for p in RUNS_DIR.iterdir() if (p / "run.json").is_file()]
    assert SIMULATED_RUN_ID in runs
    for run_id in runs:
        assert report_is_current(run_id) == []


def test_reports_are_deterministic():
    assert build_report(SIMULATED_RUN_ID) == build_report(SIMULATED_RUN_ID)


def test_report_check_detects_a_tampered_output(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    shutil.copytree(RUNS_DIR / SIMULATED_RUN_ID, runs / SIMULATED_RUN_ID)
    reports = tmp_path / "reports"
    reports.mkdir()
    for suffix in ("md", "json"):
        shutil.copy(
            RUNS_DIR.parent / "reports" / f"{SIMULATED_RUN_ID}.{suffix}", reports / f"x.{suffix}"
        )
        shutil.copy(reports / f"x.{suffix}", reports / f"{SIMULATED_RUN_ID}.{suffix}")
    monkeypatch.setattr(report_module, "RUNS_DIR", runs)
    monkeypatch.setattr(report_module, "REPORTS_DIR", reports)
    assert report_is_current(SIMULATED_RUN_ID) == []
    (runs / SIMULATED_RUN_ID / "outputs" / "case_02.raw.txt").write_text(
        '{"follow_up_questions": []}', encoding="utf-8"
    )
    assert report_is_current(SIMULATED_RUN_ID)


# ---- thresholds are the pre-registered ones ---------------------------------------------------


def test_thresholds_match_the_written_rubric():
    rubric = (RUNS_DIR.parent / "rubric.md").read_text(encoding="utf-8")
    assert THRESHOLDS == {
        "hard_checks": 1.0,
        "gap_recall": 0.70,
        "precision": 0.60,
        "graded_criterion": 1.5,
    }
    assert "| Hard checks passed (all cases, all checks) | 100% |" in rubric
    assert "at least 0.70" in rubric and "at least 0.60" in rubric and "at least 1.5" in rubric


def test_grade_parsing_accepts_only_scores_0_1_2():
    good = json.dumps(
        {
            k: {"score": 2, "justification": "ok"}
            for k in ("relevance", "factual_accuracy", "no_invented_information")
        }
    )
    scores, error = report_module._grade(good)
    assert error is None and scores["relevance"]["score"] == 2
    bad = good.replace('"score": 2', '"score": 3', 1)
    assert report_module._grade(bad)[0] is None
    assert report_module._grade("garbage")[0] is None
    assert report_module._grade(None) == (None, None)


def test_every_case_has_an_output_in_the_simulated_run():
    for case_id in case_ids():
        assert (RUNS_DIR / SIMULATED_RUN_ID / "outputs" / f"{case_id}.raw.txt").is_file()
