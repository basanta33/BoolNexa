from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"
CONTENT=ROOT/"digital_logic_lab"/"academy_content.py"
MODELS=ROOT/"digital_logic_lab"/"academy"/"models.py"


def test_path09_lesson1_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def cpu_architecture_foundations_lesson" in text
    assert "PATH 09 · LESSON 01" in text
    assert "CPU Architecture Foundations" in text


def test_lesson1_teaches_core_cpu_blocks():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "What a CPU actually does",
        "Core processor blocks",
        "Program Counter and Instruction Register",
        "Datapath versus control",
        "Buses and multiplexers",
        "How earlier BoolNexa paths connect",
    ):
        assert term in text


def test_lesson1_has_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_component", "def check_pc", "def check_datapath"):
        assert method in text


def test_path09_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "cpu_architecture_foundations_lesson" in text
    assert 'route="/academy/unit-9/cpu-architecture-foundations"' in text


def test_path09_catalog_keeps_lesson1_live():
    text=CAT.read_text(encoding="utf-8")
    assert '9: (' in text
    assert text.count("/academy/unit-9/") >= 1
    assert '"/academy/unit-9/cpu-architecture-foundations"' in text


def test_academy_metadata_registers_path09():
    assert '"Processor Architecture and CPU Datapath"' in CONTENT.read_text(encoding="utf-8")
    models=MODELS.read_text(encoding="utf-8")
    assert '9: "/academy/combinational.svg"' in models
    assert '9: ("/academy/unit-9/cpu-architecture-foundations", "Begin CPU architecture")' in models


def test_lesson1_advances_to_live_lesson2():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Fetch, Decode & Execute" in text
    assert 'href="/academy/unit-9/fetch-decode-execute"' in text
