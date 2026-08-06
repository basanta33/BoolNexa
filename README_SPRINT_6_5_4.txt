BOOLNEXA SPRINT 6.5.4 — NOR-ONLY REALIZATION

Adds
----
digital_logic_lab/nor_mapper.py

Updates
-------
digital_logic_lab/realization_engine.py

Tests
-----
tests/test_nor_realization.py

NOR-only mappings
-----------------
NOT A:
  NOR(A,A)

A OR B:
  P = NOR(A,B)
  NOR(P,P)

A AND B:
  NOR(NOR(A,A), NOR(B,B))

A XNOR B:
  four-NOR realization

A XOR B:
  four-NOR XNOR followed by a NOR inverter
  = five NOR gates

The mapper deliberately shares repeated internal technology nodes. The
circuit engine added in Sprint 6.5.3 already preserves this intentional
fan-out while keeping ordinary expression topology structural.

The tests verify:
- strict NOR-only logical gates;
- NOT;
- AND;
- OR;
- XOR;
- three-input XOR/full-adder SUM;
- a mixed Boolean expression;
- exhaustive truth-table equivalence for the tested inputs.

Next recommended sprint:
  6.5.5 — unified preferred-gate realization strategy and UI-facing
  realization summary, before wiring the policy controls into the Reflex UI.
