BOOLNEXA SPRINT 6.6.5 — UNIVERSAL-GATE CONNECTION INTEGRITY

Permanent changes
-----------------
1. Real logic-gate input/output straight-run invariant is now >=10 px.
   INPUT, OUTPUT and CONSTANT presentation pins remain exempt.

2. NAND/NOR inverter structures are explicitly regression-tested as two-input
   physical gates:
       NAND(X, X)
       NOR(X, X)

3. Both target_input=0 and target_input=1 must exist as separate graph wires.

4. Layout must terminate those two wires at two different physical input
   coordinates, with an independent >=10 px horizontal terminal run.

Important
---------
The circuit engine already creates two Wire objects for a two-input NAND/NOR,
even when both sources are the same node. This sprint therefore does not alter
the Boolean graph builder or technology mapper. It strengthens layout geometry
and adds regression protection around the physical connection invariant.

No renderer artwork or generated pictures are involved.

Files
-----
REPLACE:
  digital_logic_lab/circuit_layout.py

ADD:
  tests/test_universal_gate_connection_integrity.py
  README_SPRINT_6_6_5.txt
