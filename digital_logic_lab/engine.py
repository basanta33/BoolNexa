def evaluate_circuit(gates: dict) -> dict:
    """
    Evaluates the logic circuit state using topological traversal.
    """
    # Reset internal values for standard processing
    updated = {k: v.copy() for k, v in gates.items()}

    def get_input_val(gate_key: str, input_slot: str) -> int:
        src_key = updated[gate_key].get(input_slot, "")
        if src_key and src_key in updated:
            return updated[src_key].get("value", 0)
        return 0

    # Multi-pass evaluation to settle feedback loops & sequential paths
    for _ in range(len(updated) + 1):
        for key, g in updated.items():
            g_type = g.get("type", "")

            if g_type == "INPUT":
                continue  # Value is toggled manually by user

            i1 = get_input_val(key, "input1_src")
            i2 = get_input_val(key, "input2_src")

            if g_type == "NOT":
                g["value"] = 1 if i1 == 0 else 0
            elif g_type == "AND":
                g["value"] = 1 if (i1 == 1 and i2 == 1) else 0
            elif g_type == "NAND":
                g["value"] = 0 if (i1 == 1 and i2 == 1) else 1
            elif g_type == "OR":
                g["value"] = 1 if (i1 == 1 or i2 == 1) else 0
            elif g_type == "NOR":
                g["value"] = 0 if (i1 == 1 or i2 == 1) else 1
            elif g_type == "XOR":
                g["value"] = 1 if (i1 != i2) else 0
            elif g_type == "XNOR":
                g["value"] = 1 if (i1 == i2) else 0

    return updated