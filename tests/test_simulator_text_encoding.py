from pathlib import Path

SOURCE = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_simulator_footer_and_cascade_text_are_clean():
    assert 'Developed by B. Paudyal | v1.0.0' in SOURCE
    assert 'COUT -> CIN and BOUT -> BIN' in SOURCE
