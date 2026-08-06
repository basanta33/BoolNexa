"""Educational step generation for BoolNexa number conversions."""

from __future__ import annotations

from .conversion_engine import (
    BASE_NAMES,
    ConversionBundle,
    group_binary,
    hexadecimal_to_binary_steps,
    positional_expansion,
)


def build_explanation(bundle: ConversionBundle) -> list[str]:
    """Return readable, source-aware conversion steps."""

    parsed = bundle.parsed
    source_name = BASE_NAMES[parsed.base]
    steps = [
        f"Read {parsed.normalized} as a base-{parsed.base} ({source_name}) number.",
    ]

    if parsed.sign < 0:
        steps.append("Keep the negative sign and convert the magnitude.")

    if parsed.base == 16:
        steps.extend(hexadecimal_to_binary_steps(parsed))
        steps.append(f"Grouped binary result: {group_binary(bundle.binary)}")
    else:
        terms = positional_expansion(parsed)
        if terms:
            steps.append("Positional expansion: " + " + ".join(terms))

    steps.extend(
        [
            f"Binary: {group_binary(bundle.binary)}",
            f"Octal: {bundle.octal}",
            f"Decimal: {bundle.decimal}",
            f"Hexadecimal: {bundle.hexadecimal}",
        ]
    )
    return steps
