from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_boolean_universal_xor.py").read_text(encoding="utf-8")


def test_lessons_three_and_four_are_registered():
    assert 'route="/academy/unit-2/nand-nor"' in APP
    assert 'route="/academy/unit-2/xor-xnor"' in APP


def test_nand_nor_lesson_teaches_universal_gate_implementations():
    assert "Y = (AB)'" in LESSONS
    assert "Y = (A + B)'" in LESSONS
    assert "Why are they universal?" in LESSONS
    assert "NAND-only" in LESSONS
    assert "NOR-only" in LESSONS
    assert "check_nand" in LESSONS
    assert "check_nor" in LESSONS


def test_xor_xnor_lesson_covers_truth_arithmetic_and_parity():
    assert "A ⊕ B = A'B + AB'" in LESSONS
    assert "A XNOR B" in LESSONS
    assert "SUM   = A ⊕ B" in LESSONS
    assert "XOR and parity" in LESSONS
    assert "check_xor" in LESSONS
    assert "check_xnor" in LESSONS


def test_lessons_use_real_boolnexa_tools_and_continue_navigation():
    assert 'href="/"' in LESSONS
    assert 'href="/tools/boolean"' in LESSONS
    assert "Path 02 · Lesson 3 of 10" in LESSONS
    assert "Path 02 · Lesson 4 of 10" in LESSONS
    assert 'href="/academy/unit-2/boolean-expressions"' in LESSONS
