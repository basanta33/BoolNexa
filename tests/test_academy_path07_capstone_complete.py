from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_registers_counters_path07.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"


def test_path07_lesson_7_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def register_counter_integration_capstone_lesson" in text
    assert "Register–Counter System Integration & Design Challenge" in text
    assert "PATH 07 · LESSON 07 · PATH FINALE" in text


def test_capstone_integrates_registers_and_counters():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Separate datapath from control",
        "four-step data mover",
        "finite-state machine",
        "Path 07 concept map",
        "Engineering verification checklist",
    ):
        assert term in text


def test_lesson_6_advances_to_capstone():
    text = MOD.read_text(encoding="utf-8")
    assert 'href="/academy/unit-7/register-counter-integration"' in text


def test_path07_completion_present():
    text = MOD.read_text(encoding="utf-8")
    assert "Path 07 complete" in text
    assert "Path 07 · Complete" in text
    assert "Return to Academy" in text


def test_capstone_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "register_counter_integration_capstone_lesson" in text
    assert 'route="/academy/unit-7/register-counter-integration"' in text
