"""Reads the original questionnaire (SPEC.md section 5) so tests can check the seed against it."""

import re
from pathlib import Path

SPEC_PATH = Path(__file__).resolve().parents[1] / "SPEC.md"

# English notes SPEC.md adds to three questions; they describe the field type, not the wording.
_FIELD_NOTE = re.compile(r"\s*\((?:Repeatable rows|Fields|Date field)[^)]*\)\s*$")


def parse_spec(path: Path = SPEC_PATH) -> dict:
    text = path.read_text(encoding="utf-8")

    title = re.search(r'\*\*"(שאלון איפיון להטמעת AI - \{שם העסק\})"\*\*', text)
    intro = re.search(r'^\*\*Intro \(original\)\*\*: "(.+)"\s*$', text, re.M)
    assert title and intro, "title pattern or intro not found in SPEC.md"

    start = text.index("## 5. Original questionnaire content")
    end = text.index("## 6. Data and persistence")
    block = text[start:end]

    sections: list[dict] = []
    for line in block.splitlines():
        heading = re.match(r"^### (חלק .+)$", line)
        question = re.match(r"^(\d+)\. (.+)$", line)
        if heading:
            sections.append({"title": heading.group(1).strip(), "questions": []})
        elif question and sections:
            label = _FIELD_NOTE.sub("", question.group(2)).strip()
            sections[-1]["questions"].append({"number": int(question.group(1)), "label": label})

    return {
        "title_pattern": title.group(1),
        "intro_text": intro.group(1),
        "sections": sections,
    }
