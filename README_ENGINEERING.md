# Digital Logic Lab — Engineering Baseline

This baseline introduces a software-engineering workflow without changing the
working Reflex pointer/drag subsystem.

## Structure

- `digital_logic_lab/digital_logic_lab.py` — Reflex UI, state and browser drag/wire code.
- `digital_logic_lab/logic_core.py` — pure logic engine and MSI/LSI registry.
- `tests/` — fast regression tests that do not require Reflex compilation.
- `pyproject.toml` — pytest, Ruff and mypy configuration.
- `.github/workflows/ci.yml` — continuous integration.

## Windows setup

From the project root:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Quality checks

```bat
python -m pytest
ruff check digital_logic_lab\logic_core.py tests
ruff format --check digital_logic_lab\logic_core.py tests
mypy digital_logic_lab\logic_core.py
python -m py_compile digital_logic_lab\digital_logic_lab.py
```

Then run the actual application:

```bat
reflex run
```

## Git baseline

Before replacing a working version:

```bat
git status
git add .
git commit -m "Checkpoint before engineering baseline"
```

After this baseline passes tests and manual UI checks:

```bat
git checkout -b engineering/baseline
git add .
git commit -m "Add engineering baseline and logic regression tests"
```

## Manual UI smoke test

After every change affecting the Reflex UI:

1. Drag AND/OR/FF components.
2. Drag a wire segment.
3. Pan the workbench.
4. Connect and disconnect wires.
5. Place and edit a text annotation.
6. Delete a component, wire and annotation.
7. Undo and redo.
8. Save and load a project.
9. Test manual and automatic clock modes.
10. Connect `FULL_ADDER:COUT` to another `FULL_ADDER:CIN`.

The browser drag/pointer code should not be refactored until these behaviors are
covered by a dedicated UI automation layer.
