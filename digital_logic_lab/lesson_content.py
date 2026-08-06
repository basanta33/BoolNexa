"""Structured lesson content for BoolNexa Academy.

The lesson catalogue deliberately contains only topics that can be demonstrated,
constructed, tested or visualised in BoolNexa's digital simulator.
"""
from __future__ import annotations

from typing import Final


UNIT_1_LESSONS: Final[tuple[dict[str, object], ...]] = (
    {
        "id": "why-computers-use-binary",
        "number": 1,
        "title": "Why Computers Use Binary",
        "duration": 20,
        "status": "available",
        "summary": "Explore how two stable logic states represent information and control digital circuits.",
        "simulator_activity": "Toggle a four-bit input bank and observe its binary, decimal and weighted values.",
    },
    {
        "id": "binary-place-values",
        "number": 2,
        "title": "Binary Place Values",
        "duration": 25,
        "status": "planned",
        "summary": "Build binary numbers from powers of two and inspect each bit's contribution.",
        "simulator_activity": "Use switches and weighted LEDs to compose target values.",
    },
    {
        "id": "base-conversion",
        "number": 3,
        "title": "Base Conversion",
        "duration": 30,
        "status": "planned",
        "summary": "Convert between decimal, binary, octal and hexadecimal representations.",
        "simulator_activity": "Interactive converter with step-by-step working.",
    },
    {
        "id": "binary-arithmetic",
        "number": 4,
        "title": "Binary Arithmetic",
        "duration": 35,
        "status": "planned",
        "summary": "Perform binary addition and subtraction and detect carry and borrow.",
        "simulator_activity": "Construct and test half-adder and full-adder stages.",
    },
    {
        "id": "signed-numbers",
        "number": 5,
        "title": "Signed Numbers and Two's Complement",
        "duration": 35,
        "status": "planned",
        "summary": "Represent positive and negative values and recognise overflow.",
        "simulator_activity": "Adjust a fixed-width register and compare unsigned and signed interpretations.",
    },
    {
        "id": "digital-codes",
        "number": 6,
        "title": "Digital Codes",
        "duration": 30,
        "status": "planned",
        "summary": "Investigate BCD, Excess-3 and Gray code.",
        "simulator_activity": "Convert codes and test code-converter circuits.",
    },
    {
        "id": "parity",
        "number": 7,
        "title": "Parity and Error Detection",
        "duration": 25,
        "status": "planned",
        "summary": "Generate and check even and odd parity bits.",
        "simulator_activity": "Inject a bit error and observe parity detection.",
    },
    {
        "id": "bits-in-registers",
        "number": 8,
        "title": "Bits Stored in Registers",
        "duration": 30,
        "status": "planned",
        "summary": "See how groups of flip-flops store words of binary data.",
        "simulator_activity": "Load, clear and inspect a four-bit register.",
    },
)


def binary_value(bits: tuple[int, ...] | list[int]) -> int:
    """Return the unsigned value of a most-significant-bit-first bit sequence."""
    value = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("bits must contain only 0 or 1")
        value = (value << 1) | bit
    return value


def weighted_terms(bits: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    """Return each bit's positional contribution, MSB first."""
    width = len(bits)
    return tuple(bit * (2 ** (width - index - 1)) for index, bit in enumerate(bits))
