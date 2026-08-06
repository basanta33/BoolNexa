from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"

def test_lesson4_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def system_buses_arbitration_protocols_lesson" in text
    assert "PATH 10 · LESSON 04" in text
    assert "System Buses, Arbitration & Protocols" in text

def test_lesson4_core_topics():
    text = MOD.read_text(encoding="utf-8")
    for term in ("A bus is a shared communication path", "Bus masters initiate; targets respond",
                 "Shared buses require ownership", "Arbitration policies balance latency and fairness",
                 "A protocol defines a legal transaction", "Synchronous buses use a shared timing reference",
                 "Asynchronous buses coordinate with handshakes", "Latency and bandwidth"):
        assert term in text

def test_lesson4_route_and_catalog():
    app = APP.read_text(encoding="utf-8")
    cat = CAT.read_text(encoding="utf-8")
    assert 'route="/academy/unit-10/system-buses-arbitration-protocols"' in app
    assert '("System Buses, Arbitration & Protocols", "/academy/unit-10/system-buses-arbitration-protocols")' in cat
    assert cat.count("/academy/unit-10/") == 8

def test_lesson4_links_to_lesson5():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · DMA & High-Throughput Data Movement" in text
    assert 'href="/academy/unit-10/dma-high-throughput-data-movement"' in text

def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
