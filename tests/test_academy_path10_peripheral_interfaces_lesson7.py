from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_system_path10.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"
def test_lesson7_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def peripheral_interfaces_serial_communication_lesson" in text
    assert "PATH 10 · LESSON 07" in text
def test_lesson7_topics():
    text=MOD.read_text(encoding="utf-8")
    for term in ("Parallel and serial interfaces trade pins for timing","UART provides asynchronous point-to-point serial I/O","SPI is synchronous and clocked by a controller","I²C shares clock and data among addressed devices","Trace a UART receive operation"): assert term in text
def test_lesson7_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_serial","def check_uart","def check_spi"): assert method in text
def test_route_catalog_and_preview():
    assert 'route="/academy/unit-10/peripheral-interfaces-serial-communication"' in APP.read_text(encoding="utf-8")
    cat=CAT.read_text(encoding="utf-8")
    assert cat.count("/academy/unit-10/")==8
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Storage Systems & Block I/O" in text and 'href="/academy/unit-10/storage-systems-block-io"' in text
def test_simulator_compile_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
