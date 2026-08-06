from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_lesson5_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def dma_high_throughput_data_movement_lesson" in text
    assert "PATH 10 · LESSON 05" in text
    assert "DMA & High-Throughput Data Movement" in text


def test_lesson5_core_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Why DMA is useful",
        "A DMA engine needs transfer descriptors",
        "DMA becomes a bus master",
        "Peripheral-to-memory DMA",
        "Memory-to-peripheral DMA",
        "Burst transfers improve bus efficiency",
        "DMA completion is often reported by interrupt",
        "Buffers decouple producer and consumer timing",
        "Caches create a visibility problem",
        "High throughput still requires balanced resources",
        "Trace a complete DMA receive operation",
    ):
        assert term in text


def test_lesson5_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_dma", "def check_burst", "def check_coherence"):
        assert method in text


def test_lesson5_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    assert 'route="/academy/unit-10/dma-high-throughput-data-movement"' in app
    assert '("DMA & High-Throughput Data Movement", "/academy/unit-10/dma-high-throughput-data-movement")' in cat
    assert cat.count("/academy/unit-10/") == 8


def test_lesson5_links_to_lesson6():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Timers, Counters & System Timing" in text
    assert 'href="/academy/unit-10/timers-counters-system-timing"' in text


def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
