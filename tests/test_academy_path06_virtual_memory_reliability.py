from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEM = ROOT / "digital_logic_lab" / "academy_memory_foundations.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"

def test_path06_lessons_7_8_are_present():
    text = MEM.read_text(encoding="utf-8")
    assert "def virtual_memory_lesson" in text
    assert "def memory_reliability_lesson" in text
    assert "Virtual Memory & Address Translation" in text
    assert "Memory Reliability, Parity & ECC" in text

def test_virtual_memory_core_concepts():
    text = MEM.read_text(encoding="utf-8")
    for term in ("virtual page number", "physical frame number", "Translation Lookaside Buffer", "page-fault exception"):
        assert term in text

def test_reliability_core_concepts():
    text = MEM.read_text(encoding="utf-8")
    for term in ("Simple parity", "syndrome", "SECDED", "double-error detection"):
        assert term in text

def test_lesson_navigation_continues_from_six():
    text = MEM.read_text(encoding="utf-8")
    assert 'href="/academy/unit-6/virtual-memory"' in text
    assert 'href="/academy/unit-6/memory-reliability"' in text

def test_routes_registered():
    text = APP.read_text(encoding="utf-8")
    assert 'route="/academy/unit-6/virtual-memory"' in text
    assert 'route="/academy/unit-6/memory-reliability"' in text
    assert "virtual_memory_lesson" in text
    assert "memory_reliability_lesson" in text
