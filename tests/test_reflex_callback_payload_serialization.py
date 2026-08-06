from pathlib import Path

SOURCE = (
    Path(__file__).parents[1] / "digital_logic_lab" / "digital_logic_lab.py"
).read_text(encoding="utf-8")


def test_browser_object_callbacks_are_json_stringified():
    assert "JSON.stringify(window.__getViewChangeData" in SOURCE
    assert "JSON.stringify(window.__getDroppedGate" in SOURCE
    assert "JSON.stringify(window.__getPanData" in SOURCE
    assert "JSON.stringify((() => {" in SOURCE


def test_python_side_decodes_callback_payloads():
    assert "def _decode_callback_payload(value):" in SOURCE
    for handler in (
        "load_generated_circuit_request",
        "import_project_data",
        "drop_gate_at_location",
        "handle_canvas_click",
        "handle_pan_end",
        "handle_view_change",
        "handle_gate_drag_end",
        "handle_wire_drag_end",
        "delete_gate_by_key",
        "select_gate_by_key",
        "toggle_input_by_key",
    ):
        start = SOURCE.index(f"def {handler}")
        body = SOURCE[start:start + 260]
        assert "_decode_callback_payload" in body


def test_zoom_callbacks_do_not_return_raw_objects_to_reflex():
    assert 'JSON.stringify(window.__logicZoom ? window.__logicZoom(-0.1) : null)' in SOURCE
    assert 'JSON.stringify(window.__logicResetZoom ? window.__logicResetZoom() : null)' in SOURCE
    assert 'JSON.stringify(window.__logicFit ? window.__logicFit() : null)' in SOURCE
