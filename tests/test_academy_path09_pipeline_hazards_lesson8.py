from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_cpu_path09.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"

def test_path09_lesson8_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def pipeline_hazards_lesson" in text
    assert "PATH 09 · LESSON 08" in text
    assert "Pipeline Hazards" in text

def test_lesson8_teaches_hazards_and_resolution():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Structural hazards are resource conflicts",
        "RAW is the key data hazard",
        "Forwarding bypasses unnecessary waiting",
        "A load-use dependency may still require a stall",
        "Hazard detection decides when the pipeline must wait",
        "Control hazards come from branches and jumps",
        "Flush and prediction protect control-flow correctness",
        "Forwarding, stalling and flushing solve different problems",
        "Trace a dependent sequence",
        "PATH 09 COMPLETE",
    ):
        assert term in text

def test_lesson8_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_hazard", "def check_forwarding", "def check_controlhazard"):
        assert method in text

def test_lesson8_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "pipeline_hazards_lesson" in text
    assert 'route="/academy/unit-9/pipeline-hazards"' in text

def test_path09_catalog_has_eight_live_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Pipeline Hazards", "/academy/unit-9/pipeline-hazards")' in text

def test_path09_curriculum_finishes_at_lesson8():
    text = MOD.read_text(encoding="utf-8")
    assert "PATH 09 COMPLETE" in text
    assert "Lesson 9" not in text

def test_simulator_gate_click_compile_fix_preserved():
    text = APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
