BOOLNEXA SPRINT 6.6.4 — UNIVERSAL-GATE NETWORK OPTIMIZATION

Scope
-----
Synthesis/topology only.
No changes to:
  circuit_layout.py
  circuit_router.py
  circuit_svg_renderer.py
  circuit_visual_model.py

Problem addressed
-----------------
The previous NAND/NOR mappers frequently cloned already realized subtrees.
That could turn a single intermediate result into several physical copies,
making universal-gate diagrams much larger than necessary.

New optimization rules
----------------------
1. Structural memoization:
   identical source subexpressions map once and reuse the same result.

2. Technology-node hash-consing:
   identical NAND/NOR gates are reused.

3. Redundant inversion cancellation:
   NAND(NAND(X,X), NAND(X,X)) -> X
   NOR(NOR(X,X), NOR(X,X)) -> X

4. Canonical compact XOR networks preserved:
   NAND XOR = 4 NAND gates
   NOR XOR  = 5 NOR gates

5. Strict family guarantee:
   NAND-only graphs contain only NAND logic gates.
   NOR-only graphs contain only NOR logic gates.

6. Exhaustive truth-table verification in regression tests.

Files
-----
REPLACE:
  digital_logic_lab/nand_mapper.py
  digital_logic_lab/nor_mapper.py

ADD:
  tests/test_universal_gate_optimization.py
  README_SPRINT_6_6_4.txt
