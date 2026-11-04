"""The Eval cases are well-formed, fictional, and the model-visible prompt never leaks labels."""

import re

import pytest

from evals.cases import (
    case_ids,
    inputs_sha256,
    load_case,
    load_labels,
    render_generation_prompt,
    render_grading_prompt,
    render_questionnaire,
    template_questions,
)

IDS = case_ids()


def test_there_are_six_cases():
    assert IDS == [f"case_0{n}" for n in range(1, 7)]


@pytest.mark.parametrize("case_id", IDS)
def test_case_answers_every_template_question_once(case_id):
    case = load_case(case_id)
    assert set(case["answers"]) == set(template_questions())
    for answer in case["answers"].values():
        assert ("value" in answer) != answer.get("marked_unknown", False)


@pytest.mark.parametrize("case_id", IDS)
def test_unknown_marker_is_only_used_on_date_and_contact_group_questions(case_id):
    questions = template_questions()
    for qid, answer in load_case(case_id)["answers"].items():
        if answer.get("marked_unknown"):
            assert questions[qid]["type"] in ("date", "person_group")


@pytest.mark.parametrize("case_id", IDS)
def test_cases_are_fictional_and_contain_no_contact_details(case_id):
    case = load_case(case_id)
    assert case["fictional"] is True
    assert "(דמו)" in case["company"]
    text = render_questionnaire(case)
    assert not re.search(r"[\w.]+@[\w.]+", text)
    assert not re.search(r"\b0\d{1,2}-?\d{7}\b", text)


@pytest.mark.parametrize("case_id", IDS)
def test_labels_refer_to_real_questions_and_do_not_overlap(case_id):
    labels, valid = load_labels(case_id), set(template_questions())
    groups = [labels["expected_gaps"], labels["acceptable_targets"], labels["must_not_target"]]
    for group in groups:
        assert set(group) <= valid
    expected, acceptable, forbidden = (set(g) for g in groups)
    assert not (expected & acceptable) and not ((expected | acceptable) & forbidden)
    assert 1 <= labels["max_questions"] <= 5


def test_cases_cover_the_intended_behaviours():
    labels = {c: load_labels(c) for c in IDS}
    assert labels["case_01"]["expected_gaps"] == [] and labels["case_01"]["max_questions"] == 1
    assert labels["case_04"]["must_not_target"]  # not-applicable items
    assert labels["case_06"]["injection_marker"] == "PWNED_MARKER"
    assert "PWNED_MARKER" in render_questionnaire(load_case("case_06"))
    case_03 = load_case("case_03")["answers"]
    assert case_03["q_06"].get("marked_unknown") and case_03["q_17"].get("marked_unknown")


@pytest.mark.parametrize("case_id", IDS)
def test_generation_prompt_shows_only_the_answers_never_the_labels(case_id):
    case, labels = load_case(case_id), load_labels(case_id)
    prompt = render_generation_prompt(case)
    for forbidden in (
        "expected_gaps",
        "acceptable_targets",
        "must_not_target",
        "rationale_for_labels",
        "max_questions",
        "rubric",
        "Relevance",
        labels["rationale_for_labels"],
    ):
        assert forbidden not in prompt
    assert "{{" not in prompt
    assert case["company"] in prompt
    assert "[q_01]" in prompt and "[q_18]" in prompt


def test_grading_prompt_contains_anchors_and_output_but_not_labels():
    case = load_case("case_02")
    prompt = render_grading_prompt(case, '{"follow_up_questions": []}')
    assert "Relevance" in prompt and "Avoidance of invented information" in prompt
    assert '{"follow_up_questions": []}' in prompt
    for forbidden in ("expected_gaps", "acceptable_targets", "must_not_target", "{{"):
        assert forbidden not in prompt


def test_inputs_fingerprint_is_stable():
    assert inputs_sha256() == inputs_sha256()
    assert len(inputs_sha256()) == 64
