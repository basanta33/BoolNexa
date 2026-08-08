from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")

def _load_input_block():
    start = APP.index('id="project-file-input"')
    return APP[start:start + 2600]

def test_project_file_reader_executes_directly_on_change():
    block = _load_input_block()
    assert 'const input = document.getElementById("project-file-input");' in block
    assert 'const file = input && input.files ? input.files[0] : null;' in block
    assert "new FileReader()" in block
    assert "reader.readAsText(file);" in block
    assert "(event) => {" not in block

def test_loaded_json_reaches_existing_reflex_import_trigger():
    block = _load_input_block()
    assert "window.__importedProjectJson = JSON.parse(reader.result);" in block
    assert 'document.getElementById("import-json-trigger-btn")' in block
    assert "trigger.click();" in block
    assert "JSON.stringify(window.__importedProjectJson || null)" in APP
    assert "callback=State.import_project_data" in APP

def test_current_rc2_surface_is_preserved():
    assert APP.count('route="/academy/unit-') == 107
    assert '"Canvas Tools"' in APP
    assert '"Component Library"' in APP
    assert "def save_project_download(self):" in APP
