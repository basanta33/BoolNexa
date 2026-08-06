from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "digital_logic_lab"
APP = DL / "digital_logic_lab.py"
TOOLS = DL / "tools_hub.py"
ASSETS = ROOT / "assets"

ACADEMY_LESSON_COUNT = 107
EXPECTED_EXPLICIT_PUBLIC_ROUTES = {
    "/academy",
    "/tools",
    "/tools/number-systems",
    "/tools/boolean",
    "/tools/circuit",
}
EXPECTED_TOOL_HREFS = {
    "/",
    "/academy",
    "/tools/number-systems",
    "/tools/boolean",
    "/tools/circuit",
}


def _app_text():
    return APP.read_text(encoding="utf-8")


def _explicit_routes():
    return re.findall(r'route="([^"]+)"', _app_text())


def test_core_public_page_functions_exist():
    expected = {
        "digital_logic_lab.py": "index",
        "academy.py": "academy",
        "tools_hub.py": "tools_hub",
        "number_system_lab.py": "number_system_lab",
        "boolean_lab.py": "boolean_lab",
        "logic_circuit_lab.py": "logic_circuit_lab",
    }
    for filename, function_name in expected.items():
        tree = ast.parse((DL / filename).read_text(encoding="utf-8"))
        names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert function_name in names, f"{filename} no longer defines {function_name}()"


def test_main_reflex_app_registers_root_and_all_expected_public_surfaces():
    text = _app_text()
    assert "app.add_page(\n    index," in text
    explicit = set(_explicit_routes())
    assert EXPECTED_EXPLICIT_PUBLIC_ROUTES <= explicit


def test_all_explicit_routes_are_unique():
    routes = _explicit_routes()
    assert len(routes) == len(set(routes))


def test_whole_app_route_count_matches_completed_release_surface():
    routes = _explicit_routes()
    academy = [r for r in routes if r.startswith("/academy/unit-")]
    non_lesson = [r for r in routes if not r.startswith("/academy/unit-")]
    assert len(academy) == ACADEMY_LESSON_COUNT
    assert set(non_lesson) == EXPECTED_EXPLICIT_PUBLIC_ROUTES
    # Root simulator is registered by app.add_page(index) without an explicit route.
    assert len(routes) + 1 == ACADEMY_LESSON_COUNT + len(EXPECTED_EXPLICIT_PUBLIC_ROUTES) + 1


def test_tools_hub_links_only_to_registered_autonomous_surfaces():
    text = TOOLS.read_text(encoding="utf-8")
    hrefs = set(re.findall(r'"href": "([^"]+)"', text))
    assert hrefs == EXPECTED_TOOL_HREFS


def test_tools_hub_has_all_five_release_modules():
    text = TOOLS.read_text(encoding="utf-8")
    for title in (
        "Digital Logic Simulator",
        "Boolean Laboratory",
        "Logic Circuit Generator",
        "Number System Laboratory",
        "BoolNexa Academy",
    ):
        assert f'"title": "{title}"' in text


def test_release_assets_referenced_by_app_exist():
    text = _app_text()
    assert 'rx.script(src="/logic_interactions.js")' in text
    assert (ASSETS / "logic_interactions.js").is_file()
    for filename in (
        "favicon.ico",
        "apple-touch-icon.png",
        "icon-192.png",
        "icon-512.png",
        "manifest.webmanifest",
        "robots.txt",
        "og-image.png",
    ):
        assert (ASSETS / filename).is_file(), filename


def test_all_python_sources_in_main_package_parse_cleanly():
    failures = []
    for path in sorted(DL.rglob("*.py")):
        # Ignore generated cache directories defensively.
        if "__pycache__" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    assert failures == []


def test_simulator_gate_click_reflex_compile_fix_is_preserved():
    assert "State.handle_gate_click(cell_key)" in _app_text()


def test_release_app_keeps_main_navigation_targets_present():
    text = _app_text()
    # These are the stable product surfaces users must be able to reach.
    for target in (
        'route="/academy"',
        'route="/tools"',
        'route="/tools/number-systems"',
        'route="/tools/boolean"',
        'route="/tools/circuit"',
    ):
        assert target in text
