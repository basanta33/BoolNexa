BOOLNEXA SPRINT 6.6.1 — CIRCUIT GENERATOR REALIZATION CONTROLS

Updates
-------
digital_logic_lab/circuit_visual_model.py
digital_logic_lab/circuit_svg_renderer.py
digital_logic_lab/logic_circuit_lab.py

Adds
----
tests/test_circuit_realization_ui_backend.py

UI modes
--------
Auto
Basic
XOR Preferred
NAND Only
NOR Only

The UI now uses the unified realization strategy rather than calling the
plain circuit builder directly.

The renderer also gains:
  render_circuit_graph_svg(graph)

This is important because a realized NAND/NOR/basic circuit may no longer
match the original expression tree. The UI therefore renders the mapped
CircuitGraph directly.

The realization summary shows:
- selected mode
- gates used
- preferred gates used
- strict realization
- gate counts
- total gates
- logic depth

No route change is required. Existing URL remains:
  /tools/circuit
