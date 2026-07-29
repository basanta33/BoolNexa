from __future__ import annotations

from conftest import make_gate

from digital_logic_lab.logic_core import evaluate_circuit


def test_half_adder_truth_table() -> None:
    expected = [(0, 0), (1, 0), (1, 0), (0, 1)]
    actual: list[tuple[int, int]] = []

    for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        circuit = {
            "a": make_gate("INPUT", a),
            "b": make_gate("INPUT", b),
            "ha": make_gate("HALF_ADDER", input1_src="a", input2_src="b"),
        }
        outputs = evaluate_circuit(circuit)["ha"]["outputs"]
        actual.append((int(outputs["SUM"]), int(outputs["CARRY"])))

    assert actual == expected


def test_full_adder_all_input_combinations() -> None:
    for a in (0, 1):
        for b in (0, 1):
            for cin in (0, 1):
                circuit = {
                    "a": make_gate("INPUT", a),
                    "b": make_gate("INPUT", b),
                    "cin": make_gate("INPUT", cin),
                    "fa": make_gate(
                        "FULL_ADDER",
                        input1_src="a",
                        input2_src="b",
                        input3_src="cin",
                    ),
                }
                outputs = evaluate_circuit(circuit)["fa"]["outputs"]
                total = a + b + cin
                assert outputs["SUM"] == (total & 1)
                assert outputs["COUT"] == ((total >> 1) & 1)


def test_mux_2_to_1() -> None:
    for i0 in (0, 1):
        for i1 in (0, 1):
            for select in (0, 1):
                circuit = {
                    "i0": make_gate("INPUT", i0),
                    "i1": make_gate("INPUT", i1),
                    "s": make_gate("INPUT", select),
                    "mux": make_gate(
                        "MUX_2_1",
                        input1_src="i0",
                        input2_src="i1",
                        input3_src="s",
                    ),
                }
                output = evaluate_circuit(circuit)["mux"]["outputs"]["Y"]
                assert output == (i1 if select else i0)


def test_demux_1_to_2() -> None:
    for data in (0, 1):
        for select in (0, 1):
            circuit = {
                "d": make_gate("INPUT", data),
                "s": make_gate("INPUT", select),
                "demux": make_gate(
                    "DEMUX_1_2",
                    input1_src="d",
                    input2_src="s",
                ),
            }
            outputs = evaluate_circuit(circuit)["demux"]["outputs"]
            expected = (data, 0) if select == 0 else (0, data)
            assert (outputs["Y0"], outputs["Y1"]) == expected


def test_mux_4_to_1_all_selects() -> None:
    values = (0, 1, 1, 0)
    for select in range(4):
        circuit = {f"i{i}": make_gate("INPUT", values[i]) for i in range(4)}
        circuit.update({
            "s0": make_gate("INPUT", select & 1),
            "s1": make_gate("INPUT", (select >> 1) & 1),
            "mux": make_gate(
                "MUX_4_1",
                input1_src="i0", input2_src="i1", input3_src="i2", input4_src="i3",
                input5_src="s0", input6_src="s1",
            ),
        })
        assert evaluate_circuit(circuit)["mux"]["outputs"]["Y"] == values[select]


def test_demux_1_to_4_all_selects() -> None:
    for select in range(4):
        circuit = {
            "d": make_gate("INPUT", 1),
            "s0": make_gate("INPUT", select & 1),
            "s1": make_gate("INPUT", (select >> 1) & 1),
            "demux": make_gate("DEMUX_1_4", input1_src="d", input2_src="s0", input3_src="s1"),
        }
        outputs = evaluate_circuit(circuit)["demux"]["outputs"]
        assert [outputs[f"Y{i}"] for i in range(4)] == [1 if i == select else 0 for i in range(4)]


def test_decoder_2_to_4_truth_table() -> None:
    for value in range(4):
        circuit = {
            "a0": make_gate("INPUT", value & 1),
            "a1": make_gate("INPUT", (value >> 1) & 1),
            "dec": make_gate("DECODER_2_4", input1_src="a0", input2_src="a1"),
        }
        outputs = evaluate_circuit(circuit)["dec"]["outputs"]
        assert [outputs[f"Y{i}"] for i in range(4)] == [1 if i == value else 0 for i in range(4)]


def test_encoder_4_to_2_one_hot_inputs() -> None:
    expected = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}
    for active in range(4):
        circuit = {f"d{i}": make_gate("INPUT", 1 if i == active else 0) for i in range(4)}
        circuit["enc"] = make_gate(
            "ENCODER_4_2",
            input1_src="d0", input2_src="d1", input3_src="d2", input4_src="d3",
        )
        outputs = evaluate_circuit(circuit)["enc"]["outputs"]
        assert (outputs["A0"], outputs["A1"]) == expected[active]


def test_select_and_address_pins_use_bottom_edge():
    from digital_logic_lab.logic_core import get_input_pin_position

    # The compact 2:1 MUX and 1:2 DEMUX now intentionally place their
    # single select input S on the top edge.
    assert get_input_pin_position("MUX_2_1", 3, 3)[0] == "top"
    assert get_input_pin_position("DEMUX_1_2", 2, 2)[0] == "top"

    # Multi-select/address functional blocks retain bottom control pins.
    assert get_input_pin_position("MUX_4_1", 5, 6)[0] == "bottom"
    assert get_input_pin_position("MUX_4_1", 6, 6)[0] == "bottom"
    assert get_input_pin_position("DEMUX_1_4", 2, 3)[0] == "bottom"
    assert get_input_pin_position("DEMUX_1_4", 3, 3)[0] == "bottom"
    assert get_input_pin_position("DECODER_2_4", 1, 2)[0] == "bottom"
    assert get_input_pin_position("DECODER_2_4", 2, 2)[0] == "bottom"

def test_data_pins_remain_on_left_edge():
    from digital_logic_lab.logic_core import get_input_pin_position

    assert get_input_pin_position("MUX_4_1", 1, 6)[0] == "left"
    assert get_input_pin_position("DEMUX_1_4", 1, 3)[0] == "left"
    assert get_input_pin_position("ENCODER_4_2", 4, 4)[0] == "left"



def test_all_left_input_wires_terminate_on_component_edge():
    from digital_logic_lab.logic_core import get_input_pin_position

    cases = [
        ("NOT", 1, 1),
        ("AND", 1, 2),
        ("D_FF", 1, 2),
        ("FULL_ADDER", 1, 3),
        ("MUX_4_1", 1, 6),
        ("DEMUX_1_4", 1, 3),
        ("ENCODER_4_2", 1, 4),
    ]
    for gate_type, index, count in cases:
        side, x_offset, _y_offset = get_input_pin_position(gate_type, index, count)
        assert side == "left"
        assert x_offset == 0


def test_all_bottom_control_wires_terminate_on_component_edge():
    from digital_logic_lab.logic_core import MSI_LSI_DEFS, get_input_pin_position

    # The single S controls on the compact 2:1 MUX / 1:2 DEMUX are top-edge
    # controls by design.
    top_cases = [
        ("MUX_2_1", 3, 3),
        ("DEMUX_1_2", 2, 2),
    ]
    for gate_type, index, count in top_cases:
        side, x_offset, y_offset = get_input_pin_position(
            gate_type, index, count
        )
        assert side == "top"
        assert x_offset == 60
        assert y_offset == 0

    # The remaining multi-control MSI/LSI blocks still terminate controls on
    # their bottom component edge.
    bottom_cases = [
        ("MUX_4_1", 5, 6),
        ("MUX_4_1", 6, 6),
        ("DEMUX_1_4", 2, 3),
        ("DEMUX_1_4", 3, 3),
        ("DECODER_2_4", 1, 2),
        ("DECODER_2_4", 2, 2),
    ]
    for gate_type, index, count in bottom_cases:
        side, _x_offset, y_offset = get_input_pin_position(
            gate_type, index, count
        )
        assert side == "bottom"
        assert y_offset == MSI_LSI_DEFS[gate_type]["height"]

def test_basic_gate_input_anchor_offsets_match_symbol_centers():
    from digital_logic_lab.logic_core import get_input_pin_offset

    # Basic two-input gate cards place their 40px SVG with a 10px vertical
    # offset, so SVG y=10/y=30 map exactly to logical y=20/y=40.
    for gate_type in ("AND", "NAND", "OR", "NOR", "XOR", "XNOR"):
        assert get_input_pin_offset(gate_type, 1, 2) == 20
        assert get_input_pin_offset(gate_type, 2, 2) == 40


def test_basic_gate_input_count_rules():
    from digital_logic_lab.logic_core import normalize_basic_gate_input_count

    assert normalize_basic_gate_input_count("NOT", 8) == 1
    assert normalize_basic_gate_input_count("XOR", 5) == 2
    assert normalize_basic_gate_input_count("XNOR", 5) == 2
    for gate_type in ("AND", "NAND", "OR", "NOR"):
        assert normalize_basic_gate_input_count(gate_type, 3) == 3
        assert normalize_basic_gate_input_count(gate_type, 8) == 8


def test_variable_gate_pin_offsets_are_unique():
    from digital_logic_lab.logic_core import get_input_pin_offset

    for gate_type in ("AND", "NAND", "OR", "NOR"):
        values = [get_input_pin_offset(gate_type, i, 4) for i in range(1, 5)]
        assert values == sorted(values)
        assert len(set(values)) == 4


def test_xor_xnor_fixed_two_input_geometry():
    from digital_logic_lab.logic_core import get_input_pin_offset

    for gate_type in ("XOR", "XNOR"):
        assert get_input_pin_offset(gate_type, 1, 2) == 20
        assert get_input_pin_offset(gate_type, 2, 2) == 40
