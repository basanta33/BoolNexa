from __future__ import annotations

import pytest
from conftest import make_gate

from digital_logic_lab.logic_core import evaluate_circuit


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        ("AND", [0, 0, 0, 1]),
        ("NAND", [1, 1, 1, 0]),
        ("OR", [0, 1, 1, 1]),
        ("NOR", [1, 0, 0, 0]),
        ("XOR", [0, 1, 1, 0]),
        ("XNOR", [1, 0, 0, 1]),
    ],
)
def test_two_input_gate_truth_tables(kind: str, expected: list[int]) -> None:
    actual: list[int] = []
    for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        circuit = {
            "a": make_gate("INPUT", a),
            "b": make_gate("INPUT", b),
            "gate": make_gate(kind, input1_src="a", input2_src="b"),
        }
        actual.append(int(evaluate_circuit(circuit)["gate"]["value"]))

    assert actual == expected


def test_not_gate() -> None:
    for source, expected in ((0, 1), (1, 0)):
        circuit = {
            "a": make_gate("INPUT", source),
            "not": make_gate("NOT", input1_src="a"),
        }
        assert evaluate_circuit(circuit)["not"]["value"] == expected
