from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage8_tracks_completion_and_progress():
    assert "generated_propagation_complete: bool = False" in APP
    assert 'generated_propagation_progress: str = ""' in APP
    assert 'f"Level 0 of {self.generated_propagation_max_level}"' in APP


def test_stage8_marks_complete_at_final_level():
    block = APP[
        APP.index("def next_generated_propagation_level"):
        APP.index("def reset_generated_propagation")
    ]
    assert "self.generated_propagation_complete = True" in block
    assert "Propagation complete · the logic wave has reached the final output F." in block


def test_stage8_reset_clears_completion_state():
    block = APP[
        APP.index("def reset_generated_propagation"):
        APP.index("def start_generated_walkthrough")
    ]
    assert "self.generated_propagation_complete = False" in block
    assert 'self.generated_propagation_progress = ""' in block


def test_stage8_autoplay_timer_stops_on_backend_completion():
    assert 'id="propagation-completion-watch"' in APP
    assert "MutationObserver" in APP
    assert "data-propagation-complete" in APP
    assert "clearInterval(window.__boolnexaPropagationTimer)" in APP


def test_stage8_ui_shows_progress_and_complete_badge():
    assert "State.generated_propagation_progress" in APP
    assert '"COMPLETE"' in APP
    assert "State.generated_propagation_complete" in APP
