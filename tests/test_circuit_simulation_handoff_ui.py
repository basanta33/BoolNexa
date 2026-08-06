from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LAB=(ROOT/"digital_logic_lab"/"logic_circuit_lab.py").read_text(encoding="utf-8")


def test_generator_handoff_contains_expression_and_mode():
    assert "generated_expression=" in LAB
    assert "generated_mode=" in LAB
    assert "Simulate circuit" in LAB


def test_live_simulator_generated_banner_and_toggle_path():
    assert "generated_simulation_active" in APP
    assert "Interactive simulation · click input blocks to toggle 0 ↔ 1" in APP
    assert "GENERATED CIRCUIT" in APP
    assert "callback=State.toggle_input_by_key" in APP


def test_generated_graph_is_imported_into_live_simulator():
    assert "circuit_graph_to_simulator_project(result.graph)" in APP
    assert "self.import_project_data(project)" in APP
