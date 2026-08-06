BOOLNEXA SPRINT 6.5.3 — NAND-ONLY REALIZATION

Adds:
  digital_logic_lab/nand_mapper.py

Updates:
  digital_logic_lab/circuit_engine.py
  digital_logic_lab/realization_engine.py

Tests:
  tests/test_nand_realization.py

Mappings
--------
NOT A:
  NAND(A,A)

A AND B:
  P = NAND(A,B)
  NAND(P,P)

A OR B:
  NAND(NAND(A,A), NAND(B,B))

A XOR B:
  four-NAND realization

The NAND-only preset is a strict realization. After primary inputs/constants,
all logical gates in the resulting circuit graph are NAND.

The tests exhaustively verify small truth tables for NOT, AND, OR, XOR,
three-input XOR/full-adder SUM, and a mixed expression.

Next:
  Sprint 6.5.4 — NOR-only realization.
