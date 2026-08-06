import pytest

from digital_logic_lab.boolean_engine import (
    BooleanExpressionError,
    canonical_sum_to_expression,
    generate_truth_table,
)
from digital_logic_lab.boolean_simplifier import simplify_expression
from digital_logic_lab.kmap_engine import build_kmap


def test_explicit_sum_of_minterms_matches_boolean_expression() -> None:
    canonical = generate_truth_table("F(A,B,C) = Σm(4,6,7)", include_intermediate=False)
    algebraic = generate_truth_table("AB + AC'", include_intermediate=False)
    assert canonical.variables == ["A", "B", "C"]
    assert canonical.minterms == [4, 6, 7]
    assert canonical.rows == algebraic.rows


def test_bare_sum_of_minterms_infers_minimum_abc_width() -> None:
    table = generate_truth_table("F = Σm(4,6,7)", include_intermediate=False)
    assert table.variables == ["A", "B", "C"]
    assert table.minterms == [4, 6, 7]


def test_sum_of_minterms_drives_reduction_and_kmap() -> None:
    simplified = simplify_expression("F(A,B,C)=Σm(4,6,7)")
    kmap = build_kmap("F(A,B,C)=Σm(4,6,7)")
    assert simplified.simplified == "AB + AC'"
    assert kmap.minterms == [4, 6, 7]
    assert kmap.simplified_expression == "AB + AC'"


def test_explicit_variable_header_preserves_variable_order_and_zero_rows() -> None:
    table = generate_truth_table("F(W,X,Y,Z)=Σm(1,3)", include_intermediate=False)
    assert table.variables == ["W", "X", "Y", "Z"]
    assert len(table.rows) == 16
    assert table.minterms == [1, 3]


def test_rejects_out_of_range_minterm() -> None:
    with pytest.raises(BooleanExpressionError, match="outside the range"):
        generate_truth_table("F(A,B)=Σm(4)", include_intermediate=False)


def test_converter_returns_parser_ready_expression() -> None:
    converted = canonical_sum_to_expression("F(A,B,C)=Σm(4,6,7)")
    assert converted is not None
    expression, variables, minterms = converted
    assert variables == ["A", "B", "C"]
    assert minterms == [4, 6, 7]
    assert "*" in expression
