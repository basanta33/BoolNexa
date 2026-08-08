from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_visual_polish_has_professional_sidebar_sections():
    for token in (
        "Interactive Digital Logic Workbench",
        '"LOCAL JSON"',
        '"Canvas Tools"',
        '"Component Library"',
        'background="linear-gradient(135deg, #ffffff 0%, #f8fbff 100%)"',
        'box_shadow="0 4px 14px rgba(15,23,42,0.06)"',
    ):
        assert token in APP


def test_visual_polish_preserves_working_simulator_actions():
    for token in (
        "def save_project_download(self):",
        "def import_project_data(self, data: dict):",
        "window.__importedProjectJson = JSON.parse(reader.result)",
        "trigger.click();",
        "on_click=State.toggle_text_placement_mode",
        "on_click=State.toggle_delete_mode",
        "on_click=State.clear_canvas",
    ):
        assert token in APP


def test_visual_polish_preserves_component_library_and_academy():
    assert APP.count('route="/academy/unit-') == 107
    assert 'rx.foreach(State.active_gate_options, sidebar_symbol_tile)' in APP
    assert 'sidebar_component_card("HALF_ADDER", "Half Adder"' in APP
