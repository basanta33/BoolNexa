from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage6_has_live_step_explanation_state():
    assert 'generated_step_explanation: str = ""' in APP


def test_truth_row_application_builds_explanation():
    block = APP[
        APP.index("def apply_generated_truth_row"):
        APP.index("def verify_generated_circuit")
    ]
    assert "input_summary" in block
    assert "output_value" in block
    assert "self.generated_step_explanation =" in block
    assert "Follow the highlighted HIGH/LOW" in block


def test_explanation_mentions_realization_mode_and_output():
    block = APP[
        APP.index("def apply_generated_truth_row"):
        APP.index("def verify_generated_circuit")
    ]
    assert "self.generated_simulation_mode" in block
    assert "F={output_value}" in block


def test_stage6_ui_has_why_explanation_card():
    assert '"WHY?"' in APP
    assert "State.generated_step_explanation" in APP
    assert 'background="#eff6ff"' in APP


def test_fresh_generated_handoff_clears_old_explanation():
    load = APP[
        APP.index("def load_generated_circuit_request"):
        APP.index("# Email registration required before project saving.")
    ]
    assert 'self.generated_step_explanation = ""' in load
