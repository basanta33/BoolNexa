BOOLNEXA SPRINT 6.4.3 — OBSTACLE-AWARE CIRCUIT ROUTING

Rules enforced:
1. AND/OR/XOR/NAND/NOR/XNOR retain separate input pins.
2. NOT remains single-input.
3. No wire is allowed through an unrelated gate body.
4. Wires may cross other wires.
5. Wire crossings are NOT electrical connections.
6. Electrical connectivity is defined only by the circuit graph.
7. Fan-out junction dots continue to be drawn only for actual shared sources.

Files:
  digital_logic_lab/circuit_router.py
  digital_logic_lab/circuit_layout.py
  tests/test_circuit_obstacle_routing.py

The validated Boolean/circuit engine and professional SVG gate renderer are not replaced.
