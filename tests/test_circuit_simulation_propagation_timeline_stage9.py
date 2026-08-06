from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")


def test_stage9_has_timeline_state():
    assert "generated_propagation_timeline: list[dict[str, str]] = []" in APP
    assert 'generated_active_level_detail: str = ""' in APP


def test_stage9_builds_timeline_from_gate_levels():
    block = APP[
        APP.index("def _refresh_generated_propagation_timeline"):
        APP.index("def set_generated_propagation_speed")
    ]
    assert "for level in range(self.generated_propagation_max_level + 1)" in block
    assert "self.generated_propagation_levels.get(key, -1) != level" in block
    assert 'members.append(f"{name}={value}")' in block


def test_stage9_marks_done_active_waiting_levels():
    block = APP[
        APP.index("def _refresh_generated_propagation_timeline"):
        APP.index("def set_generated_propagation_speed")
    ]
    assert '"ACTIVE"' in block
    assert '"DONE"' in block
    assert '"WAITING"' in block


def test_stage9_refreshes_timeline_when_propagation_moves():
    start = APP[
        APP.index("def start_generated_propagation"):
        APP.index("def next_generated_propagation_level")
    ]
    nxt = APP[
        APP.index("def next_generated_propagation_level"):
        APP.index("def reset_generated_propagation")
    ]
    assert "self._refresh_generated_propagation_timeline()" in start
    assert "self._refresh_generated_propagation_timeline()" in nxt


def test_stage9_ui_shows_level_timeline():
    assert "State.generated_propagation_timeline" in APP
    assert 'item["signals"]' in APP
    assert 'item["status"]' in APP
    assert '"L" + item["level"]' in APP


def test_reset_clears_stage9_timeline():
    reset = APP[
        APP.index("def reset_generated_propagation"):
        APP.index("def start_generated_walkthrough")
    ]
    assert "self.generated_propagation_timeline = []" in reset
    assert 'self.generated_active_level_detail = ""' in reset
