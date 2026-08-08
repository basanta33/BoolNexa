from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")

def test_simulator_uses_short_developer_credit():
    assert "Developed by B. Paudyal | v1.0.0" in APP
    assert "Developed by Basanta Paudyal | v1.0.0" not in APP
