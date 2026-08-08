from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_input_source_fanout_junction_dot_is_suppressed():
    assert '"src_type": src_type' in APP
    assert '(w["is_branched"] == "true") & (w["src_type"] != "INPUT")' in APP


def test_real_input_source_terminal_remains_clickable():
    # The INPUT component's real source terminal/hitbox is preserved.
    assert 'right=rx.cond(g_type == "INPUT", "1px", "-9px")' in APP
    assert 'on_click=State.select_pin_output(cell_key)' in APP
    assert '"output-pin-bubble wiring-source-active"' in APP


def test_gate_output_fanout_junctions_are_still_supported():
    # Only INPUT-source branch markers are hidden; gate-output fan-out dots remain.
    assert 'rx.el.svg.circle(' in APP
    assert 'w["src_type"] != "INPUT"' in APP


def test_release_features_are_preserved():
    assert APP.count('route="/academy/unit-') == 107
    for token in (
        "def save_project_download(self):",
        "def import_project_data(self, data: dict):",
        "State.zoom_percent",
        "Developed by B. Paudyal | v1.0.0",
    ):
        assert token in APP
