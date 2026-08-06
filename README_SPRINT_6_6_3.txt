BOOLNEXA SPRINT 6.6.3 — SHAPE-AWARE GATE PORTS

Purpose
-------
Fix geometry only. Boolean synthesis and circuit logic are NOT changed.

Permanent geometry rules
------------------------
1. Every real gate retains the >=6 px horizontal straight-run rule.
2. AND/NAND inputs terminate on the flat left gate boundary.
3. OR/NOR/XOR/XNOR inputs terminate on the actual rendered curved rear boundary,
   rather than the rectangular node bounding box.
4. NAND/NOR/XNOR output coordinates account for the visible inversion bubble.
5. INPUT/OUTPUT presentation pins remain exempt from the 6 px gate rule.
6. Existing obstacle clearance, orthogonal routing and crossing rules remain.

Implementation
--------------
circuit_layout.py now calculates OR-family input intersections using the same
cubic Bezier geometry used by circuit_svg_renderer.py.

circuit_svg_renderer.py aligns fan-out junction placement with the corrected
visible output point for inverted-output gates.

circuit_visual_model.py is included unchanged as a complete replacement copy
for sprint consistency.

Files
-----
REPLACE:
  digital_logic_lab/circuit_layout.py
  digital_logic_lab/circuit_svg_renderer.py
  digital_logic_lab/circuit_visual_model.py

ADD:
  tests/test_shape_aware_gate_ports.py
