"""Command line for the Eval harness. Offline only: no network, no API calls, no keys.

Commands:
  simulate                 run the rule-based baseline; write its run and report (SIMULATED)
  prepare RUN_ID           write the model-visible generation prompts of a run
  prepare-grading RUN_ID   write the grading prompts, once the raw outputs are saved
  report RUN_ID            re-score a stored run and write its report
  check                    verify every stored run and report is current (used by CI)
"""

import argparse
import json
import sys

from evals import baseline
from evals.cases import (
    GENERATION_PROMPT,
    RUNS_DIR,
    case_ids,
    inputs_sha256,
    load_case,
    render_generation_prompt,
    render_grading_prompt,
)
from evals.report import (
    KIND_SIMULATED,
    RunError,
    load_run,
    report_is_current,
    run_dir,
    write_report,
)

SIMULATED_RUN_ID = "simulated-baseline"


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def simulated_run_files() -> dict:
    """Everything the simulated run consists of, as {relative path: text}."""
    run = {
        "run_id": SIMULATED_RUN_ID,
        "kind": KIND_SIMULATED,
        "label": "SIMULATED baseline (not a model)",
        "is_simulated": True,
        "generator": "evals/baseline.py (deterministic rule-based baseline)",
        "generation_prompt_version": GENERATION_PROMPT,
        "inputs_sha256": inputs_sha256(),
    }
    files = {"run.json": json.dumps(run, ensure_ascii=False, indent=2) + "\n"}
    for case_id in case_ids():
        output = baseline.generate(load_case(case_id))
        files[f"outputs/{case_id}.raw.txt"] = (
            json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        )
    return files


def cmd_simulate() -> int:
    for relative, text in simulated_run_files().items():
        _write(run_dir(SIMULATED_RUN_ID) / relative, text)
    md_path, _ = write_report(SIMULATED_RUN_ID)
    print(f"Wrote {md_path}")
    return 0


def cmd_prepare(run_id: str) -> int:
    for case_id in case_ids():
        prompt = render_generation_prompt(load_case(case_id))
        _write(run_dir(run_id) / "prompts" / f"{case_id}.md", prompt)
    print(f"Wrote {len(case_ids())} generation prompts to {run_dir(run_id) / 'prompts'}")
    return 0


def cmd_prepare_grading(run_id: str) -> int:
    for case_id in case_ids():
        raw = (run_dir(run_id) / "outputs" / f"{case_id}.raw.txt").read_text(encoding="utf-8")
        prompt = render_grading_prompt(load_case(case_id), raw)
        _write(run_dir(run_id) / "grading_prompts" / f"{case_id}.md", prompt)
    print(f"Wrote {len(case_ids())} grading prompts")
    return 0


def cmd_report(run_id: str) -> int:
    try:
        md_path, _ = write_report(run_id)
    except RunError as error:
        print(f"Refusing to write a report: {error}", file=sys.stderr)
        return 2
    print(f"Wrote {md_path}")
    return 0


def cmd_check() -> int:
    problems: list[str] = []
    # The simulated baseline must regenerate exactly as committed.
    for relative, text in simulated_run_files().items():
        path = run_dir(SIMULATED_RUN_ID) / relative
        stored = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.is_file() else None
        if stored != text:
            problems.append(f"{SIMULATED_RUN_ID}/{relative} differs from a fresh simulated run")
    # Every stored run must re-score to exactly its committed report.
    runs = sorted(p.name for p in RUNS_DIR.iterdir() if (p / "run.json").is_file())
    for run_id in runs:
        load_run(run_id)
        problems += [f"{run_id}: {p}" for p in report_is_current(run_id)]
    if problems:
        print("Eval check FAILED:", *problems, sep="\n- ", file=sys.stderr)
        return 1
    print(f"Eval check OK: {len(runs)} stored run(s) re-score to their committed reports.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m evals.run_evals", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("simulate")
    sub.add_parser("check")
    for name in ("prepare", "prepare-grading", "report"):
        sub.add_parser(name).add_argument("run_id")
    args = parser.parse_args(argv)
    if args.command == "simulate":
        return cmd_simulate()
    if args.command == "check":
        return cmd_check()
    if args.command == "prepare":
        return cmd_prepare(args.run_id)
    if args.command == "prepare-grading":
        return cmd_prepare_grading(args.run_id)
    return cmd_report(args.run_id)


if __name__ == "__main__":
    raise SystemExit(main())
