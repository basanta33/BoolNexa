from digital_logic_lab.logic_core import evaluate_circuit


def _input(v):
    return {"type": "INPUT", "value": int(v)}


def _gate(kind, **sources):
    g = {"type": kind, "value": 0, "value_bar": 1}
    g.update(sources)
    return g


def test_half_subtractor_truth_table():
    expected = {
        (0, 0): (0, 0),
        (0, 1): (1, 1),
        (1, 0): (1, 0),
        (1, 1): (0, 0),
    }
    for (a, b), (diff, borrow) in expected.items():
        gates = {
            "a": _input(a),
            "b": _input(b),
            "hs": _gate("HALF_SUBTRACTOR", input1_src="a", input2_src="b"),
        }
        outputs = evaluate_circuit(gates)["hs"]["outputs"]
        assert (outputs["DIFF"], outputs["BORROW"]) == (diff, borrow)


def test_full_subtractor_truth_table():
    for a in (0, 1):
        for b in (0, 1):
            for bin_ in (0, 1):
                gates = {
                    "a": _input(a),
                    "b": _input(b),
                    "bin": _input(bin_),
                    "fs": _gate(
                        "FULL_SUBTRACTOR",
                        input1_src="a",
                        input2_src="b",
                        input3_src="bin",
                    ),
                }
                outputs = evaluate_circuit(gates)["fs"]["outputs"]
                expected_diff = a ^ b ^ bin_
                expected_bout = ((1 - a) & b) | ((1 - (a ^ b)) & bin_)
                assert outputs["DIFF"] == expected_diff
                assert outputs["BOUT"] == expected_bout


def test_full_subtractor_bout_can_cascade_to_bin():
    gates = {
        "a0": _input(0),
        "b0": _input(1),
        "bin0": _input(0),
        "low": _gate(
            "FULL_SUBTRACTOR",
            input1_src="a0",
            input2_src="b0",
            input3_src="bin0",
        ),
        "a1": _input(1),
        "b1": _input(0),
        "high": _gate(
            "FULL_SUBTRACTOR",
            input1_src="a1",
            input2_src="b1",
            input3_src="low:BOUT",
        ),
    }
    result = evaluate_circuit(gates)
    assert result["low"]["outputs"]["BOUT"] == 1
    assert result["high"]["outputs"]["DIFF"] == 0
