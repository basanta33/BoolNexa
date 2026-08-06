from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage5_has_walkthrough_state():
    assert "generated_walkthrough_index: int = 0" in APP
    assert "generated_walkthrough_active: bool = False" in APP


def test_stage5_has_start_next_previous_stop_events():
    for method in (
        "def start_generated_walkthrough",
        "def next_generated_walkthrough",
        "def previous_generated_walkthrough",
        "def stop_generated_walkthrough",
    ):
        assert method in APP


def test_walkthrough_drives_existing_truth_row_apply_event():
    for method in (
        "start_generated_walkthrough",
        "next_generated_walkthrough",
        "previous_generated_walkthrough",
    ):
        start = APP.index(f"def {method}")
        tail = APP[start:start + 1300]
        assert "self.apply_generated_truth_row(" in tail


def test_walkthrough_is_bounded_at_truth_table_ends():
    assert "min(" in APP
    assert "len(self.generated_verification_rows) - 1" in APP
    assert "max(self.generated_walkthrough_index - 1, 0)" in APP


def test_stage5_ui_has_guided_controls():
    assert '"GUIDED WALKTHROUGH"' in APP
    assert '"Start"' in APP
    assert '"◀ Previous"' in APP
    assert '"Next ▶"' in APP
    assert '"Stop"' in APP


def test_fresh_generated_circuit_resets_walkthrough():
    load = APP[
        APP.index("def load_generated_circuit_request"):
        APP.index("# Email registration required before project saving.")
    ]
    assert "self.generated_walkthrough_index = 0" in load
    assert "self.generated_walkthrough_active = False" in load
