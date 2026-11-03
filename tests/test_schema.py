import sqlite3

import pytest

from app.db import connect, migrate, transaction

EXPECTED_TABLES = {
    "leads",
    "lead_status_history",
    "template_versions",
    "questionnaire_instances",
    "answers",
    "follow_up_questions",
    "fill_sessions",
    "progress_events",
    "contacts",
    "internal_notes",
    "ai_analysis_runs",
    "schema_migrations",
}
NOW = "2026-01-01T00:00:00+00:00"
EMPTY_DEFINITION = '{"sections": []}'


def add_lead(conn, lead_id="lead1", status="חדש"):
    conn.execute(
        "INSERT INTO leads (id, company_name, email, phone, status, created_at, updated_at) "
        "VALUES (?, 'חברת בדיקה (דמו)', 'x@example.com', '000', ?, ?, ?)",
        (lead_id, status, NOW, NOW),
    )


def add_template(conn, tpl_id="tpl1", version=1, state="published"):
    published_at = NOW if state == "published" else None
    conn.execute(
        "INSERT INTO template_versions "
        "(id, version_number, state, intro_text, title_pattern, definition, created_at, "
        "published_at) VALUES (?, ?, ?, 'intro', 'title', ?, ?, ?)",
        (tpl_id, version, state, EMPTY_DEFINITION, NOW, published_at),
    )


def add_instance(conn, inst_id="inst1", lead_id="lead1", state="active", token="hash1"):
    conn.execute(
        "INSERT INTO questionnaire_instances "
        "(id, lead_id, template_version_id, definition_snapshot, state, token_hash, created_at) "
        "VALUES (?, ?, 'tpl1', ?, ?, ?, ?)",
        (inst_id, lead_id, EMPTY_DEFINITION, state, token, NOW),
    )


def add_run(conn, run_id, kind="analysis", status="succeeded", inst_id="inst1"):
    lease = NOW if status == "pending" else None
    conn.execute(
        "INSERT INTO ai_analysis_runs (id, instance_id, kind, provider, is_simulated, "
        "prompt_version, input_hash, status, created_at, lease_expires_at) "
        "VALUES (?, ?, ?, 'mock', 1, 'v1', 'h', ?, ?, ?)",
        (run_id, inst_id, kind, status, NOW, lease),
    )


@pytest.fixture
def base(conn):
    add_lead(conn)
    add_template(conn)
    add_instance(conn)
    return conn


def test_migrations_create_every_table(conn):
    names = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert EXPECTED_TABLES <= names


def test_migrations_are_repeatable(conn):
    assert migrate(conn) == []
    applied = [r["version"] for r in conn.execute("SELECT version FROM schema_migrations")]
    assert applied == ["0001_init.sql"]


def test_foreign_keys_are_enforced(conn):
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    with pytest.raises(sqlite3.IntegrityError):
        add_instance(conn, lead_id="no-such-lead")


def test_lead_status_must_be_one_of_the_five_hebrew_statuses(conn):
    for status in ["חדש", "ממתין למילוי", "התקבל", "בבדיקה", "הושלם"]:
        add_lead(conn, lead_id=f"lead-{status}", status=status)
    with pytest.raises(sqlite3.IntegrityError):
        add_lead(conn, lead_id="bad", status="טיוטה")  # draft is not a primary status


def test_only_one_active_instance_per_lead(base):
    with pytest.raises(sqlite3.IntegrityError):
        add_instance(base, inst_id="inst2", token="hash2")
    # A voided instance does not block a new active one, and history is kept.
    base.execute("UPDATE questionnaire_instances SET state = 'void' WHERE id = 'inst1'")
    add_instance(base, inst_id="inst2", token="hash2")
    assert base.execute("SELECT count(*) FROM questionnaire_instances").fetchone()[0] == 2


def test_token_hash_is_unique(base):
    add_lead(base, lead_id="lead2")
    with pytest.raises(sqlite3.IntegrityError):
        add_instance(base, inst_id="inst2", lead_id="lead2", token="hash1")


def test_submitted_at_only_with_submitted_phase(base):
    with pytest.raises(sqlite3.IntegrityError):
        base.execute("UPDATE questionnaire_instances SET submitted_at = ? WHERE id='inst1'", (NOW,))
    with pytest.raises(sqlite3.IntegrityError):
        base.execute("UPDATE questionnaire_instances SET phase = 'submitted' WHERE id='inst1'")
    base.execute(
        "UPDATE questionnaire_instances SET phase = 'submitted', submitted_at = ? WHERE id='inst1'",
        (NOW,),
    )


def test_only_one_live_or_successful_ai_run_per_instance_and_kind(base):
    add_run(base, "r1", status="succeeded")
    with pytest.raises(sqlite3.IntegrityError):
        add_run(base, "r2", status="pending")
    with pytest.raises(sqlite3.IntegrityError):
        add_run(base, "r3", status="succeeded")
    add_run(base, "r4", kind="follow_ups", status="pending")  # other kind is independent
    # Failed runs do not occupy the slot, so an admin retry can add a new one later.
    base.execute("DELETE FROM ai_analysis_runs WHERE id = 'r1'")
    add_run(base, "r5", status="failed")
    add_run(base, "r6", status="failed")
    add_run(base, "r7", status="pending")
    with pytest.raises(sqlite3.IntegrityError):
        add_run(base, "r8", status="pending")


def test_a_pending_run_needs_a_lease(base):
    with pytest.raises(sqlite3.IntegrityError):
        base.execute(
            "INSERT INTO ai_analysis_runs (id, instance_id, kind, provider, is_simulated, "
            "prompt_version, input_hash, status, created_at) "
            "VALUES ('r', 'inst1', 'analysis', 'mock', 1, 'v1', 'h', 'pending', ?)",
            (NOW,),
        )


def insert_answer(conn, value, marked_unknown):
    conn.execute(
        "INSERT INTO answers (instance_id, question_id, value, marked_unknown, updated_at) "
        "VALUES ('inst1', ?, ?, ?, ?)",
        (f"q_{value}_{marked_unknown}", value, marked_unknown, NOW),
    )


def test_marked_unknown_cannot_coexist_with_a_value(base):
    insert_answer(base, None, 1)  # date / contact group marked unknown: no value
    insert_answer(base, '"2026-03-01"', 0)  # an ordinary value
    insert_answer(base, None, 0)  # cleared
    with pytest.raises(sqlite3.IntegrityError):
        insert_answer(base, '"2026-03-01"', 1)
    with pytest.raises(sqlite3.IntegrityError):
        insert_answer(base, None, 2)


def test_one_answer_row_per_question(base):
    insert_answer(base, '"a"', 0)
    with pytest.raises(sqlite3.IntegrityError):
        base.execute(
            "INSERT INTO answers (instance_id, question_id, value, updated_at) "
            "VALUES ('inst1', 'q_\"a\"_0', '\"b\"', ?)",
            (NOW,),
        )


def test_json_columns_must_be_valid_json(conn):
    add_lead(conn)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO template_versions (id, version_number, state, intro_text, title_pattern, "
            "definition, created_at, published_at) VALUES ('t', 1, 'published', 'i', 't', "
            "'not json', ?, ?)",
            (NOW, NOW),
        )


def test_published_templates_are_immutable_and_only_one_draft_exists(conn):
    add_template(conn, "tpl1", 1, "published")
    with pytest.raises(sqlite3.DatabaseError, match="immutable"):
        conn.execute("UPDATE template_versions SET intro_text = 'changed' WHERE id = 'tpl1'")
    with pytest.raises(sqlite3.DatabaseError, match="immutable"):
        conn.execute("DELETE FROM template_versions WHERE id = 'tpl1'")
    with pytest.raises(sqlite3.IntegrityError):
        add_template(conn, "tpl-dup", 1, "published")  # version numbers are unique
    add_template(conn, "draft1", 2, "draft")
    with pytest.raises(sqlite3.IntegrityError):
        add_template(conn, "draft2", 3, "draft")
    conn.execute("UPDATE template_versions SET intro_text = 'edited' WHERE id = 'draft1'")


def test_follow_up_ordinal_is_between_one_and_five(base):
    add_run(base, "fu", kind="follow_ups")

    def add(ordinal):
        base.execute(
            "INSERT INTO follow_up_questions (id, instance_id, ai_run_id, ordinal, text, "
            "rationale, source_question_ids) VALUES (?, 'inst1', 'fu', ?, 'שאלה', 'r', '[]')",
            (f"f{ordinal}", ordinal),
        )

    for ordinal in range(1, 6):
        add(ordinal)
    for bad in (0, 6):
        with pytest.raises(sqlite3.IntegrityError):
            add(bad)


def test_internal_notes_and_status_history_are_append_only(base):
    base.execute(
        "INSERT INTO internal_notes (id, lead_id, author_label, body, created_at) "
        "VALUES ('n1', 'lead1', 'Demo admin', 'הערה', ?)",
        (NOW,),
    )
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        base.execute("UPDATE internal_notes SET body = 'x' WHERE id = 'n1'")
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        base.execute("DELETE FROM internal_notes WHERE id = 'n1'")

    base.execute(
        "INSERT INTO lead_status_history (id, lead_id, to_status, changed_at, changed_by) "
        "VALUES ('h1', 'lead1', 'חדש', ?, 'seed')",
        (NOW,),
    )
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        base.execute("UPDATE lead_status_history SET reason = 'x' WHERE id = 'h1'")
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        base.execute("DELETE FROM lead_status_history WHERE id = 'h1'")


def test_many_notes_per_answer_are_allowed(base):
    for i in range(3):
        base.execute(
            "INSERT INTO internal_notes (id, lead_id, instance_id, question_id, author_label, "
            "body, created_at) VALUES (?, 'lead1', 'inst1', 'q_01', 'Demo admin', 'הערה', ?)",
            (f"n{i}", NOW),
        )
    assert base.execute("SELECT count(*) FROM internal_notes").fetchone()[0] == 3


def test_contacts_are_deduplicated_per_lead(base):
    def add(contact_id):
        base.execute(
            "INSERT INTO contacts (id, lead_id, name, origin, dedupe_key, created_at, updated_at) "
            "VALUES (?, 'lead1', 'דנה', 'manual', 'דנה|', ?, ?)",
            (contact_id, NOW, NOW),
        )

    add("c1")
    with pytest.raises(sqlite3.IntegrityError):
        add("c2")


def test_transaction_rolls_back_on_error(conn):
    with pytest.raises(RuntimeError):
        with transaction(conn):
            add_lead(conn)
            raise RuntimeError("boom")
    assert conn.execute("SELECT count(*) FROM leads").fetchone()[0] == 0


def test_a_failing_migration_is_rolled_back(tmp_path, monkeypatch):
    from app import db

    folder = tmp_path / "migrations"
    folder.mkdir()
    (folder / "0001_ok.sql").write_text("CREATE TABLE a (x INTEGER);", encoding="utf-8")
    (folder / "0002_bad.sql").write_text(
        "CREATE TABLE b (x INTEGER); INSERT INTO nope VALUES (1);", encoding="utf-8"
    )
    monkeypatch.setattr(db, "MIGRATIONS_DIR", folder)
    connection = connect(tmp_path / "m.db")
    with pytest.raises(sqlite3.OperationalError):
        migrate(connection)
    names = {r["name"] for r in connection.execute("SELECT name FROM sqlite_master")}
    assert "a" in names and "b" not in names
    applied = [r["version"] for r in connection.execute("SELECT version FROM schema_migrations")]
    assert applied == ["0001_ok.sql"]
