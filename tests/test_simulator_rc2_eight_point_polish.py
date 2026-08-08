from pathlib import Path
APP=Path("digital_logic_lab/digital_logic_lab.py")

def test_all_component_categories_use_visual_cards():
    t=APP.read_text(encoding="utf-8")
    for token in (
        'sidebar_component_card("INPUT", "INPUT")',
        'sidebar_component_card("D_FF", "D FF"',
        'sidebar_component_card("HALF_ADDER", "Half Adder"',
        'rx.foreach(State.active_gate_options, sidebar_symbol_tile)',
    ):
        assert token in t
    assert '-- Select Flip-Flop --' not in t
    assert '-- Select MSI / LSI Block --' not in t

def test_accordion_indicators_are_dynamic_and_library_is_bounded():
    t=APP.read_text(encoding="utf-8")
    assert 'rx.cond(State.component_library_section == "logic", "−", "+")' in t
    assert 'max_height="460px"' in t
    assert '"overflow-y": "auto"' in t

def test_project_controls_have_new_save_load_and_feedback():
    t=APP.read_text(encoding="utf-8")
    assert 'project_status: str = "Ready"' in t
    assert 'id="new-project-trigger-btn"' in t
    assert '"New", size="1"' in t
    assert 'on_click=State.save_project_download' in t
    assert "document.getElementById('project-file-input').click();" in t
    assert 'Project loaded successfully' in t

def test_release_surface_preserved():
    t=APP.read_text(encoding="utf-8")
    assert t.count('route="/academy/unit-') == 107
    assert 'State.handle_gate_click(cell_key)' in t
