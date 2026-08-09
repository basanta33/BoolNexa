# BoolNexa Final Release Checklist

## Automated release gates
- [x] Full `python -m pytest -q` passes.
- [x] Simulator `State.handle_gate_click(cell_key)` Reflex compile fix is protected.
- [x] All 107 Academy lesson routes are registered uniquely.
- [x] Core public routes are registered uniquely.
- [x] Reflex version is pinned.
- [x] Deployment URL uses HTTPS.
- [x] PWA/SEO/release assets exist and are non-empty.
- [x] Manifest and robots metadata are valid.
- [x] No accidental debug/temporary routes are registered.
- [x] Canonical repository documentation is present.
- [x] GitHub Actions runs the full pytest and core mypy release gates.
- [x] Accidental empty command-name files are absent.

## Deferred non-blocking maintenance
- Legacy Academy and test modules contain pre-existing Ruff formatting/style
  findings. They do not represent runtime failures and are intentionally
  deferred to a dedicated formatting change after v1 release verification.

## Final local verification before deployment
- [ ] Stop Reflex completely.
- [ ] Delete `.web` once.
- [ ] Run `python -m pytest -q`.
- [ ] Start Reflex once with `reflex run`.
- [ ] Confirm the simulator homepage loads.
- [ ] Confirm `/academy` loads and shows all completed paths.
- [ ] Confirm `/tools` loads.
- [ ] Confirm `/tools/number-systems` loads.
- [ ] Confirm `/tools/boolean` loads.
- [ ] Confirm `/tools/circuit` loads.
- [ ] Confirm `/academy/unit-12/complete-fpga-system-design-deployment` loads.
- [ ] Confirm no persistent frontend/backend exception appears.
- [ ] Verify the deployed HTTPS URL after release.
- [ ] Verify favicon, manifest and social image on the deployed site.
- [ ] Tag or archive the known-good release checkpoint before further development.
