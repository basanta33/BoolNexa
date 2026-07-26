from __future__ import annotations

from digital_logic_lab.logic_core import MSI_LSI_DEFS, get_component_input_count


def make_gate(kind: str, value: int = 0, **kwargs: object) -> dict[str, object]:
    n = get_component_input_count(kind)
    gate: dict[str, object] = {
        "type": kind,
        "value": value,
        "value_bar": 1 - value if value in (0, 1) else 0,
        "num_inputs": n,
        "prev_clk": 0,
        "outputs": {},
    }

    if kind in MSI_LSI_DEFS:
        gate["outputs"] = {name: 0 for name, _offset in MSI_LSI_DEFS[kind]["outputs"]}

    for idx in range(1, max(7, n + 1)):
        gate[f"input{idx}_src"] = ""

    gate.update(kwargs)
    return gate
