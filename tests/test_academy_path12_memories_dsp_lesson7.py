from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_hdl_path12.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"

def test_lesson7_present():
    t=MOD.read_text(encoding="utf-8")
    assert "def fpga_memories_dsp_pipelining_lesson" in t
    assert "PATH 12 · LESSON 07" in t

def test_lesson7_topics():
    t=MOD.read_text(encoding="utf-8")
    for term in (
        "Large storage should use dedicated memory resources",
        "Memory dimensions trade width for depth",
        "Single-port and dual-port memories support different access patterns",
        "Synchronous memory adds cycle latency",
        "DSP blocks accelerate arithmetic",
        "Coding style influences DSP inference",
        "Pipelining increases throughput",
        "Latency and throughput are different metrics",
        "Valid signals keep pipeline data aligned",
        "FIFOs decouple producers and consumers",
        "Trace a pipelined multiply-accumulate datapath",
    ):
        assert term in t

def test_lesson7_checks():
    t=MOD.read_text(encoding="utf-8")
    for m in ("def check_bram","def check_dsp","def check_pipeline"):
        assert m in t

def test_lesson7_route():
    route="/academy/unit-12/fpga-memories-dsp-pipelining"
    assert f'route="{route}"' in APP.read_text(encoding="utf-8")
    assert route in CAT.read_text(encoding="utf-8")
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-12/")>=7

def test_lesson8_link():
    t=MOD.read_text(encoding="utf-8")
    assert "Next · Complete FPGA System Design & Deployment" in t
    assert "/academy/unit-12/complete-fpga-system-design-deployment" in t

def test_simulator_fix_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
