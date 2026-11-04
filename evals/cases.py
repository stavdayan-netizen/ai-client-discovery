"""Loading Eval cases and rendering the model-visible prompts."""

import hashlib
import json
from pathlib import Path

from app.seed import load_template_v1

EVALS_DIR = Path(__file__).resolve().parent
CASES_DIR = EVALS_DIR / "cases"
LABELS_DIR = EVALS_DIR / "labels"
PROMPTS_DIR = EVALS_DIR / "prompts"
RUBRIC_PATH = EVALS_DIR / "rubric.md"
RUNS_DIR = EVALS_DIR / "runs"
REPORTS_DIR = EVALS_DIR / "reports"

GENERATION_PROMPT = "followups_v1"
GRADING_PROMPT = "grading_v1"
UNKNOWN_MARKER_TEXT = "[סומן על ידי הלקוח: לא ידוע / טרם הוחלט]"
FIELD_NAMES = {
    "name": "שם",
    "role": "תפקיד",
    "responsibility": "אחריות",
    "phone": "טלפון",
    "email": 'דוא"ל',
}


def case_ids() -> list[str]:
    return sorted(p.stem for p in CASES_DIR.glob("case_*.json"))


def load_case(case_id: str) -> dict:
    return json.loads((CASES_DIR / f"{case_id}.json").read_text(encoding="utf-8"))


def load_labels(case_id: str) -> dict:
    return json.loads((LABELS_DIR / f"{case_id}.json").read_text(encoding="utf-8"))


def template_questions() -> dict[str, dict]:
    sections = load_template_v1()["definition"]["sections"]
    return {q["id"]: q for s in sections for q in s["questions"]}


def answer_text(answer: dict) -> str | None:
    """The answer as plain text, or None when the client marked it unknown."""
    if answer.get("marked_unknown"):
        return None
    value = answer["value"]
    if isinstance(value, list):
        return "\n".join(
            "; ".join(f"{FIELD_NAMES.get(k, k)}: {v}" for k, v in row.items()) for row in value
        )
    return str(value)


def all_answer_text(case: dict) -> str:
    return "\n".join(t for a in case["answers"].values() if (t := answer_text(a)) is not None)


def render_questionnaire(case: dict) -> str:
    """The client's answers, exactly what a model is shown. Never includes labels."""
    lines = [f"שם העסק: {case['company']}", ""]
    for qid, question in template_questions().items():
        text = answer_text(case["answers"][qid])
        lines.append(f"[{qid}] {question['label']}")
        lines.append(f"תשובה: {UNKNOWN_MARKER_TEXT if text is None else text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_generation_prompt(case: dict) -> str:
    template = (PROMPTS_DIR / f"{GENERATION_PROMPT}.md").read_text(encoding="utf-8")
    return template.replace("{{QUESTIONNAIRE}}", render_questionnaire(case).rstrip())


def graded_criteria_text() -> str:
    rubric = RUBRIC_PATH.read_text(encoding="utf-8")
    start = rubric.index("<!-- GRADED-CRITERIA-START -->") + len("<!-- GRADED-CRITERIA-START -->")
    end = rubric.index("<!-- GRADED-CRITERIA-END -->")
    return rubric[start:end].strip()


def render_grading_prompt(case: dict, raw_output: str) -> str:
    template = (PROMPTS_DIR / f"{GRADING_PROMPT}.md").read_text(encoding="utf-8")
    return (
        template.replace("{{GRADED_CRITERIA}}", graded_criteria_text())
        .replace("{{QUESTIONNAIRE}}", render_questionnaire(case).rstrip())
        .replace("{{OUTPUT}}", raw_output.strip())
    )


def inputs_sha256() -> str:
    """Hash of every file that defines the evaluation (cases, labels, prompts, rubric).

    Stored with each run; a later change to any of these makes the stored results stale.
    """
    files = [
        *sorted(CASES_DIR.glob("case_*.json")),
        *sorted(LABELS_DIR.glob("case_*.json")),
        PROMPTS_DIR / f"{GENERATION_PROMPT}.md",
        PROMPTS_DIR / f"{GRADING_PROMPT}.md",
        RUBRIC_PATH,
    ]
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()
