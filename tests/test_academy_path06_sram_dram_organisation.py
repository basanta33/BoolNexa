from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_memory_foundations.py").read_text(encoding="utf-8")


def test_path06_lessons_3_4_routes_registered():
    assert 'route="/academy/unit-6/sram-dram"' in APP
    assert 'route="/academy/unit-6/memory-organisation"' in APP
    assert "sram_dram_lesson" in APP
    assert "memory_organisation_lesson" in APP


def test_sram_dram_core_content():
    for text in [
        "SRAM vs DRAM",
        "Two ways to hold a volatile bit",
        "Inside an SRAM cell",
        "Inside a DRAM cell",
        "Periodic refresh required",
        "higher storage density",
        "sense amplifier",
        "does not mean non-volatile",
        "check_sram_cell",
        "check_dram_refresh",
        "check_density",
    ]:
        assert text in LESSONS


def test_memory_organisation_core_content():
    for text in [
        "Memory Addressing, Organisation & Expansion",
        "depth × width",
        "1K × 8",
        "Address lines determine depth",
        "Width expansion",
        "Depth expansion",
        "chip-select",
        "Address maps and decoding",
        "bank matrix",
        "check_organisation",
        "check_expansion",
        "check_chip_select",
    ]:
        assert text in LESSONS


def test_memory_math_and_precision_language():
    assert "1024 × 8 = 8192 bits" in LESSONS
    assert "2¹⁰ = 1024" in LESSONS
    assert "1K × 16 from 1K × 8" in LESSONS
    assert "2K × 8 from two 1K × 8" in LESSONS
    assert "Exact command sequences and timings are device-specific" in LESSONS
    assert "consult the actual memory specification" in LESSONS


def test_path06_lessons_1_to_4_navigation_chain():
    assert 'href="/academy/unit-6/ram-rom"' in LESSONS
    assert 'href="/academy/unit-6/sram-dram"' in LESSONS
    assert 'href="/academy/unit-6/memory-organisation"' in LESSONS
    for number in range(1, 5):
        assert f"Path 06 · Lesson {number}" in LESSONS


def test_lesson_2_now_advances_to_lesson_3():
    lesson2 = LESSONS.split("def ram_rom_lesson():", 1)[1].split("def sram_dram_lesson():", 1)[0]
    assert 'href="/academy/unit-6/sram-dram"' in lesson2
    assert "Next lesson →" in lesson2
