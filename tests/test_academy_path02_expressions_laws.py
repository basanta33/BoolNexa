from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_boolean_expressions_laws.py").read_text(encoding="utf-8")


def test_lessons_five_and_six_are_registered():
    assert 'route="/academy/unit-2/boolean-expressions"' in APP
    assert 'route="/academy/unit-2/boolean-laws"' in APP


def test_expression_lesson_covers_notation_precedence_and_circuit_translation():
    assert "NOT A       → A'" in LESSONS
    assert "complement first, then AND, then OR" in LESSONS
    assert "Words → expression" in LESSONS
    assert "Expression → circuit" in LESSONS
    assert "check_expression" in LESSONS
    assert "check_precedence" in LESSONS


def test_laws_lesson_covers_core_laws_demorgan_and_simplification():
    assert "Absorption:" in LESSONS
    assert "(AB)' = A' + B'" in LESSONS
    assert "(A + B)' = A'B'" in LESSONS
    assert "F = A + AB" in LESSONS
    assert "F = AB + AB'" in LESSONS
    assert "check_law" in LESSONS
    assert "check_simplify" in LESSONS


def test_lessons_use_boolean_lab_and_circuit_generator():
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert "Path 02 · Lesson 5 of 10" in LESSONS
    assert "Path 02 · Lesson 6 of 10" in LESSONS
    assert 'href="/academy/unit-2/truth-tables"' in LESSONS
