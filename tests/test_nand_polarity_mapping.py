"""Additional polarity-aware NAND regression tests."""

from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_engine import build_realized_circuit
from digital_logic_lab.realization_policy import (
    RealizationPreset,
    realization_policy_for_preset,
)


def _graph(expr: str):
    return build_realized_circuit(
        expr,
        realization_policy_for_preset(RealizationPreset.NAND_ONLY),
    )


def test_ab_plus_ac_not_is_four_nands_after_polarity_mapping():
    graph = _graph("AB + AC'")
    nand = [n for n in graph.nodes if n.kind == GateKind.NAND]
    assert len(nand) == 4


def test_ab_plus_cd_is_three_nands():
    # SOP NAND-NAND form:
    # (AB)' and (CD)' feed final NAND.
    graph = _graph("AB + CD")
    assert graph.statistics.counts == {"NAND": 3}


def test_a_plus_b_is_three_nands():
    graph = _graph("A+B")
    assert graph.statistics.counts == {"NAND": 3}


def test_ab_is_two_nands():
    graph = _graph("AB")
    assert graph.statistics.counts == {"NAND": 2}
