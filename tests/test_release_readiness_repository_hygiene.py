from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_release_documentation_exists():
    readme = ROOT / "README.md"
    checklist = ROOT / "RELEASE_CHECKLIST_BOOLNEXA.md"

    assert readme.is_file()
    assert checklist.is_file()

    text = readme.read_text(encoding="utf-8")
    assert "# BoolNexa" in text
    assert "python -m pytest -q" in text
    assert "RELEASE_CHECKLIST_BOOLNEXA.md" in text


def test_github_ci_runs_the_supported_release_gates():
    workflow = ROOT / ".github" / "workflows" / "ci.yml"
    assert workflow.is_file()

    text = workflow.read_text(encoding="utf-8")
    assert "python-version: \"3.11\"" in text
    assert "python -m pytest -q" in text
    assert "python -m mypy digital_logic_lab/logic_core.py" in text


def test_accidental_empty_command_files_are_absent():
    for filename in ("4", "None", "assert", "cd", "cls", "copy", "g"):
        assert not (ROOT / filename).exists(), filename
