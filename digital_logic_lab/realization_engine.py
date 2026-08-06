"""High-level circuit realization entry point for BoolNexa."""

from __future__ import annotations

from .circuit_engine import build_circuit_from_node
from .gate import CircuitGraph
from .nand_mapper import map_expression_to_nand
from .nor_mapper import map_expression_to_nor
from .realization_mapper import map_expression_to_policy
from .realization_policy import RealizationPolicy, RealizationPreset


def build_realized_circuit(
    expression: str,
    policy: RealizationPolicy,
    *,
    output_label: str = "F",
) -> CircuitGraph:
    if policy.preset == RealizationPreset.NAND_ONLY:
        mapped_root = map_expression_to_nand(expression)
    elif policy.preset == RealizationPreset.NOR_ONLY:
        mapped_root = map_expression_to_nor(expression)
    else:
        mapped_root = map_expression_to_policy(expression, policy)

    return build_circuit_from_node(
        mapped_root,
        source_expression=expression,
        output_label=output_label,
    )
