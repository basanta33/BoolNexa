BOOLNEXA SPRINT 6.6.2 — GATE PORT ROUTING INVARIANTS

Permanent rule
--------------
Every REAL LOGIC GATE must have a horizontal straight wire run of at least
6 pixels:
  - immediately after its output;
  - immediately before each of its inputs.

Exempt
------
Primary INPUT pins, OUTPUT pins and CONSTANT presentation sources.

Preserved rules
---------------
- orthogonal routing only;
- wires never route through other gate bodies;
- existing 14 px obstacle clearance remains;
- wires may cross;
- crossings are not electrical junctions;
- junction dots remain graph fan-out only.

Why this is implemented in layout
---------------------------------
The general router remains an obstacle-aware Manhattan router. The layout
layer knows which endpoints are real gates, so it reserves mandatory port
stubs and asks the router to connect the ends of those stubs. This makes the
6 px rule structural rather than a visual patch.

Files
-----
REPLACE:
  digital_logic_lab/circuit_router.py
  digital_logic_lab/circuit_layout.py

ADD:
  tests/test_gate_port_invariants.py

The regression suite covers normal basic logic, XOR preferred, expanded
basic XOR, NAND-only and NOR-only circuits.
