# digital_logic_lab.py

import copy
import json
import re
import reflex as rx

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
    for g_key, g in evaluated.items():
      g_type = g.get("type", "")
      if g_type in ["INPUT", "CLK"]:
        continue

      num_in = g.get("num_inputs", 2)
      if g_type in ["NOT", "OUTPUT"]:
        num_in = 1
      elif g_type in ["D_FF", "T_FF"]:
        num_in = 2
      elif g_type in ["RS_FF", "JK_FF"]:
        num_in = 3
      elif g_type in ["XOR", "XNOR"]:
        num_in = 2
      elif g_type == "SEVEN_SEG":
        num_in = 4

      input_vals = []
      for idx in range(1, num_in + 1):
        src = g.get(f"input{idx}_src", "")
        if src:
          if ":" in src:
            base_src, pin_type = src.split(":")
            if base_src in evaluated:
              src_gate = evaluated[base_src]
              base_val = src_gate["value"]
              val = (
                  src_gate.get("value_bar", 1 - base_val)
                  if pin_type == "q_bar"
                  else base_val
              )
            else:
              val = 0
          else:
            val = evaluated[src]["value"] if src in evaluated else 0
        else:
          val = 0
        input_vals.append(val)

      new_val = g.get("value", 0)
      new_val_bar = g.get("value_bar", 1 - new_val)

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

      if g.get("value") != new_val or g.get(
          "value_bar", 1 - g.get("value", 0)
      ) != new_val_bar:
        g["value"] = new_val
        g["value_bar"] = new_val_bar
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


# =============================================================================
# 1. CORE STATE MACHINE
# =============================================================================
class State(rx.State):
  gates: dict[str, dict] = {}
  gate_keys: list[str] = []

  # Independent text notes: never part of the circuit graph.
  annotations: dict[str, dict] = {}
  annotation_keys: list[str] = []
  is_text_placement_mode: bool = False
  active_gate_options: list[str] = [
      "NOT",
      "AND",
      "NAND",
      "OR",
      "NOR",
      "XOR",
      "XNOR",
  ]

  selected_io_menu: str = ""
  selected_ff_menu: str = ""

  wires_list: list[dict[str, str]] = []
  wire_offsets: dict[str, float] = {}

  history_stack: list[dict] = []
  redo_stack: list[dict] = []
  copied_gate: dict = {}

  wiring_source: str = ""
  is_delete_mode: bool = False
  selected_gate_key: str = ""

  input_counter: int = 0
  output_counter: int = 0
  clock_counter: int = 0
  seven_seg_counter: int = 0
  gate_counter: int = 0
  annotation_counter: int = 0
  selected_gate_type: str = ""

  pan_x: float = 0.0
  pan_y: float = 0.0

  # Email registration required before project saving.
  registration_email: str = ""
  registered_email: str = ""
  registration_error: str = ""
  is_registered: bool = False

  def set_registration_email(self, value: str):
    self.registration_email = value.strip()
    self.registration_error = ""
    if self.registered_email and self.registration_email != self.registered_email:
      self.is_registered = False

  def register_email(self):
    email = self.registration_email.strip()
    valid = bool(
        re.fullmatch(
            r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+",
            email,
        )
    )
    if not valid or len(email) > 254:
      self.registered_email = ""
      self.is_registered = False
      self.registration_error = "Enter a valid email address."
      return

    self.registered_email = email
    self.is_registered = True
    self.registration_error = ""

  # Truth table modal / state
  is_truth_table_open: bool = False
  truth_table_rows: list[dict[str, str]] = []

  def toggle_truth_table(self):
    self.is_truth_table_open = not self.is_truth_table_open
    if self.is_truth_table_open:
      self.generate_truth_table()

  def generate_truth_table(self):
    inputs = [
        k for k, g in self.gates.items() if g.get("type") in ["INPUT", "CLK"]
    ]
    outputs = [k for k, g in self.gates.items() if g.get("type") == "OUTPUT"]
    if not inputs or not outputs:
      self.truth_table_rows = [{
          "info": (
              "Circuit needs at least 1 Input and 1 Output to build a truth"
              " table."
          )
      }]
      return

    num_inputs = len(inputs)
    rows = []
    original_states = {k: self.gates[k]["value"] for k in inputs}

    for i in range(2**num_inputs):
      sim_gates = copy.deepcopy(self.gates)
      row_data = {}
      for idx, inp_key in enumerate(inputs):
        bit = (i >> (num_inputs - 1 - idx)) & 1
        sim_gates[inp_key]["value"] = bit
        row_data[sim_gates[inp_key].get("label", inp_key)] = str(bit)

      evaluated_sim = evaluate_circuit(sim_gates)
      for out_key in outputs:
        out_val = evaluated_sim.get(out_key, {}).get("value", 0)
        row_data[evaluated_sim[out_key].get("label", out_key)] = str(out_val)

      rows.append(row_data)

    for k, v in original_states.items():
      self.gates[k]["value"] = v

    self.truth_table_rows = rows

  def import_project_data(self, data: dict):
    if not data or not isinstance(data, dict):
      return

    gates = data.get("gates", {})
    gate_keys = data.get("gate_keys", [])
    wire_offsets = data.get("wire_offsets", {})
    annotations = data.get("annotations", {})
    annotation_keys = data.get("annotation_keys", [])

    if not isinstance(gates, dict) or not isinstance(gate_keys, list):
      return
    if not isinstance(wire_offsets, dict):
      return
    if not isinstance(annotations, dict) or not isinstance(annotation_keys, list):
      return

    allowed_gate_types = {
        "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
        "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
        "D_FF", "T_FF", "RS_FF", "JK_FF",
    }
    gates = {
        str(key): copy.deepcopy(gate)
        for key, gate in gates.items()
        if isinstance(gate, dict)
        and gate.get("type") in allowed_gate_types
    }
    gate_keys = [str(key) for key in gate_keys if str(key) in gates]
    annotation_keys = [str(key) for key in annotation_keys if str(key) in annotations]

    self.push_undo_state()
    self.gates = gates
    self.gate_keys = gate_keys
    self.wire_offsets = copy.deepcopy(wire_offsets)
    self.annotations = copy.deepcopy(annotations)
    self.annotation_keys = annotation_keys
    self.annotation_counter = max(
        [
            int(str(k).split("_")[-1])
            for k in annotation_keys
            if str(k).startswith("note_") and str(k).split("_")[-1].isdigit()
        ] or [0]
    )
    self.run_circuit_evaluation(self.gates, record_history=False)

  def push_undo_state(self):
    snapshot = {
        "gates": copy.deepcopy(self.gates),
        "gate_keys": copy.deepcopy(self.gate_keys),
        "wire_offsets": copy.deepcopy(self.wire_offsets),
        "annotations": copy.deepcopy(self.annotations),
        "annotation_keys": copy.deepcopy(self.annotation_keys),
    }
    self.history_stack.append(snapshot)
    if len(self.history_stack) > 30:
      self.history_stack.pop(0)
    self.redo_stack.clear()

  def undo(self):
    if not self.history_stack:
      return
    current_snapshot = {
        "gates": copy.deepcopy(self.gates),
        "gate_keys": copy.deepcopy(self.gate_keys),
        "wire_offsets": copy.deepcopy(self.wire_offsets),
        "annotations": copy.deepcopy(self.annotations),
        "annotation_keys": copy.deepcopy(self.annotation_keys),
    }
    self.redo_stack.append(current_snapshot)
    previous = self.history_stack.pop()
    self.gates = previous["gates"]
    self.gate_keys = previous["gate_keys"]
    self.wire_offsets = previous.get("wire_offsets", {})
    self.annotations = previous.get("annotations", {})
    self.annotation_keys = previous.get("annotation_keys", [])
    self.run_circuit_evaluation(self.gates, record_history=False)

  def redo(self):
    if not self.redo_stack:
      return
    current_snapshot = {
        "gates": copy.deepcopy(self.gates),
        "gate_keys": copy.deepcopy(self.gate_keys),
        "wire_offsets": copy.deepcopy(self.wire_offsets),
        "annotations": copy.deepcopy(self.annotations),
        "annotation_keys": copy.deepcopy(self.annotation_keys),
    }
    self.history_stack.append(current_snapshot)
    nxt = self.redo_stack.pop()
    self.gates = nxt["gates"]
    self.gate_keys = nxt["gate_keys"]
    self.wire_offsets = nxt.get("wire_offsets", {})
    self.annotations = nxt.get("annotations", {})
    self.annotation_keys = nxt.get("annotation_keys", [])
    self.run_circuit_evaluation(self.gates, record_history=False)

  def toggle_delete_mode(self):
    self.is_delete_mode = not self.is_delete_mode
    self.selected_gate_type = ""
    self.wiring_source = ""
    self.selected_gate_key = ""

  def set_selected_type(self, gate_type: str):
    if self.selected_gate_type == gate_type:
      self.selected_gate_type = ""
    else:
      self.selected_gate_type = gate_type
    self.wiring_source = ""
    self.is_delete_mode = False

  def set_selected_io_menu(self, io_type: str):
    if io_type:
      self.add_gate_at_default_location(io_type)
      self.selected_io_menu = ""

  def set_selected_ff_menu(self, ff_type: str):
    if ff_type:
      self.add_gate_at_default_location(ff_type)
      self.selected_ff_menu = ""

  def generate_node_key(self, gate_type: str) -> str:
    if gate_type == "INPUT":
      self.input_counter += 1
      return f"input_{self.input_counter}"
    elif gate_type == "OUTPUT":
      self.output_counter += 1
      return f"output_{self.output_counter}"
    elif gate_type == "CLK":
      self.clock_counter += 1
      return f"clk_{self.clock_counter}"
    elif gate_type == "SEVEN_SEG":
      self.seven_seg_counter += 1
      return f"seven_seg_{self.seven_seg_counter}"
    else:
      self.gate_counter += 1
      return f"gate_{self.gate_counter}"

  def get_next_io_label(self, gate_type: str) -> str:
    used = {
        g.get("label", "")
        for g in self.gates.values()
        if g.get("type") == gate_type
    }
    for offset in range(26):
      char = chr(ord("A") + offset)
      if char not in used:
        return char
    return "X"

  def set_gate_label(self, key: str, label_val: str):
    if key in self.gates:
      filtered = "".join(
          c.upper() for c in label_val if "A" <= c.upper() <= "Z"
      )[:1]
      updated = copy.deepcopy(self.gates)
      updated[key]["label"] = filtered
      self.gates = updated

  def set_clock_mode(self, key: str, mode: str):
    if key in self.gates and self.gates[key]["type"] == "CLK":
      updated = copy.deepcopy(self.gates)
      updated[key]["clock_mode"] = mode
      self.gates = updated

  def set_clock_interval(self, key: str, interval_str: str):
    """Set the complete clock period in seconds (0.5 to 99 seconds)."""
    if key in self.gates and self.gates[key]["type"] == "CLK":
      try:
        val = float(interval_str)
        val = max(0.5, min(99.0, val))
      except (TypeError, ValueError):
        val = 1.0
      updated = copy.deepcopy(self.gates)
      updated[key]["clock_interval"] = val
      self.gates = updated

  def tick_clock_by_key(self, key: str):
    if key in self.gates and self.gates[key]["type"] == "CLK":
      updated = copy.deepcopy(self.gates)
      curr = updated[key].get("value", 0)
      updated[key]["value"] = 1 if curr == 0 else 0
      self.run_circuit_evaluation(updated, record_history=False)

  def set_gate_inputs_from_select(self, key: str, value_str: str):
    if key not in self.gates:
      return
    g_type = self.gates[key].get("type", "")
    if g_type not in ["AND", "NAND", "OR", "NOR"]:
      return
    try:
      new_count = int(value_str)
    except ValueError:
      return
    new_count = max(2, min(6, new_count))
    curr = self.gates[key].get("num_inputs", 2)
    if new_count != curr:
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      updated[key]["num_inputs"] = new_count
      if new_count < curr:
        for idx in range(new_count + 1, curr + 1):
          updated[key][f"input{idx}_src"] = ""
      self.run_circuit_evaluation(updated, record_history=False)

  def toggle_text_placement_mode(self):
    """Arm/disarm the one-shot canvas text tool."""
    self.is_text_placement_mode = not self.is_text_placement_mode
    if self.is_text_placement_mode:
      self.selected_gate_type = ""
      self.wiring_source = ""
      self.selected_gate_key = ""
      self.is_delete_mode = False

  def place_text_annotation(self, x: int, y: int):
    """Place one fixed text box exactly at the chosen canvas point."""
    if not self.is_text_placement_mode:
      return
    self.push_undo_state()
    self.annotation_counter += 1
    key = f"note_{self.annotation_counter}"
    updated = copy.deepcopy(self.annotations)
    updated[key] = {
        "text": "",
        "x": max(20, int(x)),
        "y": max(20, int(y)),
    }
    self.annotations = updated
    self.annotation_keys = [*self.annotation_keys, key]
    # One placement per tool activation.
    self.is_text_placement_mode = False

  def set_annotation_content(self, key: str, content: str):
    if key not in self.annotations:
      return
    updated = copy.deepcopy(self.annotations)
    updated[key]["text"] = str(content)[:60]
    self.annotations = updated

  def handle_annotation_click(self, key: str):
    """Central Delete mode also removes text boxes."""
    if self.is_delete_mode and key in self.annotations:
      self.delete_annotation(key)

  def delete_annotation(self, key: str):
    if key not in self.annotations:
      return
    self.push_undo_state()
    updated = copy.deepcopy(self.annotations)
    del updated[key]
    self.annotations = updated
    self.annotation_keys = [k for k in self.annotation_keys if k != key]

  def add_gate_at_default_location(self, gate_type: str):
    allowed_types = {
        "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
        "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
        "D_FF", "T_FF", "RS_FF", "JK_FF",
    }
    if gate_type not in allowed_types:
      return
    self.push_undo_state()
    key = self.generate_node_key(gate_type)
    updated = copy.deepcopy(self.gates)
    initial_num_inputs = (
        4
        if gate_type == "SEVEN_SEG"
        else (
            3
            if gate_type in ["RS_FF", "JK_FF"]
            else (
                2
                if gate_type in ["D_FF", "T_FF"]
                else (
                    1
                    if gate_type in ["NOT", "OUTPUT"]
                    else (0 if gate_type in ["INPUT", "CLK"] else 2)
                )
            )
        )
    )

    gate_dict = {
        "type": gate_type,
        "value": 0,
        "value_bar": 1,
        "num_inputs": initial_num_inputs,
        "x": 140,
        "y": 80,
        "label": (
            "CLK"
            if gate_type == "CLK"
            else (
                self.get_next_io_label(gate_type)
                if gate_type in ["INPUT", "OUTPUT"]
                else ""
            )
        ),
        "prev_clk": 0,
        "clock_mode": "manual",
        "clock_interval": 1,
        "seg_a": 0,
        "seg_b": 0,
        "seg_c": 0,
        "seg_d": 0,
        "seg_e": 0,
        "seg_f": 0,
        "seg_g": 0,
        "hex_char": "0",
    }
    for idx in range(1, 7):
      gate_dict[f"input{idx}_src"] = ""

    updated[key] = gate_dict
    self.gate_keys.append(key)
    self.selected_gate_type = ""
    self.wiring_source = ""
    self.run_circuit_evaluation(updated, record_history=False)

  def drop_gate_at_location(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    gate_type = data.get("type", "")
    allowed_types = {
        "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
        "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
        "D_FF", "T_FF", "RS_FF", "JK_FF",
    }
    if gate_type not in allowed_types:
      return
    self.push_undo_state()
    key = self.generate_node_key(gate_type)
    updated = copy.deepcopy(self.gates)
    initial_num_inputs = (
        4
        if gate_type == "SEVEN_SEG"
        else (
            3
            if gate_type in ["RS_FF", "JK_FF"]
            else (
                2
                if gate_type in ["D_FF", "T_FF"]
                else (
                    1
                    if gate_type in ["NOT", "OUTPUT"]
                    else (0 if gate_type in ["INPUT", "CLK"] else 2)
                )
            )
        )
    )

    gate_dict = {
        "type": gate_type,
        "value": 0,
        "value_bar": 1,
        "num_inputs": initial_num_inputs,
        "x": int(data.get("x", 140)),
        "y": int(data.get("y", 80)),
        "label": (
            "CLK"
            if gate_type == "CLK"
            else (
                self.get_next_io_label(gate_type)
                if gate_type in ["INPUT", "OUTPUT"]
                else ""
            )
        ),
        "prev_clk": 0,
        "clock_mode": "manual",
        "clock_interval": 1,
        "seg_a": 0,
        "seg_b": 0,
        "seg_c": 0,
        "seg_d": 0,
        "seg_e": 0,
        "seg_f": 0,
        "seg_g": 0,
        "hex_char": "0",
    }
    for idx in range(1, 7):
      gate_dict[f"input{idx}_src"] = ""

    updated[key] = gate_dict
    self.gate_keys.append(key)
    self.selected_gate_type = ""
    self.wiring_source = ""
    self.run_circuit_evaluation(updated, record_history=False)

  def handle_canvas_click(self, data: dict):
    if not data or not isinstance(data, dict):
      return

    if self.is_text_placement_mode:
      self.place_text_annotation(
          int(data.get("text_x", data.get("x", 140))),
          int(data.get("text_y", data.get("y", 80))),
      )
      return

    allowed_types = {
        "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
        "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
        "D_FF", "T_FF", "RS_FF", "JK_FF",
    }
    gate_type = str(self.selected_gate_type or "")
    if gate_type not in allowed_types:
      self.selected_gate_type = ""
      return

    self.selected_gate_key = ""
    self.drop_gate_at_location({
        "type": gate_type,
        "x": data.get("x", 140),
        "y": data.get("y", 80),
    })

  def handle_pan_end(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    self.pan_x = float(data.get("panX", self.pan_x))
    self.pan_y = float(data.get("panY", self.pan_y))

  def handle_gate_drag_end(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    key = data.get("key")
    x = data.get("x")
    y = data.get("y")
    if key and key in self.gates and x is not None and y is not None:
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      updated[key]["x"] = int(x)
      updated[key]["y"] = int(y)
      self.run_circuit_evaluation(updated, record_history=False)

  def handle_wire_drag_end(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    wire_id = data.get("wire_id")
    offset_dx = data.get("offset_dx")
    if wire_id and offset_dx is not None:
      self.push_undo_state()
      curr = self.wire_offsets.get(wire_id, 0.0)
      self.wire_offsets[wire_id] = curr + float(offset_dx)
      self.recalculate_all_wires()

  def delete_gate_by_key(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    key = data.get("key")
    if key:
      self.delete_gate(key)

  def select_gate_by_key(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    key = data.get("key")
    if key and key in self.gates:
      self.handle_gate_click(key)

  def toggle_input_by_key(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    key = data.get("key")
    if key:
      self.toggle_input_source(key)

  def cancel_active_actions(self):
    self.selected_gate_type = ""
    self.wiring_source = ""
    self.is_delete_mode = False
    self.selected_gate_key = ""
    self.is_text_placement_mode = False

  def select_pin_output(self, key: str):
    if self.is_delete_mode:
      base_key = key.split(":")[0] if ":" in key else key
      self.delete_gate(base_key)
      return
    if self.wiring_source == str(key):
      self.wiring_source = ""
    else:
      self.wiring_source = str(key)

  def connect_or_disconnect_input(self, target_key: str, slot: str):
    if target_key not in self.gates or slot not in self.gates[target_key]:
      self.wiring_source = ""
      return
    if self.is_delete_mode:
      self.delete_wire(target_key, slot)
      return
    if self.wiring_source:
      source_key = self.wiring_source.split(":")[0]
      if source_key not in self.gates:
        self.wiring_source = ""
        return
      if source_key == target_key:
        self.wiring_source = ""
        return
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      updated[target_key][slot] = self.wiring_source
      self.wiring_source = ""
      self.run_circuit_evaluation(updated, record_history=False)
    else:
      if target_key in self.gates and self.gates[target_key].get(slot):
        self.push_undo_state()
        updated = copy.deepcopy(self.gates)
        updated[target_key][slot] = ""
        self.run_circuit_evaluation(updated, record_history=False)

  def handle_gate_click(self, key: str):
    self.selected_gate_key = key
    if self.is_delete_mode:
      self.delete_gate(key)

  def delete_wire(self, target_key: str, slot: str):
    if not self.is_delete_mode:
      return
    if target_key in self.gates and slot in self.gates[target_key]:
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      updated[target_key][slot] = ""
      self.run_circuit_evaluation(updated, record_history=False)

  def toggle_input_source(self, key: str):
    if self.is_delete_mode:
      self.delete_gate(key)
      return
    if key in self.gates and self.gates[key]["type"] in ["INPUT", "CLK"]:
      if (
          self.gates[key].get("type") == "CLK"
          and self.gates[key].get("clock_mode", "manual") == "auto"
      ):
        return
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      updated[key]["value"] = 1 if updated[key]["value"] == 0 else 0
      self.run_circuit_evaluation(updated, record_history=False)

  def delete_gate(self, key: str):
    if key in self.gates:
      self.push_undo_state()
      updated = copy.deepcopy(self.gates)
      del updated[key]
      if key in self.gate_keys:
        self.gate_keys.remove(key)
      for _, gate in updated.items():
        for idx in range(1, 7):
          src_val = gate.get(f"input{idx}_src", "")
          base_src = src_val.split(":")[0] if ":" in src_val else src_val
          if base_src == key:
            gate[f"input{idx}_src"] = ""
      if self.selected_gate_key == key:
        self.selected_gate_key = ""
      self.run_circuit_evaluation(updated, record_history=False)

  def clear_canvas(self):
    if self.gates:
      self.push_undo_state()
    self.gates = {}
    self.gate_keys = []
    self.annotations = {}
    self.annotation_keys = []
    self.wires_list = []
    self.wire_offsets = {}
    self.wiring_source = ""
    self.selected_gate_type = ""
    self.selected_gate_key = ""
    self.is_delete_mode = False

  def run_circuit_evaluation(
      self, updated_gates: dict, record_history: bool = True
  ):
    if record_history:
      self.push_undo_state()
    self.gates = evaluate_circuit(updated_gates)
    self.recalculate_all_wires()

  def recalculate_all_wires(self):
    new_wires = []
    source_branch_counts: dict[str, int] = {}

    for target_key in self.gate_keys:
      g_data = self.gates.get(target_key, {})
      target_x = g_data.get("x", 0)
      target_y = g_data.get("y", 0)
      g_type = g_data.get("type", "")

      num_in = g_data.get("num_inputs", 2)
      if g_type in ["NOT", "OUTPUT"]:
        num_in = 1
      elif g_type in ["D_FF", "T_FF"]:
        num_in = 2
      elif g_type in ["RS_FF", "JK_FF"]:
        num_in = 3
      elif g_type == "SEVEN_SEG":
        num_in = 4

      for idx in range(1, num_in + 1):
        slot = f"input{idx}_src"
        src_composite = g_data.get(slot, "")
        if src_composite:
          base_src_key = (
              src_composite.split(":")[0]
              if ":" in src_composite
              else src_composite
          )
          is_q_bar = ":" in src_composite and "q_bar" in src_composite
          if base_src_key in self.gates:
            src_gate = self.gates[base_src_key]
            src_type = src_gate.get("type", "")

            if src_type in ["D_FF", "T_FF"]:
              src_pin_y_offset = 45 if is_q_bar else 18
            elif src_type in ["RS_FF", "JK_FF"]:
              src_pin_y_offset = 48 if is_q_bar else 18
            elif src_type in ["NOT", "INPUT", "CLK", "OUTPUT"]:
              src_pin_y_offset = 30
            elif src_type == "SEVEN_SEG":
              src_pin_y_offset = 20 * idx
            else:
              src_num_in = src_gate.get("num_inputs", 2)
              src_pin_y_offset = (
                  30 if src_num_in <= 2 else 30 + (src_num_in - 2) * 10
              )

            src_x = (
                src_gate["x"]
                + (
                    110
                    if src_type == "SEVEN_SEG"
                    else (110 if src_type == "CLK" else 86)
                )
                + 9
            )
            src_y = src_gate["y"] + src_pin_y_offset

            if g_type in ["NOT", "OUTPUT"]:
              dst_pin_y_offset = 30
            elif g_type in ["D_FF", "T_FF"]:
              dst_pin_y_offset = 15 if idx == 1 else 45
            elif g_type in ["RS_FF", "JK_FF"]:
              dst_pin_y_offset = 15 if idx == 1 else (33 if idx == 2 else 51)
            elif g_type == "SEVEN_SEG":
              dst_pin_y_offset = 20 * idx
            else:
              dst_pin_y_offset = 20 * idx

            dst_x = target_x - 9
            dst_y = target_y + dst_pin_y_offset

            wire_id = f"{src_composite}:{target_key}:{slot}"
            branch_idx = source_branch_counts.get(src_composite, 0)
            source_branch_counts[src_composite] = branch_idx + 1

            auto_stagger = 22 + (branch_idx * 20)
            user_drag_offset = self.wire_offsets.get(wire_id, 0.0)

            base_val = src_gate["value"]
            src_val = (
                src_gate.get("value_bar", 1 - base_val)
                if is_q_bar
                else base_val
            )
            wire_color = "#ef4444" if src_val == 1 else "#64748b"

            if abs(src_y - dst_y) <= 4 and dst_x >= src_x + 16:
              path_str = f"M {src_x} {src_y} L {dst_x} {dst_y}"
              mid_x = (src_x + dst_x) / 2
            elif dst_x >= src_x + 16:
              base_mid_x = src_x + (dst_x - src_x) / 2 + auto_stagger
              mid_x = base_mid_x + user_drag_offset
              path_str = f"M {src_x} {src_y} L {mid_x} {src_y} L {mid_x} {dst_y} L {dst_x} {dst_y}"
            else:
              x_out = src_x + 16 + auto_stagger + user_drag_offset
              x_in = dst_x - 16
              mid_y = (src_y + dst_y) / 2
              path_str = f"M {src_x} {src_y} L {x_out} {src_y} L {x_out} {mid_y} L {x_in} {mid_y} L {x_in} {dst_y} L {dst_x} {dst_y}"
              mid_x = x_out

            new_wires.append({
                "wire_id": wire_id,
                "src_key": src_composite,
                "target_key": target_key,
                "slot": slot,
                "d": path_str,
                "color": wire_color,
                "offset_y": str(dst_pin_y_offset),
                "mid_x": str(mid_x),
                "junc_x": str(src_x + 16 if branch_idx > 0 else src_x),
                "src_x": str(src_x),
                "src_y": str(src_y),
                "dst_x": str(dst_x),
                "dst_y": str(dst_y),
                "is_branched": "true" if branch_idx > 0 else "false",
            })
    self.wires_list = new_wires


# =============================================================================
# 2. IEEE 91/91a VECTOR SYMBOLS & PRIMITIVES (UNIFORM CAD STYLING)
# =============================================================================
def vec_input(
    is_on: rx.Var, label: rx.Var = "A", cell_key: str = ""
) -> rx.Component:
  return rx.box(
      rx.vstack(
          rx.hstack(
              rx.text(
                  "IN:",
                  font_size="9px",
                  font_weight="900",
                  color="#64748b",
                  letter_spacing="0.5px",
              ),
              rx.cond(
                  cell_key != "",
                  rx.el.input(
                      value=label,
                      on_change=lambda val, k=cell_key: State.set_gate_label(
                          k, val
                      ),
                      max_length=1,
                      class_name="input-label-field",
                      style={
                          "width": "22px",
                          "height": "18px",
                          "text_align": "center",
                          "font_size": "11px",
                          "font_weight": "900",
                          "color": "#0f172a",
                          "text_transform": "uppercase",
                          "border": "1px solid #cbd5e1",
                          "border_radius": "4px",
                          "background": "#ffffff",
                          "outline": "none",
                          "padding": "0",
                      },
                  ),
                  rx.text(label, font_size="10px", font_weight="bold", color="#0f172a"),
              ),
              spacing="1",
              align_items="center",
              justify="center",
          ),
          rx.hstack(
              rx.box(
                  width="10px",
                  height="10px",
                  border_radius="50%",
                  bg=rx.cond(is_on, "#ef4444", "#64748b"),
                  box_shadow=rx.cond(is_on, "0 0 8px #ef4444", "none"),
                  border="1.5px solid #0f172a",
              ),
              rx.text(
                  rx.cond(is_on, "1 (HIGH)", "0 (LOW)"),
                  font_size="10px",
                  font_weight="800",
              ),
              spacing="1",
              align_items="center",
              justify="center",
          ),
          spacing="1",
          align_items="center",
          justify="center",
      ),
      width="86px",
      height="60px",
      border_radius="8px",
      border="1.5px solid #0f172a",
      bg=rx.cond(is_on, "#fef2f2", "#ffffff"),
      box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
      style={
          "display": "flex",
          "align_items": "center",
          "justify_content": "center",
      },
  )


def vec_output(
    is_on: rx.Var, label: rx.Var = "Q", cell_key: str = ""
) -> rx.Component:
  return rx.box(
      rx.vstack(
          rx.hstack(
              rx.text(
                  "OUT:",
                  font_size="9px",
                  font_weight="900",
                  color="#64748b",
                  letter_spacing="0.5px",
              ),
              rx.cond(
                  cell_key != "",
                  rx.el.input(
                      value=label,
                      on_change=lambda val, k=cell_key: State.set_gate_label(
                          k, val
                      ),
                      max_length=1,
                      class_name="input-label-field",
                      style={
                          "width": "22px",
                          "height": "18px",
                          "text_align": "center",
                          "font_size": "11px",
                          "font_weight": "900",
                          "color": "#0f172a",
                          "text_transform": "uppercase",
                          "border": "1px solid #cbd5e1",
                          "border_radius": "4px",
                          "background": "#ffffff",
                          "outline": "none",
                          "padding": "0",
                      },
                  ),
                  rx.text(label, font_size="10px", font_weight="bold", color="#0f172a"),
              ),
              spacing="1",
              align_items="center",
              justify="center",
          ),
          rx.hstack(
              rx.box(
                  width="10px",
                  height="10px",
                  border_radius="50%",
                  bg=rx.cond(is_on, "#ef4444", "#94a3b8"),
                  box_shadow=rx.cond(
                      is_on,
                      "0 0 10px #ef4444",
                      "inset 0 1px 2px rgba(0,0,0,0.3)",
                  ),
                  border=rx.cond(
                      is_on, "1.5px solid #b91c1c", "1.5px solid #64748b"
                  ),
              ),
              rx.text(
                  rx.cond(is_on, "1 (ON)", "0 (OFF)"),
                  font_size="10px",
                  font_weight="800",
              ),
              spacing="1",
              align_items="center",
              justify="center",
          ),
          spacing="1",
          align_items="center",
          justify="center",
      ),
      width="86px",
      height="60px",
      border_radius="8px",
      border="1.5px solid #0f172a",
      bg=rx.cond(is_on, "#fef2f2", "#f8fafc"),
      box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
      style={
          "display": "flex",
          "align_items": "center",
          "justify_content": "center",
      },
  )


def vec_clock(
    is_on: rx.Var, clock_mode: rx.Var, clock_interval, cell_key: str
) -> rx.Component:
  interval_str = str(clock_interval)
  return rx.box(
      rx.vstack(
          rx.hstack(
              rx.text("CLK", font_size="10px", font_weight="900", color="#2563eb"),
              rx.el.svg(
                  rx.el.svg.path(
                      d="M 0 8 L 3 8 L 3 0 L 9 0 L 9 8 L 12 8",
                      fill="none",
                      stroke=rx.cond(is_on, "#ef4444", "#2563eb"),
                      stroke_width="2.5",
                  ),
                  width="16px",
                  height="14px",
                  view_box="0 0 12 8",
              ),
              spacing="2",
              align_items="center",
          ),
          rx.hstack(
              rx.el.select(
                  rx.el.option("Man", value="manual"),
                  rx.el.option("Auto", value="auto"),
                  value=clock_mode,
                  on_change=lambda val, k=cell_key: State.set_clock_mode(k, val),
                  style={
                      "font_size": "9px",
                      "font_weight": "bold",
                      "color": "#1e40af",
                      "background": "#eff6ff",
                      "border": "1.5px solid #93c5fd",
                      "border_radius": "4px",
                      "padding": "2px 4px",
                      "cursor": "pointer",
                      "outline": "none",
                      "pointer_events": "auto",
                  },
              ),
              rx.el.input(
                  value=interval_str,
                  on_change=lambda val, k=cell_key: State.set_clock_interval(
                      k, val
                  ),
                  max_length=4,
                  placeholder="1.0",
                  title="Full clock period in seconds (0.5 to 99)",
                  style={
                      "width": "38px",
                      "height": "22px",
                      "text_align": "center",
                      "font_size": "10px",
                      "font_weight": "bold",
                      "color": "#1e40af",
                      "background": "#eff6ff",
                      "border": "1.5px solid #93c5fd",
                      "border_radius": "4px",
                      "padding": "0",
                      "outline": "none",
                      "pointer_events": "auto",
                  },
              ),
              spacing="2",
              align_items="center",
          ),
          rx.hstack(
              rx.box(
                  width="12px",
                  height="12px",
                  border_radius="50%",
                  bg=rx.cond(is_on, "#ef4444", "#2563eb"),
                  box_shadow=rx.cond(is_on, "0 0 10px #ef4444", "none"),
                  border="1.5px solid #0f172a",
                  transition="all 0.2s ease",
              ),
              rx.text(
                  rx.cond(is_on, "1", "0"),
                  font_size="11px",
                  font_weight="800",
                  color=rx.cond(is_on, "#ef4444", "#0f172a"),
              ),
              spacing="2",
              align_items="center",
          ),
          spacing="2",
          align_items="center",
      ),
      width="110px",
      height="90px",
      border_radius="8px",
      border=rx.cond(is_on, "2px solid #ef4444", "1.5px solid #2563eb"),
      bg=rx.cond(is_on, "#fef2f2", "#ffffff"),
      box_shadow=rx.cond(
          is_on,
          "0 0 12px rgba(239, 68, 68, 0.3)",
          "0 4px 6px -1px rgba(0,0,0,0.05)",
      ),
      style={
          "display": "flex",
          "align_items": "center",
          "justify_content": "center",
          "transition": "all 0.2s ease",
          "pointer_events": "auto",
      },
  )


def vec_seven_seg(
    hex_char,
    seg_a=0,
    seg_b=0,
    seg_c=0,
    seg_d=0,
    seg_e=0,
    seg_f=0,
    seg_g=0,
) -> rx.Component:
  off_color = "#1e293b"
  on_color = "#ef4444"
  display_val = (
      hex_char.to_string() if isinstance(hex_char, rx.Var) else str(hex_char)
  )

  return rx.box(
      rx.vstack(
          rx.hstack(
              rx.text(
                  "HEX",
                  font_size="8px",
                  font_weight="black",
                  color="#64748b",
                  letter_spacing="0.5px",
              ),
              rx.text(
                  display_val, font_size="9px", font_weight="bold", color="#ef4444"
              ),
              spacing="2",
              align_items="center",
          ),
          rx.el.svg(
              rx.el.svg.rect(
                  x="0",
                  y="0",
                  width="56",
                  height="78",
                  rx="6",
                  fill="#090d16",
                  stroke="#334155",
                  stroke_width="2",
              ),
              rx.el.svg.text(
                  "X3", x="1", y="23", font_size="6px", font_weight="bold", fill="#94a3b8"
              ),
              rx.el.svg.text(
                  "X2", x="1", y="43", font_size="6px", font_weight="bold", fill="#94a3b8"
              ),
              rx.el.svg.text(
                  "X1", x="1", y="63", font_size="6px", font_weight="bold", fill="#94a3b8"
              ),
              rx.el.svg.text(
                  "X0", x="1", y="75", font_size="6px", font_weight="bold", fill="#94a3b8"
              ),
              rx.el.svg.polygon(
                  points="12,8 46,8 42,13 16,13",
                  fill=rx.cond(seg_a == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="10,11 15,15 15,35 12,39 8,34 8,15",
                  fill=rx.cond(seg_f == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="48,11 50,15 50,34 46,39 43,35 43,15",
                  fill=rx.cond(seg_b == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="14,38 44,38 40,42 18,42 14,38",
                  fill=rx.cond(seg_g == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="8,43 12,41 15,45 15,65 12,69 8,63",
                  fill=rx.cond(seg_e == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="43,45 46,41 50,43 50,63 46,69 43,65",
                  fill=rx.cond(seg_c == 1, on_color, off_color),
              ),
              rx.el.svg.polygon(
                  points="12,71 46,71 42,66 16,66",
                  fill=rx.cond(seg_d == 1, on_color, off_color),
              ),
              rx.el.svg.circle(cx="52", cy="68", r="2.5", fill=off_color),
              view_box="0 0 56 78",
              width="48px",
              height="66px",
          ),
          spacing="1",
          align_items="center",
          justify="center",
      ),
      width="110px",
      height="100px",
      border_radius="8px",
      border="1.5px solid #0f172a",
      bg="#f8fafc",
      box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
      style={
          "display": "flex",
          "align_items": "center",
          "justify_content": "center",
      },
  )


def vec_not_ieee() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.line(
          x1="0", y1="20", x2="16", y2="20", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="62", y1="20", x2="86", y2="20", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.path(
          d="M 16 5 L 52 20 L 16 35 Z",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
          stroke_linejoin="round",
      ),
      rx.el.svg.circle(
          cx="58", cy="20", r="4", fill="#ffffff", stroke="#0f172a", stroke_width="2.5"
      ),
      view_box="0 0 86 40",
      width="86px",
      height="40px",
      style={"pointerEvents": "none"},
  )


def vec_and_ieee(invert=False) -> rx.Component:
  elements = [
      rx.el.svg.line(
          x1="0", y1="12", x2="16", y2="12", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="28", x2="16", y2="28", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="62" if invert else "54",
          y1="20",
          x2="86",
          y2="20",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.path(
          d="M 16 5 L 38 5 A 15 15 0 0 1 38 35 L 16 35 Z",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
          stroke_linejoin="round",
      ),
  ]
  if invert:
    elements.append(
        rx.el.svg.circle(
            cx="58",
            cy="20",
            r="4",
            fill="#ffffff",
            stroke="#0f172a",
            stroke_width="2.5",
        )
    )
  return rx.el.svg(
      *elements,
      view_box="0 0 86 40",
      width="86px",
      height="40px",
      style={"pointerEvents": "none"},
  )


def vec_or_ieee(invert=False, exclusive=False) -> rx.Component:
  or_body = "M 16 5 Q 28 20 16 35 Q 38 35 54 20 Q 38 5 16 5 Z"
  xor_back = "M 10 5 Q 22 20 10 35"
  lead_x2 = "10" if exclusive else "16"

  elements = [
      rx.el.svg.line(
          x1="0",
          y1="12",
          x2=lead_x2,
          y2="12",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.line(
          x1="0",
          y1="28",
          x2=lead_x2,
          y2="28",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.line(
          x1="62" if invert else "54",
          y1="20",
          x2="86",
          y2="20",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
  ]
  if exclusive:
    elements.append(
        rx.el.svg.path(
            d=xor_back,
            fill="none",
            stroke="#0f172a",
            stroke_width="2.5",
            stroke_linecap="round",
        )
    )
    elements.extend([
        rx.el.svg.line(
            x1="10",
            y1="12",
            x2="16",
            y2="12",
            stroke="#0f172a",
            stroke_width="2.5",
        ),
        rx.el.svg.line(
            x1="10",
            y1="28",
            x2="16",
            y2="28",
            stroke="#0f172a",
            stroke_width="2.5",
        ),
    ])
  elements.append(
      rx.el.svg.path(
          d=or_body,
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
          stroke_linejoin="round",
      )
  )
  if invert:
    elements.append(
        rx.el.svg.circle(
            cx="58",
            cy="20",
            r="4",
            fill="#ffffff",
            stroke="#0f172a",
            stroke_width="2.5",
        )
    )
  return rx.el.svg(
      *elements,
      view_box="0 0 86 40",
      width="86px",
      height="40px",
      style={"pointerEvents": "none"},
  )


def vec_d_ff() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="16",
          y="5",
          width="54",
          height="56",
          rx="4",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.text(
          "D", x="22", y="20", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.polygon(points="16,41 24,45 16,49", fill="#0f172a"),
      rx.el.svg.text(
          "CLK", x="28", y="48", font_size="8px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q", x="56", y="22", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q'", x="54", y="48", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.line(
          x1="0", y1="15", x2="16", y2="15", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="45", x2="16", y2="45", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="18", x2="86", y2="18", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="45", x2="86", y2="45", stroke="#0f172a", stroke_width="2.5"
      ),
      view_box="0 0 86 66",
      width="86px",
      height="66px",
      style={"pointerEvents": "none"},
  )


def vec_rs_ff() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="16",
          y="5",
          width="54",
          height="60",
          rx="4",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.text(
          "S", x="22", y="18", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.polygon(points="16,29 24,33 16,37", fill="#0f172a"),
      rx.el.svg.text(
          "CLK", x="28", y="36", font_size="8px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "R", x="22", y="54", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q", x="56", y="22", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q'", x="54", y="50", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.line(
          x1="0", y1="15", x2="16", y2="15", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="33", x2="16", y2="33", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="51", x2="16", y2="51", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="18", x2="86", y2="18", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="48", x2="86", y2="48", stroke="#0f172a", stroke_width="2.5"
      ),
      view_box="0 0 86 70",
      width="86px",
      height="70px",
      style={"pointerEvents": "none"},
  )


def vec_jk_ff() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="16",
          y="5",
          width="54",
          height="60",
          rx="4",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.text(
          "J", x="22", y="18", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.polygon(points="16,29 24,33 16,37", fill="#0f172a"),
      rx.el.svg.text(
          "CLK", x="28", y="36", font_size="8px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "K", x="22", y="54", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q", x="56", y="22", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q'", x="54", y="50", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.line(
          x1="0", y1="15", x2="16", y2="15", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="33", x2="16", y2="33", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="51", x2="16", y2="51", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="18", x2="86", y2="18", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="48", x2="86", y2="48", stroke="#0f172a", stroke_width="2.5"
      ),
      view_box="0 0 86 70",
      width="86px",
      height="70px",
      style={"pointerEvents": "none"},
  )


def vec_t_ff() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="16",
          y="5",
          width="54",
          height="56",
          rx="4",
          fill="#ffffff",
          stroke="#0f172a",
          stroke_width="2.5",
      ),
      rx.el.svg.text(
          "T", x="22", y="20", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.polygon(points="16,41 24,45 16,49", fill="#0f172a"),
      rx.el.svg.text(
          "CLK", x="28", y="48", font_size="8px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q", x="56", y="22", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.text(
          "Q'", x="54", y="48", font_size="10px", font_weight="bold", fill="#0f172a"
      ),
      rx.el.svg.line(
          x1="0", y1="15", x2="16", y2="15", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="0", y1="45", x2="16", y2="45", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="18", x2="86", y2="18", stroke="#0f172a", stroke_width="2.5"
      ),
      rx.el.svg.line(
          x1="70", y1="45", x2="86", y2="45", stroke="#0f172a", stroke_width="2.5"
      ),
      view_box="0 0 86 66",
      width="86px",
      height="66px",
      style={"pointerEvents": "none"},
  )


def render_schematic_symbol(
    gate_type: rx.Var,
    is_on=False,
    label: rx.Var = "",
    cell_key: str = "",
    clock_mode: rx.Var = "manual",
    clock_interval=1,
    seg_a=0,
    seg_b=0,
    seg_c=0,
    seg_d=0,
    seg_e=0,
    seg_f=0,
    seg_g=0,
    hex_char="0",
) -> rx.Component:
  return rx.cond(
      gate_type == "INPUT",
      vec_input(is_on, label, cell_key),
      rx.cond(
          gate_type == "OUTPUT",
          vec_output(is_on, label, cell_key),
          rx.cond(
              gate_type == "CLK",
              vec_clock(is_on, clock_mode, clock_interval, cell_key),
              rx.cond(
                  gate_type == "SEVEN_SEG",
                  vec_seven_seg(
                      hex_char, seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g
                  ),
                  rx.cond(
                      gate_type == "NOT",
                      vec_not_ieee(),
                      rx.cond(
                          gate_type == "AND",
                              vec_and_ieee(False),
                              rx.cond(
                                  gate_type == "NAND",
                                  vec_and_ieee(True),
                                  rx.cond(
                                      gate_type == "OR",
                                      vec_or_ieee(False, False),
                                      rx.cond(
                                          gate_type == "NOR",
                                          vec_or_ieee(True, False),
                                          rx.cond(
                                              gate_type == "XOR",
                                              vec_or_ieee(False, True),
                                              rx.cond(
                                                  gate_type == "XNOR",
                                                  vec_or_ieee(True, True),
                                                  rx.cond(
                                                      gate_type == "D_FF",
                                                      vec_d_ff(),
                                                      rx.cond(
                                                          gate_type == "RS_FF",
                                                          vec_rs_ff(),
                                                          rx.cond(
                                                              gate_type
                                                              == "JK_FF",
                                                              vec_jk_ff(),
                                                              rx.cond(
                                                                  gate_type
                                                                  == "T_FF",
                                                                  vec_t_ff(),
                                                                  rx.fragment(),
                                                              ),
                                                          ),
                                                      ),
                                                  ),
                                              ),
                                          ),
                                      ),
                                  ),
                              ),
                          ),
                      ),
              ),
          ),
      ),
  )



def annotation_node(note_key: rx.Var) -> rx.Component:
  """Small transparent fixed text field, independent of the circuit graph."""
  note = State.annotations[note_key]

  return rx.box(
      rx.el.input(
          value=note["text"],
          on_change=lambda value, k=note_key: State.set_annotation_content(k, value),
          placeholder="...",
          max_length=60,
          autofocus=True,
          class_name="canvas-text-editor",
          style={
              "width": "8ch",
              "min_width": "8ch",
              "height": "22px",
              "border": "none",
              "outline": "none",
              "background": "transparent",
              "padding": "0",
              "margin": "0",
              "font_size": "13px",
              "font_weight": "600",
              "color": "#1e293b",
              "box_sizing": "content-box",
          },
      ),
      position="absolute",
      left=note["x"].to_string() + "px",
      top=note["y"].to_string() + "px",
      width="8ch",
      height="22px",
      z_index="30",
      class_name="canvas-text-box",
      on_click=State.handle_annotation_click(note_key),
      style={
          "pointerEvents": "auto",
          "background": "transparent",
          "border": "none",
      },
  )


# =============================================================================
# 3. INTERACTIVE GATE NODE
# =============================================================================
def render_input_pin_item(
    cell_key: rx.Var, idx: int, offset_y: int
) -> rx.Component:
  slot_name = f"input{idx}_src"
  return rx.box(
      rx.box(
          width="8px",
          height="8px",
          border_radius="50%",
          bg="#0f172a",
          border="2px solid #ffffff",
          _hover={
              "bg": "#ef4444",
              "transform": "scale(1.8)",
              "border-color": "#b91c1c",
          },
          transition="all 0.15s ease",
      ),
      width="18px",
      height="18px",
      position="absolute",
      left="-9px",
      top=f"{offset_y}px",
      transform="translateY(-50%)",
      z_index="15",
      style={
          "display": "flex",
          "align_items": "center",
          "justify_content": "center",
      },
      class_name="input-pin-bubble",
      cursor="pointer",
      custom_attrs={
          "data-pin-gate": cell_key,
          "data-pin-slot": slot_name,
          "data-offset-y": str(offset_y),
      },
      on_click=State.connect_or_disconnect_input(cell_key, slot_name),
  )


def schematic_gate_node(cell_key: rx.Var) -> rx.Component:
  g_data = State.gates[cell_key]
  g_type = g_data["type"]
  g_label = g_data["label"]
  clock_mode = g_data.get("clock_mode", "manual")
  clock_interval = g_data.get("clock_interval", 1)
  seg_a = g_data.get("seg_a", 0)
  seg_b = g_data.get("seg_b", 0)
  seg_c = g_data.get("seg_c", 0)
  seg_d = g_data.get("seg_d", 0)
  seg_e = g_data.get("seg_e", 0)
  seg_f = g_data.get("seg_f", 0)
  seg_g = g_data.get("seg_g", 0)
  hex_char = g_data.get("hex_char", "0")

  is_input = (g_type == "INPUT") | (g_type == "CLK")
  is_output = g_type == "OUTPUT"
  is_seven_seg = g_type == "SEVEN_SEG"
  is_source = State.wiring_source == cell_key
  is_source_bar = State.wiring_source == cell_key + ":q_bar"
  is_selected = State.selected_gate_key == cell_key
  is_on = g_data["value"] == 1

  num_inputs = g_data["num_inputs"]
  is_variable_gate = (
      (g_type == "AND")
      | (g_type == "NAND")
      | (g_type == "OR")
      | (g_type == "NOR")
  )
  is_ff = (
      (g_type == "D_FF")
      | (g_type == "T_FF")
      | (g_type == "RS_FF")
      | (g_type == "JK_FF")
  )

  card_height = rx.cond(
      g_type == "CLK",
          "90px",
          rx.cond(
              is_seven_seg,
              "100px",
              rx.cond(
                  (g_type == "RS_FF") | (g_type == "JK_FF"),
                  "70px",
                  rx.cond(
                      (g_type == "D_FF") | (g_type == "T_FF"),
                      "66px",
                      rx.cond(
                          num_inputs == 3,
                          "80px",
                          rx.cond(
                              num_inputs == 4,
                              "100px",
                              rx.cond(
                                  num_inputs == 5,
                                  "120px",
                                  rx.cond(num_inputs == 6, "140px", "60px"),
                              ),
                          ),
                      ),
                  ),
              ),
          ),
  )

  output_pin_top = rx.cond(
      is_seven_seg,
      "50px",
      rx.cond(
          (g_type == "RS_FF") | (g_type == "JK_FF"),
          "18px",
          rx.cond(
              (g_type == "D_FF") | (g_type == "T_FF"),
              "18px",
              rx.cond(
                  num_inputs == 3,
                  "40px",
                  rx.cond(
                      num_inputs == 4,
                      "50px",
                      rx.cond(
                          num_inputs == 5,
                          "60px",
                          rx.cond(num_inputs == 6, "70px", "30px"),
                      ),
                  ),
              ),
          ),
      ),
  )

  output_pin_offset_attr = rx.cond(
      is_seven_seg,
      "50",
      rx.cond(
          (g_type == "RS_FF") | (g_type == "JK_FF"),
          "18",
          rx.cond(
              (g_type == "D_FF") | (g_type == "T_FF"),
              "18",
              rx.cond(
                  num_inputs == 3,
                  "40",
                  rx.cond(
                      num_inputs == 4,
                      "50",
                      rx.cond(
                          num_inputs == 5,
                          "60",
                          rx.cond(num_inputs == 6, "70", "30"),
                      ),
                  ),
              ),
          ),
      ),
  )

  ff_output_pin_bottom = rx.cond(
      (g_type == "RS_FF") | (g_type == "JK_FF"), "48px", "45px"
  )

  ff_bottom_offset_attr = rx.cond(
      (g_type == "RS_FF") | (g_type == "JK_FF"), "48", "45"
  )

  pin1 = rx.cond(
      (g_type == "NOT") | is_output,
      render_input_pin_item(cell_key, 1, 30),
      rx.cond(
          is_seven_seg,
          render_input_pin_item(cell_key, 1, 20),
          rx.cond(
              (g_type == "D_FF") | (g_type == "T_FF"),
              render_input_pin_item(cell_key, 1, 15),
              rx.cond(
                  (g_type == "RS_FF") | (g_type == "JK_FF"),
                  render_input_pin_item(cell_key, 1, 15),
                  render_input_pin_item(cell_key, 1, 20),
              ),
          ),
      ),
  )

  pin2 = rx.cond(
      is_seven_seg,
      render_input_pin_item(cell_key, 2, 40),
      rx.cond(
          (g_type == "D_FF") | (g_type == "T_FF"),
          render_input_pin_item(cell_key, 2, 45),
          rx.cond(
              (g_type == "RS_FF") | (g_type == "JK_FF"),
              render_input_pin_item(cell_key, 2, 33),
              rx.cond(
                  ((num_inputs != 1)
                   & (~is_output)
                   & (~is_input)
                   & (g_type != "NOT")),
                  render_input_pin_item(cell_key, 2, 40),
                  rx.fragment(),
              ),
          ),
      ),
  )

  pin3 = rx.cond(
      is_seven_seg,
      render_input_pin_item(cell_key, 3, 60),
      rx.cond(
          (g_type == "RS_FF") | (g_type == "JK_FF"),
          render_input_pin_item(cell_key, 3, 51),
          rx.cond(
              ((num_inputs == 3)
               | (num_inputs == 4)
               | (num_inputs == 5)
               | (num_inputs == 6))
              & (~is_output)
              & (~is_input)
,
              render_input_pin_item(cell_key, 3, 60),
              rx.fragment(),
          ),
      ),
  )

  has_pin4 = (
      (num_inputs == 4) | (num_inputs == 5) | (num_inputs == 6)
  ) & (~is_output) & (~is_input)
  has_pin5 = (
      (num_inputs == 5) | (num_inputs == 6)
  ) & (~is_output) & (~is_input)
  has_pin6 = (
      (num_inputs == 6)
  ) & (~is_output) & (~is_input)

  pin4 = rx.cond(
      is_seven_seg,
      render_input_pin_item(cell_key, 4, 80),
      rx.cond(has_pin4, render_input_pin_item(cell_key, 4, 80), rx.fragment()),
  )
  pin5 = rx.cond(
      has_pin5, render_input_pin_item(cell_key, 5, 100), rx.fragment()
  )
  pin6 = rx.cond(
      has_pin6, render_input_pin_item(cell_key, 6, 120), rx.fragment()
  )

  return rx.box(
      rx.cond(
          is_selected
          & (~is_input)
          & (~is_output)
          & (~is_seven_seg),
          rx.hstack(
              rx.text(
                  g_type,
                  font_size="10px",
                  font_weight="black",
                  color="#1e293b",
                  user_select="none",
              ),
              rx.cond(
                  is_variable_gate,
                  rx.el.select(
                      rx.el.option("2 In", value="2"),
                      rx.el.option("3 In", value="3"),
                      rx.el.option("4 In", value="4"),
                      rx.el.option("5 In", value="5"),
                      rx.el.option("6 In", value="6"),
                      value=num_inputs.to_string(),
                      on_change=lambda val, k=cell_key: State.set_gate_inputs_from_select(
                          k, val
                      ),
                      class_name="gate-input-dropdown",
                      style={
                          "font_size": "8px",
                          "font_weight": "bold",
                          "color": "#1e40af",
                          "background": "#eff6ff",
                          "border": "1px solid #93c5fd",
                          "border_radius": "3px",
                          "padding": "0px 2px",
                          "cursor": "pointer",
                          "outline": "none",
                      },
                  ),
              ),
              spacing="1",
              justify="center",
              align_items="center",
              position="absolute",
              top="-24px",
              left="0",
              width="100%",
              z_index="25",
          ),
      ),
      rx.box(
          render_schematic_symbol(
              g_type,
              is_on,
              g_label,
              cell_key,
              clock_mode,
              clock_interval,
              seg_a,
              seg_b,
              seg_c,
              seg_d,
              seg_e,
              seg_f,
              seg_g,
              hex_char,
          ),
          style={
              "display": "flex",
              "align_items": "center",
              "justify_content": "center",
              "width": "100%",
              "height": "100%",
              "pointerEvents": "none",
          },
          class_name=rx.cond(is_input, "input-toggle-btn", ""),
          cursor=rx.cond(is_input, "pointer", "inherit"),
      ),
      rx.cond(
          ~is_input,
          rx.fragment(pin1, pin2, pin3, pin4, pin5, pin6),
      ),
      rx.cond(
          (~is_output) & (~is_seven_seg),
          rx.box(
              rx.box(
                  width="8px",
                  height="8px",
                  border_radius="50%",
                  border=rx.cond(
                      is_source, "2px solid #b91c1c", "2px solid #0f172a"
                  ),
                  bg=rx.cond(is_source, "#ef4444", "#ffffff"),
                  box_shadow=rx.cond(is_source, "0 0 8px #ef4444", "none"),
                  _hover={
                      "bg": "#ef4444",
                      "transform": "scale(1.8)",
                      "border-color": "#b91c1c",
                  },
                  transition="all 0.15s ease",
              ),
              width="18px",
              height="18px",
              position="absolute",
              right="-9px",
              top=output_pin_top,
              transform="translateY(-50%)",
              z_index="15",
              style={
                  "display": "flex",
                  "align_items": "center",
                  "justify_content": "center",
              },
              class_name="output-pin-bubble",
              cursor="pointer",
              custom_attrs={
                  "data-pin-gate": cell_key,
                  "data-pin-type": "output",
                  "data-offset-y": output_pin_offset_attr,
              },
              on_click=State.select_pin_output(cell_key),
          ),
      ),
      rx.cond(
          is_ff,
          rx.box(
              rx.box(
                  width="8px",
                  height="8px",
                  border_radius="50%",
                  border=rx.cond(
                      is_source_bar, "2px solid #b91c1c", "2px solid #0f172a"
                  ),
                  bg=rx.cond(is_source_bar, "#ef4444", "#ffffff"),
                  box_shadow=rx.cond(
                      is_source_bar, "0 0 8px #ef4444", "none"
                  ),
                  _hover={
                      "bg": "#ef4444",
                      "transform": "scale(1.8)",
                      "border-color": "#b91c1c",
                  },
                  transition="all 0.15s ease",
              ),
              width="18px",
              height="18px",
              position="absolute",
              right="-9px",
              top=ff_output_pin_bottom,
              transform="translateY(-50%)",
              z_index="15",
              style={
                  "display": "flex",
                  "align_items": "center",
                  "justify_content": "center",
              },
              class_name="output-pin-bubble",
              cursor="pointer",
              custom_attrs={
                  "data-pin-gate": cell_key + ":q_bar",
                  "data-pin-type": "output",
                  "data-offset-y": ff_bottom_offset_attr,
              },
              on_click=State.select_pin_output(cell_key + ":q_bar"),
          ),
          rx.fragment(),
      ),
      class_name="schematic-gate-card",
      custom_attrs={"data-gate-id": cell_key, "data-gate-type": g_type},
      position="absolute",
      left=g_data["x"].to_string() + "px",
      top=g_data["y"].to_string() + "px",
      width=rx.cond(
          is_seven_seg,
          "110px",
          rx.cond(g_type == "CLK", "110px", "86px"),
      ),
      height=card_height,
      z_index="10",
      background_color="rgba(255, 255, 255, 0.01)",
      border=rx.cond(is_selected, "1.5px dashed #2563eb", "none"),
      border_radius="4px",
      box_shadow="none",
      cursor=rx.cond(State.is_delete_mode, "crosshair", "grab"),
      user_select="none",
      style={"pointerEvents": "auto"},
  )


def render_wire_path(w: rx.Var) -> rx.Component:
  return rx.el.svg.g(
      rx.cond(
          w["is_branched"] == "true",
          rx.el.svg.circle(
              cx=w["junc_x"],
              cy=w["src_y"],
              r="3.5",
              fill="#0f172a",
              style={"pointerEvents": "none"},
          ),
      ),
      rx.el.svg.path(
          d=w["d"],
          stroke="rgba(0,0,0,0.001)",
          stroke_width="14",
          fill="none",
          cursor=rx.cond(State.is_delete_mode, "crosshair", "move"),
          class_name="wire-drag-segment",
          style={"pointerEvents": "stroke"},
          custom_attrs={
              "data-wire-id": w["wire_id"],
              "data-src-key": w["src_key"],
              "data-target-key": w["target_key"],
              "data-slot": w["slot"],
              "data-offset-y": w["offset_y"],
              "data-mid-x": w["mid_x"],
              "data-src-x": w["src_x"],
              "data-src-y": w["src_y"],
              "data-dst-x": w["dst_x"],
              "data-dst-y": w["dst_y"],
          },
          on_click=State.delete_wire(w["target_key"], w["slot"]),
          _hover={"stroke": "rgba(37, 99, 235, 0.4)"},
      ),
      rx.el.svg.path(
          d=w["d"],
          stroke=w["color"],
          stroke_width="2.5",
          fill="none",
          stroke_linecap="round",
          class_name="wire-visible-line",
          style={"pointerEvents": "none"},
      ),
  )


# =============================================================================
# 4. WORKBENCH & SIDEBAR
# =============================================================================
def index() -> rx.Component:
  def sidebar_symbol_tile(gate_name: rx.Var):
    is_selected = State.selected_gate_type == gate_name

    return rx.el.div(
        rx.box(
            rx.text("+", font_size="11px", font_weight="bold", color="#ffffff"),
            title="Quick Spawn",
            position="absolute",
            top="4px",
            right="4px",
            width="18px",
            height="18px",
            border_radius="4px",
            bg="#2563eb",
            style={
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
            },
            on_click=State.add_gate_at_default_location(gate_name),
            _hover={"bg": "#1d4ed8", "transform": "scale(1.15)"},
            z_index="2",
        ),
        rx.vstack(
            rx.center(
                rx.box(
                    render_schematic_symbol(
                        gate_name,
                        False,
                        "",
                        "",
                        "manual",
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        "0",
                    ),
                    style={
                        "transform": "scale(0.8)",
                        "transform_origin": "center",
                    },
                ),
                height="36px",
                width="100%",
            ),
            rx.text(
                gate_name,
                font_size="10px",
                font_weight="black",
                color=rx.cond(is_selected, "#1e40af", "#475569"),
            ),
            spacing="1",
            align_items="center",
        ),
        position="relative",
        style={
            "width": "47%",
            "padding": "6px 0px 8px 0px",
            "cursor": "grab",
            "overflow": "hidden",
            "border-radius": "8px",
            "background": rx.cond(is_selected, "#dbeafe", "#ffffff"),
            "border": rx.cond(
                is_selected, "2px solid #2563eb", "1px solid #cbd5e1"
            ),
        },
        on_click=State.set_selected_type(gate_name),
        on_double_click=State.add_gate_at_default_location(gate_name),
        _hover={"border-color": "#3b82f6", "background": "#f1f5f9"},
        custom_attrs={
            "draggable": "true",
            "data-gate-type": gate_name,
            "ondragstart": (
                "event.dataTransfer.clearData();"
                "event.dataTransfer.setData('application/x-circuit-gate',"
                " event.currentTarget.getAttribute('data-gate-type'));"
                "event.dataTransfer.effectAllowed='copy';"
            ),
        },
    )

  return rx.flex(
      rx.html("""
          <style>
              #logic-workspace[data-delete-mode="true"],
              #logic-workspace[data-delete-mode="true"] *,
              #logic-workspace[data-delete-mode="true"] *:hover,
              #logic-workspace[data-delete-mode="true"] *:active {
                  cursor: crosshair !important;
              }
          </style>
      """),
      rx.button(
          id="drop-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              "window.__getDroppedGate ? window.__getDroppedGate() : null",
              callback=State.drop_gate_at_location,
          ),
      ),
      rx.button(
          id="drag-end-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              "window.__getDragEndData ? window.__getDragEndData() : null",
              callback=State.handle_gate_drag_end,
          ),
      ),
      rx.button(
          id="wire-drag-end-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              (
                  "window.__getWireDragEndData ? window.__getWireDragEndData()"
                  " : null"
              ),
              callback=State.handle_wire_drag_end,
          ),
      ),
      rx.button(
          id="delete-gate-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              (
                  "window.__getDeleteGateData ? window.__getDeleteGateData() :"
                  " null"
              ),
              callback=State.delete_gate_by_key,
          ),
      ),
      rx.button(
          id="select-gate-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              (
                  "window.__getSelectGateData ? window.__getSelectGateData() :"
                  " null"
              ),
              callback=State.select_gate_by_key,
          ),
      ),
      rx.button(
          id="toggle-input-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              (
                  "window.__getToggleInputData ? window.__getToggleInputData()"
                  " : null"
              ),
              callback=State.toggle_input_by_key,
          ),
      ),
      rx.button(
          id="clock-tick-key-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              "window.__getClockTickKey ? window.__getClockTickKey() : null",
              callback=State.tick_clock_by_key,
          ),
      ),
      rx.button(
          id="cancel-action-trigger-btn",
          style={"display": "none"},
          on_click=State.cancel_active_actions,
      ),
      rx.button(
          id="undo-trigger-btn",
          style={"display": "none"},
          on_click=State.undo,
      ),
      rx.button(
          id="redo-trigger-btn",
          style={"display": "none"},
          on_click=State.redo,
      ),
      rx.button(
          id="import-json-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              "window.__getImportedProjectData ? window.__getImportedProjectData() : null",
              callback=State.import_project_data,
          ),
      ),
      # Hidden file input for loading project JSON files
      rx.el.input(
          type="file",
          id="project-file-input",
          accept=".json",
          style={"display": "none"},
          on_change=rx.call_script(
              """
              (event) => {
                  const file = event.target.files[0];
                  if (!file) return;
                  const reader = new FileReader();
                  reader.onload = (e) => {
                      try {
                          window.__importedProjectJson = JSON.parse(e.target.result);
                          const btn = document.getElementById("import-json-trigger-btn");
                          if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                      } catch (err) {
                          alert("Invalid project JSON file.");
                      }
                  };
                  reader.readAsText(file);
                  event.target.value = '';
              }
              """,
          ),
      ),
      rx.box(
          rx.vstack(
              rx.hstack(
                  rx.vstack(
                      rx.text(
                          "CircuitLab Pro",
                          font_weight="black",
                          font_size="16px",
                          color="#0f172a",
                      ),
                      rx.text(
                          "Sequential & Combinational",
                          font_size="9px",
                          color="#64748b",
                          margin_top="-6px",
                      ),
                      spacing="0",
                  ),
                  rx.box(flex="1"),
                  rx.hstack(
                      rx.icon_button(
                          rx.icon(tag="type", size=15),
                          color_scheme=rx.cond(
                              State.is_text_placement_mode, "blue", "gray"
                          ),
                          variant=rx.cond(
                              State.is_text_placement_mode, "solid", "ghost"
                          ),
                          size="1",
                          on_click=State.toggle_text_placement_mode,
                          cursor="pointer",
                          title="Place Text",
                      ),
                      rx.icon_button(
                          rx.icon(tag="trash-2", size=15),
                          color_scheme=rx.cond(
                              State.is_delete_mode, "red", "gray"
                          ),
                          variant=rx.cond(
                              State.is_delete_mode, "solid", "ghost"
                          ),
                          size="1",
                          on_click=State.toggle_delete_mode,
                          cursor="pointer",
                          title="Toggle Delete Mode (X)",
                      ),
                      rx.icon_button(
                          rx.icon(tag="rotate-ccw", size=15),
                          color_scheme="red",
                          variant="ghost",
                          size="1",
                          on_click=State.clear_canvas,
                          cursor="pointer",
                          title="Clear Canvas",
                      ),
                      spacing="1",
                  ),
                  align_items="center",
                  width="100%",
              ),
              rx.divider(color="#e2e8f0"),
              # Project Save/Load & Truth Table Actions
              rx.vstack(
                  rx.text(
                      "Project & Analysis",
                      font_size="10px",
                      font_weight="black",
                      color="#1e293b",
                  ),
                  rx.vstack(
                      rx.text(
                          "Register to Save",
                          font_size="9px",
                          font_weight="800",
                          color="#475569",
                      ),
                      rx.hstack(
                          rx.el.input(
                              value=State.registration_email,
                              on_change=State.set_registration_email,
                              placeholder="you@example.com",
                              type="email",
                              autocomplete="email",
                              style={
                                  "width": "100%",
                                  "height": "28px",
                                  "font_size": "10px",
                                  "border": "1px solid #cbd5e1",
                                  "border_radius": "5px",
                                  "padding": "0 7px",
                                  "outline": "none",
                                  "background": "#ffffff",
                              },
                          ),
                          rx.button(
                              rx.cond(State.is_registered, "Registered", "Register"),
                              size="1",
                              color_scheme=rx.cond(
                                  State.is_registered, "green", "blue"
                              ),
                              variant=rx.cond(
                                  State.is_registered, "soft", "solid"
                              ),
                              on_click=State.register_email,
                              cursor="pointer",
                              min_width="72px",
                          ),
                          width="100%",
                          spacing="1",
                      ),
                      rx.cond(
                          State.registration_error != "",
                          rx.text(
                              State.registration_error,
                              font_size="9px",
                              color="#dc2626",
                          ),
                          rx.cond(
                              State.is_registered,
                              rx.text(
                                  "Registered: " + State.registered_email,
                                  font_size="9px",
                                  color="#15803d",
                              ),
                              rx.fragment(),
                          ),
                      ),
                      width="100%",
                      spacing="1",
                  ),
                  rx.hstack(
                      rx.button(
                          "Save Project",
                          size="1",
                          color_scheme=rx.cond(
                              State.is_registered, "blue", "gray"
                          ),
                          variant="soft",
                          cursor=rx.cond(
                              State.is_registered, "pointer", "not-allowed"
                          ),
                          disabled=~State.is_registered,
                          title=rx.cond(
                              State.is_registered,
                              "Save circuit project",
                              "Register a valid email before saving",
                          ),
                          width="48%",
                          on_click=rx.call_script(
                              f"""
                              const data = {{
                                  gates: {State.gates.to(str)},
                                  gate_keys: {State.gate_keys.to(str)},
                                  wire_offsets: {State.wire_offsets.to(str)},
                                  annotations: {State.annotations.to(str)},
                                  annotation_keys: {State.annotation_keys.to(str)},
                                  saved_by_email: {State.registered_email.to(str)}
                              }};
                              const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
                              const url = URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = url;
                              a.download = 'circuit_project.json';
                              a.click();
                              URL.revokeObjectURL(url);
                              """
                          ),
                      ),
                      rx.button(
                          "Load",
                          size="1",
                          color_scheme="blue",
                          variant="soft",
                          cursor="pointer",
                          width="48%",
                          on_click=rx.call_script(
                              "document.getElementById('project-file-input').click();"
                          ),
                      ),
                      width="100%",
                      justify="between",
                  ),
                  rx.button(
                      "Generate Truth Table",
                      size="1",
                      color_scheme="purple",
                      variant="solid",
                      cursor="pointer",
                      width="100%",
                      margin_top="4px",
                      on_click=State.toggle_truth_table,
                  ),
                  width="100%",
                  spacing="1",
              ),
              rx.divider(color="#e2e8f0"),
              rx.vstack(
                  rx.text(
                      "Inputs & Outputs",
                      font_size="10px",
                      font_weight="black",
                      color="#1e293b",
                  ),
                  rx.el.select(
                      rx.el.option("-- Select Input / Output --", value=""),
                      rx.el.option("Input (INPUT)", value="INPUT"),
                      rx.el.option("Output (OUTPUT)", value="OUTPUT"),
                      rx.el.option("Clock (CLK)", value="CLK"),
                      rx.el.option(
                          "7-Segment Display (SEVEN_SEG)", value="SEVEN_SEG"
                      ),
                      value=State.selected_io_menu,
                      on_change=State.set_selected_io_menu,
                      style={
                          "font_size": "10px",
                          "font_weight": "bold",
                          "color": "#0f172a",
                          "background": "#ffffff",
                          "border": "1px solid #cbd5e1",
                          "border_radius": "4px",
                          "padding": "6px",
                          "outline": "none",
                          "width": "100%",
                          "cursor": "pointer",
                      },
                  ),
                  width="100%",
                  spacing="1",
              ),
              rx.vstack(
                  rx.text(
                      "Flip-Flops (Sequential)",
                      font_size="10px",
                      font_weight="black",
                      color="#1e293b",
                  ),
                  rx.el.select(
                      rx.el.option("-- Select Flip-Flop --", value=""),
                      rx.el.option("D Flip-Flop (D_FF)", value="D_FF"),
                      rx.el.option("RS Flip-Flop (RS_FF)", value="RS_FF"),
                      rx.el.option("JK Flip-Flop (JK_FF)", value="JK_FF"),
                      rx.el.option("T Flip-Flop (T_FF)", value="T_FF"),
                      value=State.selected_ff_menu,
                      on_change=State.set_selected_ff_menu,
                      style={
                          "font_size": "10px",
                          "font_weight": "bold",
                          "color": "#1e40af",
                          "background": "#ffffff",
                          "border": "1.5px solid #cbd5e1",
                          "border_radius": "4px",
                          "padding": "6px",
                          "outline": "none",
                          "width": "100%",
                          "cursor": "pointer",
                      },
                  ),
                  width="100%",
                  spacing="1",
              ),
              rx.divider(color="#e2e8f0"),
              rx.flex(
                  rx.foreach(State.active_gate_options, sidebar_symbol_tile),
                  width="100%",
                  flex_wrap="wrap",
                  justify="between",
                  style={"gap": "10px 0px"},
              ),
              rx.box(flex="1"),
              width="100%",
              height="100%",
              spacing="3",
          ),
          width="260px",
          height="100vh",
          padding="16px",
          bg="#ffffff",
          border_right="2px solid #e2e8f0",
          style={"overflow-y": "auto"},
      ),
      rx.box(
          rx.box(
              rx.el.svg(
                  rx.el.svg.path(
                      id="live-wire-preview",
                      d="",
                      stroke="#ef4444",
                      stroke_width="2.5",
                      stroke_dasharray="4 4",
                      fill="none",
                      style={"display": "none", "pointerEvents": "none"},
                  ),
                  rx.foreach(State.wires_list, render_wire_path),
                  id="logic-svg-layer",
                  style={
                      "position": "absolute",
                      "top": 0,
                      "left": 0,
                      "width": "10000px",
                      "height": "10000px",
                      "pointerEvents": "auto",
                      "zIndex": 5,
                  },
              ),
              rx.foreach(State.gate_keys, schematic_gate_node),
              rx.foreach(State.annotation_keys, annotation_node),
              rx.box(
                  rx.vstack(
                      rx.icon(tag="trash-2", size=20, color="#ef4444"),
                      rx.text(
                          "DROP TO DELETE",
                          font_size="9px",
                          font_weight="extrabold",
                          color="#b91c1c",
                      ),
                      spacing="1",
                      align_items="center",
                  ),
                  id="canvas-delete-zone",
                  position="absolute",
                  bottom="20px",
                  right="20px",
                  width="130px",
                  height="80px",
                  border="2px dashed #f87171",
                  border_radius="10px",
                  bg="rgba(254, 226, 226, 0.85)",
                  box_shadow="0 8px 12px -2px rgba(239, 68, 68, 0.2)",
                  style={
                      "display": "flex",
                      "align_items": "center",
                      "justify_content": "center",
                      "zIndex": "20",
                  },
              ),
              id="logic-viewport",
              style={
                  "position": "absolute",
                  "top": 0,
                  "left": 0,
                  "width": "10000px",
                  "height": "10000px",
                  "transform": f"translate({State.pan_x}px, {State.pan_y}px)",
                  "transformOrigin": "0 0",
              },
          ),
          on_context_menu=State.cancel_active_actions,
          on_click=rx.call_script(
              "window.__calcCanvasClick ? window.__calcCanvasClick() : null",
              callback=State.handle_canvas_click,
          ),
          on_mouse_up=rx.call_script(
              "window.__getPanData ? window.__getPanData() : null",
              callback=State.handle_pan_end,
          ),
          id="logic-workspace",
          custom_attrs={
              "data-selected-gate": State.selected_gate_type,
              "data-wiring-source": State.wiring_source,
              "data-delete-mode": State.is_delete_mode.to_string(),
              "data-text-placement": State.is_text_placement_mode.to_string(),
              "data-pan-x": State.pan_x,
              "data-pan-y": State.pan_y,
          },
          style={
              "position": "relative",
              "flex": "1",
              "height": "100vh",
              "backgroundColor": "#f8fafc",
              "backgroundImage": (
                  "linear-gradient(#e2e8f0 1px, transparent 1px),"
                  " linear-gradient(90deg, #e2e8f0 1px, transparent 1px)"
              ),
              "backgroundSize": "20px 20px",
              "overflow": "hidden",
              "userSelect": "none",
              "cursor": rx.cond(
                  State.is_delete_mode,
                  "crosshair",
                  rx.cond(State.is_text_placement_mode, "text", "default"),
              ),
          },
      ),
      # Truth Table Modal Dialog
      rx.cond(
          State.is_truth_table_open,
          rx.box(
              rx.box(
                  rx.vstack(
                      rx.hstack(
                          rx.text(
                              "Circuit Truth Table",
                              font_weight="bold",
                              font_size="16px",
                              color="#0f172a",
                          ),
                          rx.spacer(),
                          rx.button(
                              "✕",
                              on_click=State.toggle_truth_table,
                              variant="ghost",
                              size="1",
                              cursor="pointer",
                          ),
                          width="100%",
                          align_items="center",
                      ),
                      rx.divider(),
                      rx.box(
                          rx.el.table(
                              rx.foreach(
                                  State.truth_table_rows,
                                  lambda row: rx.el.tr(
                                      rx.foreach(
                                          row,
                                          lambda k, v: rx.el.td(
                                              v,
                                              style={
                                                  "padding": "6px 12px",
                                                  "border": "1px solid #cbd5e1",
                                                  "text_align": "center",
                                              },
                                          ),
                                      )
                                  ),
                              ),
                              style={
                                  "width": "100%",
                                  "border_collapse": "collapse",
                                  "font_size": "12px",
                              },
                          ),
                          style={
                              "max_height": "300px",
                              "overflow_y": "auto",
                              "width": "100%",
                          },
                      ),
                      spacing="3",
                      width="100%",
                  ),
                  bg="white",
                  padding="20px",
                  border_radius="10px",
                  box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1)",
                  width="400px",
                  max_width="90vw",
              ),
              position="fixed",
              top="0",
              left="0",
              width="100vw",
              height="100vh",
              bg="rgba(0,0,0,0.4)",
              style={
                  "display": "flex",
                  "align_items": "center",
                  "justify_content": "center",
                  "zIndex": "1000",
              },
          ),
      ),
      rx.script("""
            (() => {
                if (window.__logicInitialized && window.__logicListenersBound) return;
                window.__logicInitialized = true;
                window.__logicListenersBound = true;

                const GRID_SIZE = 20, GATE_WIDTH = 86;
                window.__isPanning = false; window.__draggedGate = null; window.__draggedWire = null;
                
                // Per-clock runtime. clock_interval is the FULL period,
                // so the square wave toggles every period / 2.
                window.__clockRuntime = {};

                window.__getImportedProjectData = () => { const r = window.__importedProjectJson; window.__importedProjectJson = null; return r; };

                if (window.__autoClockInterval) clearInterval(window.__autoClockInterval);
                window.__autoClockInterval = setInterval(() => {
                    if (window.__draggedGate || window.__draggedWire || window.__isPanning) return;

                    const now = performance.now();
                    const liveClockIds = new Set();
                    const clockCards = document.querySelectorAll('.schematic-gate-card[data-gate-type="CLK"]');

                    clockCards.forEach(card => {
                        const gateId = card.getAttribute('data-gate-id');
                        if (!gateId) return;
                        liveClockIds.add(gateId);

                        const sel = card.querySelector('select');
                        const inputField = card.querySelector('input[type="text"]');
                        const isAuto = !!(sel && sel.value === 'auto');

                        let periodSec = parseFloat(inputField ? inputField.value : '1');
                        if (!Number.isFinite(periodSec)) periodSec = 1.0;
                        periodSec = Math.max(0.5, Math.min(99.0, periodSec));

                        if (!isAuto) {
                            delete window.__clockRuntime[gateId];
                            return;
                        }

                        const halfPeriodMs = (periodSec * 1000) / 2;
                        let runtime = window.__clockRuntime[gateId];

                        if (!runtime || Math.abs(runtime.periodSec - periodSec) > 0.0001) {
                            window.__clockRuntime[gateId] = {
                                periodSec: periodSec,
                                lastToggleMs: now
                            };
                            return;
                        }

                        if (now - runtime.lastToggleMs >= halfPeriodMs) {
                            runtime.lastToggleMs = now;
                            window.__pendingClockTickKey = gateId;
                            const btn = document.getElementById("clock-tick-key-btn");
                            if (btn) {
                                btn.dispatchEvent(new MouseEvent('click', {
                                    bubbles: true,
                                    cancelable: true
                                }));
                            }
                        }
                    });

                    Object.keys(window.__clockRuntime).forEach(gateId => {
                        if (!liveClockIds.has(gateId)) {
                            delete window.__clockRuntime[gateId];
                        }
                    });
                }, 50);

                function getOrthogonalPath(srcX, srcY, dstX, dstY, customMidX) {
                    const midX = customMidX !== undefined ? customMidX : (srcX + (dstX - srcX) / 2);
                    if (Math.abs(srcY - dstY) <= 4 && dstX >= srcX + 16 && customMidX === undefined) {
                        return `M ${srcX} ${srcY} L ${dstX} ${dstY}`;
                    } else if (dstX >= srcX + 16) {
                        return `M ${srcX} ${srcY} L ${midX} ${srcY} L ${midX} ${dstY} L ${dstX} ${dstY}`;
                    } else {
                        const xOut = srcX + 16, xIn = dstX - 16, midY = (srcY + dstY) / 2;
                        return `M ${srcX} ${srcY} L ${xOut} ${srcY} L ${xOut} ${midY} L ${xIn} ${midY} L ${xIn} ${dstY} L ${dstX} ${dstY}`;
                    }
                }
                function getGateCoordinates(el) {
                    if (!el) return { x: 140, y: 80 };
                    const styleX = parseFloat(el.style.left), styleY = parseFloat(el.style.top);
                    if (!isNaN(styleX) && !isNaN(styleY)) return { x: styleX, y: styleY };
                    const vp = document.getElementById("logic-viewport"), vpRect = vp.getBoundingClientRect(), elRect = el.getBoundingClientRect();
                    return { x: Math.round((elRect.left - vpRect.left) / GRID_SIZE) * GRID_SIZE, y: Math.round((elRect.top - vpRect.top) / GRID_SIZE) * GRID_SIZE };
                }
                function updateAttachedWiresLive(gateId, newX, newY) {
                    document.querySelectorAll('#logic-svg-layer g').forEach(g => {
                        const pathHitbox = g.querySelector('path[data-src-key], path[data-target-key]');
                        if (!pathHitbox) return;
                        const srcKey = pathHitbox.getAttribute('data-src-key'), targetKey = pathHitbox.getAttribute('data-target-key'), offsetY = parseFloat(pathHitbox.getAttribute('data-offset-y')) || 30;
                        let srcX, srcY, dstX, dstY;
                        if (srcKey.startsWith(gateId)) {
                            const baseSrcKey = srcKey.includes(':') ? srcKey.split(':')[0] : srcKey;
                            const isQBar = srcKey.includes('q_bar');
                            const srcEl = document.querySelector(`[data-gate-id="${baseSrcKey}"]`);
                            if (!srcEl) return;
                            const gateType = srcEl.getAttribute('data-gate-type');
                            let srcPinY = 30;
                            if (gateType === 'D_FF' || gateType === 'T_FF') srcPinY = isQBar ? 45 : 18;
                            else if (gateType === 'RS_FF' || gateType === 'JK_FF') srcPinY = isQBar ? 48 : 18;
                            else if (gateType === 'SEVEN_SEG') srcPinY = 30;
                            else {
                                const outputBubble = srcEl.querySelector('.output-pin-bubble');
                                if (outputBubble) {
                                    const attr = outputBubble.getAttribute('data-offset-y');
                                    if (attr) srcPinY = parseFloat(attr);
                                }
                            }
                            const compWidth = gateType === 'SEVEN_SEG' ? 110 : (gateType === 'CLK' ? 110 : 86);
                            srcX = newX + compWidth + 9;
                            srcY = newY + srcPinY;
                            const targetEl = document.querySelector(`[data-gate-id="${targetKey}"]`);
                            if (!targetEl) return;
                            const pos = getGateCoordinates(targetEl);
                            dstX = pos.x - 9; dstY = pos.y + offsetY;
                        } else if (targetKey === gateId) {
                            dstX = newX - 9; dstY = newY + offsetY;
                            const srcEl = document.querySelector(`[data-gate-id="${srcKey.split(':')[0]}"]`);
                            if (!srcEl) return;
                            const gateType = srcEl.getAttribute('data-gate-type');
                            const isQBar = srcKey.includes('q_bar');
                            let srcPinY = 30;
                            if (gateType === 'D_FF' || gateType === 'T_FF') srcPinY = isQBar ? 45 : 18;
                            else if (gateType === 'RS_FF' || gateType === 'JK_FF') srcPinY = isQBar ? 48 : 18;
                            else if (gateType === 'SEVEN_SEG') srcPinY = 30;
                            else {
                                const outputBubble = srcEl.querySelector('.output-pin-bubble');
                                if (outputBubble) {
                                    const attr = outputBubble.getAttribute('data-offset-y');
                                    if (attr) srcPinY = parseFloat(attr);
                                }
                            }
                            const pos = getGateCoordinates(srcEl);
                            const compWidth = gateType === 'SEVEN_SEG' ? 110 : (gateType === 'CLK' ? 110 : 86);
                            srcX = pos.x + compWidth + 9; srcY = pos.y + srcPinY;
                        } else { return; }
                        const newPathStr = getOrthogonalPath(srcX, srcY, dstX, dstY);
                        g.querySelectorAll('path').forEach(p => p.setAttribute('d', newPathStr));
                    });
                }
                function dispatchProxyClick(btnId) {
                    const btn = document.getElementById(btnId);
                    if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                }

                function setupWorkspaceDrop() {
                    const ws = document.getElementById("logic-workspace");
                    if (ws) {
                        const allowedGateTypes = new Set([
                            "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
                            "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
                            "D_FF", "T_FF", "RS_FF", "JK_FF"
                        ]);

                        ws.ondragover = e => {
                            const types = Array.from(e.dataTransfer.types || []);
                            if (types.includes("application/x-circuit-gate")) {
                                e.preventDefault();
                                e.dataTransfer.dropEffect = "copy";
                            }
                        };

                        ws.ondrop = e => {
                            const gateType = e.dataTransfer.getData(
                                "application/x-circuit-gate"
                            );
                            if (!allowedGateTypes.has(gateType)) {
                                return;
                            }

                            e.preventDefault();
                            e.stopPropagation();

                            const rect = ws.getBoundingClientRect();
                            const panX = parseFloat(
                                ws.getAttribute("data-pan-x")
                            ) || 0;
                            const panY = parseFloat(
                                ws.getAttribute("data-pan-y")
                            ) || 0;
                            const rawX = e.clientX - rect.left - panX;
                            const rawY = e.clientY - rect.top - panY;
                            const snapX = Math.max(
                                40,
                                Math.round(
                                    (rawX - (GATE_WIDTH / 2)) / GRID_SIZE
                                ) * GRID_SIZE
                            );
                            const snapY = Math.max(
                                20,
                                Math.round(
                                    (rawY - 30) / GRID_SIZE
                                ) * GRID_SIZE
                            );
                            const dropBtn = document.getElementById(
                                "drop-trigger-btn"
                            );
                            if (dropBtn) {
                                dropBtn.setAttribute("data-type", gateType);
                                dropBtn.setAttribute("data-x", snapX);
                                dropBtn.setAttribute("data-y", snapY);
                                dispatchProxyClick("drop-trigger-btn");
                            }
                        };
                    }
                }
                setupWorkspaceDrop();
                setTimeout(setupWorkspaceDrop, 100);

                window.__getDroppedGate = () => {
                    const btn = document.getElementById("drop-trigger-btn"); if (!btn) return null;
                    const type = btn.getAttribute("data-type"), x = parseInt(btn.getAttribute("data-x")), y = parseInt(btn.getAttribute("data-y"));
                    return (!type || isNaN(x) || isNaN(y)) ? null : { type, x, y };
                };
                window.__getDragEndData = () => {
                    const btn = document.getElementById("drag-end-trigger-btn"); if (!btn) return null;
                    const key = btn.getAttribute("data-key"), x = parseInt(btn.getAttribute("data-x")), y = parseInt(btn.getAttribute("data-y"));
                    return (!key || isNaN(x) || isNaN(y)) ? null : { key, x, y };
                };
                window.__getWireDragEndData = () => { const r = window.__pendingWireDragEnd; window.__pendingWireDragEnd = null; return r; };
                window.__getDeleteGateData = () => { const r = window.__pendingDeleteGate; window.__pendingDeleteGate = null; return r; };
                window.__getToggleInputData = () => { const r = window.__pendingToggleInput; window.__pendingToggleInput = null; return r; };
                window.__getSelectGateData = () => { const r = window.__pendingSelectGate; window.__pendingSelectGate = null; return r; };
                window.__getClockTickKey = () => { const r = window.__pendingClockTickKey; window.__pendingClockTickKey = null; return r; };

                const onKeyDown = e => {
                    const ws = document.getElementById("logic-workspace");
                    const activeEl = document.activeElement, isTyping = activeEl && (activeEl.tagName === "INPUT" || activeEl.tagName === "TEXTAREA" || activeEl.tagName === "SELECT") && !activeEl.readOnly;
                    if (e.code === "Space" && !e.repeat && !isTyping) { window.__logicSpaceDown = true; if (ws) ws.style.cursor = ws.getAttribute("data-delete-mode") === "true" ? "crosshair" : "grab"; }
                    if (isTyping) return;
                    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); dispatchProxyClick(e.shiftKey ? "redo-trigger-btn" : "undo-trigger-btn"); }
                    else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') { e.preventDefault(); dispatchProxyClick("redo-trigger-btn"); }
                    else if (e.key.toLowerCase() === 'x') { const btn = document.querySelector('button[title*="Delete Mode"]'); if (btn) btn.click(); }
                    if (e.key === "Escape") { const p = document.getElementById("live-wire-preview"); if (p) p.style.display = "none"; dispatchProxyClick("cancel-action-trigger-btn"); }
                };
                const onKeyUp = e => { 
                    const ws = document.getElementById("logic-workspace");
                    if (e.code === "Space") { window.__logicSpaceDown = false; if (ws) ws.style.cursor = ws.getAttribute("data-delete-mode") === "true" ? "crosshair" : "default"; } 
                };

                const onPointerDown = e => {
                    const ws = document.getElementById("logic-workspace");
                    if (!ws || !ws.contains(e.target)) return;
                    window.__lastClientX = e.clientX; window.__lastClientY = e.clientY; window.__wasDraggingGate = false;
                    
                    const wireSegment = e.target.closest('.wire-drag-segment');
                    const pinBubble = e.target.closest('.input-pin-bubble, .output-pin-bubble');
                    const isDeleteMode = ws.getAttribute("data-delete-mode") === "true";

                    if (wireSegment && !isDeleteMode) {
                        window.__draggedWire = { wire_id: wireSegment.getAttribute('data-wire-id'), element: wireSegment, startX: e.clientX, baseMidX: parseFloat(wireSegment.getAttribute('data-mid-x')) || 0, srcX: parseFloat(wireSegment.getAttribute('data-src-x')) || 0, srcY: parseFloat(wireSegment.getAttribute('data-src-y')) || 0, dstX: parseFloat(wireSegment.getAttribute('data-dst-x')) || 0, dstY: parseFloat(wireSegment.getAttribute('data-dst-y')) || 0, offsetDx: 0 };
                        return;
                    }
                    if (pinBubble) return;

                    let gateCard = e.target.closest('[data-gate-id]');
                    if (isDeleteMode && gateCard) {
                        window.__pendingDeleteGate = { key: gateCard.getAttribute('data-gate-id') }; dispatchProxyClick("delete-gate-trigger-btn"); return;
                    }
                    if (e.target.closest('.input-label-field') || e.target.tagName === 'SELECT' || (e.target.tagName === 'INPUT' && !e.target.readOnly)) return;
                    
                    const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
                    if (e.button === 1 || (e.button === 0 && window.__logicSpaceDown === true) || !gateCard) {
                        window.__isPanning = true; window.__startMouseX = e.clientX; window.__startMouseY = e.clientY; window.__startPanX = wsPanX; window.__startPanY = wsPanY; ws.style.cursor = isDeleteMode ? "crosshair" : "grabbing"; return;
                    }
                    if (gateCard && e.button === 0) {
                        e.preventDefault();
                        const gateId = gateCard.getAttribute('data-gate-id');
                        window.__selectedGateKey = gateId;
                        const rect = ws.getBoundingClientRect(), mouseWorldX = (e.clientX - rect.left) - wsPanX, mouseWorldY = (e.clientY - rect.top) - wsPanY, pos = getGateCoordinates(gateCard);
                        window.__draggedGate = { id: gateId, pointerId: e.pointerId, startX: mouseWorldX, startY: mouseWorldY, startClientX: e.clientX, startClientY: e.clientY, origX: pos.x, origY: pos.y, worldX: pos.x, worldY: pos.y };
                        gateCard.style.zIndex = "100"; gateCard.style.cursor = isDeleteMode ? "crosshair" : "grabbing";
                    }
                };

                const onPointerMove = e => {
                    const ws = document.getElementById("logic-workspace");
                    const vp = document.getElementById("logic-viewport");
                    if (window.__draggedWire) {
                        const dx = e.clientX - window.__draggedWire.startX; window.__draggedWire.offsetDx = Math.round(dx / GRID_SIZE) * GRID_SIZE;
                        const newMidX = window.__draggedWire.baseMidX + dx, group = window.__draggedWire.element.closest('g');
                        if (group) {
                            const livePath = getOrthogonalPath(window.__draggedWire.srcX, window.__draggedWire.srcY, window.__draggedWire.dstX, window.__draggedWire.dstY, newMidX);
                            group.querySelectorAll('path').forEach(p => p.setAttribute('d', livePath));
                        }
                        return;
                    }
                    if (window.__draggedGate && ws) {
                        const rawDx = Math.abs(e.clientX - window.__draggedGate.startClientX);
                        const rawDy = Math.abs(e.clientY - window.__draggedGate.startClientY);
                        if (rawDx + rawDy > 4) window.__wasDraggingGate = true;

                        const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
                        const rect = ws.getBoundingClientRect(), mouseWorldX = (e.clientX - rect.left) - wsPanX, mouseWorldY = (e.clientY - rect.top) - wsPanY;
                        
                        const dx = mouseWorldX - window.__draggedGate.startX;
                        const dy = mouseWorldY - window.__draggedGate.startY;
                        
                        let newX = Math.round((window.__draggedGate.origX + dx) / GRID_SIZE) * GRID_SIZE;
                        let newY = Math.round((window.__draggedGate.origY + dy) / GRID_SIZE) * GRID_SIZE;
                        newX = Math.max(40, newX); newY = Math.max(20, newY);
                        window.__draggedGate.worldX = newX; window.__draggedGate.worldY = newY;
                        
                        const gateEl = document.querySelector(`[data-gate-id="${window.__draggedGate.id}"]`);
                        if (gateEl) {
                            gateEl.style.left = `${newX}px`; gateEl.style.top = `${newY}px`;
                        }
                        updateAttachedWiresLive(window.__draggedGate.id, newX, newY);
                        return;
                    }
                    const stateSource = ws ? ws.getAttribute("data-wiring-source") : null, previewPath = document.getElementById("live-wire-preview");
                    if (stateSource && previewPath && ws) {
                        const baseSrcKey = stateSource.includes(':') ? stateSource.split(':')[0] : stateSource;
                        const srcEl = document.querySelector(`[data-gate-id="${baseSrcKey}"]`);
                        if (srcEl) {
                            const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
                            const rect = ws.getBoundingClientRect(), mouseWorldX = (e.clientX - rect.left) - wsPanX, mouseWorldY = (e.clientY - rect.top) - wsPanY;
                            const pos = getGateCoordinates(srcEl);
                            const gateType = srcEl.getAttribute('data-gate-type');
                            const isQBar = stateSource.includes('q_bar');
                            let pinOffset = 30;
                            const gateWidth = gateType === 'SEVEN_SEG' ? 110 : (gateType === 'CLK' ? 110 : 86);
                            if (gateType === 'D_FF' || gateType === 'T_FF') pinOffset = isQBar ? 45 : 18;
                            else if (gateType === 'RS_FF' || gateType === 'JK_FF') pinOffset = isQBar ? 48 : 18;
                            else if (gateType === 'SEVEN_SEG') pinOffset = 30;
                            else {
                                const outputBubble = srcEl.querySelector('.output-pin-bubble');
                                if (outputBubble) {
                                    const attr = outputBubble.getAttribute('data-offset-y');
                                    if (attr) pinOffset = parseFloat(attr);
                                }
                            }
                            previewPath.setAttribute('d', getOrthogonalPath(pos.x + gateWidth + 9, pos.y + pinOffset, mouseWorldX, mouseWorldY));
                            previewPath.style.display = "block";
                        }
                    } else if (previewPath) { previewPath.style.display = "none"; }
                    if (window.__isPanning && vp && ws) {
                        const curPanX = window.__startPanX + (e.clientX - window.__startMouseX), curPanY = window.__startPanY + (e.clientY - window.__startMouseY);
                        vp.style.transform = `translate(${curPanX}px, ${curPanY}px)`;
                        ws.style.backgroundPosition = `${curPanX}px ${curPanY}px`;
                        window.__currentPanX = curPanX; window.__currentPanY = curPanY; window.__wasPanning = true;
                    }
                };

                const onPointerUp = e => {
                    const ws = document.getElementById("logic-workspace");
                    const isDeleteMode = ws ? ws.getAttribute("data-delete-mode") === "true" : false;
                    if (window.__draggedWire) {
                        if (window.__draggedWire.offsetDx !== 0) {
                            window.__pendingWireDragEnd = { wire_id: window.__draggedWire.wire_id, offset_dx: window.__draggedWire.offsetDx };
                            dispatchProxyClick("wire-drag-end-trigger-btn");
                        }
                        window.__draggedWire = null; return;
                    }
                    if (window.__draggedGate) {
                        const gateEl = document.querySelector(`[data-gate-id="${window.__draggedGate.id}"]`);
                        if (gateEl) {
                            gateEl.style.zIndex = "10"; gateEl.style.cursor = isDeleteMode ? "crosshair" : "grab";
                        }
                        const deleteZone = document.getElementById("canvas-delete-zone");
                        let droppedInDelete = false;
                        if (deleteZone && gateEl) {
                            const dzRect = deleteZone.getBoundingClientRect(), gateRect = gateEl.getBoundingClientRect();
                            droppedInDelete = !(dzRect.right < gateRect.left || dzRect.left > gateRect.right || dzRect.bottom < gateRect.top || dzRect.bottom > gateRect.bottom);
                        }
                        if (droppedInDelete) {
                            window.__pendingDeleteGate = { key: window.__draggedGate.id }; window.__draggedGate = null; dispatchProxyClick("delete-gate-trigger-btn"); return;
                        }
                        const gateId = window.__draggedGate.id, gateType = gateEl ? gateEl.getAttribute("data-gate-type") : "";
                        if (window.__wasDraggingGate) {
                            const dragEndBtn = document.getElementById("drag-end-trigger-btn");
                            if (dragEndBtn) { dragEndBtn.setAttribute("data-key", gateId); dragEndBtn.setAttribute("data-x", window.__draggedGate.worldX); dragEndBtn.setAttribute("data-y", window.__draggedGate.worldY); dispatchProxyClick("drag-end-trigger-btn"); }
                        } else {
                            if (gateType === "INPUT" || gateType === "CLK") { window.__pendingToggleInput = { key: gateId }; dispatchProxyClick("toggle-input-trigger-btn"); }
                            else { window.__pendingSelectGate = { key: gateId }; dispatchProxyClick("select-gate-trigger-btn"); }
                        }
                        window.__draggedGate = null;
                    }
                    if (window.__isPanning) {
                        window.__isPanning = false; if (ws) ws.style.cursor = isDeleteMode ? "crosshair" : "default";
                        if (window.__wasPanning) {
                            window.__pendingPanData = { panX: window.__currentPanX, panY: window.__currentPanY };
                        }
                    }
                };

                document.addEventListener("keydown", onKeyDown); 
                document.addEventListener("keyup", onKeyUp);
                document.addEventListener("pointerdown", onPointerDown); 
                document.addEventListener("pointermove", onPointerMove); 
                document.addEventListener("pointerup", onPointerUp);

                window.__calcCanvasClick = () => {
                    const ws = document.getElementById("logic-workspace");
                    if (window.__wasPanning) { window.__wasPanning = false; return null; }
                    if (!ws) return null;
                    const hit = document.elementFromPoint(window.__lastClientX, window.__lastClientY);
                    if (hit && hit.closest('.canvas-text-box, .schematic-gate-card, textarea, .input-label-field, select, input, button, .input-pin-bubble, .output-pin-bubble')) return null;
                    const rect = ws.getBoundingClientRect(), panX = parseFloat(ws.getAttribute("data-pan-x")) || 0, panY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
                    const rawX = window.__lastClientX - rect.left - panX, rawY = window.__lastClientY - rect.top - panY;
                    return {
                        x: Math.max(40, Math.round((rawX - (GATE_WIDTH / 2)) / GRID_SIZE) * GRID_SIZE),
                        y: Math.max(20, Math.round((rawY - 30) / GRID_SIZE) * GRID_SIZE),
                        text_x: Math.max(20, Math.round(rawX / GRID_SIZE) * GRID_SIZE),
                        text_y: Math.max(20, Math.round(rawY / GRID_SIZE) * GRID_SIZE)
                    };
                };
                window.__getPanData = () => { const r = window.__pendingPanData; window.__pendingPanData = null; return r; };
            })();
        """),
      direction="row",
      width="100vw",
      height="100vh",
  )


app = rx.App()
app.add_page(index)