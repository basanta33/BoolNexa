"""Pure digital-logic engine and component definitions.

This module intentionally has no Reflex dependency.  It can therefore be
tested quickly with pytest and reused by the UI without compiling the web app.
"""

import copy
from typing import TypedDict

# =============================================================================
# COMPONENT REGISTRY
# =============================================================================
PortDef = tuple[str, int]


class ComponentDef(TypedDict):
    label: str
    inputs: list[PortDef]
    outputs: list[PortDef]
    width: int
    height: int
    primary_output: str


# MSI/LSI v1 deliberately exposes only the logical pins needed to build and
# cascade circuits. Electrical loading, package pins, and device-specific
# enable pins are outside the scope of this educational logic simulator.
MSI_LSI_DEFS: dict[str, ComponentDef] = {
    "HALF_ADDER": {
        "label": "HALF ADDER",
        "inputs": [("A", 25), ("B", 50)],
        "outputs": [("SUM", 25), ("CARRY", 50)],
        "width": 120,
        "height": 70,
        "primary_output": "SUM",
    },
    "FULL_ADDER": {
        "label": "FULL ADDER",
        "inputs": [("A", 22), ("B", 45), ("CIN", 68)],
        "outputs": [("SUM", 30), ("COUT", 60)],
        "width": 130,
        "height": 90,
        "primary_output": "SUM",
    },
    "MUX_2_1": {
        "label": "2:1 MUX",
        "inputs": [("I0", 22), ("I1", 48), ("S", 68)],
        "outputs": [("Y", 40)],
        "width": 120,
        "height": 80,
        "primary_output": "Y",
    },
    "DEMUX_1_2": {
        "label": "1:2 DEMUX",
        "inputs": [("D", 30), ("S", 62)],
        "outputs": [("Y0", 22), ("Y1", 55)],
        "width": 120,
        "height": 80,
        "primary_output": "Y0",
    },
    "MUX_4_1": {
        "label": "4:1 MUX",
        "inputs": [("I0", 18), ("I1", 36), ("I2", 54), ("I3", 72), ("S0", 90), ("S1", 108)],
        "outputs": [("Y", 54)],
        "width": 130,
        "height": 120,
        "primary_output": "Y",
    },
    "DEMUX_1_4": {
        "label": "1:4 DEMUX",
        "inputs": [("D", 30), ("S0", 78), ("S1", 100)],
        "outputs": [("Y0", 18), ("Y1", 42), ("Y2", 66), ("Y3", 90)],
        "width": 130,
        "height": 110,
        "primary_output": "Y0",
    },
    "DECODER_2_4": {
        "label": "2→4 DECODER",
        "inputs": [("A0", 38), ("A1", 72)],
        "outputs": [("Y0", 18), ("Y1", 38), ("Y2", 58), ("Y3", 78)],
        "width": 130,
        "height": 96,
        "primary_output": "Y0",
    },
    "ENCODER_4_2": {
        "label": "4→2 ENCODER",
        "inputs": [("D0", 18), ("D1", 38), ("D2", 58), ("D3", 78)],
        "outputs": [("A0", 34), ("A1", 64)],
        "width": 130,
        "height": 96,
        "primary_output": "A0",
    },
}

MSI_LSI_TYPES = tuple(MSI_LSI_DEFS.keys())

SUPPORTED_GATE_TYPES = {
    "NOT",
    "AND",
    "NAND",
    "OR",
    "NOR",
    "XOR",
    "XNOR",
    "INPUT",
    "OUTPUT",
    "CLK",
    "SEVEN_SEG",
    "D_FF",
    "T_FF",
    "RS_FF",
    "JK_FF",
    *MSI_LSI_TYPES,
}


def get_component_input_count(gate_type: str) -> int:
    if gate_type in MSI_LSI_DEFS:
        return len(MSI_LSI_DEFS[gate_type]["inputs"])
    if gate_type == "SEVEN_SEG":
        return 4
    if gate_type in ["RS_FF", "JK_FF"]:
        return 3
    if gate_type in ["D_FF", "T_FF", "XOR", "XNOR"]:
        return 2
    if gate_type in ["NOT", "OUTPUT"]:
        return 1
    if gate_type in ["INPUT", "CLK"]:
        return 0
    return 2


def normalize_basic_gate_input_count(gate_type: str, requested: int) -> int:
    """Normalize the selectable input count for basic gates."""
    if gate_type == "NOT":
        return 1
    if gate_type in {"XOR", "XNOR"}:
        return 2
    if gate_type in {"AND", "NAND", "OR", "NOR"}:
        return max(2, min(8, int(requested)))
    return get_component_input_count(gate_type)


def get_component_width(gate_type: str) -> int:
    if gate_type in MSI_LSI_DEFS:
        return int(MSI_LSI_DEFS[gate_type]["width"])
    if gate_type in ["SEVEN_SEG", "CLK"]:
        return 110
    return 86


def get_input_pin_offset(gate_type: str, idx: int, num_inputs: int) -> int:
    """Return the vertical input-pin offset in component coordinates."""
    if gate_type == "NOT":
        return 30
    if gate_type in {"XOR", "XNOR"}:
        return 20 if idx == 1 else 40
    if gate_type in {"AND", "NAND", "OR", "NOR"}:
        count = max(2, min(8, int(num_inputs)))
        if count == 2:
            positions = [20, 40]
        else:
            top, bottom = 16, 44
            step = (bottom - top) / (count - 1)
            positions = [round(top + i * step) for i in range(count)]
        safe_idx = max(1, min(count, int(idx))) - 1
        return positions[safe_idx]
    if gate_type == "OUTPUT":
        return 30
    if gate_type == "SEVEN_SEG":
        return 18 + (idx - 1) * 18
    if gate_type in {"D_FF", "T_FF"}:
        return 18 if idx == 1 else 42
    if gate_type in {"RS_FF", "JK_FF"}:
        return {1: 18, 2: 30, 3: 48}.get(idx, 30)
    if gate_type in MSI_LSI_DEFS:
        inputs = MSI_LSI_DEFS[gate_type]["inputs"]
        if 1 <= idx <= len(inputs):
            return int(inputs[idx - 1][1])
    return 30

def get_input_pin_position(gate_type: str, idx: int, num_inputs: int) -> tuple[str, int, int]:
    """Return the actual component-edge connection point for an input pin."""
    bottom: dict[str, dict[int, int]] = {
        "MUX_2_1": {3: 60},
        "DEMUX_1_2": {2: 60},
        "MUX_4_1": {5: 50, 6: 80},
        "DEMUX_1_4": {2: 50, 3: 80},
        "DECODER_2_4": {1: 50, 2: 80},
    }
    if gate_type in bottom and idx in bottom[gate_type]:
        height = int(MSI_LSI_DEFS[gate_type]["height"])
        return ("bottom", bottom[gate_type][idx], height)
    return ("left", 0, get_input_pin_offset(gate_type, idx, num_inputs))

def get_output_pin_offset(gate_type: str, port_name: str = "") -> int:
    if gate_type in MSI_LSI_DEFS:
        outputs = MSI_LSI_DEFS[gate_type]["outputs"]
        for name, offset in outputs:
            if str(name) == str(port_name):
                return int(offset)
        return int(outputs[0][1])
    if gate_type in ["D_FF", "T_FF"]:
        return 45 if port_name == "q_bar" else 18
    if gate_type in ["RS_FF", "JK_FF"]:
        return 48 if port_name == "q_bar" else 18
    if gate_type == "SEVEN_SEG":
        return 30
    return 30


def get_source_value(gates: dict, source_ref: str) -> int:
    """Resolve gate or named-port references such as fa_1:COUT."""
    if not source_ref:
        return 0

    source_ref = str(source_ref)
    if ":" in source_ref:
        base_key, port_name = source_ref.split(":", 1)
        src_gate = gates.get(base_key)
        if not isinstance(src_gate, dict):
            return 0

        if port_name == "q_bar":
            base_val = int(src_gate.get("value", 0))
            return int(src_gate.get("value_bar", 1 - base_val))

        outputs = src_gate.get("outputs", {})
        if isinstance(outputs, dict) and port_name in outputs:
            return int(outputs.get(port_name, 0))

        # Unknown named output is deliberately LOW rather than silently using the
        # component's primary output.
        return 0

    src_gate = gates.get(source_ref)
    if not isinstance(src_gate, dict):
        return 0
    return int(src_gate.get("value", 0))


# =============================================================================
# 0. COMBINATIONAL & SEQUENTIAL DIGITAL LOGIC EVALUATION ENGINE
# =============================================================================


def evaluate_circuit(gates: dict) -> dict:
    """Evaluates combinational and sequential logic nodes with realistic IC behaviors (supporting independent Q and Q')."""
    evaluated = copy.deepcopy(gates)

    # 7-Segment HEX Decoder Truth Table (4-bit X3..X0 input; Active-High segments a..g)
    # Segments order: [a, b, c, d, e, f, g]
    SEVEN_SEG_TABLE = {
        0: [1, 1, 1, 1, 1, 1, 0],
        1: [0, 1, 1, 0, 0, 0, 0],
        2: [1, 1, 0, 1, 1, 0, 1],
        3: [1, 1, 1, 1, 0, 0, 1],
        4: [0, 1, 1, 0, 0, 1, 1],
        5: [1, 0, 1, 1, 0, 1, 1],
        6: [1, 0, 1, 1, 1, 1, 1],
        7: [1, 1, 1, 0, 0, 0, 0],
        8: [1, 1, 1, 1, 1, 1, 1],
        9: [1, 1, 1, 1, 0, 1, 1],  # Only e (index 4) is 0 (off)
        10: [1, 1, 1, 0, 1, 1, 1],  # A
        11: [0, 0, 1, 1, 1, 1, 1],  # b
        12: [1, 0, 0, 1, 1, 1, 0],  # C
        13: [0, 1, 1, 1, 1, 0, 1],  # d
        14: [1, 0, 0, 1, 1, 1, 1],  # E
        15: [1, 0, 0, 0, 1, 1, 1],  # F
    }

    hex_chars = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "b",
        "C",
        "d",
        "E",
        "F",
    ]

    # Scale the convergence bound with circuit size instead of using a fixed 15 passes.
    max_iterations = max(32, len(evaluated) * 2 + 4)
    converged = False
    for _ in range(max_iterations):
        changed = False
        for _g_key, g in evaluated.items():
            g_type = g.get("type", "")
            if g_type in ["INPUT", "CLK"]:
                continue

            num_in = get_component_input_count(g_type)

            input_vals = []
            for idx in range(1, num_in + 1):
                src = g.get(f"input{idx}_src", "")
                val = get_source_value(evaluated, src)
                input_vals.append(val)

            new_val = g.get("value", 0)
            new_val_bar = g.get("value_bar", 1 - new_val)
            old_outputs = copy.deepcopy(g.get("outputs", {}))
            new_outputs = copy.deepcopy(old_outputs)

            if g_type == "OUTPUT":
                new_val = input_vals[0] if input_vals else 0
                new_val_bar = 1 - new_val
            elif g_type == "NOT":
                new_val = 0 if (input_vals and input_vals[0] == 1) else 1
                new_val_bar = 1 - new_val
            elif g_type == "AND":
                new_val = 1 if (input_vals and all(v == 1 for v in input_vals)) else 0
                new_val_bar = 1 - new_val
            elif g_type == "NAND":
                new_val = 0 if (input_vals and all(v == 1 for v in input_vals)) else 1
                new_val_bar = 1 - new_val
            elif g_type == "OR":
                new_val = 1 if (input_vals and any(v == 1 for v in input_vals)) else 0
                new_val_bar = 1 - new_val
            elif g_type == "NOR":
                new_val = 0 if (input_vals and any(v == 1 for v in input_vals)) else 1
                new_val_bar = 1 - new_val
            elif g_type == "XOR":
                val1 = input_vals[0] if len(input_vals) > 0 else 0
                val2 = input_vals[1] if len(input_vals) > 1 else 0
                new_val = 1 if (val1 != val2) else 0
                new_val_bar = 1 - new_val
            elif g_type == "XNOR":
                val1 = input_vals[0] if len(input_vals) > 0 else 0
                val2 = input_vals[1] if len(input_vals) > 1 else 0
                new_val = 1 if (val1 == val2) else 0
                new_val_bar = 1 - new_val
            elif g_type == "SEVEN_SEG":
                # Four-bit hexadecimal input: X3 is MSB and X0 is LSB.
                x3 = input_vals[0] if len(input_vals) > 0 else 0
                x2 = input_vals[1] if len(input_vals) > 1 else 0
                x1 = input_vals[2] if len(input_vals) > 2 else 0
                x0 = input_vals[3] if len(input_vals) > 3 else 0
                val_val = (x3 << 3) | (x2 << 2) | (x1 << 1) | x0

                new_val = val_val
                new_val_bar = 0
                segs = SEVEN_SEG_TABLE.get(val_val & 0x0F, [0, 0, 0, 0, 0, 0, 0])
                g["seg_a"] = segs[0]
                g["seg_b"] = segs[1]
                g["seg_c"] = segs[2]
                g["seg_d"] = segs[3]
                g["seg_e"] = segs[4]
                g["seg_f"] = segs[5]
                g["seg_g"] = segs[6]
                g["hex_char"] = hex_chars[val_val & 0x0F]
            elif g_type == "HALF_ADDER":
                a_val = input_vals[0] if len(input_vals) > 0 else 0
                b_val = input_vals[1] if len(input_vals) > 1 else 0
                sum_val = a_val ^ b_val
                carry_val = a_val & b_val
                new_outputs = {"SUM": sum_val, "CARRY": carry_val}
                new_val = sum_val
                new_val_bar = 1 - sum_val
            elif g_type == "FULL_ADDER":
                a_val = input_vals[0] if len(input_vals) > 0 else 0
                b_val = input_vals[1] if len(input_vals) > 1 else 0
                cin_val = input_vals[2] if len(input_vals) > 2 else 0
                sum_val = a_val ^ b_val ^ cin_val
                cout_val = (a_val & b_val) | (a_val & cin_val) | (b_val & cin_val)
                new_outputs = {"SUM": sum_val, "COUT": cout_val}
                new_val = sum_val
                new_val_bar = 1 - sum_val
            elif g_type == "MUX_2_1":
                i0_val = input_vals[0] if len(input_vals) > 0 else 0
                i1_val = input_vals[1] if len(input_vals) > 1 else 0
                s_val = input_vals[2] if len(input_vals) > 2 else 0
                y_val = i1_val if s_val else i0_val
                new_outputs = {"Y": y_val}
                new_val = y_val
                new_val_bar = 1 - y_val
            elif g_type == "DEMUX_1_2":
                d_val = input_vals[0] if len(input_vals) > 0 else 0
                s_val = input_vals[1] if len(input_vals) > 1 else 0
                y0_val = d_val if s_val == 0 else 0
                y1_val = d_val if s_val == 1 else 0
                new_outputs = {"Y0": y0_val, "Y1": y1_val}
                new_val = y0_val
                new_val_bar = 1 - y0_val
            elif g_type == "MUX_4_1":
                data = [(input_vals[i] if len(input_vals) > i else 0) for i in range(4)]
                s0 = input_vals[4] if len(input_vals) > 4 else 0
                s1 = input_vals[5] if len(input_vals) > 5 else 0
                selected = (s1 << 1) | s0
                y_val = data[selected]
                new_outputs = {"Y": y_val}
                new_val = y_val
                new_val_bar = 1 - y_val
            elif g_type == "DEMUX_1_4":
                d_val = input_vals[0] if len(input_vals) > 0 else 0
                s0 = input_vals[1] if len(input_vals) > 1 else 0
                s1 = input_vals[2] if len(input_vals) > 2 else 0
                selected = (s1 << 1) | s0
                new_outputs = {f"Y{i}": (d_val if i == selected else 0) for i in range(4)}
                new_val = new_outputs["Y0"]
                new_val_bar = 1 - new_val
            elif g_type == "DECODER_2_4":
                a0 = input_vals[0] if len(input_vals) > 0 else 0
                a1 = input_vals[1] if len(input_vals) > 1 else 0
                selected = (a1 << 1) | a0
                new_outputs = {f"Y{i}": (1 if i == selected else 0) for i in range(4)}
                new_val = new_outputs["Y0"]
                new_val_bar = 1 - new_val
            elif g_type == "ENCODER_4_2":
                d = [(input_vals[i] if len(input_vals) > i else 0) for i in range(4)]
                # Basic 4-to-2 encoder: intended for one-hot input. If several inputs
                # are high, this implements the standard OR equations rather than priority.
                a0 = d[1] | d[3]
                a1 = d[2] | d[3]
                new_outputs = {"A0": a0, "A1": a1}
                new_val = a0
                new_val_bar = 1 - a0
            elif g_type == "D_FF":
                d_val = input_vals[0] if len(input_vals) > 0 else 0
                clk_val = input_vals[1] if len(input_vals) > 1 else 0
                prev_clk = g.get("prev_clk", 0)
                if prev_clk == 0 and clk_val == 1:
                    new_val = d_val
                    new_val_bar = 1 - d_val
                g["prev_clk"] = clk_val
            elif g_type == "RS_FF":
                s_val = input_vals[0] if len(input_vals) > 0 else 0
                clk_val = input_vals[1] if len(input_vals) > 1 else 0
                r_val = input_vals[2] if len(input_vals) > 2 else 0
                prev_clk = g.get("prev_clk", 0)
                if prev_clk == 0 and clk_val == 1:
                    if s_val == 1 and r_val == 0:
                        new_val = 1
                        new_val_bar = 0
                    elif s_val == 0 and r_val == 1:
                        new_val = 0
                        new_val_bar = 1
                    elif s_val == 1 and r_val == 1:
                        new_val = 1
                        new_val_bar = 1
                        g["invalid_state"] = True
                    else:
                        g["invalid_state"] = False
                g["prev_clk"] = clk_val
            elif g_type == "JK_FF":
                j_val = input_vals[0] if len(input_vals) > 0 else 0
                clk_val = input_vals[1] if len(input_vals) > 1 else 0
                k_val = input_vals[2] if len(input_vals) > 2 else 0
                prev_clk = g.get("prev_clk", 0)
                if prev_clk == 0 and clk_val == 1:
                    curr_q = g.get("value", 0)
                    if j_val == 0 and k_val == 1:
                        new_val = 0
                        new_val_bar = 1
                    elif j_val == 1 and k_val == 0:
                        new_val = 1
                        new_val_bar = 0
                    elif j_val == 1 and k_val == 1:
                        new_val = 0 if curr_q == 1 else 1
                        new_val_bar = 1 - new_val
                g["prev_clk"] = clk_val
            elif g_type == "T_FF":
                t_val = input_vals[0] if len(input_vals) > 0 else 0
                clk_val = input_vals[1] if len(input_vals) > 1 else 0
                prev_clk = g.get("prev_clk", 0)
                if prev_clk == 0 and clk_val == 1:
                    if t_val == 1:
                        curr_q = g.get("value", 0)
                        new_val = 0 if curr_q == 1 else 1
                        new_val_bar = 1 - new_val
                g["prev_clk"] = clk_val

            value_changed = (
                g.get("value") != new_val
                or g.get("value_bar", 1 - g.get("value", 0)) != new_val_bar
            )
            outputs_changed = old_outputs != new_outputs

            if value_changed or outputs_changed:
                g["value"] = new_val
                g["value_bar"] = new_val_bar
                if g_type in MSI_LSI_DEFS:
                    g["outputs"] = new_outputs
                changed = True

        if not changed:
            converged = True
            break

    if not converged:
        for gate in evaluated.values():
            if gate.get("type") not in [
                "INPUT",
                "CLK",
                "D_FF",
                "T_FF",
                "RS_FF",
                "JK_FF",
            ]:
                gate["unstable"] = True

    return evaluated
