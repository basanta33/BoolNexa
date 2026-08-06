from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"digital_logic_lab"/"academy_cpu_path09.py"
APP=ROOT/"digital_logic_lab"/"digital_logic_lab.py"
CAT=ROOT/"digital_logic_lab"/"academy_route_catalog.py"


def test_path09_lesson2_present():
    text=MOD.read_text(encoding="utf-8")
    assert "def fetch_decode_execute_lesson" in text
    assert "PATH 09 · LESSON 02" in text
    assert "Fetch, Decode & Execute" in text


def test_lesson2_teaches_complete_instruction_cycle():
    text=MOD.read_text(encoding="utf-8")
    for term in (
        "The instruction cycle",
        "Fetch: obtain the instruction",
        "Decode: understand the instruction",
        "Execute: make the datapath act",
        "Write-back and architectural state",
        "ADD R3, R1, R2",
        "Control-flow instructions change the sequence",
    ):
        assert term in text


def test_lesson2_interactive_checks():
    text=MOD.read_text(encoding="utf-8")
    for method in ("def check_fetch", "def check_decode", "def check_execute"):
        assert method in text


def test_lesson2_route_registered():
    text=APP.read_text(encoding="utf-8")
    assert "fetch_decode_execute_lesson" in text
    assert 'route="/academy/unit-9/fetch-decode-execute"' in text


def test_path09_has_eight_live_routes_after_lesson7():
    assert CAT.read_text(encoding="utf-8").count("/academy/unit-9/") == 8


def test_lesson2_advances_to_live_lesson3():
    text=MOD.read_text(encoding="utf-8")
    assert "Next · Registers, Buses & Register Transfer" in text
    assert 'href="/academy/unit-9/register-transfer"' in text
