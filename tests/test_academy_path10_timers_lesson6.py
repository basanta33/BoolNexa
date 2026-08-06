from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_lesson6_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def timers_counters_system_timing_lesson" in text
    assert "PATH 10 · LESSON 06" in text
    assert "Timers, Counters & System Timing" in text


def test_lesson6_core_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "A timer is a counter with a time base",
        "Timer registers make timing programmable",
        "Prescalers extend the useful timing range",
        "Overflow and compare-match create events",
        "Periodic timers schedule repeated work",
        "Input capture timestamps external events",
        "Output compare can control hardware precisely",
        "PWM encodes control in pulse width",
        "Watchdog timers detect missing progress",
        "Clock domains and timer sources matter",
        "Trace a periodic interrupt timer",
    ):
        assert term in text


def test_lesson6_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_timer", "def check_prescaler", "def check_watchdog"):
        assert method in text


def test_lesson6_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    assert 'route="/academy/unit-10/timers-counters-system-timing"' in app
    assert '("Timers, Counters & System Timing", "/academy/unit-10/timers-counters-system-timing")' in cat
    assert cat.count("/academy/unit-10/") == 8


def test_lesson6_links_to_lesson7():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Peripheral Interfaces & Serial Communication" in text
    assert 'href="/academy/unit-10/peripheral-interfaces-serial-communication"' in text


def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
