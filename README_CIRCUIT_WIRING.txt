BOOLNEXA SPRINT 6.4.1 — WIRING GEOMETRY CORRECTION

COPY TO:
D:\Projects\BoolNexa\digital_logic_lab\
  circuit_layout.py

COPY TO:
D:\Projects\BoolNexa\tests\
  test_circuit_wiring_geometry.py

PURPOSE
Fix only circuit placement and wire geometry.

For AB + AC':
- A fans out clearly to both AND gates.
- B feeds only the first AND.
- C -> NOT feeds only the second AND.
- both AND outputs enter separate OR input pins.
- input pins use separate Y positions.
- fan-out uses a short shared trunk.
- all routes remain orthogonal.

NOT MODIFIED
- Boolean parser
- circuit engine
- circuit validator
- professional gate renderer
- Boolean Lab
- Karnaugh map
- simulator
