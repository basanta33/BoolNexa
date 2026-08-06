BOOLNEXA SPRINT 6.4 — PROFESSIONAL LOGIC-GATE RENDERING

COPY TO:
D:\Projects\BoolNexa\digital_logic_lab\
  circuit_svg_renderer.py

COPY TO:
D:\Projects\BoolNexa\tests\
  test_circuit_professional_rendering.py

WHAT CHANGES
- AND becomes a D-shaped ANSI-style gate.
- OR becomes a curved ANSI-style gate.
- NOT becomes a triangle with inversion bubble.
- XOR gains the extra curved input line.
- NAND/NOR/XNOR rendering support is included.
- Input/output labels become cleaner.
- Fan-out junction dots are rendered.
- Existing orthogonal wiring remains.

WHAT DOES NOT CHANGE
- circuit_engine.py
- circuit_validator.py
- circuit_layout.py
- Boolean Lab
- Mano K-map
- simplifier
- routing

Run the entire pytest suite before starting Reflex.
