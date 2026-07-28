# digital_logic_lab.py

import copy
import json
import re
import reflex as rx


from .logic_core import (
    MSI_LSI_DEFS,
    MSI_LSI_TYPES,
    SUPPORTED_GATE_TYPES,
    evaluate_circuit,
    get_component_input_count,
    get_component_width,
    get_input_pin_offset,
    get_input_pin_position,
    get_output_pin_offset,
    get_source_value,
)


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
  selected_msi_menu: str = ""

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
  msi_counter: int = 0
  annotation_counter: int = 0
  selected_gate_type: str = ""

  pan_x: float = 0.0
  pan_y: float = 0.0
  zoom: float = 1.0

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

    allowed_gate_types = set(SUPPORTED_GATE_TYPES)
    gates = {
        str(key): copy.deepcopy(gate)
        for key, gate in gates.items()
        if isinstance(gate, dict)
        and gate.get("type") in allowed_gate_types
    }
    gate_keys = [str(key) for key in gate_keys if str(key) in gates]
    annotation_keys = [str(key) for key in annotation_keys if str(key) in annotations]

    for gate in gates.values():
      gate_type = gate.get("type", "")
      if gate_type in MSI_LSI_DEFS:
        gate["num_inputs"] = get_component_input_count(gate_type)
        outputs = gate.get("outputs", {})
        if not isinstance(outputs, dict):
          outputs = {}
        gate["outputs"] = {
            name: int(outputs.get(name, 0))
            for name, _ in MSI_LSI_DEFS[gate_type]["outputs"]
        }
        for idx in range(1, gate["num_inputs"] + 1):
          gate.setdefault(f"input{idx}_src", "")

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

  def set_selected_msi_menu(self, block_type: str):
    if block_type:
      self.add_gate_at_default_location(block_type)
      self.selected_msi_menu = ""

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
    elif gate_type in MSI_LSI_DEFS:
      self.msi_counter += 1
      return f"{gate_type.lower()}_{self.msi_counter}"
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
    allowed_types = set(SUPPORTED_GATE_TYPES)
    if gate_type not in allowed_types:
      return
    self.push_undo_state()
    key = self.generate_node_key(gate_type)
    updated = copy.deepcopy(self.gates)
    initial_num_inputs = get_component_input_count(gate_type)

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
        "outputs": (
            {
                name: 0
                for name, _ in MSI_LSI_DEFS[gate_type]["outputs"]
            }
            if gate_type in MSI_LSI_DEFS
            else {}
        ),
    }
    for idx in range(1, max(7, initial_num_inputs + 1)):
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
    allowed_types = set(SUPPORTED_GATE_TYPES)
    if gate_type not in allowed_types:
      return
    self.push_undo_state()
    key = self.generate_node_key(gate_type)
    updated = copy.deepcopy(self.gates)
    initial_num_inputs = get_component_input_count(gate_type)

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
        "outputs": (
            {
                name: 0
                for name, _ in MSI_LSI_DEFS[gate_type]["outputs"]
            }
            if gate_type in MSI_LSI_DEFS
            else {}
        ),
    }
    for idx in range(1, max(7, initial_num_inputs + 1)):
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

    allowed_types = set(SUPPORTED_GATE_TYPES)
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

  def handle_view_change(self, data: dict):
    if not data or not isinstance(data, dict):
      return
    self.pan_x = float(data.get("panX", self.pan_x))
    self.pan_y = float(data.get("panY", self.pan_y))
    self.zoom = max(0.25, min(2.0, float(data.get("zoom", self.zoom))))

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
        max_inputs = max(6, int(gate.get("num_inputs", 0)))
        for idx in range(1, max_inputs + 1):
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
      num_in = int(
          g_data.get("num_inputs", get_component_input_count(g_type))
      )

      for idx in range(1, num_in + 1):
        slot = f"input{idx}_src"
        src_composite = g_data.get(slot, "")
        if not src_composite:
          continue

        base_src_key = (
            src_composite.split(":", 1)[0]
            if ":" in src_composite
            else src_composite
        )
        port_name = (
            src_composite.split(":", 1)[1]
            if ":" in src_composite
            else ""
        )

        if base_src_key not in self.gates:
          continue

        src_gate = self.gates[base_src_key]
        src_type = src_gate.get("type", "")
        src_pin_y_offset = get_output_pin_offset(src_type, port_name)
        src_x = src_gate["x"] + get_component_width(src_type)
        src_y = src_gate["y"] + src_pin_y_offset

        dst_side, dst_pin_x_offset, dst_pin_y_offset = get_input_pin_position(g_type, idx, num_in)
        dst_x = target_x + dst_pin_x_offset
        dst_y = target_y + dst_pin_y_offset

        wire_id = f"{src_composite}:{target_key}:{slot}"
        branch_idx = source_branch_counts.get(src_composite, 0)
        source_branch_counts[src_composite] = branch_idx + 1

        auto_stagger = 22 + (branch_idx * 20)
        user_drag_offset = self.wire_offsets.get(wire_id, 0.0)
        src_val = get_source_value(self.gates, src_composite)
        wire_color = "#ef4444" if src_val == 1 else "#64748b"

        if abs(src_y - dst_y) <= 4 and dst_x >= src_x + 16:
          path_str = f"M {src_x} {src_y} L {dst_x} {dst_y}"
          mid_x = (src_x + dst_x) / 2
        elif dst_x >= src_x + 16:
          base_mid_x = src_x + (dst_x - src_x) / 2 + auto_stagger
          mid_x = base_mid_x + user_drag_offset
          path_str = (
              f"M {src_x} {src_y} L {mid_x} {src_y} "
              f"L {mid_x} {dst_y} L {dst_x} {dst_y}"
          )
        else:
          x_out = src_x + 16 + auto_stagger + user_drag_offset
          x_in = dst_x - 16
          mid_y = (src_y + dst_y) / 2
          path_str = (
              f"M {src_x} {src_y} L {x_out} {src_y} "
              f"L {x_out} {mid_y} L {x_in} {mid_y} "
              f"L {x_in} {dst_y} L {dst_x} {dst_y}"
          )
          mid_x = x_out

        new_wires.append({
            "wire_id": wire_id,
            "src_key": src_composite,
            "target_key": target_key,
            "slot": slot,
            "d": path_str,
            "color": wire_color,
            "offset_y": str(dst_pin_y_offset),
            "offset_x": str(dst_pin_x_offset),
            "dst_side": dst_side,
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


# Basic two-input gates use pin centers at y=10 and y=30 inside the
# 40px symbol. The gate card adds the remaining vertical offset, matching
# shared logical wire anchors exactly and preventing 2px visual misalignment.
def vec_and_ieee(invert=False, num_inputs=2) -> rx.Component:
  """IEEE AND/NAND symbol sized to the selected number of inputs."""
  count = max(2, min(6, int(num_inputs)))
  height = 20 * (count + 1)
  center_y = height // 2
  body_top = 10
  body_bottom = height - 10
  radius = (body_bottom - body_top) // 2
  body_right = 30 + radius
  bubble_x = body_right + 5
  output_start = bubble_x + 4 if invert else body_right
  output_end = 86

  leads = [
      rx.el.svg.line(
          x1="0", y1=str(20 * idx), x2="16", y2=str(20 * idx),
          stroke="#0f172a", stroke_width="2.5",
      )
      for idx in range(1, count + 1)
  ]

  parts = [
      rx.el.svg.line(
          x1="16", y1=str(body_top), x2="16", y2=str(body_bottom),
          stroke="#0f172a", stroke_width="2.5",
      ),
      rx.el.svg.path(
          d=(
              f"M 16 {body_top} L 30 {body_top} "
              f"A {radius} {radius} 0 0 1 30 {body_bottom} "
              f"L 16 {body_bottom} Z"
          ),
          fill="#ffffff", stroke="#0f172a", stroke_width="2.5",
      ),
  ]

  if invert:
    parts.append(
        rx.el.svg.circle(
            cx=str(bubble_x), cy=str(center_y), r="4",
            fill="#ffffff", stroke="#0f172a", stroke_width="2.5",
        )
    )

  parts.append(
      rx.el.svg.line(
          x1=str(output_start), y1=str(center_y),
          x2=str(output_end), y2=str(center_y),
          stroke="#0f172a", stroke_width="2.5",
      )
  )

  return rx.el.svg(
      *leads,
      *parts,
      view_box=f"0 0 86 {height}",
      width="86px",
      height=f"{height}px",
      style={"pointerEvents": "none"},
  )


def vec_or_ieee(invert=False, xor=False, num_inputs=2) -> rx.Component:
  """IEEE OR/NOR/XOR/XNOR symbol sized to the selected number of inputs."""
  count = 2 if xor else max(2, min(6, int(num_inputs)))
  height = 20 * (count + 1)
  center_y = height // 2
  top = 10
  bottom = height - 10
  right = 62
  bubble_x = 66
  output_start = 70 if invert else right

  leads = [
      rx.el.svg.line(
          x1="0", y1=str(20 * idx), x2="18", y2=str(20 * idx),
          stroke="#0f172a", stroke_width="2.5",
      )
      for idx in range(1, count + 1)
  ]

  parts = []
  if xor:
    parts.append(
        rx.el.svg.path(
            d=f"M 9 {top} Q 22 {center_y} 9 {bottom}",
            fill="none", stroke="#0f172a", stroke_width="2.5",
        )
    )

  parts.extend([
      rx.el.svg.path(
          d=f"M 14 {top} Q 27 {center_y} 14 {bottom}",
          fill="none", stroke="#0f172a", stroke_width="2.5",
      ),
      rx.el.svg.path(
          d=(
              f"M 14 {top} "
              f"Q 45 {top} {right} {center_y} "
              f"Q 45 {bottom} 14 {bottom}"
          ),
          fill="#ffffff", stroke="#0f172a", stroke_width="2.5",
      ),
  ])

  if invert:
    parts.append(
        rx.el.svg.circle(
            cx=str(bubble_x), cy=str(center_y), r="4",
            fill="#ffffff", stroke="#0f172a", stroke_width="2.5",
        )
    )

  parts.append(
      rx.el.svg.line(
          x1=str(output_start), y1=str(center_y), x2="86", y2=str(center_y),
          stroke="#0f172a", stroke_width="2.5",
      )
  )

  return rx.el.svg(
      *leads,
      *parts,
      view_box=f"0 0 86 {height}",
      width="86px",
      height=f"{height}px",
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



def vec_half_adder() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="10", y="5", width="90", height="60", rx="5",
          fill="#ffffff", stroke="#0f172a", stroke_width="2",
      ),
      rx.el.svg.text(
          "HALF ADDER", x="55", y="18", text_anchor="middle",
          font_size="8px", font_weight="bold", fill="#0f172a",
      ),
      rx.el.svg.text("A", x="16", y="29", font_size="8px", font_weight="bold"),
      rx.el.svg.text("B", x="16", y="54", font_size="8px", font_weight="bold"),
      rx.el.svg.text("SUM", x="77", y="29", font_size="7px", font_weight="bold"),
      rx.el.svg.text("C", x="87", y="54", font_size="8px", font_weight="bold"),
      rx.el.svg.line(x1="0", y1="25", x2="10", y2="25", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="0", y1="50", x2="10", y2="50", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="100", y1="25", x2="120", y2="25", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="100", y1="50", x2="120", y2="50", stroke="#0f172a", stroke_width="2"),
      view_box="0 0 120 70", width="120px", height="70px",
      style={"pointerEvents": "none"},
  )


def vec_full_adder() -> rx.Component:
  return rx.el.svg(
      rx.el.svg.rect(
          x="10", y="5", width="100", height="78", rx="5",
          fill="#ffffff", stroke="#0f172a", stroke_width="2",
      ),
      rx.el.svg.text(
          "FULL ADDER", x="60", y="18", text_anchor="middle",
          font_size="8px", font_weight="bold", fill="#0f172a",
      ),
      rx.el.svg.text("A", x="16", y="27", font_size="8px", font_weight="bold"),
      rx.el.svg.text("B", x="16", y="50", font_size="8px", font_weight="bold"),
      rx.el.svg.text("Cin", x="16", y="73", font_size="7px", font_weight="bold"),
      rx.el.svg.text("SUM", x="84", y="35", font_size="7px", font_weight="bold"),
      rx.el.svg.text("Cout", x="82", y="65", font_size="7px", font_weight="bold"),
      rx.el.svg.line(x1="0", y1="22", x2="10", y2="22", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="0", y1="45", x2="10", y2="45", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="0", y1="68", x2="10", y2="68", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="110", y1="30", x2="130", y2="30", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="110", y1="60", x2="130", y2="60", stroke="#0f172a", stroke_width="2"),
      view_box="0 0 130 90", width="130px", height="90px",
      style={"pointerEvents": "none"},
  )


def vec_mux_2_1() -> rx.Component:
  # Conventional multiplexer wedge/trapezoid.
  return rx.el.svg(
      rx.el.svg.polygon(
          points="18,6 94,18 94,62 18,74",
          fill="#ffffff", stroke="#0f172a", stroke_width="2",
      ),
      rx.el.svg.text(
          "2:1 MUX", x="57", y="18", text_anchor="middle",
          font_size="8px", font_weight="bold", fill="#0f172a",
      ),
      rx.el.svg.text("I0", x="25", y="28", font_size="7px", font_weight="bold"),
      rx.el.svg.text("I1", x="25", y="54", font_size="7px", font_weight="bold"),
      rx.el.svg.text("S", x="60", y="72", text_anchor="middle", font_size="7px", font_weight="bold"),
      rx.el.svg.text("Y", x="82", y="44", font_size="8px", font_weight="bold"),
      rx.el.svg.line(x1="0", y1="22", x2="21", y2="22", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="0", y1="48", x2="21", y2="48", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="60", y1="62", x2="60", y2="80", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="94", y1="40", x2="120", y2="40", stroke="#0f172a", stroke_width="2"),
      view_box="0 0 120 80", width="120px", height="80px",
      style={"pointerEvents": "none"},
  )


def vec_demux_1_2() -> rx.Component:
  # Conventional demultiplexer wedge, widening toward its outputs.
  return rx.el.svg(
      rx.el.svg.polygon(
          points="18,18 94,6 94,74 18,62",
          fill="#ffffff", stroke="#0f172a", stroke_width="2",
      ),
      rx.el.svg.text(
          "1:2 DEMUX", x="57", y="18", text_anchor="middle",
          font_size="8px", font_weight="bold", fill="#0f172a",
      ),
      rx.el.svg.text("D", x="26", y="36", font_size="8px", font_weight="bold"),
      rx.el.svg.text("S", x="60", y="70", text_anchor="middle", font_size="7px", font_weight="bold"),
      rx.el.svg.text("Y0", x="79", y="27", font_size="7px", font_weight="bold"),
      rx.el.svg.text("Y1", x="79", y="60", font_size="7px", font_weight="bold"),
      rx.el.svg.line(x1="0", y1="30", x2="21", y2="30", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="60", y1="62", x2="60", y2="80", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="94", y1="22", x2="120", y2="22", stroke="#0f172a", stroke_width="2"),
      rx.el.svg.line(x1="94", y1="55", x2="120", y2="55", stroke="#0f172a", stroke_width="2"),
      view_box="0 0 120 80", width="120px", height="80px",
      style={"pointerEvents": "none"},
  )


def vec_functional_block(
    title: str,
    inputs: tuple[tuple[str, int], ...],
    outputs: tuple[tuple[str, int], ...],
    width: int,
    height: int,
    controls: tuple[tuple[str, int], ...] = (),
) -> rx.Component:
  """IEC-style rectangular functional block with named logical ports."""
  children: list[rx.Component] = [
      rx.el.svg.rect(
          x="18", y="5", width=str(width - 44), height=str(height - 10),
          rx="3", fill="#ffffff", stroke="#0f172a", stroke_width="2",
      ),
      rx.el.svg.text(
          title, x=str(width // 2), y="15", text_anchor="middle",
          font_size="8px", font_weight="bold", fill="#0f172a",
      ),
  ]
  for name, offset in inputs:
    children.extend([
        rx.el.svg.line(
            x1="0", y1=str(offset), x2="18", y2=str(offset),
            stroke="#0f172a", stroke_width="2",
        ),
        rx.el.svg.text(
            name, x="22", y=str(offset + 3), font_size="7px",
            font_weight="bold", fill="#0f172a",
        ),
    ])
  for name, offset_x in controls:
    children.extend([
        rx.el.svg.line(
            x1=str(offset_x), y1=str(height - 5), x2=str(offset_x), y2=str(height),
            stroke="#0f172a", stroke_width="2",
        ),
        rx.el.svg.text(
            name, x=str(offset_x), y=str(height - 10), text_anchor="middle",
            font_size="7px", font_weight="bold", fill="#0f172a",
        ),
    ])
  for name, offset in outputs:
    children.extend([
        rx.el.svg.line(
            x1=str(width - 26), y1=str(offset), x2=str(width), y2=str(offset),
            stroke="#0f172a", stroke_width="2",
        ),
        rx.el.svg.text(
            name, x=str(width - 31), y=str(offset + 3), text_anchor="end",
            font_size="7px", font_weight="bold", fill="#0f172a",
        ),
    ])
  return rx.el.svg(
      *children, view_box=f"0 0 {width} {height}",
      width=f"{width}px", height=f"{height}px",
      style={"pointerEvents": "none"},
  )


def vec_mux_4_1() -> rx.Component:
  return vec_functional_block(
      "4:1 MUX",
      (("I0", 18), ("I1", 36), ("I2", 54), ("I3", 72)),
      (("Y", 54),), 130, 120, (("S0", 50), ("S1", 80)),
  )


def vec_demux_1_4() -> rx.Component:
  return vec_functional_block(
      "1:4 DEMUX", (("D", 30),),
      (("Y0", 18), ("Y1", 42), ("Y2", 66), ("Y3", 90)), 130, 110, (("S0", 50), ("S1", 80)),
  )


def vec_decoder_2_4() -> rx.Component:
  return vec_functional_block(
      "2→4 DEC", (),
      (("Y0", 18), ("Y1", 38), ("Y2", 58), ("Y3", 78)), 130, 96, (("A0", 50), ("A1", 80)),
  )


def vec_encoder_4_2() -> rx.Component:
  return vec_functional_block(
      "4→2 ENC", (("D0", 18), ("D1", 38), ("D2", 58), ("D3", 78)),
      (("A0", 34), ("A1", 64)), 130, 96,
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
    num_inputs=2,
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
                      gate_type == "HALF_ADDER",
                      vec_half_adder(),
                      rx.cond(
                          gate_type == "FULL_ADDER",
                          vec_full_adder(),
                          rx.cond(
                              gate_type == "MUX_2_1",
                              vec_mux_2_1(),
                              rx.cond(
                                  gate_type == "DEMUX_1_2",
                                  vec_demux_1_2(),
                                  rx.cond(
                                      gate_type == "MUX_4_1",
                                      vec_mux_4_1(),
                                      rx.cond(
                                          gate_type == "DEMUX_1_4",
                                          vec_demux_1_4(),
                                          rx.cond(
                                              gate_type == "DECODER_2_4",
                                              vec_decoder_2_4(),
                                              rx.cond(
                                                  gate_type == "ENCODER_4_2",
                                                  vec_encoder_4_2(),
                                                  rx.cond(
                                                      gate_type == "NOT",
                                                      vec_not_ieee(),
                      rx.cond(
                          gate_type == "AND",
                              rx.cond(
                                   num_inputs == 6, vec_and_ieee(False, 6),
                                   rx.cond(
                                       num_inputs == 5, vec_and_ieee(False, 5),
                                       rx.cond(
                                           num_inputs == 4, vec_and_ieee(False, 4),
                                           rx.cond(
                                               num_inputs == 3, vec_and_ieee(False, 3),
                                               vec_and_ieee(False, 2),
                                           ),
                                       ),
                                   ),
                               ),
                              rx.cond(
                                  gate_type == "NAND",
                                  rx.cond(
                                   num_inputs == 6, vec_and_ieee(True, 6),
                                   rx.cond(
                                       num_inputs == 5, vec_and_ieee(True, 5),
                                       rx.cond(
                                           num_inputs == 4, vec_and_ieee(True, 4),
                                           rx.cond(
                                               num_inputs == 3, vec_and_ieee(True, 3),
                                               vec_and_ieee(True, 2),
                                           ),
                                       ),
                                   ),
                               ),
                                  rx.cond(
                                      gate_type == "OR",
                                      rx.cond(
                                   num_inputs == 6, vec_or_ieee(False, False, 6),
                                   rx.cond(
                                       num_inputs == 5, vec_or_ieee(False, False, 5),
                                       rx.cond(
                                           num_inputs == 4, vec_or_ieee(False, False, 4),
                                           rx.cond(
                                               num_inputs == 3, vec_or_ieee(False, False, 3),
                                               vec_or_ieee(False, False, 2),
                                           ),
                                       ),
                                   ),
                               ),
                                      rx.cond(
                                          gate_type == "NOR",
                                          rx.cond(
                                   num_inputs == 6, vec_or_ieee(True, False, 6),
                                   rx.cond(
                                       num_inputs == 5, vec_or_ieee(True, False, 5),
                                       rx.cond(
                                           num_inputs == 4, vec_or_ieee(True, False, 4),
                                           rx.cond(
                                               num_inputs == 3, vec_or_ieee(True, False, 3),
                                               vec_or_ieee(True, False, 2),
                                           ),
                                       ),
                                   ),
                               ),
                                          rx.cond(
                                              gate_type == "XOR",
                                              vec_or_ieee(False, True, 2),
                                              rx.cond(
                                                  gate_type == "XNOR",
                                                  vec_or_ieee(True, True, 2),
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
          class_name="terminal-dot",
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


def render_bottom_input_pin(
    cell_key: rx.Var, idx: int, offset_x: int, offset_y: int
) -> rx.Component:
  slot_name = f"input{idx}_src"
  return rx.box(
      rx.box(
          width="8px", height="8px", border_radius="50%", bg="#0f172a",
          border="2px solid #ffffff",
          _hover={"bg": "#ef4444", "transform": "scale(1.8)", "border-color": "#b91c1c"},
          transition="all 0.15s ease",
          class_name="terminal-dot",
      ),
      width="18px", height="18px", position="absolute",
      left=f"{offset_x}px", top=f"{offset_y}px",
      transform="translate(-50%, -50%)", z_index="15",
      style={"display": "flex", "align_items": "center", "justify_content": "center"},
      class_name="input-pin-bubble bottom-input-pin", cursor="pointer",
      custom_attrs={
          "data-pin-gate": cell_key, "data-pin-slot": slot_name,
          "data-offset-x": str(offset_x), "data-offset-y": str(offset_y),
          "data-pin-side": "bottom",
      },
      on_click=State.connect_or_disconnect_input(cell_key, slot_name),
  )


def render_named_output_pin(
    cell_key: rx.Var, port_name: str, offset_y: int
) -> rx.Component:
  composite_key = cell_key + ":" + port_name
  is_selected = State.wiring_source == composite_key
  return rx.box(
      rx.box(
          width="8px",
          height="8px",
          border_radius="50%",
          border=rx.cond(
              is_selected, "2px solid #b91c1c", "2px solid #0f172a"
          ),
          bg=rx.cond(is_selected, "#ef4444", "#ffffff"),
          box_shadow=rx.cond(is_selected, "0 0 8px #ef4444", "none"),
          _hover={
              "bg": "#ef4444",
              "transform": "scale(1.8)",
              "border-color": "#b91c1c",
          },
          transition="all 0.15s ease",
          class_name="terminal-dot",
      ),
      width="18px",
      height="18px",
      position="absolute",
      right="-9px",
      top=f"{offset_y}px",
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
          "data-pin-gate": composite_key,
          "data-pin-type": "output",
          "data-output-port": port_name,
          "data-offset-y": str(offset_y),
      },
      on_click=State.select_pin_output(composite_key),
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
  is_half_adder = g_type == "HALF_ADDER"
  is_full_adder = g_type == "FULL_ADDER"
  is_mux_2_1 = g_type == "MUX_2_1"
  is_demux_1_2 = g_type == "DEMUX_1_2"
  is_mux_4_1 = g_type == "MUX_4_1"
  is_demux_1_4 = g_type == "DEMUX_1_4"
  is_decoder_2_4 = g_type == "DECODER_2_4"
  is_encoder_4_2 = g_type == "ENCODER_4_2"
  is_msi_lsi = (
      is_half_adder | is_full_adder | is_mux_2_1 | is_demux_1_2
      | is_mux_4_1 | is_demux_1_4 | is_decoder_2_4 | is_encoder_4_2
  )
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
      is_half_adder, "70px",
      rx.cond(
          is_full_adder, "90px",
          rx.cond(
              is_mux_4_1, "120px",
              rx.cond(
                  is_demux_1_4, "110px",
                  rx.cond(
                      is_decoder_2_4 | is_encoder_4_2, "96px",
                      rx.cond(
                          is_mux_2_1 | is_demux_1_2, "80px",
                          rx.cond(
                              g_type == "CLK", "90px",
                              rx.cond(
                                  is_seven_seg, "100px",
                                  rx.cond(
                                      (g_type == "RS_FF") | (g_type == "JK_FF"), "70px",
                                      rx.cond(
                                          (g_type == "D_FF") | (g_type == "T_FF"), "66px",
                                          rx.cond(
                                              num_inputs == 3, "80px",
                                              rx.cond(
                                                  num_inputs == 4, "100px",
                                                  rx.cond(
                                                      num_inputs == 5, "120px",
                                                      rx.cond(num_inputs == 6, "140px", "60px"),
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
      is_half_adder, render_input_pin_item(cell_key, 1, 25),
      rx.cond(
          is_full_adder | is_mux_2_1, render_input_pin_item(cell_key, 1, 22),
          rx.cond(
              is_demux_1_2 | is_demux_1_4, render_input_pin_item(cell_key, 1, 30),
              rx.cond(
                  is_mux_4_1 | is_encoder_4_2, render_input_pin_item(cell_key, 1, 18),
                  rx.cond(
                      is_decoder_2_4, rx.fragment(),
                      rx.cond(
                          (g_type == "NOT") | is_output, render_input_pin_item(cell_key, 1, 30),
                          rx.cond(
                              is_seven_seg, render_input_pin_item(cell_key, 1, 20),
                              rx.cond(
                                  (g_type == "D_FF") | (g_type == "T_FF"), render_input_pin_item(cell_key, 1, 15),
                                  rx.cond(
                                      (g_type == "RS_FF") | (g_type == "JK_FF"), render_input_pin_item(cell_key, 1, 15),
                                      render_input_pin_item(cell_key, 1, 20),
                                  ),
                              ),
                          ),
                      ),
                  ),
              ),
          ),
      ),
  )

  pin2 = rx.cond(
      is_half_adder, render_input_pin_item(cell_key, 2, 50),
      rx.cond(
          is_full_adder, render_input_pin_item(cell_key, 2, 45),
          rx.cond(
              is_mux_2_1, render_input_pin_item(cell_key, 2, 48),
              rx.cond(
                  is_demux_1_2, rx.fragment(),
                  rx.cond(
                      is_mux_4_1, render_input_pin_item(cell_key, 2, 36),
                      rx.cond(
                          is_demux_1_4, rx.fragment(),
                          rx.cond(
                              is_decoder_2_4, rx.fragment(),
                              rx.cond(
                                  is_encoder_4_2, render_input_pin_item(cell_key, 2, 38),
                                  rx.cond(
                                      is_seven_seg, render_input_pin_item(cell_key, 2, 40),
                                      rx.cond(
                                          (g_type == "D_FF") | (g_type == "T_FF"), render_input_pin_item(cell_key, 2, 45),
                                          rx.cond(
                                              (g_type == "RS_FF") | (g_type == "JK_FF"), render_input_pin_item(cell_key, 2, 33),
                                              rx.cond(
                                                  ((num_inputs != 1) & (~is_output) & (~is_input) & ((g_type != "NOT") & (g_type != "XOR") & (g_type != "XNOR"))),
                                                  render_input_pin_item(cell_key, 2, 40), rx.fragment(),
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

  pin3 = rx.cond(
      is_full_adder, render_input_pin_item(cell_key, 3, 68),
      rx.cond(
          is_mux_4_1, render_input_pin_item(cell_key, 3, 54),
          rx.cond(
              is_demux_1_4, rx.fragment(),
              rx.cond(
                  is_encoder_4_2, render_input_pin_item(cell_key, 3, 58),
                  rx.cond(
                      is_seven_seg, render_input_pin_item(cell_key, 3, 60),
                      rx.cond(
                          (g_type == "RS_FF") | (g_type == "JK_FF"), render_input_pin_item(cell_key, 3, 51),
                          rx.cond(
                              ((num_inputs == 3) | (num_inputs == 4) | (num_inputs == 5) | (num_inputs == 6))
                              & (~is_output) & (~is_input) & (~is_msi_lsi),
                              render_input_pin_item(cell_key, 3, 60), rx.fragment(),
                          ),
                      ),
                  ),
              ),
          ),
      ),
  )

  pin4 = rx.cond(
      is_mux_4_1, render_input_pin_item(cell_key, 4, 72),
      rx.cond(
          is_encoder_4_2, render_input_pin_item(cell_key, 4, 78),
          rx.cond(
              is_seven_seg, render_input_pin_item(cell_key, 4, 80),
              rx.cond(
                  ((num_inputs == 4) | (num_inputs == 5) | (num_inputs == 6))
                  & (~is_output) & (~is_input) & (~is_msi_lsi),
                  render_input_pin_item(cell_key, 4, 80), rx.fragment(),
              ),
          ),
      ),
  )
  pin5 = rx.cond(
      is_mux_4_1, rx.fragment(),
      rx.cond(
          ((num_inputs == 5) | (num_inputs == 6)) & (~is_output) & (~is_input) & (~is_msi_lsi),
          render_input_pin_item(cell_key, 5, 100), rx.fragment(),
      ),
  )
  pin6 = rx.cond(
      is_mux_4_1, rx.fragment(),
      rx.cond(
          (num_inputs == 6) & (~is_output) & (~is_input) & (~is_msi_lsi),
          render_input_pin_item(cell_key, 6, 120), rx.fragment(),
      ),
  )

  return rx.box(
      rx.cond(
          is_selected
          & (~is_input)
          & (~is_output)
          & (~is_seven_seg)
          & (~is_msi_lsi),
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
              num_inputs,
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
          is_mux_2_1, render_bottom_input_pin(cell_key, 3, 60, 89),
          rx.cond(
              is_demux_1_2, render_bottom_input_pin(cell_key, 2, 60, 89),
              rx.cond(
                  is_mux_4_1, rx.fragment(
                      render_bottom_input_pin(cell_key, 5, 50, 129),
                      render_bottom_input_pin(cell_key, 6, 80, 129),
                  ),
                  rx.cond(
                      is_demux_1_4, rx.fragment(
                          render_bottom_input_pin(cell_key, 2, 50, 119),
                          render_bottom_input_pin(cell_key, 3, 80, 119),
                      ),
                      rx.cond(
                          is_decoder_2_4, rx.fragment(
                              render_bottom_input_pin(cell_key, 1, 50, 105),
                              render_bottom_input_pin(cell_key, 2, 80, 105),
                          ),
                          rx.fragment(),
                      ),
                  ),
              ),
          ),
      ),
      rx.cond(
          (~is_output) & (~is_seven_seg) & (~is_msi_lsi),
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
                  class_name="terminal-dot",
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
          is_half_adder,
          rx.fragment(
              render_named_output_pin(cell_key, "SUM", 25),
              render_named_output_pin(cell_key, "CARRY", 50),
          ),
          rx.cond(
              is_full_adder,
              rx.fragment(
                  render_named_output_pin(cell_key, "SUM", 30),
                  render_named_output_pin(cell_key, "COUT", 60),
              ),
              rx.cond(
                  is_mux_2_1, render_named_output_pin(cell_key, "Y", 40),
                  rx.cond(
                      is_demux_1_2,
                      rx.fragment(
                          render_named_output_pin(cell_key, "Y0", 22),
                          render_named_output_pin(cell_key, "Y1", 55),
                      ),
                      rx.cond(
                          is_mux_4_1, render_named_output_pin(cell_key, "Y", 54),
                          rx.cond(
                              is_demux_1_4,
                              rx.fragment(
                                  render_named_output_pin(cell_key, "Y0", 18),
                                  render_named_output_pin(cell_key, "Y1", 42),
                                  render_named_output_pin(cell_key, "Y2", 66),
                                  render_named_output_pin(cell_key, "Y3", 90),
                              ),
                              rx.cond(
                                  is_decoder_2_4,
                                  rx.fragment(
                                      render_named_output_pin(cell_key, "Y0", 18),
                                      render_named_output_pin(cell_key, "Y1", 38),
                                      render_named_output_pin(cell_key, "Y2", 58),
                                      render_named_output_pin(cell_key, "Y3", 78),
                                  ),
                                  rx.cond(
                                      is_encoder_4_2,
                                      rx.fragment(
                                          render_named_output_pin(cell_key, "A0", 34),
                                          render_named_output_pin(cell_key, "A1", 64),
                                      ),
                                      rx.fragment(),
                                  ),
                              ),
                          ),
                      ),
                  ),
              ),
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
                  class_name="terminal-dot",
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
          is_half_adder,
          "120px",
          rx.cond(
              is_full_adder,
              "130px",
              rx.cond(
                  is_mux_4_1 | is_demux_1_4 | is_decoder_2_4 | is_encoder_4_2,
                  "130px",
                  rx.cond(
                      is_mux_2_1 | is_demux_1_2,
                      "120px",
                      rx.cond(
                          is_seven_seg,
                          "110px",
                          rx.cond(g_type == "CLK", "110px", "86px"),
                      ),
                  ),
              ),
          ),
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
              "data-offset-x": w["offset_x"],
              "data-dst-side": w["dst_side"],
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

              .input-pin-bubble.connected-terminal > .terminal-dot,
              .output-pin-bubble.connected-terminal > .terminal-dot {
                  opacity: 0 !important;
                  transform: scale(1) !important;
              }
              .input-pin-bubble.connected-terminal:hover > .terminal-dot,
              .output-pin-bubble.connected-terminal:hover > .terminal-dot {
                  opacity: 0.32 !important;
              }

              .output-pin-bubble.wiring-source-active > .terminal-dot {
                  opacity: 1 !important;
                  background: #ef4444 !important;
                  border-color: #b91c1c !important;
                  transform: scale(1.35) !important;
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
          id="view-change-trigger-btn",
          style={"display": "none"},
          on_click=rx.call_script(
              "window.__getViewChangeData ? window.__getViewChangeData() : null",
              callback=State.handle_view_change,
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
              rx.vstack(
                  rx.text(
                      "MSI / LSI (Functional Blocks)",
                      font_size="10px",
                      font_weight="black",
                      color="#1e293b",
                  ),
                  rx.el.select(
                      rx.el.option("-- Select MSI / LSI Block --", value=""),
                      rx.el.option("Half Adder", value="HALF_ADDER"),
                      rx.el.option("Full Adder", value="FULL_ADDER"),
                      rx.el.option("2:1 Multiplexer", value="MUX_2_1"),
                      rx.el.option("1:2 Demultiplexer", value="DEMUX_1_2"),
                      rx.el.option("4:1 Multiplexer", value="MUX_4_1"),
                      rx.el.option("1:4 Demultiplexer", value="DEMUX_1_4"),
                      rx.el.option("2→4 Decoder", value="DECODER_2_4"),
                      rx.el.option("4→2 Encoder", value="ENCODER_4_2"),
                      value=State.selected_msi_menu,
                      on_change=State.set_selected_msi_menu,
                      style={
                          "font_size": "10px",
                          "font_weight": "bold",
                          "color": "#7c3aed",
                          "background": "#ffffff",
                          "border": "1.5px solid #c4b5fd",
                          "border_radius": "4px",
                          "padding": "6px",
                          "outline": "none",
                          "width": "100%",
                          "cursor": "pointer",
                      },
                  ),
                  rx.text(
                      "All pins are wireable; Full Adders can cascade COUT → CIN.",
                      font_size="8px",
                      color="#64748b",
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
                  "transform": f"translate({State.pan_x}px, {State.pan_y}px) scale({State.zoom})",
                  "transformOrigin": "0 0",
              },
          ),
          rx.hstack(
              rx.button("−", size="1", variant="soft", on_click=rx.call_script("window.__logicZoom ? window.__logicZoom(-0.1) : null", callback=State.handle_view_change), title="Zoom Out"),
              rx.button("100%", size="1", variant="ghost", on_click=rx.call_script("window.__logicResetZoom ? window.__logicResetZoom() : null", callback=State.handle_view_change), title="Reset to 100%"),
              rx.button("+", size="1", variant="soft", on_click=rx.call_script("window.__logicZoom ? window.__logicZoom(0.1) : null", callback=State.handle_view_change), title="Zoom In"),
              rx.button("Fit", size="1", variant="soft", on_click=rx.call_script("window.__logicFit ? window.__logicFit() : null", callback=State.handle_view_change), title="Fit Circuit"),
              position="absolute", top="14px", right="18px", z_index="50",
              padding="6px", border="1px solid #cbd5e1", border_radius="8px",
              bg="rgba(255,255,255,0.94)", box_shadow="0 2px 8px rgba(15,23,42,0.12)", spacing="1",
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
              "data-zoom": State.zoom,
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
      rx.box(
          id="logic-interaction-bootstrap",
          width="0px",
          height="0px",
          overflow="hidden",
          on_mount=rx.call_script(
              """
              (() => {
                  const tryReady = () => {
                      if (window.__logicEnsureReady) {
                          window.__logicEnsureReady();
                          return true;
                      }
                      return false;
                  };
                  if (!tryReady()) {
                      [50, 100, 250, 500, 1000, 2000].forEach(ms => {
                          setTimeout(tryReady, ms);
                      });
                  }
              })();
              """
          ),
      ),
      direction="row",
      width="100vw",
      height="100vh",
  )


app = rx.App(
    head_components=[
        rx.script(src="/logic_interactions.js"),
    ],
)
app.add_page(index)