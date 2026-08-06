from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_system_path10.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_path10_lesson2_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def io_organisation_memory_mapped_io_lesson" in text
    assert "PATH 10 · LESSON 02" in text
    assert "I/O Organisation & Memory-Mapped I/O" in text


def test_lesson2_teaches_io_organisation_and_mmio():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "A peripheral is controlled through registers",
        "Two classic ways to organise processor I/O",
        "Memory-mapped I/O treats device registers like addressed locations",
        "Address decoding routes each access to the correct device",
        "Status registers let software observe device state",
        "Control registers let software command the peripheral",
        "Polling is the simplest way to wait for a device",
        "Read-only, write-only and read/write behavior matter",
        "Trace a complete MMIO output operation",
        "Why MMIO fits naturally with the CPU datapath",
    ):
        assert term in text


def test_lesson2_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_mappedio", "def check_status", "def check_polling"):
        assert method in text


def test_lesson2_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "io_organisation_memory_mapped_io_lesson" in text
    assert 'route="/academy/unit-10/io-organisation-memory-mapped-io"' in text


def test_path10_catalog_has_eight_live_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert text.count("/academy/unit-10/") == 8
    assert '("I/O Organisation & Memory-Mapped I/O", "/academy/unit-10/io-organisation-memory-mapped-io")' in text


def test_lesson2_links_to_lesson3():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Interrupts & Interrupt-Driven I/O" in text
    assert 'href="/academy/unit-10/interrupts-interrupt-driven-io"' in text


def test_simulator_gate_click_compile_fix_preserved():
    text = APP.read_text(encoding="utf-8")
    assert "State.handle_gate_click(cell_key)" in text
