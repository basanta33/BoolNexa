from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_each_standalone_release_page_highlights_its_own_navigation_item():
    expected = {
        "academy/pages/home.py": 'app_header("academy")',
        "tools_hub.py": 'app_header("tools")',
        "number_system_lab.py": 'app_header("numbers")',
        "boolean_lab.py": 'app_header("boolean")',
        "logic_circuit_lab.py": 'app_header("circuit")',
    }

    package = ROOT / "digital_logic_lab"
    for relative_path, marker in expected.items():
        source = (package / relative_path).read_text(encoding="utf-8")
        assert marker in source, relative_path
