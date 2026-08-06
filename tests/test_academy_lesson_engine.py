import pytest

from digital_logic_lab.lesson_content import UNIT_1_LESSONS, binary_value, weighted_terms


def test_unit_one_lessons_are_simulation_led():
    assert UNIT_1_LESSONS[0]["id"] == "why-computers-use-binary"
    assert UNIT_1_LESSONS[0]["status"] == "available"
    assert all(lesson["simulator_activity"] for lesson in UNIT_1_LESSONS)


def test_binary_value_uses_msb_first_order():
    assert binary_value((1, 0, 1, 0)) == 10
    assert binary_value((1, 1, 1, 1)) == 15
    assert binary_value((0, 0, 0, 0)) == 0


def test_weighted_terms_explain_each_bit_contribution():
    assert weighted_terms((1, 0, 1, 0)) == (8, 0, 2, 0)


def test_binary_helpers_reject_non_binary_digits():
    with pytest.raises(ValueError):
        binary_value((1, 2, 0))
