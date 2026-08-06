"""Tests for BoolNexa Boolean simplification."""

from itertools import product

from digital_logic_lab.boolean_engine import evaluate_expression, parse_expression
from digital_logic_lab.boolean_simplifier import simplify_expression


def assert_equivalent(original: str, simplified: str) -> None:
    node = parse_expression(original)
    variables = sorted(node.variables())
    for bits in product((False, True), repeat=len(variables)):
        values = dict(zip(variables, bits))
        assert evaluate_expression(original, values) == evaluate_expression(
            simplified, values
        )


def test_absorption_style_expression() -> None:
    result = simplify_expression("A + AB")
    assert result.simplified == "A"
    assert_equivalent("A + AB", result.simplified)


def test_complement_pair_factorization() -> None:
    result = simplify_expression("AB + AB'")
    assert result.simplified == "A"
    assert_equivalent("AB + AB'", result.simplified)


def test_majority_function_is_already_minimal() -> None:
    result = simplify_expression("AB + BC + CA")
    assert_equivalent("AB + BC + CA", result.simplified)
    assert result.literal_count_after <= result.literal_count_before


def test_tautology() -> None:
    result = simplify_expression("A + A'")
    assert result.simplified == "1"


def test_contradiction() -> None:
    result = simplify_expression("AA'")
    assert result.simplified == "0"


def test_three_variable_minimization() -> None:
    result = simplify_expression("A'B'C + A'BC + AB'C + ABC")
    assert result.simplified == "C"
    assert_equivalent(result.original, result.simplified)


def test_steps_are_educational() -> None:
    result = simplify_expression("AB + AB'")
    assert result.steps
    assert all(step.law_name for step in result.steps)
    assert all(step.explanation for step in result.steps)
