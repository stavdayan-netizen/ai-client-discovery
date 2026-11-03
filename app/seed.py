"""Seed data: questionnaire template v1 and clearly fictional demo leads.

Run with `python -m app.seed`. The seed is repeatable: existing rows are never changed or
duplicated, so running it twice leaves the database exactly as after the first run.
"""

import json
import sqlite3
from pathlib import Path

from app.config import BASE_DIR, load_settings
from app.db import connect, migrate, transaction, utc_now

TEMPLATE_V1_PATH = BASE_DIR / "seed_data" / "template_v1.json"
TEMPLATE_V1_ID = "tpl_v1"
SEED_AUTHOR = "seed"

# Fictional demo data only: names carry a "(דמו)" marker, emails use the reserved example.com
# domain and phone numbers are obviously fake. None of this refers to a real business or person.
DEMO_LEADS = [
    {
        "id": "lead_demo_1",
        "company_name": "חברת דוגמה אלפא (דמו)",
        "contact_name": "איש קשר לדוגמה א׳ (דמו)",
        "email": "demo-alpha@example.com",
        "phone": "000-0000001",
    },
    {
        "id": "lead_demo_2",
        "company_name": "מסעדת דוגמה בטא (דמו)",
        "contact_name": "איש קשר לדוגמה ב׳ (דמו)",
        "email": "demo-beta@example.com",
        "phone": "000-0000002",
    },
    {
        "id": "lead_demo_3",
        "company_name": "סטודיו דוגמה גמא (דמו)",
        "contact_name": None,
        "email": "demo-gamma@example.com",
        "phone": "000-0000003",
    },
]


def load_template_v1(path: Path = TEMPLATE_V1_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def seed(conn: sqlite3.Connection) -> dict[str, int]:
    """Insert template v1 and the demo leads if missing. Returns how many rows were added."""
    template = load_template_v1()
    now = utc_now()
    added = {"template_versions": 0, "leads": 0, "lead_status_history": 0}

    with transaction(conn):
        cursor = conn.execute(
            "INSERT OR IGNORE INTO template_versions "
            "(id, version_number, state, intro_text, title_pattern, definition, "
            "created_at, published_at) VALUES (?, 1, 'published', ?, ?, ?, ?, ?)",
            (
                TEMPLATE_V1_ID,
                template["intro_text"],
                template["title_pattern"],
                json.dumps(template["definition"], ensure_ascii=False),
                now,
                now,
            ),
        )
        added["template_versions"] += cursor.rowcount

        for lead in DEMO_LEADS:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO leads "
                "(id, company_name, contact_name, email, phone, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 'חדש', ?, ?)",
                (
                    lead["id"],
                    lead["company_name"],
                    lead["contact_name"],
                    lead["email"],
                    lead["phone"],
                    now,
                    now,
                ),
            )
            added["leads"] += cursor.rowcount
            cursor = conn.execute(
                "INSERT OR IGNORE INTO lead_status_history "
                "(id, lead_id, from_status, to_status, changed_at, changed_by) "
                "VALUES (?, ?, NULL, 'חדש', ?, ?)",
                (f"hist_{lead['id']}", lead["id"], now, SEED_AUTHOR),
            )
            added["lead_status_history"] += cursor.rowcount
    return added


def main() -> int:
    settings = load_settings()
    conn = connect(settings.database_path)
    try:
        migrate(conn)
        added = seed(conn)
    finally:
        conn.close()
    print(f"Seeded {settings.database_path}: {added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
