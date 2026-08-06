from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage7b_tracks_gate_levels_for_rendering():
    assert "generated_propagation_levels: dict[str, int] = {}" in APP
    assert "self.generated_propagation_levels = levels" in APP
    assert "State.generated_propagation_levels.get(cell_key, -1)" in APP


def test_stage7b_highlights_active_gate_layer():
    assert "propagation_is_active" in APP
    assert "drop-shadow(0 0 9px rgba(124,58,237,0.95))" in APP
    assert '"ACTIVE LEVEL "' in APP


def test_stage7b_highlights_active_wire_layer():
    assert "propagation_wire_active" in APP
    assert 'stroke=rx.cond(' in APP
    assert '"#7c3aed"' in APP
    assert 'stroke_width=rx.cond(' in APP


def test_stage7b_has_adjustable_propagation_speed():
    assert "generated_propagation_speed_ms: int = 700" in APP
    assert "def set_generated_propagation_speed" in APP
    assert '["250", "500", "700", "1000", "1500"]' in APP


def test_stage7b_has_autoplay_and_pause_controls():
    assert '"Auto Play"' in APP
    assert '"Pause"' in APP
    assert "window.__boolnexaPropagationTimer" in APP
    assert "setInterval(clickNext, speed)" in APP
    assert "clearInterval(window.__boolnexaPropagationTimer)" in APP


def test_stage7b_has_hidden_next_level_trigger():
    assert 'id="propagation-next-trigger-btn"' in APP
    assert "on_click=State.next_generated_propagation_level" in APP
