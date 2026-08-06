from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"
CONTENT = ROOT / "digital_logic_lab" / "academy_content.py"


def test_path10_lesson1_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def system_interconnect_foundations_lesson" in text
    assert "PATH 10 · LESSON 01" in text
    assert "System Interconnect & CPU–Memory/I/O Foundations" in text


def test_lesson1_teaches_system_interconnect_foundations():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "From CPU datapath to complete computer system",
        "Three kinds of information travel through an interconnect",
        "Address decoding selects exactly one target",
        "A read transaction has a direction and an owner",
        "A write transaction reverses the data direction",
        "Memory-mapped I/O gives devices addresses",
        "Fast and slow components need timing coordination",
        "Interconnect correctness rules",
        "Trace one complete peripheral write",
    ):
        assert term in text


def test_lesson1_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_interface", "def check_address", "def check_handshake"):
        assert method in text


def test_path10_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "system_interconnect_foundations_lesson" in text
    assert 'route="/academy/unit-10/system-interconnect-foundations"' in text


def test_path10_catalog_has_eight_live_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-10/") == 8
    assert '("System Interconnect & CPU–Memory/I/O Foundations", "/academy/unit-10/system-interconnect-foundations")' in text


def test_path10_curriculum_foundation_declares_eight_lessons():
    text = CONTENT.read_text(encoding="utf-8")
    assert '{"number": 10, "title": "Computer Organisation and System Integration", "hours": 8, "lessons": 8' in text


def test_lesson1_links_to_lesson2():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · I/O Organisation & Memory-Mapped I/O" in text
    assert 'href="/academy/unit-10/io-organisation-memory-mapped-io"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text = APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
