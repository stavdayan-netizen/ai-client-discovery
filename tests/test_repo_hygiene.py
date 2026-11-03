"""Guards for the repository rules in practice.md: no secrets, no paid services in default CI."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_env_example_lists_names_only():
    lines = [
        line
        for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert lines, "expected variable names"
    for line in lines:
        name, _, value = line.partition("=")
        assert re.fullmatch(r"[A-Z_]+", name) and value == "", line


def test_ci_workflow_runs_lint_and_tests_without_secrets():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert re.search(r"^\s*pull_request:", workflow, re.M)
    assert "secrets." not in workflow
    assert "ruff check" in workflow
    assert "pytest" in workflow
    assert re.search(r"contents:\s*read", workflow)


def test_runtime_dependencies_are_pinned():
    for name in ("requirements.txt", "requirements-dev.txt"):
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("-r"):
                assert "==" in line, f"{name}: {line} is not pinned"


def test_database_and_env_files_are_git_ignored():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in ("*.db", "data/", ".env", ".venv/"):
        assert pattern in ignore
