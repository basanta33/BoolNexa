BOOLNEXA BOOLEAN SIMPLIFIER v1

COPY TO:
D:\Projects\BoolNexa\digital_logic_lab\
  boolean_laws.py
  simplification_steps.py
  boolean_simplifier.py
  boolean_lab.py

COPY TO:
D:\Projects\BoolNexa\tests\
  test_boolean_simplifier.py

The updated Boolean Lab keeps the compact truth table and adds:
- exact minimum-SOP simplification
- step-by-step law explanations
- literal and term reduction summary
- tautology and contradiction handling
- reusable simplifier engine for future K-map integration

TEST:
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest tests -q

RUN:
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run

OPEN:
http://localhost:3000/tools/boolean
