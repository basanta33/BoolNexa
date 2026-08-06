BOOLNEXA SPRINT 6.5.5 — UNIFIED REALIZATION STRATEGY

Adds
----
digital_logic_lab/realization_strategy.py
tests/test_realization_strategy.py

Purpose
-------
Creates one stable UI-facing API above the realization engines.

The UI can now request a realization through:
  realize(expression, policy)
or:
  realize_preset(expression, preset, objective=...)

The result contains:
  graph
  policy
  summary

Summary fields include:
  selected preset
  optimization objective
  allowed gates
  preferred gates
  gates actually used
  preferred gates actually used
  total gate count
  logic depth
  strict/forced status
  functional-completeness status
  explanatory note

A deterministic candidate_score() is also included as groundwork for future
automatic comparison between multiple legal realizations.

Important
---------
This sprint does NOT alter the renderer or Reflex UI.
It consolidates the backend first so the next UI sprint has one clean API.

Recommended next sprint:
  6.6.1 — Circuit Generator realization controls:
  Auto / Basic / XOR Preferred / NAND Only / NOR Only,
  plus realization summary in the UI.
