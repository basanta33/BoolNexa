from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_academy_route_catalog_is_valid_python():
    text = CATALOG.read_text(encoding="utf-8")
    compile(text, str(CATALOG), "exec")


def test_academy_route_catalog_has_no_double_comma_tuple_terminator():
    text = CATALOG.read_text(encoding="utf-8")
    assert "),," not in text


def test_path09_lesson1_remains_registered():
    text = CATALOG.read_text(encoding="utf-8")
    assert '9: (' in text
    assert '"/academy/unit-9/cpu-architecture-foundations"' in text
