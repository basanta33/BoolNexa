BOOLNEXA SPRINT 6.5.1 — GATE-SET & REALIZATION POLICY MODEL

Purpose
-------
Adds the policy layer between a Boolean function and the future synthesis /
technology-mapping engine.

New file:
  digital_logic_lab/realization_policy.py

New test:
  tests/test_realization_policy.py

Concepts
--------
1. Allowed gates
   Hard constraint. The mapper may use only these gates.

2. Preferred gates
   Soft preference. Preferred gates must also be allowed.

3. Forced-only mode
   The mapper must not silently introduce another gate family.

4. Optimization objective
   BALANCED
   MIN_GATE_COUNT
   MIN_LOGIC_DEPTH
   PREFERRED_GATES

5. Presets
   AUTO
   BASIC_ONLY
   XOR_PREFERRED
   NAND_ONLY
   NOR_ONLY
   CUSTOM

6. Functional completeness
   Standard complete sets recognised in this sprint:
   - NAND
   - NOR
   - AND + OR + NOT
   - AND + NOT
   - OR + NOT

This sprint does NOT yet synthesize or transform circuits.
Sprint 6.5.2 will add XOR/XNOR decomposition and basic-gate mapping.
