from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")

def test_generated_handoff_legacy_boundary_is_preserved():
    start = APP.index("def load_generated_circuit_request")
    boundary = APP.index("# Email registration required before project saving.")
    save = APP.index("def save_project_download")
    assert start < boundary < save

def test_project_save_still_uses_reflex_download():
    assert "on_click=State.save_project_download" in APP
    assert "return rx.download(" in APP
    assert 'filename="boolnexa_project.json"' in APP
