from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_sidebar_order_is_library_project_canvas_tools():
    library = APP.index('rx.text("Component Library"')
    project = APP.index('rx.text("Project"', library)
    canvas = APP.index('rx.text("Canvas Tools"', project)
    assert library < project < canvas


def test_footer_last_three_lines_are_more_readable():
    assert 'rx.text("BoolNexa", font_size="11px"' in APP
    assert '"Developed by B. Paudyal | v1.0.0",\n                          font_size="10px",' in APP
    assert 'rx.text("boolnexa.sim@gmail.com", font_size="10px"' in APP


def test_sidebar_functionality_is_preserved():
    for token in (
        'max_height="460px"',
        "on_click=State.save_project_download",
        "on_click=State.toggle_text_placement_mode",
        "on_click=State.toggle_delete_mode",
        "on_click=State.clear_canvas",
        '(w["is_branched"] == "true") & (w["src_type"] != "INPUT")',
    ):
        assert token in APP


def test_academy_routes_are_preserved():
    assert APP.count('route="/academy/unit-') == 107
