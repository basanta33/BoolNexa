BOOLNEXA LABEL ORDER FIX

Cause
-----
The NAND mapper was sorting actual gate inputs by Python object id in order to
canonicalize commutative NAND gates.

That made visible signal labels nondeterministic. Depending on object ids:
  (AB)' could appear as (BA)'
  (AC')' could appear as (C'A)'
  (BC')' could appear as (C'B)'

This explains why a one-off command could show the correct labels while pytest
in another process could fail.

Fix
---
The NAND cache key remains order-independent, but the actual Node preserves the
left/right order of the first logical construction.

No logic, gate count, routing, renderer, or 10 px rule changes.

REPLACE:
  digital_logic_lab/nand_mapper.py

ADD:
  tests/test_nand_label_order.py
