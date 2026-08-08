from pathlib import Path
import re


APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_clock_output_terminal_is_on_visible_right_edge_at_vertical_center():
    assert re.search(r'g_type == "CLK",\s*"45px"', APP)
    assert re.search(r'g_type == "CLK",\s*"45"', APP)
    assert 'right=rx.cond(g_type == "INPUT", "1px", "-9px")' in APP
