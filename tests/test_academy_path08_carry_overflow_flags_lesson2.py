from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_alu_path08.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_path08_lesson2_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def carry_overflow_status_flags_lesson" in text
    assert "PATH 08 · LESSON 02" in text
    assert "Carry, Overflow & Status Flags" in text


def test_lesson2_teaches_core_status_flags():
    text = MOD.read_text(encoding="utf-8")
    for term in ("Carry flag", "Signed overflow is different", "Zero flag", "Negative flag", "Borrow and subtraction", "Status register concept"):
        assert term in text


def test_lesson2_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_overflow", "def check_zero_flag", "def check_negative_flag"):
        assert method in text


def test_lesson2_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "carry_overflow_status_flags_lesson" in text
    assert 'route="/academy/unit-8/carry-overflow-flags"' in text


def test_catalog_has_two_live_path08_lessons():
    text = CAT.read_text(encoding="utf-8")
    assert '"/academy/unit-8/binary-arithmetic-hardware"' in text
    assert '"/academy/unit-8/carry-overflow-flags"' in text


def test_lesson2_advances_to_live_lesson3():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Fast Adder Architectures" in text
    assert 'href="/academy/unit-8/fast-adders"' in text
