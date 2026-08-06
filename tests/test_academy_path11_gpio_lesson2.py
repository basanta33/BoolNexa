from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_embedded_path11.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_lesson2_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def gpio_pin_control_hardware_interfacing_lesson" in text
    assert "PATH 11 · LESSON 02" in text
    assert "GPIO, Pin Control & Hardware Interfacing" in text


def test_lesson2_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "GPIO turns processor pins into programmable digital interfaces",
        "Direction decides whether the pin senses or drives",
        "GPIO registers expose pin state to firmware",
        "Inputs must not be left electrically undefined",
        "Mechanical switches can bounce",
        "Logic levels and voltage limits matter",
        "High-current loads need a driver stage",
        "Inductive loads need protection",
        "Pin multiplexing selects GPIO or peripheral ownership",
        "Safe initialization prevents unwanted output glitches",
        "Trace a button-controlled LED",
    ):
        assert term in text


def test_lesson2_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_gpio", "def check_pull", "def check_driver"):
        assert method in text


def test_lesson2_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    assert 'route="/academy/unit-11/gpio-pin-control-hardware-interfacing"' in app
    assert '("GPIO, Pin Control & Hardware Interfacing", "/academy/unit-11/gpio-pin-control-hardware-interfacing")' in cat
    assert cat.count("/academy/unit-11/") >= 2


def test_lesson3_link_present():
    text = MOD.read_text(encoding="utf-8")
    assert "Lesson 3 · ADC, Analog Signals & Sensor Acquisition" in text
    assert "/academy/unit-11/adc-analog-signals-sensor-acquisition" in text


def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
