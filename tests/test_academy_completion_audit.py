from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "digital_logic_lab"
CONTENT = DL / "academy_content.py"
CATALOG = DL / "academy_route_catalog.py"
APP = DL / "digital_logic_lab.py"

EXPECTED_LESSONS = {
    1: 10,
    2: 10,
    3: 10,
    4: 10,
    5: 10,
    6: 10,
    7: 7,
    8: 8,
    9: 8,
    10: 8,
    11: 8,
    12: 8,
}
EXPECTED_TOTAL = sum(EXPECTED_LESSONS.values())


def _catalog_routes():
    text = CATALOG.read_text(encoding="utf-8")
    return re.findall(r'"(/academy/unit-(\d+)/[^"]+)"', text)


def _app_routes():
    text = APP.read_text(encoding="utf-8")
    return re.findall(r'route="(/academy/unit-(\d+)/[^"]+)"', text)


def test_all_twelve_curriculum_paths_are_declared():
    text = CONTENT.read_text(encoding="utf-8")
    numbers = [int(n) for n in re.findall(r'\{"number": (\d+),', text)]
    assert numbers == list(range(1, 13))


def test_declared_lesson_counts_match_completed_curriculum():
    text = CONTENT.read_text(encoding="utf-8")
    for path, lessons in EXPECTED_LESSONS.items():
        assert re.search(
            rf'\{{"number": {path}, .*?"lessons": {lessons},',
            text,
        )


def test_route_catalog_has_exactly_107_unique_live_lessons():
    routes = [route for route, _ in _catalog_routes()]
    assert len(routes) == EXPECTED_TOTAL == 107
    assert len(set(routes)) == EXPECTED_TOTAL


def test_each_path_has_expected_number_of_catalog_routes():
    routes = _catalog_routes()
    for path, expected in EXPECTED_LESSONS.items():
        assert sum(int(route_path) == path for _, route_path in routes) == expected


def test_every_catalog_route_is_registered_in_reflex_app():
    catalog = {route for route, _ in _catalog_routes()}
    app = {route for route, _ in _app_routes()}
    assert catalog == app


def test_no_duplicate_academy_page_routes_are_registered():
    routes = [route for route, _ in _app_routes()]
    assert len(routes) == len(set(routes)) == EXPECTED_TOTAL


def test_route_unit_number_matches_catalog_path_number():
    for route, route_path in _catalog_routes():
        assert f"/academy/unit-{route_path}/" in route


def test_completed_academy_has_no_disabled_lesson_navigation_buttons():
    offenders = []
    for path in sorted(DL.glob("academy*_path*.py")):
        text = path.read_text(encoding="utf-8")
        if re.search(r'rx\.button\(".*?Lesson.*?".*?disabled=True', text):
            offenders.append(path.name)
    assert offenders == []


def test_recent_terminal_paths_have_explicit_completion_markers():
    expectations = {
        "academy_cpu_path09.py": "PATH 09 COMPLETE",
        "academy_system_path10.py": "PATH 10 COMPLETE",
        "academy_embedded_path11.py": "PATH 11 COMPLETE",
        "academy_hdl_path12.py": "PATH 12 COMPLETE",
    }
    for filename, marker in expectations.items():
        assert marker in (DL / filename).read_text(encoding="utf-8")


def test_simulator_gate_click_compile_fix_is_preserved():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")


def test_academy_route_catalog_total_constant_matches_live_routes():
    namespace = {}
    exec(CATALOG.read_text(encoding="utf-8"), namespace)
    assert namespace["ACADEMY_TOTAL_LESSONS"] == EXPECTED_TOTAL
