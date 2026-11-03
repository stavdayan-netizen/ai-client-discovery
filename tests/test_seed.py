import json
import re

import pytest

from app.seed import DEMO_LEADS, load_template_v1, seed
from tests.spec_parser import parse_spec

TABLES = ["template_versions", "leads", "lead_status_history"]


def dump(conn):
    return {
        table: [tuple(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()]
        for table in TABLES
    }


def questions(template):
    return [q for s in template["definition"]["sections"] for q in s["questions"]]


@pytest.fixture
def seeded(conn):
    seed(conn)
    return conn


def test_seed_is_repeatable(conn):
    first = seed(conn)
    after_first = dump(conn)
    second = seed(conn)
    assert first == {"template_versions": 1, "leads": 3, "lead_status_history": 3}
    assert second == {"template_versions": 0, "leads": 0, "lead_status_history": 0}
    assert dump(conn) == after_first


def test_template_v1_is_published_version_one(seeded):
    row = seeded.execute("SELECT * FROM template_versions").fetchone()
    assert (row["version_number"], row["state"]) == (1, "published")
    assert row["published_at"] is not None
    assert json.loads(row["definition"]) == load_template_v1()["definition"]


def test_all_18_questions_are_required_and_active():
    qs = questions(load_template_v1())
    assert len(qs) == 18
    assert all(q["required"] is True and q["active"] is True for q in qs)


def test_stable_ids():
    template = load_template_v1()
    assert [s["id"] for s in template["definition"]["sections"]] == [f"sec_{c}" for c in "abcdef"]
    assert [q["id"] for q in questions(template)] == [f"q_{n:02d}" for n in range(1, 19)]


def test_wording_matches_the_original_in_spec():
    spec = parse_spec()
    template = load_template_v1()
    assert template["title_pattern"] == spec["title_pattern"]
    assert template["intro_text"] == spec["intro_text"]
    sections = template["definition"]["sections"]
    assert [s["title"] for s in sections] == [s["title"] for s in spec["sections"]]
    assert [len(s["questions"]) for s in sections] == [3, 4, 4, 2, 3, 2]
    for seeded_section, spec_section in zip(sections, spec["sections"], strict=True):
        assert [q["label"] for q in seeded_section["questions"]] == [
            q["label"] for q in spec_section["questions"]
        ]
    assert [int(q["id"][2:]) for q in questions(template)] == list(range(1, 19))


def test_field_types():
    by_id = {q["id"]: q for q in questions(load_template_v1())}
    assert by_id["q_05"]["type"] == "person_group"
    assert by_id["q_05"]["config"]["fields"] == ["name", "role", "responsibility"]
    assert by_id["q_06"]["type"] == "person_group"
    assert by_id["q_06"]["config"]["fields"] == ["name", "role"]
    assert by_id["q_06"]["config"]["max"] == 1
    assert by_id["q_17"]["type"] == "date"
    assert by_id["q_13"]["type"] == "short_text"
    plain = set(by_id) - {"q_05", "q_06", "q_17", "q_13"}
    assert {by_id[q]["type"] for q in plain} == {"long_text"}
    for q in by_id.values():
        if q["type"] != "person_group":
            assert q["config"] == {}


def test_semantic_tags_are_on_the_right_questions_and_unique():
    tags = {q["id"]: q["tag"] for q in questions(load_template_v1()) if q["tag"]}
    assert tags == {"q_05": "stakeholders", "q_06": "sponsor", "q_07": "end_users"}


def test_demo_leads_are_clearly_fictional(seeded):
    rows = seeded.execute("SELECT * FROM leads ORDER BY id").fetchall()
    assert len(rows) == len(DEMO_LEADS) == 3
    for row in rows:
        assert "(דמו)" in row["company_name"]
        assert row["email"].endswith("@example.com")
        assert re.fullmatch(r"000-\d{7}", row["phone"])
        assert row["status"] == "חדש"
    history = seeded.execute("SELECT * FROM lead_status_history").fetchall()
    assert {h["changed_by"] for h in history} == {"seed"}


def test_seed_creates_no_instances_or_answers(seeded):
    for table in ["questionnaire_instances", "answers", "ai_analysis_runs", "internal_notes"]:
        assert seeded.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0
