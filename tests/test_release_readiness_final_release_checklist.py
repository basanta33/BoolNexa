from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
RXCONFIG = ROOT / "rxconfig.py"
REQ = ROOT / "requirements.txt"
PYPROJECT = ROOT / "pyproject.toml"
ASSETS = ROOT / "assets"
CATALOG = ROOT / "digital_logic_lab" / "academy_route_catalog.py"

EXPECTED_ACADEMY_LESSONS = 107


def test_release_entrypoint_files_exist():
    for path in (
        APP,
        RXCONFIG,
        REQ,
        PYPROJECT,
        CATALOG,
    ):
        assert path.is_file(), path


def test_release_entrypoint_python_files_parse_cleanly():
    for path in (APP, RXCONFIG, CATALOG):
        ast.parse(path.read_text(encoding="utf-8"))


def test_reflex_release_version_is_pinned():
    lines = [
        line.strip()
        for line in REQ.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert "reflex==0.9.7" in lines


def test_deploy_target_is_https_and_not_local():
    text = RXCONFIG.read_text(encoding="utf-8")
    match = re.search(r'deploy_url="([^"]+)"', text)
    assert match
    deploy_url = match.group(1)
    assert deploy_url.startswith("https://")
    assert "localhost" not in deploy_url
    assert "127.0.0.1" not in deploy_url


def test_release_app_name_matches_python_package():
    text = RXCONFIG.read_text(encoding="utf-8")
    assert 'app_name="digital_logic_lab"' in text
    assert (ROOT / "digital_logic_lab" / "__init__.py").is_file()


def test_academy_total_constant_matches_completed_release():
    namespace = {}
    exec(CATALOG.read_text(encoding="utf-8"), namespace)
    assert namespace["ACADEMY_TOTAL_LESSONS"] == EXPECTED_ACADEMY_LESSONS


def test_all_107_academy_routes_are_registered_in_main_app():
    text = APP.read_text(encoding="utf-8")
    routes = re.findall(r'route="(/academy/unit-\d+/[^"]+)"', text)
    assert len(routes) == EXPECTED_ACADEMY_LESSONS
    assert len(set(routes)) == EXPECTED_ACADEMY_LESSONS


def test_no_duplicate_explicit_release_routes():
    text = APP.read_text(encoding="utf-8")
    routes = re.findall(r'route="([^"]+)"', text)
    assert len(routes) == len(set(routes))


def test_release_assets_are_present_and_nonempty():
    for filename in (
        "favicon.ico",
        "apple-touch-icon.png",
        "icon-192.png",
        "icon-512.png",
        "manifest.webmanifest",
        "robots.txt",
        "og-image.png",
        "logic_interactions.js",
    ):
        path = ASSETS / filename
        assert path.is_file(), filename
        assert path.stat().st_size > 0, filename


def test_manifest_has_valid_release_start_url():
    data = json.loads((ASSETS / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert data["start_url"] == "/"
    assert data["name"]
    assert data["short_name"]
    assert data["icons"]


def test_robots_txt_is_parseable_as_text_and_targets_crawlers():
    text = (ASSETS / "robots.txt").read_text(encoding="utf-8")
    assert re.search(r"(?im)^\s*User-agent\s*:", text)


def test_pytest_is_configured_as_release_gate():
    text = PYPROJECT.read_text(encoding="utf-8")
    assert '[tool.pytest.ini_options]' in text
    assert 'testpaths = ["tests"]' in text
    assert 'addopts = "-q"' in text


def test_root_simulator_release_hook_and_compile_fix_are_preserved():
    text = APP.read_text(encoding="utf-8")
    assert 'rx.script(src="/logic_interactions.js")' in text
    assert "State.handle_gate_click(cell_key)" in text


def test_release_core_routes_are_registered():
    text = APP.read_text(encoding="utf-8")
    for route in (
        "/academy",
        "/tools",
        "/tools/number-systems",
        "/tools/boolean",
        "/tools/circuit",
    ):
        assert text.count(f'route="{route}"') == 1


def test_no_accidental_debug_or_temporary_routes_are_registered():
    text = APP.read_text(encoding="utf-8")
    routes = re.findall(r'route="([^"]+)"', text)
    forbidden_fragments = (
        "/debug",
        "/tmp",
        "/temp",
        "/test-only",
        "/dev-only",
        "/internal-only",
    )
    assert all(
        not any(fragment in route for fragment in forbidden_fragments)
        for route in routes
    )
