from pathlib import Path

from digital_logic_lab.circuit_simulator_transfer import circuit_graph_to_simulator_project
from digital_logic_lab.logic_core import evaluate_circuit
from digital_logic_lab.realization_policy import OptimizationObjective, RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def _project(expression, preset):
    graph = realize_preset(
        expression, preset, objective=OptimizationObjective.BALANCED
    ).graph
    return circuit_graph_to_simulator_project(graph)


def test_generated_internal_net_values_change_with_live_evaluation():
    project = _project("A^B", RealizationPreset.NAND_ONLY)
    gates = project["gates"]

    inputs = {g["label"]: key for key, g in gates.items() if g["type"] == "INPUT"}
    gates[inputs["A"]]["value"] = 0
    gates[inputs["B"]]["value"] = 0
    low = evaluate_circuit(gates)

    gates[inputs["A"]]["value"] = 1
    gates[inputs["B"]]["value"] = 0
    high = evaluate_circuit(gates)

    internal_keys = [
        key for key, gate in gates.items()
        if gate["type"] not in {"INPUT", "OUTPUT"}
    ]
    assert internal_keys
    assert any(low[key]["value"] != high[key]["value"] for key in internal_keys)


def test_every_generated_internal_gate_has_trace_identity():
    project = _project("A^B", RealizationPreset.NOR_ONLY)
    internal = [
        gate for gate in project["gates"].values()
        if gate["type"] not in {"INPUT", "OUTPUT"}
    ]
    assert all(gate["generated_net"].startswith("N") for gate in internal)
    assert all(gate["generated_expression"] for gate in internal)


def test_simulator_renders_live_internal_net_badges():
    assert 'generated_net = g_data.get("generated_net", "")' in APP
    assert 'generated_expression = g_data.get("generated_expression", "")' in APP
    assert '& (g_label != "")' in APP
    assert 'g_label,' in APP
    assert 'g_data["value"].to_string()' in APP


def test_simulator_renders_prominent_live_output_badge():
    assert "State.generated_simulation_active & is_output" in APP
    assert "g_label," in APP
    assert 'border="1px solid #93c5fd"' in APP


def test_full_boolean_expression_is_available_as_trace_tooltip():
    assert "title=generated_expression" in APP
