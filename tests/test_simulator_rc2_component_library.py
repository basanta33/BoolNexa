from pathlib import Path
APP=Path("digital_logic_lab/digital_logic_lab.py")
def test_component_library_and_advanced_paths():
    t=APP.read_text(encoding="utf-8")
    for x in ("Component Library","I/O & Sources","Logic Gates","Flip-Flops","MSI / LSI Blocks"):
        assert x in t
    for x in ("academy_system_path10","academy_embedded_path11","academy_hdl_path12"):
        assert x in t
    assert "COUT -> CIN and BOUT -> BIN" in t
