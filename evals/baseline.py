"""Simulated baseline: a deterministic, rule-based stand-in for the mock follow-up provider.

It is NOT a model and is never presented as model evaluation. The rules follow
architecture.md section 6.3 (unknown phrases, a fixed list of important topics, a short-text rule)
and were written from that description, not tuned on the Eval labels. It exists to exercise the
pipeline and CI, and to give a labelled reference point.
"""

import json

from evals.cases import EVALS_DIR, answer_text

BANK = json.loads((EVALS_DIR / "baseline_bank.json").read_text(encoding="utf-8"))

UNKNOWN_PHRASES = (
    "לא יודע",
    "לא יודעת",
    "לא יודעים",
    "טרם הוחלט",
    "עדיין לא הוחלט",
    "עדיין לא הוגדר",
    "לא סגרנו",
    "לא הגדרנו",
    "לא בדקנו",
    "לא דיברנו",
)
NOT_APPLICABLE_PHRASES = ("לא רלוונטי",)
# Important topics, in the order listed in architecture.md: success measures, sponsor,
# data location, sensitive data, human approval, budget.
IMPORTANT = ("q_03", "q_06", "q_08", "q_14", "q_16", "q_18")
# Questions asked about only when the answer is very short.
SHORT_ANSWER_TOPICS = ("q_01", "q_02", "q_04")
SHORT_ANSWER_WORDS = 5
MAX_QUESTIONS = 5


def _is_gap(question_id: str, answer: dict) -> bool:
    text = answer_text(answer)
    if text is None:  # marked unknown by the client
        return True
    if any(phrase in text for phrase in NOT_APPLICABLE_PHRASES):
        return False
    if any(phrase in text for phrase in UNKNOWN_PHRASES):
        return True
    if question_id == "q_03" and not any(ch.isdigit() for ch in text):
        return True
    return False


def generate(case: dict) -> dict:
    """Return follow-up questions for a case in the Eval output format."""
    answers = case["answers"]
    chosen = [q for q in IMPORTANT if _is_gap(q, answers[q])]
    for question_id in SHORT_ANSWER_TOPICS:
        text = answer_text(answers[question_id])
        if text is not None and len(text.split()) < SHORT_ANSWER_WORDS:
            chosen.append(question_id)
    return {
        "follow_up_questions": [
            {
                "text": BANK[q]["text"],
                "rationale": BANK[q]["rationale"],
                "source_question_ids": [q],
            }
            for q in chosen[:MAX_QUESTIONS]
        ]
    }
