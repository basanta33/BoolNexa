from digital_logic_lab.gate import GateKind
from digital_logic_lab.realization_policy import (
    OptimizationObjective,
    RealizationPreset,
)
from digital_logic_lab.realization_strategy import (
    candidate_score,
    realize_preset,
)


def test_basic_summary_reports_only_basic_gates_for_xor():
    result = realize_preset("A^B", RealizationPreset.BASIC_ONLY)
    assert "XOR" not in result.summary.gates_used
    assert set(result.summary.gates_used) <= {"AND", "OR", "NOT"}
    assert result.summary.strict is True


def test_xor_preferred_summary_reports_xor_used():
    result = realize_preset("A^B", RealizationPreset.XOR_PREFERRED)
    assert result.summary.gates_used == ("XOR",)
    assert result.summary.preferred_gates_used == ("XOR",)
    assert result.summary.preferred_requirement_satisfied is True


def test_xor_preferred_does_not_claim_xor_required_for_plain_and():
    result = realize_preset("AB", RealizationPreset.XOR_PREFERRED)
    assert result.summary.gates_used == ("AND",)
    assert result.summary.preferred_gates_used == ()
    assert result.summary.preferred_requirement_satisfied is False
    assert "No preferred gate" in result.summary.note


def test_nand_summary_is_strict_and_nand_only():
    result = realize_preset("A^B", RealizationPreset.NAND_ONLY)
    assert result.summary.gates_used == ("NAND",)
    assert result.summary.total_gates == 4
    assert result.summary.strict is True


def test_nor_summary_is_strict_and_nor_only():
    result = realize_preset("A^B", RealizationPreset.NOR_ONLY)
    assert result.summary.gates_used == ("NOR",)
    assert result.summary.total_gates == 5
    assert result.summary.strict is True


def test_summary_matches_graph_statistics():
    result = realize_preset("AB+AC'", RealizationPreset.BASIC_ONLY)
    assert result.summary.total_gates == result.graph.statistics.total_gates
    assert result.summary.logic_depth == result.graph.statistics.logic_depth


def test_gate_count_objective_scores_gate_count_first():
    result = realize_preset(
        "A^B",
        RealizationPreset.NAND_ONLY,
        objective=OptimizationObjective.MIN_GATE_COUNT,
    )
    score = candidate_score(result.summary)
    assert score[0] == result.summary.total_gates


def test_depth_objective_scores_depth_first():
    result = realize_preset(
        "AB+AC'",
        RealizationPreset.BASIC_ONLY,
        objective=OptimizationObjective.MIN_LOGIC_DEPTH,
    )
    score = candidate_score(result.summary)
    assert score[0] == result.summary.logic_depth


def test_preferred_objective_scores_preference_first():
    used = realize_preset(
        "A^B",
        RealizationPreset.XOR_PREFERRED,
        objective=OptimizationObjective.PREFERRED_GATES,
    )
    unused = realize_preset(
        "AB",
        RealizationPreset.XOR_PREFERRED,
        objective=OptimizationObjective.PREFERRED_GATES,
    )
    assert candidate_score(used.summary)[0] == 0
    assert candidate_score(unused.summary)[0] == 1


def test_summary_exposes_functional_completeness():
    result = realize_preset("AB", RealizationPreset.BASIC_ONLY)
    assert result.summary.functionally_complete is True
