from digital_logic_lab.logic_core import evaluate_circuit


def _gate(gate_type, num_inputs=2, **sources):
    g = {"type": gate_type, "value": 0, "num_inputs": num_inputs}
    for i in range(1, num_inputs + 1):
        g[f"input{i}_src"] = sources.get(f"input{i}_src", "")
    return g


def test_dynamic_four_input_logic_uses_all_inputs():
    gates = {
        "a": {"type": "INPUT", "value": 1},
        "b": {"type": "INPUT", "value": 1},
        "c": {"type": "INPUT", "value": 1},
        "d": {"type": "INPUT", "value": 0},
        "and4": _gate("AND", 4, input1_src="a", input2_src="b", input3_src="c", input4_src="d"),
        "nand4": _gate("NAND", 4, input1_src="a", input2_src="b", input3_src="c", input4_src="d"),
        "or4": _gate("OR", 4, input1_src="d", input2_src="d", input3_src="d", input4_src="a"),
        "nor4": _gate("NOR", 4, input1_src="d", input2_src="d", input3_src="d", input4_src="a"),
    }
    result = evaluate_circuit(gates)
    assert result["and4"]["value"] == 0
    assert result["nand4"]["value"] == 1
    assert result["or4"]["value"] == 1
    assert result["nor4"]["value"] == 0


def test_nand_four_inputs_with_three_low_one_high_is_high():
    gates = {
        "a": {"type": "INPUT", "value": 0},
        "b": {"type": "INPUT", "value": 0},
        "c": {"type": "INPUT", "value": 0},
        "d": {"type": "INPUT", "value": 1},
        "nand4": _gate("NAND", 4, input1_src="a", input2_src="b", input3_src="c", input4_src="d"),
    }
    result = evaluate_circuit(gates)
    assert result["nand4"]["value"] == 1
