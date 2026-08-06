from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_combinational_foundations_adders.py").read_text(encoding="utf-8")

def test_path04_lessons_one_and_two_are_registered():
    assert 'route="/academy/unit-4/combinational-foundations"' in APP
    assert 'route="/academy/unit-4/adders"' in APP

def test_foundations_teach_real_design_workflow():
    assert "A combinational circuit has no stored state" in LESSONS
    assert "Truth table" in LESSONS
    assert "Simplification / K-map" in LESSONS
    assert "Gate-level circuit" in LESSONS
    assert "Combinational versus sequential" in LESSONS
    assert "check_memory" in LESSONS

def test_adder_lesson_is_technically_complete():
    assert "S = A ⊕ B" in LESSONS
    assert "C = AB" in LESSONS
    assert "S = A ⊕ B ⊕ Cin" in LESSONS
    assert "Cout = AB + ACin + BCin" in LESSONS
    assert "ripple-carry adder" in LESSONS
    assert "propagation delay" in LESSONS
    assert "check_half_adder" in LESSONS
    assert "check_full_inputs" in LESSONS

def test_real_boolnexa_tool_integration():
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert 'href="/tools/boolean"' in LESSONS
    assert "Path 04 · Lesson 1" in LESSONS
    assert "Path 04 · Lesson 2" in LESSONS
