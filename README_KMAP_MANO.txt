BOOLNEXA KARNAUGH MAP — MANO EDITION v1

COPY TO D:\Projects\BoolNexa\digital_logic_lab\
  gray_code.py
  kmap_engine.py
  kmap_renderer.py
  boolean_lab.py

COPY TO D:\Projects\BoolNexa\tests\
  test_gray_code.py
  test_kmap_engine.py

FEATURES
- Mano textbook variable arrangement
- 2–6 variable support
- Gray-code ordering
- 2 variables: one 2×2 map
- 3 variables: one 2×4 map
- 4 variables: one 4×4 map
- 5 variables: two 4×4 maps
- 6 variables: four 4×4 maps
- automatic prime-implicant grouping
- essential-prime indication
- minterm labels
- simplified SOP linked to existing simplifier

TEST
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest tests -q

RUN
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run

OPEN
http://localhost:3000/tools/boolean
