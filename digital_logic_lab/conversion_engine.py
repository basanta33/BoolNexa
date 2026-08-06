"""Exact base-conversion engine for BoolNexa.

Supports signed integer and fractional values in bases 2, 8, 10 and 16.
Internally, values are represented as fractions so conversions do not suffer
from binary floating-point rounding errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Final

SUPPORTED_BASES: Final[tuple[int, ...]] = (2, 8, 10, 16)
BASE_NAMES: Final[dict[int, str]] = {
    2: "Binary",
    8: "Octal",
    10: "Decimal",
    16: "Hexadecimal",
}
DIGITS: Final[str] = "0123456789ABCDEF"


class ConversionError(ValueError):
    """Raised when a number cannot be parsed or converted."""


@dataclass(frozen=True)
class ParsedNumber:
    """Normalized parsed number."""

    original: str
    normalized: str
    base: int
    sign: int
    integer_digits: str
    fractional_digits: str
    value: Fraction


@dataclass(frozen=True)
class ConversionBundle:
    """All standard BoolNexa representations for one value."""

    parsed: ParsedNumber
    binary: str
    octal: str
    decimal: str
    hexadecimal: str


def _strip_prefix(value: str, base: int) -> str:
    prefixes = {2: "0b", 8: "0o", 16: "0x"}
    prefix = prefixes.get(base)
    if prefix and value.lower().startswith(prefix):
        return value[2:]
    return value


def _digit_value(character: str) -> int:
    index = DIGITS.find(character.upper())
    if index < 0:
        raise ConversionError(f"Unsupported digit {character!r}.")
    return index


def validate_number(text: str, base: int) -> str:
    """Validate and normalize a number without converting it."""

    if base not in SUPPORTED_BASES:
        raise ConversionError("Base must be 2, 8, 10 or 16.")

    if text is None:
        raise ConversionError("Enter a value to convert.")

    value = str(text).strip().replace("_", "").replace(" ", "")
    if not value:
        raise ConversionError("Enter a value to convert.")

    if value[0] in "+-":
        value = value[1:]

    value = _strip_prefix(value, base)
    if not value:
        raise ConversionError("A base prefix must be followed by digits.")

    if value.count(".") > 1:
        raise ConversionError("Use only one radix point.")

    if value == ".":
        raise ConversionError("Enter at least one digit.")

    for character in value:
        if character == ".":
            continue
        digit = _digit_value(character)
        if digit >= base:
            raise ConversionError(
                f"Digit {character.upper()} is not valid in base {base}."
            )

    integer, dot, fraction = value.partition(".")
    integer = integer or "0"
    normalized = integer.upper()
    if dot:
        normalized += "." + fraction.upper()
    return normalized


def parse_number(text: str, base: int) -> ParsedNumber:
    """Parse a signed fixed-radix number into an exact Fraction."""

    raw = str(text).strip()
    sign = -1 if raw.startswith("-") else 1
    normalized_unsigned = validate_number(raw, base)

    integer_digits, dot, fractional_digits = normalized_unsigned.partition(".")

    integer_value = 0
    for character in integer_digits:
        integer_value = integer_value * base + _digit_value(character)

    fractional_value = Fraction(0, 1)
    place = base
    for character in fractional_digits:
        fractional_value += Fraction(_digit_value(character), place)
        place *= base

    exact_value = sign * (Fraction(integer_value, 1) + fractional_value)
    normalized = ("-" if sign < 0 and exact_value != 0 else "") + normalized_unsigned

    return ParsedNumber(
        original=raw,
        normalized=normalized,
        base=base,
        sign=-1 if exact_value < 0 else 1,
        integer_digits=integer_digits,
        fractional_digits=fractional_digits,
        value=exact_value,
    )


def _integer_to_base(integer: int, base: int) -> str:
    if integer == 0:
        return "0"

    digits: list[str] = []
    remaining = integer
    while remaining:
        remaining, remainder = divmod(remaining, base)
        digits.append(DIGITS[remainder])
    return "".join(reversed(digits))


def _fraction_to_base(
    fraction: Fraction,
    base: int,
    precision: int,
) -> tuple[str, bool]:
    """Return fractional digits and whether conversion was truncated."""

    digits: list[str] = []
    remaining = fraction
    for _ in range(max(0, precision)):
        if remaining == 0:
            return "".join(digits), False
        remaining *= base
        digit = remaining.numerator // remaining.denominator
        digits.append(DIGITS[digit])
        remaining -= digit
    return "".join(digits), remaining != 0


def format_fraction(
    value: Fraction,
    base: int,
    *,
    precision: int = 32,
    trim_trailing_zeros: bool = True,
) -> str:
    """Format an exact fraction in a target radix."""

    if base not in SUPPORTED_BASES:
        raise ConversionError("Base must be 2, 8, 10 or 16.")
    if precision < 0 or precision > 512:
        raise ConversionError("Precision must be between 0 and 512 digits.")

    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    integer = magnitude.numerator // magnitude.denominator
    fractional = magnitude - integer

    integer_text = _integer_to_base(integer, base)
    fraction_text, truncated = _fraction_to_base(fractional, base, precision)

    if trim_trailing_zeros and not truncated:
        fraction_text = fraction_text.rstrip("0")

    result = sign + integer_text
    if fraction_text:
        result += "." + fraction_text
    if truncated:
        result += "…"
    return result


def convert_all(text: str, source_base: int, precision: int = 32) -> ConversionBundle:
    """Convert an input to all four standard bases."""

    parsed = parse_number(text, source_base)
    return ConversionBundle(
        parsed=parsed,
        binary=format_fraction(parsed.value, 2, precision=precision),
        octal=format_fraction(parsed.value, 8, precision=precision),
        decimal=format_fraction(parsed.value, 10, precision=precision),
        hexadecimal=format_fraction(parsed.value, 16, precision=precision),
    )


def group_binary(binary_text: str, group_size: int = 4) -> str:
    """Group binary digits around the radix point for readability."""

    suffix = "…" if binary_text.endswith("…") else ""
    text = binary_text[:-1] if suffix else binary_text
    sign = "-" if text.startswith("-") else ""
    unsigned = text[1:] if sign else text
    integer, dot, fraction = unsigned.partition(".")

    left_groups: list[str] = []
    while integer:
        left_groups.append(integer[-group_size:])
        integer = integer[:-group_size]
    grouped_integer = " ".join(reversed(left_groups)) or "0"

    grouped_fraction = " ".join(
        fraction[index : index + group_size]
        for index in range(0, len(fraction), group_size)
    )
    result = sign + grouped_integer
    if dot:
        result += "." + grouped_fraction
    return result + suffix


def hexadecimal_to_binary_steps(parsed: ParsedNumber) -> list[str]:
    """Create digit-to-nibble steps for a hexadecimal source value."""

    if parsed.base != 16:
        return []

    steps: list[str] = []
    unsigned = parsed.normalized.lstrip("-")
    for character in unsigned:
        if character == ".":
            steps.append("Radix point stays in the same position.")
        else:
            steps.append(f"{character}₁₆ → {_digit_value(character):04b}₂")
    return steps


def positional_expansion(parsed: ParsedNumber) -> list[str]:
    """Create exact positional-weight terms for any supported source base."""

    terms: list[str] = []
    integer_len = len(parsed.integer_digits)
    for index, character in enumerate(parsed.integer_digits):
        exponent = integer_len - index - 1
        digit = _digit_value(character)
        terms.append(f"{digit} × {parsed.base}^{exponent}")

    for index, character in enumerate(parsed.fractional_digits, start=1):
        digit = _digit_value(character)
        terms.append(f"{digit} × {parsed.base}^-{index}")
    return terms
