BOOLNEXA SPRINT 6.6.7 FIX — COMPOUND COMPLEMENT LABELS

Observed wrong labels:
  AB'
  AC''

Correct BoolNexa labels:
  (AB)'
  (AC')'

Cause:
The formatter was treating multi-letter uppercase products as atomic identifiers.

Fix:
Adjacent uppercase symbols are now treated as Boolean products and are grouped
before complement notation is applied.

No logic, mapper, layout, routing, gate geometry, or 10 px rule changes.
