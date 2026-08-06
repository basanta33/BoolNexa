from pathlib import Path

ROOT = Path(__file__).parents[1]
MODELS = (ROOT / "digital_logic_lab" / "academy" / "models.py").read_text(encoding="utf-8")
CARDS = (ROOT / "digital_logic_lab" / "academy" / "widgets" / "cards.py").read_text(encoding="utf-8")
HOME = (ROOT / "digital_logic_lab" / "academy" / "pages" / "home.py").read_text(encoding="utf-8")
LESSON1 = (ROOT / "digital_logic_lab" / "academy_lesson.py").read_text(encoding="utf-8")
LESSON2 = (ROOT / "digital_logic_lab" / "academy_binary_place_value.py").read_text(encoding="utf-8")


def test_academy_labs_are_live_real_tools_not_coming_soon():
    assert 'status: str = "live"' in MODELS
    assert '"Coming soon"' not in CARDS
    assert 'rx.badge("LIVE"' in CARDS
    for route in (
        '"/"',
        '"/tools/boolean"',
        '"/tools/circuit"',
        '"/tools/number-systems"',
    ):
        assert route in MODELS


def test_each_learning_path_has_contextual_practice_tool():
    assert "PATH_PRACTICE" in MODELS
    for unit in range(1, 8):
        assert f"{unit}:" in MODELS
    assert "path.practice_href" in CARDS
    assert "path.practice_label" in CARDS


def test_academy_uses_shared_global_navigation():
    assert "from ...ui import app_header" in HOME
    assert 'app_header("academy")' in HOME


def test_binary_lessons_link_to_real_number_system_lab():
    assert 'href="/tools/number-systems"' in LESSON1
    assert 'href="/tools/number-systems"' in LESSON2
    assert "Open Number System Laboratory" in LESSON2
