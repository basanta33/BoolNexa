from pathlib import Path


APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_clock_period_input_uses_reactive_numeric_string():
    block = APP[APP.index("def vec_clock("):APP.index("def vec_seven_seg(")]
    assert "interval_str = str(clock_interval)" not in block
    assert "if isinstance(clock_interval, rx.Var)" in block
    assert "clock_interval.to_string()" in block
    assert "else str(clock_interval)" in block
    assert "value=interval_value" in block
    assert "on_change=lambda val, k=cell_key: State.set_clock_interval(" in block
