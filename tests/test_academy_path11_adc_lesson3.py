from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_embedded_path11.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_lesson3_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def adc_analog_signals_sensor_acquisition_lesson" in text
    assert "PATH 11 · LESSON 03" in text
    assert "ADC, Analog Signals & Sensor Acquisition" in text


def test_lesson3_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Analog signals vary continuously over a range",
        "An ADC quantises voltage into discrete codes",
        "The reference voltage defines the conversion scale",
        "Sampling turns a time-varying signal into measurements",
        "Sampling too slowly causes aliasing",
        "Sensor conditioning prepares the signal for the ADC",
        "Source impedance and acquisition time affect accuracy",
        "Noise and grounding can move measured codes",
        "Calibration converts ADC codes into useful units",
        "ADC acquisition can be polled, interrupted or DMA-driven",
        "Trace a complete temperature-sensor acquisition",
    ):
        assert term in text


def test_lesson3_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_adc", "def check_nyquist", "def check_reference"):
        assert method in text


def test_lesson3_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    route = "/academy/unit-11/adc-analog-signals-sensor-acquisition"
    assert f'route="{route}"' in app
    assert f'("ADC, Analog Signals & Sensor Acquisition", "{route}")' in cat
    assert cat.count("/academy/unit-11/") >= 3


def test_lesson4_link_present():
    text = MOD.read_text(encoding="utf-8")
    assert "Lesson 4 · PWM, Timers & Waveform Generation" in text
    assert "/academy/unit-11/pwm-timers-waveform-generation" in text


def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
