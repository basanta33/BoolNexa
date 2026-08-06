from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_gate_card_uses_existing_selection_event():
    assert "def handle_gate_click(self, key: str)" in APP
    assert "State.handle_gate_click(cell_key)" in APP
    assert "State.select_gate(cell_key)" not in APP


def test_generated_gate_click_still_opens_signal_inspector():
    assert "State.inspect_generated_gate(cell_key)" in APP
    assert "State.generated_simulation_active" in APP
