from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_fsm_design.py").read_text(encoding="utf-8")
PREVIOUS=(ROOT/"digital_logic_lab"/"academy_registers_counters.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-5/fsm"' in APP
    assert 'route="/academy/unit-5/fsm-design"' in APP

def test_fsm_foundations():
    for x in ["What is a state?","State diagrams","State tables","Moore versus Mealy machines","Present state + current inputs","FSM hardware structure","check_moore","check_next"]: assert x in LESSONS

def test_fsm_design():
    for x in ["The FSM design workflow","Worked example: simple controller","State encoding","ceil(log₂N)","Binary, one-hot and other encodings","Avoid incomplete behaviour","Verification challenge","check_bits"]: assert x in LESSONS

def test_engineering_precision():
    assert "Unused encodings should be considered deliberately" in LESSONS
    assert "specification-driven" in LESSONS
    assert "What happens if START remains high?" in LESSONS

def test_navigation():
    assert 'href="/academy/unit-5/fsm"' in PREVIOUS
    assert 'href="/academy/unit-5/fsm-design"' in LESSONS
    assert "Path 05 · Lesson 7" in LESSONS and "Path 05 · Lesson 8" in LESSONS
