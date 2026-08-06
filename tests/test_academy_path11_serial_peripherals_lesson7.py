from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_embedded_path11.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson7_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def uart_spi_i2c_peripheral_communication_lesson" in t
    assert "PATH 11 · LESSON 07" in t

def test_lesson7_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in ("Serial links move information over a small number of wires","UART is asynchronous serial communication","UART is naturally point-to-point at the logic level","SPI is synchronous and typically full-duplex","SPI mode defines clock polarity and phase","I²C shares two open-drain-style signal lines","I²C transfers include addressing and acknowledgement","Pull-ups and bus capacitance shape I²C timing","Choose an interface from system requirements","Interrupts and DMA reduce communication overhead","Trace an I²C sensor register read"):
        assert term in t

def test_lesson7_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_uart","def check_spi","def check_i2c"):
        assert m in t

def test_lesson7_route():
    route="/academy/unit-11/uart-spi-i2c-peripheral-communication"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-11/")>=7

def test_lesson8_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Embedded System Integration, Reliability & Debugging" in t
    assert "/academy/unit-11/embedded-system-integration-reliability-debugging" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
