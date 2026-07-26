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
