from pathlib import Path

APP = Path("digital_logic_lab/digital_logic_lab.py").read_text(encoding="utf-8")


def test_load_bridge_reads_the_object_written_by_file_reader():
    assert "window.__importedProjectJson = JSON.parse(reader.result)" in APP
    assert "JSON.stringify(window.__importedProjectJson || null)" in APP
    assert "__getImportedProjectData ?" not in APP


def test_import_restores_canvas_and_rebuilds_component_id_counters():
    for token in (
        "self.gates = gates",
        "self.gate_keys = gate_keys",
        "self.wire_offsets = copy.deepcopy(wire_offsets)",
        "self.annotations = copy.deepcopy(annotations)",
        "self.annotation_keys = annotation_keys",
        'self.input_counter = _max_loaded_suffix("input_")',
        'self.output_counter = _max_loaded_suffix("output_")',
        'self.gate_counter = _max_loaded_suffix("gate_")',
        "self.run_circuit_evaluation(self.gates, record_history=False)",
        'self.project_status = "Project loaded successfully"',
    ):
        assert token in APP


def test_rc2_ui_and_academy_are_preserved():
    assert '"Canvas Tools"' in APP
    assert '"Component Library"' in APP
    assert "save_project_download" in APP
    assert APP.count('route="/academy/unit-') == 107
