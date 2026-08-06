from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"


def test_path09_lesson6_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def control_signals_branching_lesson" in text
    assert "PATH 09 · LESSON 06" in text
    assert "Control Signals & Branching" in text


def test_lesson6_teaches_control_and_branching():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "Control turns an instruction into datapath decisions",
        "The main single-cycle control signals",
        "Opcode decoding creates a control word",
        "ALU control refines the requested operation",
        "Conditional branches combine control with a status result",
        "The branch target is formed in parallel",
        "PCSrc selects the next instruction address",
        "Trace a branch-equal instruction",
        "Not-taken branches and unconditional jumps",
        "Safe control prevents unintended state changes",
    ):
        assert term in text


def test_lesson6_has_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_branch", "def check_zero", "def check_pcsrc"):
        assert method in text


def test_lesson6_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "control_signals_branching_lesson" in text
    assert 'route="/academy/unit-9/control-signals-branching"' in text


def test_path09_catalog_has_eight_live_lessons():
    text=CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Control Signals and Branching", "/academy/unit-9/control-signals-branching")' in text


def test_lesson6_links_to_live_lesson7():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Pipeline Fundamentals" in text
    assert 'href="/academy/unit-9/pipeline-fundamentals"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text=APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
