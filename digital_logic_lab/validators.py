"""Validation helpers for BoolNexa number-system tools."""

from __future__ import annotations

from .conversion_engine import ConversionError, SUPPORTED_BASES, validate_number


def validate_precision(value: str | int) -> int:
    """Return a safe fractional precision from user input."""

    try:
        precision = int(value)
    except (TypeError, ValueError) as exc:
        raise ConversionError("Precision must be a whole number.") from exc

    if not 1 <= precision <= 128:
        raise ConversionError("Precision must be between 1 and 128 digits.")
    return precision


def validate_source_base(value: str | int) -> int:
    """Normalize and validate a source base."""

    try:
        base = int(value)
    except (TypeError, ValueError) as exc:
        raise ConversionError("Choose a valid input base.") from exc

    if base not in SUPPORTED_BASES:
        raise ConversionError("Choose Binary, Octal, Decimal or Hexadecimal.")
    return base


__all__ = [
    "ConversionError",
    "validate_number",
    "validate_precision",
    "validate_source_base",
]
