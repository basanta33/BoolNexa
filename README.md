# BoolNexa

BoolNexa is a free digital-logic learning and simulation application built with
[Reflex](https://reflex.dev/). It combines an interactive circuit workbench,
standalone engineering tools, and a 107-lesson Academy.

## Release surfaces

- `/` — Digital Logic Simulator
- `/academy` — BoolNexa Academy
- `/tools` — Tools hub
- `/tools/number-systems` — Number System Laboratory
- `/tools/boolean` — Boolean Laboratory
- `/tools/circuit` — Logic Circuit Generator

## Main capabilities

- Interactive gates, flip-flops, clocks, inputs, outputs, and MSI/LSI blocks
- Wire creation, editing, signal propagation, and circuit evaluation
- Project save/load using portable JSON
- Boolean simplification, truth tables, Karnaugh maps, and circuit generation
- 107 Academy lessons covering digital logic through computer architecture,
  embedded systems, HDL, FPGA design, synthesis, and verification

## Local setup on Windows

```bat
cd /d D:\Projects\BoolNexa
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pytest -q
reflex run
```

The local application is available at `http://localhost:3000` after Reflex
starts successfully.

## Release verification

Run the automated release gate:

```bat
python -m pytest -q
```

Then follow [RELEASE_CHECKLIST_BOOLNEXA.md](RELEASE_CHECKLIST_BOOLNEXA.md) for
the required browser and deployment checks.

## Deployment

The configured Reflex deployment target is:

`https://boolnexa-teal-ring.reflex.run`

Deployment credentials and environment-specific settings must not be committed
to this repository.

## Project status

The current v1 release candidate is based on the green Clock Generator
checkpoint. Further development should begin only after creating a new Git tag
or backup from the verified release state.
