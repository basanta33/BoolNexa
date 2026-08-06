from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"


def test_path09_lesson3_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def registers_buses_register_transfer_lesson" in text
    assert "PATH 09 · LESSON 03" in text
    assert "Registers, Buses & Register Transfer" in text


def test_lesson3_teaches_register_transfer_datapath():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "Registers are the CPU's working storage",
        "A register is a group of flip-flops",
        "Buses move whole words",
        "Only one selected source should drive a shared bus",
        "Register-transfer notation",
        "A transfer requires control and timing",
        "Register transfer through the ALU",
        "Trace a complete micro-operation",
    ):
        assert term in text


def test_lesson3_has_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_register", "def check_bus", "def check_transfer"):
        assert method in text


def test_lesson3_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "registers_buses_register_transfer_lesson" in text
    assert 'route="/academy/unit-9/register-transfer"' in text


def test_path09_catalog_has_lesson3_lesson4_and_lesson5():
    text=CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Registers, Buses and Register Transfer", "/academy/unit-9/register-transfer")' in text


def test_lesson3_advances_to_live_lesson4():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Instruction Formats & Data Movement" in text
    assert 'href="/academy/unit-9/instruction-formats"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text=APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
