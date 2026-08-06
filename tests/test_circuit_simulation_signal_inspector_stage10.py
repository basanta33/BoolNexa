from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage10_has_signal_inspector_state():
    assert 'generated_inspector_gate_key: str = ""' in APP
    assert 'generated_inspector_title: str = ""' in APP
    assert 'generated_inspector_detail: str = ""' in APP


def test_stage10_inspector_reports_gate_type_level_inputs_and_output():
    block = APP[APP.index("def inspect_generated_gate"):APP.index("def clear_generated_gate_inspector")]
    assert 'gate_type = str(gate.get("type", ""))' in block
    assert "self.generated_propagation_levels.get(key, -1)" in block
    assert 'inputs.append(f"{source_name}={source_value}")' in block
    assert 'f"Its current output is {value}."' in block


def test_stage10_generated_gate_click_opens_inspector():
    assert "State.inspect_generated_gate(cell_key)" in APP
    assert "State.generated_simulation_active" in APP


def test_stage10_ui_has_signal_inspector_card():
    assert '"SIGNAL INSPECTOR"' in APP
    assert "State.generated_inspector_title" in APP
    assert "State.generated_inspector_detail" in APP
    assert 'background="#f0f9ff"' in APP


def test_stage10_inspector_can_be_closed_and_resets_on_new_handoff():
    assert "def clear_generated_gate_inspector" in APP
    load = APP[APP.index("def load_generated_circuit_request"):APP.index("# Email registration required before project saving.")]
    assert "self.clear_generated_gate_inspector()" in load
