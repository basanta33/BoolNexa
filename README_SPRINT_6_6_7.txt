BOOLNEXA SPRINT 6.6.7 — UNIFORM BOOLEAN SIGNAL LABELS

Purpose
-------
Fix visible notation only. Circuit logic, NAND mapping, layout, routing,
10 px gate-port spacing, and gate geometry remain unchanged.

Problem
-------
Technology-mapped Node.display() strings use NAND/NOR technology operators.
Those strings were being placed directly on circuit wires, causing labels
such as arrow-based NAND expressions.

New visible notation
--------------------
NAND(A,B)       -> (AB)'
NAND(C,C)       -> C'
NAND(A,C')      -> (AC')'

For F = AB + AC':

  N1 output -> (AB)'
  N2 output -> C'
  N3 output -> (AC')'
  Final wire -> AB + AC'

For F = A + BC':

  inverter output -> C'
  product NAND    -> (BC')'
  A inverter      -> A'
  Final wire      -> A + BC'

The final wire always shows the original Boolean function entered by the user.

REPLACE:
  digital_logic_lab/circuit_visual_model.py

ADD:
  tests/test_circuit_signal_labels.py
  README_SPRINT_6_6_7.txt
