BOOLNEXA SPRINT 6.6.6 — NAND LOGIC REPAIR

Exact verified realization for F = AB + AC':

N1 = NAND(A,B)       = (AB)'
N2 = NAND(C,C)       = C'
N3 = NAND(A,N2)      = (AC')'
N4 = NAND(N1,N3)     = AB + AC'

No layout or renderer changes.
The 10 px gate-port rule remains intact.

A second expression, A + BC', is included for independent simulator testing.

REPLACE:
  digital_logic_lab/nand_mapper.py

ADD:
  tests/test_nand_logic_repair.py
  README_SPRINT_6_6_6.txt
