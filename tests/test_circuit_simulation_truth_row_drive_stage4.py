from pathlib import Path
import copy

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


def _drive(project, **values):
    gates = copy.deepcopy(project["gates"])
    for gate in gates.values():
        if gate["type"] == "INPUT":
            gate["value"] = int(values[gate["label"]])
    return evaluate_circuit(gates)


def _output(gates):
    return [g["value"] for g in gates.values() if g["type"] == "OUTPUT"][0]


def test_truth_row_drive_semantics_match_xor():
    project = _project("A^B", RealizationPreset.NOR_ONLY)
    assert _output(_drive(project, A=0, B=0)) == 0
    assert _output(_drive(project, A=0, B=1)) == 1
    assert _output(_drive(project, A=1, B=0)) == 1
    assert _output(_drive(project, A=1, B=1)) == 0


def test_stage4_has_apply_truth_row_event():
    assert "def apply_generated_truth_row" in APP
    assert "assignments: dict[str, int]" in APP
    assert "self.run_circuit_evaluation(updated, record_history=False)" in APP


def test_stage4_truth_rows_expose_apply_action():
    assert '"Apply"' in APP
    assert "State.apply_generated_truth_row(" in APP
    assert 'row["inputs"]' in APP


def test_stage4_marks_current_demonstration_row():
    assert "generated_active_truth_inputs" in APP
    assert '"CURRENT"' in APP
    assert "State.generated_active_truth_inputs == row[\"inputs\"]" in APP


def test_new_generated_transfer_resets_current_truth_row():
    load_block = APP[
        APP.index("def load_generated_circuit_request"):
        APP.index("# Email registration required before project saving.")
    ]
    assert 'self.generated_active_truth_inputs = ""' in load_block
