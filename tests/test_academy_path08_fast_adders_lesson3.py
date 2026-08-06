from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "digital_logic_lab" / "academy_alu_path08.py"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
CAT = ROOT / "digital_logic_lab" / "academy_route_catalog.py"


def test_path08_lesson3_present():
    text = MOD.read_text(encoding="utf-8")
    assert "def fast_adder_architectures_lesson" in text
    assert "PATH 08 · LESSON 03" in text
    assert "Fast Adder Architectures" in text


def test_lesson3_teaches_fast_adder_concepts():
    text = MOD.read_text(encoding="utf-8")
    for term in (
        "Why ripple carry becomes slow",
        "Generate and propagate",
        "Carry-lookahead adder",
        "Parallel-prefix adders",
        "Kogge–Stone",
        "Brent–Kung",
        "Architecture trade-offs",
    ):
        assert term in text


def test_lesson3_has_interactive_checks():
    text = MOD.read_text(encoding="utf-8")
    for method in ("def check_ripple_delay", "def check_cla", "def check_prefix"):
        assert method in text


def test_lesson3_route_registered():
    text = APP.read_text(encoding="utf-8")
    assert "fast_adder_architectures_lesson" in text
    assert 'route="/academy/unit-8/fast-adders"' in text


def test_catalog_has_three_live_path08_lessons():
    text = CAT.read_text(encoding="utf-8")
    for route in (
        "/academy/unit-8/binary-arithmetic-hardware",
        "/academy/unit-8/carry-overflow-flags",
        "/academy/unit-8/fast-adders",
    ):
        assert route in text


def test_lesson3_advances_to_live_lesson4():
    text = MOD.read_text(encoding="utf-8")
    assert "Next · Arithmetic Operations & Datapaths" in text
    assert 'href="/academy/unit-8/arithmetic-datapaths"' in text
