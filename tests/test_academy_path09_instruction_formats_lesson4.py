from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"


def test_path09_lesson4_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def instruction_formats_data_movement_lesson" in text
    assert "PATH 09 · LESSON 04" in text
    assert "Instruction Formats & Data Movement" in text


def test_lesson4_teaches_instruction_formats_and_data_movement():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "Why instructions need fields",
        "Opcode and register fields",
        "Register-register data movement",
        "Immediate data travels with the instruction",
        "Immediate width, extension and range",
        "Load and store connect registers to memory",
        "Effective addresses combine fields and registers",
        "One instruction format drives several datapath choices",
        "Trace three common instruction classes",
    ):
        assert term in text


def test_lesson4_has_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_format", "def check_immediate", "def check_loadstore"):
        assert method in text


def test_lesson4_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "instruction_formats_data_movement_lesson" in text
    assert 'route="/academy/unit-9/instruction-formats"' in text


def test_path09_catalog_has_eight_live_lessons():
    text=CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Instruction Formats and Data Movement", "/academy/unit-9/instruction-formats")' in text


def test_lesson4_links_to_live_lesson5():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Single-Cycle Datapath" in text
    assert 'href="/academy/unit-9/single-cycle-datapath"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text=APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
