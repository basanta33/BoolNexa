from pathlib import Path
import ast
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RXCONFIG = ROOT / "rxconfig.py"
REQ = ROOT / "requirements.txt"
PYPROJECT = ROOT / "pyproject.toml"
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
ASSETS = ROOT / "assets"


def test_required_release_files_exist():
    for filename in ("rxconfig.py", "requirements.txt", "pyproject.toml"):
        assert (ROOT / filename).is_file(), filename


def test_reflex_dependency_is_pinned_to_expected_release():
    text = REQ.read_text(encoding="utf-8")
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert "reflex==0.9.7" in lines


def test_rxconfig_has_stable_app_name_and_https_deploy_url():
    text = RXCONFIG.read_text(encoding="utf-8")
    assert 'app_name="digital_logic_lab"' in text
    match = re.search(r'deploy_url="([^"]+)"', text)
    assert match
    assert match.group(1).startswith("https://")
    assert "localhost" not in match.group(1)


def test_rxconfig_plugins_are_explicitly_configured():
    text = RXCONFIG.read_text(encoding="utf-8")
    assert "RadixThemesPlugin()" in text
    assert "SitemapPlugin()" in text


def test_reflex_base_plugin_is_intentionally_loaded_via_reflex_runtime_dependency():
    # Reflex 0.9.7 includes reflex-base as a runtime dependency; BoolNexa pins
    # the top-level Reflex release rather than separately pinning its internals.
    text = RXCONFIG.read_text(encoding="utf-8")
    assert "from reflex_base.plugins.sitemap import SitemapPlugin" in text
    assert "reflex==0.9.7" in REQ.read_text(encoding="utf-8")


def test_application_package_uses_only_reflex_as_external_top_level_dependency():
    stdlib = set(sys.stdlib_module_names)
    stdlib.add("__future__")
    third_party = set()
    package = ROOT / "digital_logic_lab"

    for path in package.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split(".")[0]
                    if name not in stdlib and name != "digital_logic_lab":
                        third_party.add(name)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                name = node.module.split(".")[0]
                if name not in stdlib and name != "digital_logic_lab":
                    third_party.add(name)

    assert third_party == {"reflex"}


def test_pytest_configuration_points_at_project_tests():
    text = PYPROJECT.read_text(encoding="utf-8")
    assert '[tool.pytest.ini_options]' in text
    assert 'testpaths = ["tests"]' in text
    assert 'addopts = "-q"' in text


def test_app_module_and_rxconfig_parse_without_syntax_errors():
    ast.parse(APP.read_text(encoding="utf-8"))
    ast.parse(RXCONFIG.read_text(encoding="utf-8"))


def test_release_web_metadata_files_are_nonempty():
    for filename in (
        "manifest.webmanifest",
        "robots.txt",
        "favicon.ico",
        "apple-touch-icon.png",
        "icon-192.png",
        "icon-512.png",
        "og-image.png",
    ):
        path = ASSETS / filename
        assert path.is_file()
        assert path.stat().st_size > 0


def test_manifest_is_valid_json_and_has_core_pwa_fields():
    data = json.loads((ASSETS / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert data.get("name")
    assert data.get("short_name")
    assert data.get("icons")
    assert data.get("start_url") is not None


def test_robots_file_has_content():
    text = (ASSETS / "robots.txt").read_text(encoding="utf-8").strip()
    assert text


def test_simulator_compile_fix_remains_protected_for_release():
    assert "State.handle_gate_click(cell_key)" in APP.read_text(encoding="utf-8")
