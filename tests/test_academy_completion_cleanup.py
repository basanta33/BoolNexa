from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMY = ROOT / "digital_logic_lab" / "academy.py"


def test_obsolete_unit_one_prototype_grid_not_rendered():
    text = ACADEMY.read_text(encoding="utf-8")
    home = text.split("def academy()", 1)[1]
    assert "_unit_one_lessons()," not in home
    assert "_completed_path_browser()," in home


def test_home_challenge_is_live():
    text = ACADEMY.read_text(encoding="utf-8")
    assert "Challenge coming soon" not in text
    assert "Open NAND/XOR challenge" in text
    assert 'href="/academy/unit-2/mastery-challenge"' in text
