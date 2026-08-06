BOOLNEXA SPRINT 6.6.6 FIX — POLARITY-AWARE NAND MAPPING

Why the previous version produced 8 NAND gates
----------------------------------------------
It first built positive AND outputs and then converted OR using additional
inverters. For SOP expressions this destroys the natural NAND-NAND form.

New method
----------
The mapper can realize either:
  F
or:
  F'

for every subexpression.

This allows:
  AB + AC'

to map directly as:

  N1 = NAND(A,B)      = (AB)'
  N2 = NAND(C,C)      = C'
  N3 = NAND(A,N2)     = (AC')'
  N4 = NAND(N1,N3)    = AB + AC'

Exactly four NAND gates.

No changes to layout, renderer, graph models, or the 10 px routing invariant.

REPLACE:
  digital_logic_lab/nand_mapper.py

ADD:
  tests/test_nand_polarity_mapping.py
