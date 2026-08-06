from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_embedded_path11.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_lesson4_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def pwm_timers_waveform_generation_lesson" in text
    assert "PATH 11 · LESSON 04" in text
    assert "PWM, Timers & Waveform Generation" in text


def test_lesson4_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "A hardware timer counts from a time base",
        "Period and frequency describe repeating waveforms",
        "Compare registers schedule events at exact counts",
        "PWM encodes control in pulse width",
        "Duty cycle is the active fraction of a period",
        "Timer resolution limits waveform choices",
        "PWM can control LEDs and motor drivers",
        "Hardware PWM reduces timing jitter",
        "Input capture measures external timing",
        "Timers can trigger other peripherals",
        "Trace a PWM configuration",
    ):
        assert term in text


def test_lesson4_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_pwm", "def check_duty", "def check_timer"):
        assert method in text


def test_lesson4_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    route = "/academy/unit-11/pwm-timers-waveform-generation"
    assert f'route="{route}"' in app
    assert f'("PWM, Timers & Waveform Generation", "{route}")' in cat
    assert cat.count("/academy/unit-11/") >= 4


def test_lesson5_link_present():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Interrupts, Priorities & ISR Design" in text
    assert "/academy/unit-11/interrupts-priorities-isr-design" in text


def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
