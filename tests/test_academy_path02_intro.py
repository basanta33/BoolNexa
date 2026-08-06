from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_boolean_gates_intro.py").read_text(encoding="utf-8")
MODELS = (ROOT / "digital_logic_lab" / "academy" / "models.py").read_text(encoding="utf-8")


def test_path02_lessons_one_and_two_are_registered():
    assert 'route="/academy/unit-2/logic-states-and-gates"' in APP
    assert 'route="/academy/unit-2/and-or-not"' in APP
    assert "logic_states_gates_lesson" in APP
    assert "and_or_not_lesson" in APP


def test_lesson_one_teaches_logic_states_and_truth_tables():
    assert "Logic 0 and logic 1" in LESSONS
    assert "LOW" in LESSONS and "HIGH" in LESSONS
    assert "truth table" in LESSONS.lower()
    assert "check_logic_state" in LESSONS


def test_lesson_two_teaches_and_or_not_with_interaction():
    assert "Y = A·B = AB" in LESSONS
    assert "Y = A + B" in LESSONS
    assert "Y = A'" in LESSONS
    assert "check_and" in LESSONS
    assert "check_or" in LESSONS
    assert "check_not" in LESSONS


def test_path02_uses_real_boolnexa_tools_and_card_entry():
    assert 'href="/"' in LESSONS
    assert 'href="/tools/boolean"' in LESSONS
    assert '2: ("/academy/unit-2/logic-states-and-gates", "Begin Path 02")' in MODELS
    assert "Path 02 · Lesson 1 of 10" in LESSONS
    assert "Path 02 · Lesson 2 of 10" in LESSONS
