from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_system_path10.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson8_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def storage_systems_block_io_lesson" in text
    assert "PATH 10 · LESSON 08" in text

def test_lesson8_topics():
    text=MOD.read_text(encoding="utf-8")
    for term in ("Block I/O moves addressed chunks","Logical block addressing hides physical details","DMA is a natural partner for block storage","Queues allow multiple storage requests","Caching improves apparent storage performance","Flush and ordering protect persistence semantics","Trace a complete block read","Path 10 integration checkpoint"):
        assert term in text

def test_lesson8_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_block","def check_sector","def check_queue"):
        assert method in text

def test_lesson8_route_catalog_and_completion():
    assert 'route="/academy/unit-10/storage-systems-block-io"' in APP.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-10/")==8
    text=MOD.read_text(encoding="utf-8")
    assert "PATH 10 COMPLETE" in text
    assert "Lesson 9" not in text

def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
