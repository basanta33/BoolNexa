from pathlib import Path

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "digital_logic_lab.py"
).read_text(encoding="utf-8")


def test_simulator_has_no_known_mojibake_markers():
    for marker in ("Γ", "Ç", "ê", "å"):
        assert marker not in SOURCE


def test_simulator_controls_use_safe_symbols():
    assert 'rx.button("-"' in SOURCE
    assert '2->4 Decoder' in SOURCE
    assert '4->2 Encoder' in SOURCE


def test_simulator_footer_and_cascade_text_are_clean():
    assert 'Developed by Basanta Paudyal | v1.0.0' in SOURCE
    assert 'COUT -> CIN and BOUT -> BIN' in SOURCE
