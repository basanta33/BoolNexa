from pathlib import Path

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "digital_logic_lab.py"
).read_text(encoding="utf-8")


def test_multiline_json_stringify_callbacks_are_closed():
    assert (
        '"JSON.stringify(window.__getWireDragEndData ? window.__getWireDragEndData()"'
        '\n                  " : null)"'
    ) in SOURCE
    assert (
        '"JSON.stringify(window.__getDeleteGateData ? window.__getDeleteGateData() :"'
        '\n                  " null)"'
    ) in SOURCE
    assert (
        '"JSON.stringify(window.__getSelectGateData ? window.__getSelectGateData() :"'
        '\n                  " null)"'
    ) in SOURCE
    assert (
        '"JSON.stringify(window.__getToggleInputData ? window.__getToggleInputData()"'
        '\n                  " : null)"'
    ) in SOURCE


def test_canvas_json_stringify_iife_is_closed():
    assert "JSON.stringify((() => {" in SOURCE
    assert "})())" in SOURCE
