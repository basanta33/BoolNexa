from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_boolean_truth_circuit.py").read_text(encoding="utf-8")


def test_lessons_seven_and_eight_are_registered():
    assert 'route="/academy/unit-2/truth-tables"' in APP
    assert 'route="/academy/unit-2/expression-to-circuit"' in APP


def test_truth_table_lesson_covers_rows_analysis_equivalence_and_minterms():
    assert "2ⁿ possible binary input combinations" in LESSONS
    assert "Analyse F = AB + A'C" in LESSONS
    assert "logically equivalent" in LESSONS
    assert "From output rows to minterms" in LESSONS
    assert "check_rows" in LESSONS
    assert "check_output" in LESSONS


def test_circuit_lesson_has_workflow_manual_design_and_simplification():
    assert "Design workflow" in LESSONS
    assert "Worked design: F = AB + A'C" in LESSONS
    assert "Simplify before building" in LESSONS
    assert "check_gate" in LESSONS
    assert "check_stage" in LESSONS


def test_lessons_integrate_boolean_lab_generator_and_simulator():
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert 'href="/tools/circuit"' in LESSONS
    assert 'href="/"' in LESSONS
    assert "Path 02 · Lesson 7 of 10" in LESSONS
    assert "Path 02 · Lesson 8 of 10" in LESSONS
    assert 'href="/academy/unit-2/universal-implementation"' in LESSONS
