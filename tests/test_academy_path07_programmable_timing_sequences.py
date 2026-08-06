from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_registers_counters_path07.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"


def test_path07_lessons_5_6_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def up_down_programmable_counters_lesson" in text
    assert "def timing_sequences_counter_control_lesson" in text
    assert "Up/Down & Programmable Counters" in text
    assert "Timing Sequences & Counter-Based Control" in text


def test_programmable_counter_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Bidirectional counting", "Count enable", "Parallel load / preset", "Terminal count and cascading"):
        assert term in text


def test_timing_sequence_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Counter as a timing step generator", "One-hot timing outputs", "Generating control signals", "Timing hazards"):
        assert term in text


def test_navigation_4_to_5_to_6():
    text = MOD.read_text(encoding="utf-8")
    assert 'href="/academy/unit-7/up-down-programmable-counters"' in text
    assert 'href="/academy/unit-7/timing-sequences"' in text


def test_routes_registered():
    text = APP.read_text(encoding="utf-8")
    assert "up_down_programmable_counters_lesson" in text
    assert "timing_sequences_counter_control_lesson" in text
    assert 'route="/academy/unit-7/up-down-programmable-counters"' in text
    assert 'route="/academy/unit-7/timing-sequences"' in text
