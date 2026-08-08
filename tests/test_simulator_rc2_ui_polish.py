from pathlib import Path
APP=Path("digital_logic_lab/digital_logic_lab.py")
def test_component_library_is_single_open_accordion():
    t=APP.read_text(encoding="utf-8")
    assert 'component_library_section: str = "logic"' in t
    assert 'def toggle_component_library_section(self, section: str):' in t
def test_sidebar_uses_release_geometry_without_horizontal_scroll():
    t=APP.read_text(encoding="utf-8")
    assert 'width="300px"' in t
    assert '"overflow-x": "hidden"' in t
