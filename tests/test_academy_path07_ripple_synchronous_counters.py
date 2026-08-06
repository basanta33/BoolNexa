from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_registers_counters_path07.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"


def test_path07_lessons_3_4_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def ripple_counters_frequency_division_lesson" in text
    assert "def synchronous_counters_modulo_n_lesson" in text
    assert "Ripple Counters & Frequency Division" in text
    assert "Synchronous Counters & Modulo-N Design" in text


def test_ripple_counter_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Why it is called ripple", "Frequency division", "Counter modulus", "Ripple-counter timing caution"):
        assert term in text


def test_synchronous_counter_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Common-clock architecture", "Modulo-N counters", "present-state/next-state table", "Ripple vs synchronous"):
        assert term in text


def test_path07_navigation_2_to_3_to_4():
    text = MOD.read_text(encoding="utf-8")
    assert 'href="/academy/unit-7/ripple-counters"' in text
    assert 'href="/academy/unit-7/synchronous-counters"' in text


def test_path07_counter_routes_registered():
    text = APP.read_text(encoding="utf-8")
    assert "ripple_counters_frequency_division_lesson" in text
    assert "synchronous_counters_modulo_n_lesson" in text
    assert 'route="/academy/unit-7/ripple-counters"' in text
    assert 'route="/academy/unit-7/synchronous-counters"' in text
