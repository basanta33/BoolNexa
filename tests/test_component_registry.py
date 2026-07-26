from __future__ import annotations

from digital_logic_lab.logic_core import MSI_LSI_DEFS, SUPPORTED_GATE_TYPES


def test_pilot_msi_lsi_components_are_registered() -> None:
    expected = {"HALF_ADDER", "FULL_ADDER", "MUX_2_1", "DEMUX_1_2"}
    assert expected <= set(MSI_LSI_DEFS)
    assert expected <= SUPPORTED_GATE_TYPES


def test_full_adder_cascade_ports_exist() -> None:
    definition = MSI_LSI_DEFS["FULL_ADDER"]
    input_names = [name for name, _offset in definition["inputs"]]
    output_names = [name for name, _offset in definition["outputs"]]

    assert input_names == ["A", "B", "CIN"]
    assert output_names == ["SUM", "COUT"]
