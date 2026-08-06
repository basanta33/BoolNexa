# BoolNexa Academy v2.0 — Sprint A1

This package replaces the monolithic Academy page with a modular package while preserving the existing `/academy` import and route.

## Included
- Typed curriculum models and registries
- Shared Academy state for path selection, completion, XP and streaks
- Modern responsive Academy home page
- Reusable hero, learning-path and laboratory cards
- Foundation tests
- Existing first binary lesson route remains unchanged

## Install
Copy the package over the project root. The previous `digital_logic_lab/academy.py` is retained as `academy_legacy.py` for reference.

## Verify
```bat
set PYTHONNOUSERSITE=1
set PYTHONPATH=
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest tests -q
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run
```
