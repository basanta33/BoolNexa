from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_registers_counters_path07.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"


def test_path07_lessons_1_2_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def registers_parallel_storage_lesson" in text
    assert "def shift_registers_data_movement_lesson" in text
    assert "Registers & Parallel Data Storage" in text
    assert "Shift Registers & Serial/Parallel Data Movement" in text


def test_register_foundation_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Register width", "Parallel load", "Load enable and hold", "Registers inside a datapath"):
        assert term in text


def test_shift_register_modes():
    text = MOD.read_text(encoding="utf-8")
    for term in ("SISO", "SIPO", "PISO", "PIPO", "Bidirectional and universal shift registers"):
        assert term in text


def test_path07_navigation():
    text = MOD.read_text(encoding="utf-8")
    assert 'href="/academy/unit-7/registers-parallel-storage"' in text
    assert 'href="/academy/unit-7/shift-registers"' in text


def test_path07_routes_registered():
    text = APP.read_text(encoding="utf-8")
    assert "registers_parallel_storage_lesson" in text
    assert "shift_registers_data_movement_lesson" in text
    assert 'route="/academy/unit-7/registers-parallel-storage"' in text
    assert 'route="/academy/unit-7/shift-registers"' in text
