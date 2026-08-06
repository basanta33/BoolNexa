from pathlib import Path


def test_simulate_circuit_opens_new_browser_tab() -> None:
    source = Path(__file__).parents[1] / "digital_logic_lab" / "logic_circuit_lab.py"
    text = source.read_text(encoding="utf-8")

    assert "window.open" in text
    assert "'_blank'" in text
    assert "noopener,noreferrer" in text
    assert "rx.redirect(" not in text[text.index("def simulate_circuit"):text.index("def generate", text.index("def simulate_circuit"))]
