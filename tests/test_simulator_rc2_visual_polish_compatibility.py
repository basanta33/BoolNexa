from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_visual_polish_keeps_release_contracts():
    assert 'max_height="460px"' in APP
    assert 'Developed by B. Paudyal | v1.0.0' in APP


def test_visual_polish_keeps_working_rc2_surface():
    assert APP.count('route="/academy/unit-') == 107
    assert "def save_project_download(self):" in APP
    assert "def import_project_data(self, data: dict):" in APP
    assert '"Canvas Tools"' in APP
    assert '"Component Library"' in APP
