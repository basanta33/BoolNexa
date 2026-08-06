"""Gate-set and realization-policy model for BoolNexa.

Sprint 6.5.1 introduces a technology-mapping policy layer between a logical
Boolean function and the circuit-synthesis engine.

This module does not perform synthesis yet. It defines:
- which gates are allowed;
- which allowed gates are preferred;
- whether the selection is a strict/forced family;
- the optimization objective;
- reusable presets;
- validation and functional-completeness checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .gate import GateKind


SYNTHESIS_GATES: frozenset[GateKind] = frozenset(
    {
        GateKind.BUFFER,
        GateKind.NOT,
        GateKind.AND,
        GateKind.OR,
        GateKind.XOR,
        GateKind.NAND,
        GateKind.NOR,
        GateKind.XNOR,
    }
)


class RealizationPreset(str, Enum):
    AUTO = "AUTO"
    BASIC_ONLY = "BASIC_ONLY"
    XOR_PREFERRED = "XOR_PREFERRED"
    NAND_ONLY = "NAND_ONLY"
    NOR_ONLY = "NOR_ONLY"
    CUSTOM = "CUSTOM"


class OptimizationObjective(str, Enum):
    BALANCED = "BALANCED"
    MIN_GATE_COUNT = "MIN_GATE_COUNT"
    MIN_LOGIC_DEPTH = "MIN_LOGIC_DEPTH"
    PREFERRED_GATES = "PREFERRED_GATES"


@dataclass(frozen=True)
class RealizationPolicy:
    """Technology-mapping constraints for a circuit realization."""

    allowed_gates: frozenset[GateKind]
    preferred_gates: frozenset[GateKind] = frozenset()
    objective: OptimizationObjective = OptimizationObjective.BALANCED
    forced_only: bool = False
    preset: RealizationPreset = RealizationPreset.CUSTOM

    def __post_init__(self) -> None:
        invalid_allowed = set(self.allowed_gates) - set(SYNTHESIS_GATES)
        if invalid_allowed:
            names = ", ".join(sorted(g.value for g in invalid_allowed))
            raise ValueError(
                f"Non-synthesis gate(s) cannot be selected for realization: {names}"
            )

        invalid_preferred = set(self.preferred_gates) - set(self.allowed_gates)
        if invalid_preferred:
            names = ", ".join(sorted(g.value for g in invalid_preferred))
            raise ValueError(
                "Preferred gates must also be allowed. "
                f"Not allowed: {names}"
            )

        if not self.allowed_gates:
            raise ValueError("At least one synthesis gate must be allowed.")

    def allows(self, kind: GateKind) -> bool:
        return kind in self.allowed_gates

    def prefers(self, kind: GateKind) -> bool:
        return kind in self.preferred_gates

    def is_universal_single_gate_family(self) -> bool:
        return self.allowed_gates in (
            frozenset({GateKind.NAND}),
            frozenset({GateKind.NOR}),
        )

    def is_functionally_complete_for_arbitrary_boolean(self) -> bool:
        gates = self.allowed_gates

        if GateKind.NAND in gates:
            return True
        if GateKind.NOR in gates:
            return True

        if {GateKind.AND, GateKind.OR, GateKind.NOT}.issubset(gates):
            return True

        if {GateKind.AND, GateKind.NOT}.issubset(gates):
            return True

        if {GateKind.OR, GateKind.NOT}.issubset(gates):
            return True

        return False

    def insufficiency_message(self) -> str:
        if self.is_functionally_complete_for_arbitrary_boolean():
            return ""

        selected = ", ".join(sorted(g.value for g in self.allowed_gates))
        return (
            "Selected gate set is not functionally complete for arbitrary "
            f"Boolean realization: {selected}. Add NOT with AND or OR, "
            "or use NAND-only / NOR-only realization."
        )


def realization_policy_for_preset(
    preset: RealizationPreset,
    *,
    objective: OptimizationObjective = OptimizationObjective.BALANCED,
) -> RealizationPolicy:
    if preset == RealizationPreset.AUTO:
        return RealizationPolicy(
            allowed_gates=frozenset(
                {
                    GateKind.NOT,
                    GateKind.AND,
                    GateKind.OR,
                    GateKind.XOR,
                    GateKind.NAND,
                    GateKind.NOR,
                    GateKind.XNOR,
                    GateKind.BUFFER,
                }
            ),
            preferred_gates=frozenset(
                {
                    GateKind.XOR,
                    GateKind.XNOR,
                    GateKind.AND,
                    GateKind.OR,
                    GateKind.NOT,
                }
            ),
            objective=objective,
            forced_only=False,
            preset=preset,
        )

    if preset == RealizationPreset.BASIC_ONLY:
        return RealizationPolicy(
            allowed_gates=frozenset(
                {GateKind.AND, GateKind.OR, GateKind.NOT}
            ),
            preferred_gates=frozenset(),
            objective=objective,
            forced_only=True,
            preset=preset,
        )

    if preset == RealizationPreset.XOR_PREFERRED:
        return RealizationPolicy(
            allowed_gates=frozenset(
                {
                    GateKind.AND,
                    GateKind.OR,
                    GateKind.NOT,
                    GateKind.XOR,
                    GateKind.XNOR,
                }
            ),
            preferred_gates=frozenset(
                {GateKind.XOR, GateKind.XNOR}
            ),
            objective=objective,
            forced_only=False,
            preset=preset,
        )

    if preset == RealizationPreset.NAND_ONLY:
        return RealizationPolicy(
            allowed_gates=frozenset({GateKind.NAND}),
            preferred_gates=frozenset({GateKind.NAND}),
            objective=objective,
            forced_only=True,
            preset=preset,
        )

    if preset == RealizationPreset.NOR_ONLY:
        return RealizationPolicy(
            allowed_gates=frozenset({GateKind.NOR}),
            preferred_gates=frozenset({GateKind.NOR}),
            objective=objective,
            forced_only=True,
            preset=preset,
        )

    raise ValueError(
        "CUSTOM policies must be created explicitly with RealizationPolicy."
    )


def gate_names(gates: frozenset[GateKind]) -> tuple[str, ...]:
    return tuple(sorted(gate.value for gate in gates))
