"""BoolNexa Sprint 6.5.5 — unified realization strategy.

Provides one UI-facing entry point that:
- applies the selected realization policy;
- builds the realized circuit;
- reports gate usage/count/depth;
- reports whether preferred gates were actually used;
- produces deterministic candidate scores for future automatic selection.
"""

from __future__ import annotations

from dataclasses import dataclass

from .gate import CircuitGraph, GateKind
from .realization_engine import build_realized_circuit
from .realization_policy import (
    OptimizationObjective,
    RealizationPolicy,
    RealizationPreset,
    gate_names,
    realization_policy_for_preset,
)


@dataclass(frozen=True)
class RealizationSummary:
    preset: RealizationPreset
    objective: OptimizationObjective
    allowed_gates: tuple[str, ...]
    preferred_gates: tuple[str, ...]
    gates_used: tuple[str, ...]
    preferred_gates_used: tuple[str, ...]
    total_gates: int
    logic_depth: int
    strict: bool
    preferred_requirement_satisfied: bool
    functionally_complete: bool
    note: str


@dataclass(frozen=True)
class RealizationResult:
    graph: CircuitGraph
    policy: RealizationPolicy
    summary: RealizationSummary


def _logical_gate_kinds(graph: CircuitGraph) -> frozenset[GateKind]:
    return frozenset(
        node.kind
        for node in graph.nodes
        if node.kind not in {
            GateKind.INPUT,
            GateKind.CONSTANT,
            GateKind.OUTPUT,
        }
    )


def summarize_realization(
    graph: CircuitGraph,
    policy: RealizationPolicy,
) -> RealizationSummary:
    used = _logical_gate_kinds(graph)
    preferred_used = used & policy.preferred_gates

    if policy.preferred_gates:
        preferred_ok = bool(preferred_used)
        note = (
            "Preferred gate(s) used."
            if preferred_ok
            else "No preferred gate was required by this realization."
        )
    else:
        preferred_ok = True
        note = "No preferred-gate requirement."

    return RealizationSummary(
        preset=policy.preset,
        objective=policy.objective,
        allowed_gates=gate_names(policy.allowed_gates),
        preferred_gates=gate_names(policy.preferred_gates),
        gates_used=gate_names(used),
        preferred_gates_used=gate_names(preferred_used),
        total_gates=graph.statistics.total_gates,
        logic_depth=graph.statistics.logic_depth,
        strict=policy.forced_only,
        preferred_requirement_satisfied=preferred_ok,
        functionally_complete=policy.is_functionally_complete_for_arbitrary_boolean(),
        note=note,
    )


def realize(
    expression: str,
    policy: RealizationPolicy,
    *,
    output_label: str = "F",
) -> RealizationResult:
    graph = build_realized_circuit(
        expression,
        policy,
        output_label=output_label,
    )
    return RealizationResult(
        graph=graph,
        policy=policy,
        summary=summarize_realization(graph, policy),
    )


def realize_preset(
    expression: str,
    preset: RealizationPreset,
    *,
    objective: OptimizationObjective = OptimizationObjective.BALANCED,
    output_label: str = "F",
) -> RealizationResult:
    policy = realization_policy_for_preset(
        preset,
        objective=objective,
    )
    return realize(expression, policy, output_label=output_label)


def candidate_score(
    summary: RealizationSummary,
) -> tuple[int, int, int]:
    """Return a deterministic lower-is-better score.

    The objective controls the primary optimization dimension. A penalty is
    applied when a preferred-gate policy does not actually use a preferred
    gate. This is groundwork for future multi-candidate AUTO selection.
    """
    preference_penalty = (
        0 if summary.preferred_requirement_satisfied else 1
    )

    if summary.objective == OptimizationObjective.MIN_GATE_COUNT:
        return (
            summary.total_gates,
            summary.logic_depth,
            preference_penalty,
        )

    if summary.objective == OptimizationObjective.MIN_LOGIC_DEPTH:
        return (
            summary.logic_depth,
            summary.total_gates,
            preference_penalty,
        )

    if summary.objective == OptimizationObjective.PREFERRED_GATES:
        return (
            preference_penalty,
            summary.total_gates,
            summary.logic_depth,
        )

    # BALANCED: gate count first, then depth, then preference.
    return (
        summary.total_gates,
        summary.logic_depth,
        preference_penalty,
    )
