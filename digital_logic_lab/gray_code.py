"""Gray-code utilities for BoolNexa Karnaugh maps."""

from __future__ import annotations


def gray_code(bits: int) -> list[str]:
    """Return reflected Gray-code strings of the requested width."""
    if bits < 0:
        raise ValueError("bits must be non-negative")
    if bits == 0:
        return [""]
    values = [""]
    for _ in range(bits):
        values = ["0" + value for value in values] + [
            "1" + value for value in reversed(values)
        ]
    return values


def gray_index(value: int) -> int:
    """Convert a binary integer to its Gray-code integer."""
    if value < 0:
        raise ValueError("value must be non-negative")
    return value ^ (value >> 1)
