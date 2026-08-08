from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_zoom_indicator_is_reactive_not_static():
    assert 'zoom_percent: str = "100%"' in APP
    assert 'self.zoom_percent = f"{round(next_zoom * 100)}%"' in APP
    assert "State.zoom_percent" in APP


def test_all_view_controls_update_through_the_same_state_handler():
    assert "window.__logicZoom(-0.1)" in APP
    assert "window.__logicZoom(0.1)" in APP
    assert "window.__logicResetZoom" in APP
    assert "window.__logicFit" in APP
    assert "callback=State.handle_view_change" in APP


def test_zoom_toolbar_has_stable_percentage_width():
    assert 'min_width="52px"' in APP
    assert 'title="Reset to 100%"' in APP


def test_final_zoom_polish_preserves_green_rc2_features():
    assert APP.count('route="/academy/unit-') == 107
    for token in (
        "def save_project_download(self):",
        "def import_project_data(self, data: dict):",
        '"Canvas Tools"',
        '"Component Library"',
        "Developed by B. Paudyal | v1.0.0",
    ):
        assert token in APP
