from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"


def test_path09_lesson5_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def single_cycle_datapath_lesson" in text
    assert "PATH 09 · LESSON 05" in text
    assert "Single-Cycle Datapath" in text


def test_lesson5_teaches_complete_single_cycle_datapath():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "One instruction, one clock interval",
        "The main datapath blocks",
        "Follow the fetch path",
        "Decode turns fields into selections",
        "Operand selection feeds the ALU",
        "Load and store extend the path through data memory",
        "Write-back selects the architectural result",
        "Trace an ADD instruction end-to-end",
        "Trace a LOAD instruction end-to-end",
        "Why the longest path matters",
    ):
        assert term in text


def test_lesson5_has_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_flow", "def check_control", "def check_writeback"):
        assert method in text


def test_lesson5_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "single_cycle_datapath_lesson" in text
    assert 'route="/academy/unit-9/single-cycle-datapath"' in text


def test_path09_catalog_has_eight_live_lessons():
    text=CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Single-Cycle Datapath", "/academy/unit-9/single-cycle-datapath")' in text


def test_lesson5_links_to_live_lesson6():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Control Signals & Branching" in text
    assert 'href="/academy/unit-9/control-signals-branching"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text=APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
