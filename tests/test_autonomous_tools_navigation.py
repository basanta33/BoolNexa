from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
UI = (ROOT / "digital_logic_lab" / "ui" / "components.py").read_text(encoding="utf-8")
HUB = (ROOT / "digital_logic_lab" / "tools_hub.py").read_text(encoding="utf-8")


def test_tools_hub_route_is_registered():
    assert "from .tools_hub import tools_hub" in APP
    assert 'route="/tools"' in APP
    assert "Digital Logic Tools | BoolNexa" in APP


def test_shared_header_exposes_autonomous_modules():
    for label in (
        "Simulator",
        "Academy",
        "Tools",
        "Number Systems",
        "Boolean Lab",
        "Circuit Generator",
    ):
        assert f'nav_link("{label}"' in UI


def test_tools_hub_links_to_real_existing_routes():
    for href in (
        '"/"',
        '"/academy"',
        '"/tools/boolean"',
        '"/tools/circuit"',
        '"/tools/number-systems"',
    ):
        assert f'"href": {href}' in HUB


def test_simulator_has_direct_links_to_other_modules():
    for href in (
        'href="/tools"',
        'href="/tools/boolean"',
        'href="/tools/circuit"',
        'href="/tools/number-systems"',
        'href="/academy"',
    ):
        assert href in APP
