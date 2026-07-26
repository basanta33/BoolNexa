from __future__ import annotations

from conftest import make_gate

from digital_logic_lab.logic_core import evaluate_circuit, get_source_value


def build_ripple_adder(a_value: int, b_value: int, bits: int) -> dict[str, dict[str, object]]:
    circuit: dict[str, dict[str, object]] = {
        "cin0": make_gate("INPUT", 0),
    }

    for bit in range(bits):
        circuit[f"a{bit}"] = make_gate("INPUT", (a_value >> bit) & 1)
        circuit[f"b{bit}"] = make_gate("INPUT", (b_value >> bit) & 1)
        carry_source = "cin0" if bit == 0 else f"fa{bit - 1}:COUT"
        circuit[f"fa{bit}"] = make_gate(
            "FULL_ADDER",
            input1_src=f"a{bit}",
            input2_src=f"b{bit}",
            input3_src=carry_source,
        )

    return circuit


def read_sum(evaluated: dict[str, dict[str, object]], bits: int) -> int:
    total = 0
    for bit in range(bits):
        outputs = evaluated[f"fa{bit}"]["outputs"]
        total |= int(outputs["SUM"]) << bit

    total |= int(evaluated[f"fa{bits - 1}"]["outputs"]["COUT"]) << bits
    return total


def test_eight_bit_full_adder_cascade() -> None:
    a_value = 0xA7
    b_value = 0x5D
    evaluated = evaluate_circuit(build_ripple_adder(a_value, b_value, 8))
    assert read_sum(evaluated, 8) == a_value + b_value


def test_sixteen_bit_full_adder_cascade() -> None:
    a_value = 0xA75C
    b_value = 0x5D3A
    evaluated = evaluate_circuit(build_ripple_adder(a_value, b_value, 16))
    assert read_sum(evaluated, 16) == a_value + b_value


def test_named_output_reference() -> None:
    circuit = {
        "a": make_gate("INPUT", 1),
        "b": make_gate("INPUT", 1),
        "ha": make_gate("HALF_ADDER", input1_src="a", input2_src="b"),
    }
    evaluated = evaluate_circuit(circuit)

    assert get_source_value(evaluated, "ha:SUM") == 0
    assert get_source_value(evaluated, "ha:CARRY") == 1


def test_one_output_can_feed_multiple_inputs() -> None:
    circuit = {
        "a": make_gate("INPUT", 1),
        "b": make_gate("INPUT", 0),
        "ha": make_gate("HALF_ADDER", input1_src="a", input2_src="b"),
        "out1": make_gate("OUTPUT", input1_src="ha:SUM"),
        "out2": make_gate("OUTPUT", input1_src="ha:SUM"),
    }
    evaluated = evaluate_circuit(circuit)

    assert evaluated["out1"]["value"] == 1
    assert evaluated["out2"]["value"] == 1
