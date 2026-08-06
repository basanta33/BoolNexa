from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MEM=ROOT/"digital_logic_lab"/"academy_memory_foundations.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"

def test_lessons_9_10_present():
 text=MEM.read_text(encoding="utf-8")
 assert "def memory_hierarchy_performance_lesson" in text
 assert "def memory_system_integration_lesson" in text
 assert "Memory Hierarchy & Performance" in text
 assert "Memory System Integration & Design Challenge" in text

def test_performance_concepts():
 text=MEM.read_text(encoding="utf-8")
 for term in ("Latency and bandwidth","AMAT = hit time + miss rate × miss penalty","Temporal locality","Spatial locality"):
  assert term in text

def test_finale_integrates_path():
 text=MEM.read_text(encoding="utf-8")
 for term in ("TLB + page tables","cache hierarchy","parity / ECC","Path 06 · Complete"):
  assert term in text

def test_navigation_8_to_9_to_10():
 text=MEM.read_text(encoding="utf-8")
 assert 'href="/academy/unit-6/memory-hierarchy-performance"' in text
 assert 'href="/academy/unit-6/memory-system-integration"' in text

def test_routes_registered():
 text=APP.read_text(encoding="utf-8")
 assert 'route="/academy/unit-6/memory-hierarchy-performance"' in text
 assert 'route="/academy/unit-6/memory-system-integration"' in text
