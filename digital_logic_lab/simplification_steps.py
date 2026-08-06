"""Data structures for BoolNexa simplification walkthroughs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimplificationStep:
    number: int
    before: str
    after: str
    law_key: str
    law_name: str
    formula: str
    explanation: str


@dataclass(frozen=True)
class SimplificationResult:
    original: str
    normalized: str
    simplified: str
    variables: list[str]
    minterms: list[int]
    steps: list[SimplificationStep]
    literal_count_before: int
    literal_count_after: int
    term_count_before: int
    term_count_after: int
