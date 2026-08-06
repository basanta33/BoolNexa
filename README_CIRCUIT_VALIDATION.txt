BOOLNEXA SPRINT 6.3 — CIRCUIT VALIDATION & TOPOLOGY CORRECTION

COPY TO:
D:\Projects\BoolNexa\digital_logic_lab\
  circuit_engine.py
  circuit_validator.py

COPY TO:
D:\Projects\BoolNexa\tests\
  test_circuit_validation.py

PURPOSE
- Preserve the structural Boolean parse tree in generated circuits.
- Share primary inputs for fan-out.
- Avoid automatically collapsing repeated gate subexpressions.
- Verify generated circuit truth tables against the Boolean engine.
- Validate precedence, complements, parentheses, XOR, gate counts, and depth.

REFERENCE CASE
AB + AC'
Expected:
  inputs: A, B, C
  AND: 2
  NOT: 1
  OR: 1
  total gates: 4
  logic depth: 3

IMPORTANT
This package does not modify:
- boolean_lab.py
- kmap_engine.py
- logic_circuit_lab.py
- digital_logic_lab.py

After copying, run the entire BoolNexa test suite before Reflex.
