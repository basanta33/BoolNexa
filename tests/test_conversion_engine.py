"""Regression tests for BoolNexa exact number conversion."""

from fractions import Fraction

from digital_logic_lab.conversion_engine import (
    convert_all,
    format_fraction,
    group_binary,
    parse_number,
)


def test_hex_fraction_example() -> None:
    result = convert_all("2FD34.2FF", 16, precision=48)
    assert result.binary == "101111110100110100.001011111111"
    assert result.decimal == "195892.187255859375"
    assert result.hexadecimal == "2FD34.2FF"


def test_binary_fraction_is_exact() -> None:
    parsed = parse_number("101.101", 2)
    assert parsed.value == Fraction(45, 8)
    assert format_fraction(parsed.value, 10) == "5.625"


def test_negative_and_prefix() -> None:
    result = convert_all("-0xA.F", 16)
    assert result.decimal == "-10.9375"
    assert result.binary == "-1010.1111"


def test_group_binary() -> None:
    assert group_binary("101111110100110100.001011111111") == (
        "10 1111 1101 0011 0100.0010 1111 1111"
    )
