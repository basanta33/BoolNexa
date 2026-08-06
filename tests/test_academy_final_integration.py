from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "digital_logic_lab"
APP = DL / "digital_logic_lab.py"
ACADEMY = DL / "academy.py"
CONTENT = DL / "academy_content.py"
CATALOG = DL / "academy_route_catalog.py"


def _registered_academy_routes() -> list[str]:
    text = APP.read_text(encoding="utf-8")
    return re.findall(r'route\s*=\s*"(/academy[^"]*)"', text)


def test_all_academy_routes_are_unique():
    routes = _registered_academy_routes()
    assert len(routes) == len(set(routes))


def test_catalog_contains_all_live_lessons():
    ns = {}
    exec(CATALOG.read_text(encoding="utf-8"), ns)
    paths = ns["ACADEMY_PATH_ROUTES"]
    assert [len(paths[n]) for n in range(1, 8)] == [10, 10, 10, 10, 10, 10, 7]
    assert ns["ACADEMY_TOTAL_LESSONS"] == 107


def test_every_catalog_lesson_route_is_registered():
    ns = {}
    exec(CATALOG.read_text(encoding="utf-8"), ns)
    registered = set(_registered_academy_routes())
    for lessons in ns["ACADEMY_PATH_ROUTES"].values():
        for _title, route in lessons:
            assert route in registered


def test_every_internal_academy_href_resolves():
    registered = set(_registered_academy_routes())
    for source in DL.glob("academy*.py"):
        text = source.read_text(encoding="utf-8")
        for route in re.findall(r'href\s*=\s*"(/academy[^"]*)"', text):
            assert route in registered, f"{source.name}: unresolved Academy link {route}"


def test_curriculum_metadata_matches_implemented_paths():
    text = CONTENT.read_text(encoding="utf-8")
    expected = {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 7, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}
    for path, lessons in expected.items():
        assert re.search(
            rf'\{{"number": {path}, .*?"lessons": {lessons},',
            text,
        )


def test_academy_home_exposes_complete_curriculum_browser():
    text = ACADEMY.read_text(encoding="utf-8")
    assert "def _completed_path_browser" in text
    assert "All Academy lessons" in text
    assert "ACADEMY_PATH_ROUTES" in text
    assert "_completed_path_browser()," in text
    assert "ACADEMY_TOTAL_LESSONS" in text
