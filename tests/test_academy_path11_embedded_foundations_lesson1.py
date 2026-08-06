from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_embedded_path11.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"
CONTENT = ROOT / "digital_logic_lab" / "academy_content.py"

def test_path11_lesson1_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def embedded_systems_foundations_lesson" in text
    assert "PATH 11 · LESSON 01" in text
    assert "Embedded Systems Foundations" in text

def test_lesson1_teaches_embedded_foundations():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "What makes a computer embedded",
        "Embedded design begins with system requirements",
        "Microcontrollers integrate a small computer on one chip",
        "Inputs connect software to the physical world",
        "Outputs let software affect the physical world",
        "Firmware is the hardware-aware software layer",
        "Super-loop firmware is the simplest execution model",
        "Interrupts make embedded systems event-responsive",
        "Real-time correctness includes time",
        "Resource constraints shape architecture",
        "Trace a simple temperature-control system",
    ):
        assert term in text

def test_lesson1_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_embedded", "def check_realtime", "def check_firmware"):
        assert method in text

def test_path11_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    assert 'route="/academy/unit-11/embedded-systems-foundations"' in app
    assert '("Embedded Systems Foundations", "/academy/unit-11/embedded-systems-foundations")' in cat
    assert cat.count("/academy/unit-11/") >= 1

def test_path11_curriculum_declares_eight_lessons():
    text = CONTENT.read_text(encoding="utf-8")
    assert '{"number": 11, "title": "Embedded Systems and Real-Time Computing", "hours": 8, "lessons": 8' in text

def test_lesson1_links_to_lesson2():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · GPIO, Pin Control & Hardware Interfacing" in text
    assert 'href="/academy/unit-11/gpio-pin-control-hardware-interfacing"' in text

def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
