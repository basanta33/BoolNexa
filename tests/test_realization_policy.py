import pytest

from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_policy import (
    OptimizationObjective,
    RealizationPolicy,
    RealizationPreset,
    gate_names,
    realization_policy_for_preset,
)


def test_basic_only_preset():
    policy = realization_policy_for_preset(RealizationPreset.BASIC_ONLY)
    assert policy.allowed_gates == frozenset(
        {GateKind.AND, GateKind.OR, GateKind.NOT}
    )
    assert policy.forced_only is True
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_xor_preferred_is_allowed_and_preferred():
    policy = realization_policy_for_preset(RealizationPreset.XOR_PREFERRED)
    assert policy.allows(GateKind.XOR)
    assert policy.prefers(GateKind.XOR)
    assert policy.allows(GateKind.AND)
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_nand_only_is_universal():
    policy = realization_policy_for_preset(RealizationPreset.NAND_ONLY)
    assert policy.allowed_gates == frozenset({GateKind.NAND})
    assert policy.is_universal_single_gate_family()
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_nor_only_is_universal():
    policy = realization_policy_for_preset(RealizationPreset.NOR_ONLY)
    assert policy.allowed_gates == frozenset({GateKind.NOR})
    assert policy.is_universal_single_gate_family()
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_and_not_is_functionally_complete():
    policy = RealizationPolicy(
        allowed_gates=frozenset({GateKind.AND, GateKind.NOT})
    )
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_or_not_is_functionally_complete():
    policy = RealizationPolicy(
        allowed_gates=frozenset({GateKind.OR, GateKind.NOT})
    )
    assert policy.is_functionally_complete_for_arbitrary_boolean()


def test_xor_alone_is_reported_insufficient():
    policy = RealizationPolicy(
        allowed_gates=frozenset({GateKind.XOR}),
        forced_only=True,
    )
    assert not policy.is_functionally_complete_for_arbitrary_boolean()
    assert "not functionally complete" in policy.insufficiency_message()


def test_preferred_gate_must_also_be_allowed():
    with pytest.raises(ValueError, match="Preferred gates must also be allowed"):
        RealizationPolicy(
            allowed_gates=frozenset({GateKind.AND, GateKind.OR}),
            preferred_gates=frozenset({GateKind.XOR}),
        )


def test_input_output_cannot_be_realization_gate():
    with pytest.raises(ValueError, match="Non-synthesis gate"):
        RealizationPolicy(
            allowed_gates=frozenset({GateKind.INPUT, GateKind.AND})
        )


def test_empty_gate_set_is_rejected():
    with pytest.raises(ValueError, match="At least one synthesis gate"):
        RealizationPolicy(allowed_gates=frozenset())


def test_objective_is_preserved_by_preset():
    policy = realization_policy_for_preset(
        RealizationPreset.AUTO,
        objective=OptimizationObjective.MIN_LOGIC_DEPTH,
    )
    assert policy.objective == OptimizationObjective.MIN_LOGIC_DEPTH


def test_gate_names_are_stable_for_ui():
    policy = RealizationPolicy(
        allowed_gates=frozenset(
            {GateKind.XOR, GateKind.NOT, GateKind.AND}
        )
    )
    assert gate_names(policy.allowed_gates) == ("AND", "NOT", "XOR")
