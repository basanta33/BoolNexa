from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
SEO = ROOT / "digital_logic_lab" / "seo.py"
ASSETS = ROOT / "assets"
RXCONFIG = ROOT / "rxconfig.py"

PUBLIC_CORE_ROUTES = {
    "/academy",
    "/tools",
    "/tools/number-systems",
    "/tools/boolean",
    "/tools/circuit",
}


def _app_text():
    return APP.read_text(encoding="utf-8")


def _page_blocks():
    return re.findall(r'app\.add_page\((?:(?!app\.add_page).)*?\)', _app_text(), re.S)


def test_public_core_routes_have_titles_and_descriptions():
    for route in PUBLIC_CORE_ROUTES:
        matches = [b for b in _page_blocks() if f'route="{route}"' in b]
        assert len(matches) == 1, route
        block = matches[0]
        assert 'title=' in block, route
        assert 'description=' in block, route


def test_all_academy_lesson_routes_have_titles_and_descriptions():
    lesson_blocks = [b for b in _page_blocks() if '/academy/unit-' in b]
    assert len(lesson_blocks) == 107
    for block in lesson_blocks:
        assert 'title=' in block
        assert 'description=' in block


def test_literal_registered_page_titles_reference_boolnexa_brand():
    for block in _page_blocks():
        match = re.search(r'title="([^"]+)"', block)
        if match:
            assert "BoolNexa" in match.group(1)


def test_root_page_uses_centralized_boolnexa_seo_metadata():
    app_text = _app_text()
    seo_text = SEO.read_text(encoding="utf-8")
    root_block = next(b for b in _page_blocks() if "app.add_page(\n    index," in b)
    assert "title=PAGE_TITLE" in root_block
    assert "description=PAGE_DESCRIPTION" in root_block
    assert "meta=seo_meta()" in root_block
    assert "from .seo import PAGE_DESCRIPTION, PAGE_TITLE" in app_text
    assert 'PAGE_TITLE = "BoolNexa - Free Online Digital Logic Simulator"' in seo_text
    assert "PAGE_DESCRIPTION = (" in seo_text
    assert "BoolNexa" in seo_text


def test_manifest_core_identity_and_start_url():
    data = json.loads((ASSETS / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert data["name"]
    assert data["short_name"]
    assert data["start_url"] == "/"
    assert data.get("display")
    assert data.get("icons")


def test_manifest_icons_exist():
    data = json.loads((ASSETS / "manifest.webmanifest").read_text(encoding="utf-8"))
    icon_srcs = [icon["src"].lstrip("/") for icon in data["icons"]]
    assert icon_srcs
    for src in icon_srcs:
        assert (ASSETS / src).is_file(), src


def test_standard_release_icons_and_social_image_exist():
    for filename in (
        "favicon.ico",
        "apple-touch-icon.png",
        "icon-192.png",
        "icon-512.png",
        "og-image.png",
    ):
        path = ASSETS / filename
        assert path.is_file()
        assert path.stat().st_size > 0


def test_robots_txt_has_user_agent_directive():
    text = (ASSETS / "robots.txt").read_text(encoding="utf-8")
    assert re.search(r"(?im)^\s*User-agent\s*:", text)


def test_deploy_url_is_https_and_not_local():
    text = RXCONFIG.read_text(encoding="utf-8")
    match = re.search(r'deploy_url="([^"]+)"', text)
    assert match
    url = match.group(1)
    assert url.startswith("https://")
    assert "localhost" not in url
    assert "127.0.0.1" not in url


def test_public_release_routes_are_all_registered_once():
    text = _app_text()
    for route in PUBLIC_CORE_ROUTES:
        assert text.count(f'route="{route}"') == 1


def test_simulator_gate_click_compile_fix_is_still_preserved():
    assert "State.handle_gate_click(cell_key)" in _app_text()
