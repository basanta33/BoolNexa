from pathlib import Path

from digital_logic_lab.boolean_engine import generate_truth_table
from digital_logic_lab.circuit_simulator_transfer import circuit_graph_to_simulator_project
from digital_logic_lab.logic_core import evaluate_circuit
from digital_logic_lab.realization_policy import OptimizationObjective, RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def _verify(expression, preset):
    graph = realize_preset(
        expression, preset, objective=OptimizationObjective.BALANCED
    ).graph
    project = circuit_graph_to_simulator_project(graph)
    truth = generate_truth_table(expression, include_intermediate=False, max_variables=6)
    inputs = {
        gate["label"]: key
        for key, gate in project["gates"].items()
        if gate["type"] == "INPUT"
    }
    results = []
    for row in truth.rows:
        gates = project["gates"]
        import copy
        gates = copy.deepcopy(gates)
        for variable in truth.variables:
            gates[inputs[variable]]["value"] = int(row[variable])
        evaluated = evaluate_circuit(gates)
        actual = [g["value"] for g in evaluated.values() if g["type"] == "OUTPUT"][0]
        results.append((actual, int(row["F"])))
    return results


def test_nand_xor_truth_table_verifies_transferred_network():
    results = _verify("A^B", RealizationPreset.NAND_ONLY)
    assert results
    assert all(actual == expected for actual, expected in results)


def test_nor_xor_truth_table_verifies_transferred_network():
    results = _verify("A^B", RealizationPreset.NOR_ONLY)
    assert results
    assert all(actual == expected for actual, expected in results)


def test_basic_three_input_expression_verifies_all_eight_rows():
    results = _verify("AB+AC'", RealizationPreset.BASIC_ONLY)
    assert len(results) == 8
    assert all(actual == expected for actual, expected in results)


def test_stage3_ui_exposes_verification_status_and_rows():
    assert "generated_verification_rows" in APP
    assert "generated_verification_status" in APP
    assert "generated_verification_summary" in APP
    assert "Truth-table verification" in APP
    assert "Re-verify" in APP


def test_generated_handoff_runs_verification_automatically():
    load_block = APP[
        APP.index("def load_generated_circuit_request"):
        APP.index("# Email registration required before project saving.")
    ]
    assert "self.verify_generated_circuit()" in load_block
