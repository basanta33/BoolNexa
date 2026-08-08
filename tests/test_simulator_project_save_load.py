from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py")


def test_save_project_uses_reflex_download():
    text = APP.read_text(encoding="utf-8")
    assert "def save_project_download(self):" in text
    assert "return rx.download(" in text
    assert 'filename="boolnexa_project.json"' in text
    assert "on_click=State.save_project_download" in text
    assert '"format": "boolnexa-project"' in text


def test_load_project_remains_wired():
    text = APP.read_text(encoding="utf-8")
    assert 'id="project-file-input"' in text
    assert 'accept=".json"' in text
    assert "callback=State.import_project_data" in text
    assert "window.__importedProjectJson = JSON.parse(reader.result)" in text
    assert "trigger.click();" in text
