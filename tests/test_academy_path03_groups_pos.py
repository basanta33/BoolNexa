from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_kmap_groups_pos.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_kmap_three_four.py").read_text(encoding="utf-8")


def test_lessons_five_and_six_are_registered():
    assert 'route="/academy/unit-3/prime-implicants"' in APP
    assert 'route="/academy/unit-3/sop-pos-dont-cares"' in APP


def test_prime_implicant_lesson_covers_maximal_essential_and_overlap():
    assert "A prime implicant is a valid power-of-two group" in LESSONS
    assert "essential" in LESSONS.lower()
    assert "Why overlap is allowed" in LESSONS
    assert "Coverage strategy" in LESSONS
    assert "check_prime" in LESSONS
    assert "check_essential" in LESSONS


def test_sop_pos_dontcare_lesson_is_complete():
    assert "SOP: group the 1s" in LESSONS
    assert "POS: group the 0s" in LESSONS
    assert "Don't-care conditions" in LESSONS
    assert "may act as 0 or 1" in LESSONS
    assert "check_pos" in LESSONS
    assert "check_dontcare" in LESSONS


def test_navigation_and_real_tool_integration():
    assert 'href="/academy/unit-3/prime-implicants"' in PREVIOUS
    assert 'href="/academy/unit-3/sop-pos-dont-cares"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert 'href="/tools/circuit"' in LESSONS
    assert "Path 03 · Lesson 5" in LESSONS
    assert "Path 03 · Lesson 6" in LESSONS
