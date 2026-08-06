from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_generated_trace_overlay_uses_imported_gate_label():
    assert "State.generated_simulation_active" in APP
    assert '& (g_label != "")' in APP
    assert "g_label," in APP
    assert 'g_data["value"].to_string()' in APP


def test_quick_spawn_selects_new_component():
    block = APP[APP.index("def add_gate_at_default_location"):APP.index("def drop_gate_at_location")]
    assert "self.selected_gate_key = key" in block
    assert block.index("self.selected_gate_key = key") < block.index("self.run_circuit_evaluation")


def test_drop_placement_selects_new_component():
    block = APP[APP.index("def drop_gate_at_location"):APP.index("def handle_canvas_click")]
    assert "self.selected_gate_key = key" in block
    assert block.index("self.selected_gate_key = key") < block.index("self.run_circuit_evaluation")


def test_paste_already_selects_new_component():
    block = APP[APP.index("def paste_copied_gate"):APP.index("def duplicate_selected_gate")]
    assert "self.selected_gate_key = key" in block
