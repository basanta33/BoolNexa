from digital_logic_lab.academy_content import ACADEMY_UNITS, LABS, LESSON_SECTIONS


def test_academy_has_complete_seven_unit_curriculum():
    assert [unit["number"] for unit in ACADEMY_UNITS] == list(range(1, 13))
    assert sum(int(unit["hours"]) for unit in ACADEMY_UNITS) == 82
    assert all(unit["title"] and unit["summary"] for unit in ACADEMY_UNITS)


def test_boolean_algebra_unit_preserves_historical_context():
    unit = ACADEMY_UNITS[1]
    assert "George Boole" in str(unit["summary"])
    assert "Claude Shannon" in str(unit["summary"])


def test_laboratory_and_lesson_templates_are_complete():
    assert len(LABS) == 9
    assert "Clock pulse generator" in LABS
    assert "Historical background" in LESSON_SECTIONS
    assert "Originator and contributors" in LESSON_SECTIONS
    assert "Interactive simulation" in LESSON_SECTIONS
    assert "References" in LESSON_SECTIONS
