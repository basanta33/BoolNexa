from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_cpu_path09.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_path09_lesson7_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def pipeline_fundamentals_lesson" in text
    assert "PATH 09 · LESSON 07" in text
    assert "Pipeline Fundamentals" in text


def test_lesson7_teaches_pipeline_foundations():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Why processors use pipelining",
        "The classic five-stage instruction pipeline",
        "Pipeline registers separate the stages",
        "Several instructions occupy the processor together",
        "Latency and throughput are different",
        "The pipeline must first fill and finally drain",
        "Stage balance determines the clock period",
        "Ideal speedup has limits",
        "Why perfect overlap is not always possible",
        "Trace a three-instruction pipeline",
    ):
        assert term in text


def test_lesson7_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_pipeline", "def check_stage", "def check_throughput"):
        assert method in text


def test_lesson7_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "pipeline_fundamentals_lesson" in text
    assert 'route="/academy/unit-9/pipeline-fundamentals"' in text


def test_path09_catalog_has_eight_live_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-9/") == 8
    assert '("Pipeline Fundamentals", "/academy/unit-9/pipeline-fundamentals")' in text


def test_lesson7_links_to_lesson8():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Pipeline Hazards" in text
    assert 'href="/academy/unit-9/pipeline-hazards"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text = APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
