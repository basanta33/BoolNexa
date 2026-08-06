from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_path10_lesson3_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def interrupts_interrupt_driven_io_lesson" in text
    assert "PATH 10 · LESSON 03" in text
    assert "Interrupts & Interrupt-Driven I/O" in text


def test_lesson3_teaches_interrupt_driven_io():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Why interrupts exist",
        "An interrupt is a controlled change in program flow",
        "Interrupt enable and masking control whether requests are accepted",
        "Interrupt vectors identify the correct service routine",
        "The CPU must preserve the interrupted program",
        "A good ISR handles the cause, not just the request",
        "Polling and interrupts trade simplicity for responsiveness",
        "Priority resolves simultaneous interrupt requests",
        "Interrupt latency measures response delay",
        "Trace one complete interrupt-driven input",
    ):
        assert term in text


def test_lesson3_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_interrupt", "def check_vector", "def check_context"):
        assert method in text


def test_lesson3_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "interrupts_interrupt_driven_io_lesson" in text
    assert 'route="/academy/unit-10/interrupts-interrupt-driven-io"' in text


def test_path10_catalog_has_eight_live_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-10/") == 8
    assert '("Interrupts & Interrupt-Driven I/O", "/academy/unit-10/interrupts-interrupt-driven-io")' in text


def test_lesson3_links_to_lesson4():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · System Buses, Arbitration & Protocols" in text
    assert 'href="/academy/unit-10/system-buses-arbitration-protocols"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text = APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
