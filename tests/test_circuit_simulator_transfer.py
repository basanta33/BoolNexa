from digital_logic_lab.circuit_simulator_transfer import circuit_graph_to_simulator_project
from digital_logic_lab.realization_policy import OptimizationObjective, RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _graph(expression: str, preset: RealizationPreset):
    return realize_preset(
        expression, preset, objective=OptimizationObjective.BALANCED
    ).graph


def test_nand_inverter_keeps_both_physical_inputs_connected() -> None:
    project = circuit_graph_to_simulator_project(_graph("AB+AC'", RealizationPreset.NAND_ONLY))
    nand_inverters = [
        gate for gate in project["gates"].values()
        if gate["type"] == "NAND"
        and gate.get("input1_src")
        and gate.get("input1_src") == gate.get("input2_src")
    ]
    assert nand_inverters


def test_transfer_preserves_all_graph_wires_by_target_pin() -> None:
    graph = _graph("AB+AC'", RealizationPreset.NAND_ONLY)
    project = circuit_graph_to_simulator_project(graph)
    for wire in graph.wires:
        target = project["gates"][wire.target]
        assert target[f"input{wire.target_input + 1}_src"] == wire.source


def test_transfer_preserves_input_and_output_labels() -> None:
    project = circuit_graph_to_simulator_project(_graph("A+B", RealizationPreset.BASIC_ONLY))
    inputs = [g["label"] for g in project["gates"].values() if g["type"] == "INPUT"]
    outputs = [g["label"] for g in project["gates"].values() if g["type"] == "OUTPUT"]
    assert inputs == ["A", "B"]
    assert outputs == ["F"]


def test_transfer_positions_are_deterministic() -> None:
    graph = _graph("AB+AC'", RealizationPreset.NAND_ONLY)
    first = circuit_graph_to_simulator_project(graph)
    second = circuit_graph_to_simulator_project(graph)
    assert first == second
