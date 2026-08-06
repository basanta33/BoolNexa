from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage7_has_propagation_state():
    assert "generated_propagation_active: bool = False" in APP
    assert "generated_propagation_level: int = 0" in APP
    assert "generated_propagation_max_level: int = 0" in APP


def test_stage7_computes_gate_levels_from_connections():
    block = APP[APP.index("def _generated_gate_levels"):APP.index("def start_generated_propagation")]
    assert 'gate.get("type") in {"INPUT", "CONSTANT", "CLOCK"}' in block
    assert 'str(value).split(":", 1)[0]' in block
    assert "max(levels[source] for source in sources) + 1" in block


def test_stage7_has_start_next_reset_controls():
    for method in (
        "def start_generated_propagation",
        "def next_generated_propagation_level",
        "def reset_generated_propagation",
    ):
        assert method in APP
    assert '"Start propagation"' in APP
    assert '"Next level ▶"' in APP
    assert '"Reset"' in APP


def test_stage7_reports_completion():
    assert "Propagation complete · the logic wave has reached the final output F." in APP


def test_evaluation_helper_returns_live_evaluated_gate_map():
    block = APP[APP.index("def run_circuit_evaluation"):APP.index("def recalculate_all_wires")]
    assert "return self.gates" in block


def test_new_generated_handoff_resets_propagation():
    load = APP[APP.index("def load_generated_circuit_request"):APP.index("# Email registration required before project saving.")]
    assert "self.reset_generated_propagation()" in load
