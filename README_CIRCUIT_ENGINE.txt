BOOLNEXA CIRCUIT ENGINE v1

COPY TO:
D:\Projects\BoolNexa\digital_logic_lab\
  gate.py
  gate_library.py
  circuit_engine.py
  circuit_layout.py
  circuit_renderer.py

COPY TO:
D:\Projects\BoolNexa\tests\
  test_gate.py
  test_circuit_engine.py
  test_circuit_layout.py

FEATURES
- Boolean expression to gate graph
- AND, OR, XOR, NOT support from existing parser
- shared sub-expression reuse
- layered automatic layout
- orthogonal wire paths
- ANSI-inspired SVG rendering
- gate count and logic depth support

TEST:
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest tests -q

This package is the core engine only.
The Reflex UI integration is the next sub-sprint.
