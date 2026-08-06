"""Boolean law catalogue used by BoolNexa educational explanations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BooleanLaw:
    key: str
    name: str
    formula: str
    explanation: str


LAWS: dict[str, BooleanLaw] = {
    "normalization": BooleanLaw(
        "normalization",
        "Expression normalization",
        "Equivalent operator notation",
        "Convert the entered notation into BoolNexa's standard Boolean notation.",
    ),
    "identity": BooleanLaw(
        "identity",
        "Identity law",
        "X + 0 = X,  X·1 = X",
        "Adding 0 or multiplying by 1 leaves a Boolean expression unchanged.",
    ),
    "domination": BooleanLaw(
        "domination",
        "Domination law",
        "X + 1 = 1,  X·0 = 0",
        "OR with 1 is always 1, while AND with 0 is always 0.",
    ),
    "idempotent": BooleanLaw(
        "idempotent",
        "Idempotent law",
        "X + X = X,  X·X = X",
        "Repeating the same Boolean term does not change its value.",
    ),
    "complement": BooleanLaw(
        "complement",
        "Complement law",
        "X + X' = 1,  X·X' = 0",
        "A variable and its complement cover all cases under OR and no cases under AND.",
    ),
    "absorption": BooleanLaw(
        "absorption",
        "Absorption law",
        "X + XY = X,  X(X + Y) = X",
        "The broader term already covers the more specific term.",
    ),
    "double_negation": BooleanLaw(
        "double_negation",
        "Double-negation law",
        "(X')' = X",
        "Negating a Boolean value twice returns the original value.",
    ),
    "de_morgan": BooleanLaw(
        "de_morgan",
        "De Morgan's law",
        "(X + Y)' = X'Y',  (XY)' = X' + Y'",
        "Negating a group swaps AND and OR while complementing every input.",
    ),
    "canonical_sop": BooleanLaw(
        "canonical_sop",
        "Canonical SOP construction",
        "F = Σm(...)",
        "Write one product term for every truth-table row where the output is 1.",
    ),
    "adjacent_combination": BooleanLaw(
        "adjacent_combination",
        "Adjacent minterm combination",
        "XY + XY' = X",
        "Terms that differ in exactly one literal can be combined by removing that literal.",
    ),
    "prime_implicant": BooleanLaw(
        "prime_implicant",
        "Prime implicant selection",
        "Cover every required minterm",
        "Choose the smallest set of combined terms that covers every output-1 row.",
    ),
    "equivalent_minimum": BooleanLaw(
        "equivalent_minimum",
        "Equivalent minimum form",
        "F_original = F_simplified",
        "The final expression has the same truth table but uses fewer literals or terms.",
    ),
}


def get_law(key: str) -> BooleanLaw:
    try:
        return LAWS[key]
    except KeyError as exc:
        raise KeyError(f"Unknown Boolean law: {key}") from exc
