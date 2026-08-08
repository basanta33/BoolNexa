(() => {
    // UI-001: deterministic browser interaction bootstrap.
    if (window.__logicHandlers) {
        const h = window.__logicHandlers;
        if (h.onKeyDown) document.removeEventListener("keydown", h.onKeyDown);
        if (h.onKeyUp) document.removeEventListener("keyup", h.onKeyUp);
        if (h.onPointerDown) document.removeEventListener("pointerdown", h.onPointerDown);
        if (h.onPointerMove) document.removeEventListener("pointermove", h.onPointerMove);
        if (h.onPointerUp) document.removeEventListener("pointerup", h.onPointerUp);
        if (h.onWheel) document.removeEventListener("wheel", h.onWheel);
    }

    window.__logicInitialized = true;
    window.__logicListenersBound = false;

    const GRID_SIZE = 20, GATE_WIDTH = 86;
    window.__isPanning = false; window.__draggedGate = null; window.__draggedWire = null;
    
    // Per-clock runtime. clock_interval is the FULL period,
    // so the square wave toggles every period / 2.
    window.__clockRuntime = {};

    window.__getImportedProjectData = () => { const r = window.__importedProjectJson; window.__importedProjectJson = null; return r; };

    if (window.__autoClockInterval) clearInterval(window.__autoClockInterval);
    window.__autoClockInterval = setInterval(() => {
        if (window.__draggedGate || window.__draggedWire || window.__isPanning) return;

        const now = performance.now();
        const liveClockIds = new Set();
        const clockCards = document.querySelectorAll('.schematic-gate-card[data-gate-type="CLK"]');

        clockCards.forEach(card => {
            const gateId = card.getAttribute('data-gate-id');
            if (!gateId) return;
            liveClockIds.add(gateId);

            const sel = card.querySelector('select');
            const inputField = card.querySelector('input[type="text"]');
            const isAuto = !!(sel && sel.value === 'auto');

            let periodSec = parseFloat(inputField ? inputField.value : '1');
            if (!Number.isFinite(periodSec)) periodSec = 1.0;
            periodSec = Math.max(0.5, Math.min(99.0, periodSec));

            if (!isAuto) {
                delete window.__clockRuntime[gateId];
                return;
            }

            const halfPeriodMs = (periodSec * 1000) / 2;
            let runtime = window.__clockRuntime[gateId];

            if (!runtime || Math.abs(runtime.periodSec - periodSec) > 0.0001) {
                window.__clockRuntime[gateId] = {
                    periodSec: periodSec,
                    lastToggleMs: now
                };
                return;
            }

            if (now - runtime.lastToggleMs >= halfPeriodMs) {
                runtime.lastToggleMs = now;
                window.__pendingClockTickKey = gateId;
                const btn = document.getElementById("clock-tick-key-btn");
                if (btn) {
                    btn.dispatchEvent(new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true
                    }));
                }
            }
        });

        Object.keys(window.__clockRuntime).forEach(gateId => {
            if (!liveClockIds.has(gateId)) {
                delete window.__clockRuntime[gateId];
            }
        });
    }, 50);

    function getOrthogonalPath(srcX, srcY, dstX, dstY, customMidX) {
        const midX = customMidX !== undefined ? customMidX : (srcX + (dstX - srcX) / 2);
        if (Math.abs(srcY - dstY) <= 4 && dstX >= srcX + 16 && customMidX === undefined) {
            return `M ${srcX} ${srcY} L ${dstX} ${dstY}`;
        } else if (dstX >= srcX + 16) {
            return `M ${srcX} ${srcY} L ${midX} ${srcY} L ${midX} ${dstY} L ${dstX} ${dstY}`;
        } else {
            const xOut = srcX + 16, xIn = dstX - 16, midY = (srcY + dstY) / 2;
            return `M ${srcX} ${srcY} L ${xOut} ${srcY} L ${xOut} ${midY} L ${xIn} ${midY} L ${xIn} ${dstY} L ${dstX} ${dstY}`;
        }
    }
    function getGateCoordinates(el) {
        if (!el) return { x: 140, y: 80 };
        const styleX = parseFloat(el.style.left), styleY = parseFloat(el.style.top);
        if (!isNaN(styleX) && !isNaN(styleY)) return { x: styleX, y: styleY };
        const vp = document.getElementById("logic-viewport"), vpRect = vp.getBoundingClientRect(), elRect = el.getBoundingClientRect();
        return { x: Math.round((elRect.left - vpRect.left) / GRID_SIZE) * GRID_SIZE, y: Math.round((elRect.top - vpRect.top) / GRID_SIZE) * GRID_SIZE };
    }
    function getComponentWidthByType(gateType) {
        if (gateType === 'FULL_ADDER' || gateType === 'MUX_4_1' || gateType === 'DEMUX_1_4' || gateType === 'DECODER_2_4' || gateType === 'ENCODER_4_2') return 130;
        if (gateType === 'HALF_ADDER' || gateType === 'MUX_2_1' || gateType === 'DEMUX_1_2') return 120;
        if (gateType === 'SEVEN_SEG' || gateType === 'CLK') return 110;
        return 86;
    }

    function getOutputPinOffsetFromElement(srcEl, srcKey) {
        if (!srcEl) return 30;
        const gateType = srcEl.getAttribute('data-gate-type') || '';
        const portName = srcKey && srcKey.includes(':') ? srcKey.split(':').slice(1).join(':') : '';

        if (portName === 'q_bar') {
            if (gateType === 'D_FF' || gateType === 'T_FF') return 45;
            if (gateType === 'RS_FF' || gateType === 'JK_FF') return 48;
        }

        let selector = '.output-pin-bubble';
        if (portName && portName !== 'q_bar') {
            selector = `.output-pin-bubble[data-output-port="${portName}"]`;
        }
        const outputBubble = srcEl.querySelector(selector);
        if (outputBubble) {
            const attr = outputBubble.getAttribute('data-offset-y');
            if (attr !== null && attr !== '') return parseFloat(attr);
        }

        if (gateType === 'D_FF' || gateType === 'T_FF' ||
            gateType === 'RS_FF' || gateType === 'JK_FF') return 18;
        return 30;
    }

    function refreshConnectionTerminalVisibility() {
        const inputPins = document.querySelectorAll('.input-pin-bubble');
        const outputPins = document.querySelectorAll('.output-pin-bubble');

        inputPins.forEach(pin => pin.classList.remove('connected-terminal'));
        outputPins.forEach(pin => {
            pin.classList.remove('connected-terminal');
            pin.classList.remove('wiring-source-active');
        });

        document.querySelectorAll(
            '#logic-svg-layer path[data-src-key][data-target-key][data-slot]'
        ).forEach(path => {
            const srcKey = path.getAttribute('data-src-key') || '';
            const targetKey = path.getAttribute('data-target-key') || '';
            const slot = path.getAttribute('data-slot') || '';

            outputPins.forEach(pin => {
                if ((pin.getAttribute('data-pin-gate') || '') === srcKey) {
                    pin.classList.add('connected-terminal');
                }
            });

            inputPins.forEach(pin => {
                if (
                    (pin.getAttribute('data-pin-gate') || '') === targetKey &&
                    (pin.getAttribute('data-pin-slot') || '') === slot
                ) {
                    pin.classList.add('connected-terminal');
                }
            });
        });
    }


    // Resolve a terminal anchor from the actual rendered pin bubble.
    // This keeps MSI/LSI live wire movement identical to ordinary logic gates
    // and avoids duplicating component-width / pin-offset geometry in JS.
    function getPinLocalAnchor(gateEl, selector, fallbackX, fallbackY) {
        if (!gateEl) return { x: fallbackX, y: fallbackY };
        const pin = gateEl.querySelector(selector);
        if (!pin) return { x: fallbackX, y: fallbackY };
        return {
            x: pin.offsetLeft + (pin.offsetWidth / 2),
            y: pin.offsetTop + (pin.offsetHeight / 2)
        };
    }

    function getOutputLocalAnchor(srcEl, srcKey) {
        if (!srcEl) return { x: GATE_WIDTH, y: 30 };
        const gateType = srcEl.getAttribute('data-gate-type') || '';
        const portName = srcKey && srcKey.includes(':') ? srcKey.split(':').slice(1).join(':') : '';
        let selector = '.output-pin-bubble';
        if (portName && portName !== 'q_bar') {
            selector = `.output-pin-bubble[data-output-port="${portName}"]`;
        } else if (portName === 'q_bar') {
            const pins = srcEl.querySelectorAll('.output-pin-bubble');
            if (pins.length > 1) {
                const pin = pins[pins.length - 1];
                return { x: pin.offsetLeft + pin.offsetWidth / 2, y: pin.offsetTop + pin.offsetHeight / 2 };
            }
        }
        return getPinLocalAnchor(
            srcEl, selector,
            getComponentWidthByType(gateType),
            getOutputPinOffsetFromElement(srcEl, srcKey)
        );
    }

    function getInputLocalAnchor(targetEl, slot, fallbackX, fallbackY) {
        if (!targetEl) return { x: fallbackX, y: fallbackY };
        return getPinLocalAnchor(
            targetEl,
            `.input-pin-bubble[data-pin-slot="${slot}"]`,
            fallbackX, fallbackY
        );
    }

    function updateAttachedWiresLive(gateId, newX, newY) {
        document.querySelectorAll('#logic-svg-layer g').forEach(g => {
            const pathHitbox = g.querySelector('path[data-src-key], path[data-target-key]');
            if (!pathHitbox) return;

            const srcKey = pathHitbox.getAttribute('data-src-key') || '';
            const targetKey = pathHitbox.getAttribute('data-target-key') || '';
            const offsetY = parseFloat(pathHitbox.getAttribute('data-offset-y')) || 30;
            const offsetXAttr = pathHitbox.getAttribute('data-offset-x');
            const offsetX = offsetXAttr !== null ? parseFloat(offsetXAttr) : 0;
            const baseSrcKey = srcKey.includes(':') ? srcKey.split(':')[0] : srcKey;

            let srcX, srcY, dstX, dstY;

            if (baseSrcKey === gateId) {
                const srcEl = document.querySelector(`[data-gate-id="${baseSrcKey}"]`);
                if (!srcEl) return;
                const srcAnchor = getOutputLocalAnchor(srcEl, srcKey);
                srcX = newX + srcAnchor.x;
                srcY = newY + srcAnchor.y;

                const targetEl = document.querySelector(`[data-gate-id="${targetKey}"]`);
                if (!targetEl) return;
                const pos = getGateCoordinates(targetEl);
                const slot = pathHitbox.getAttribute('data-slot') || '';
                const dstAnchor = getInputLocalAnchor(targetEl, slot, offsetX, offsetY);
                dstX = pos.x + dstAnchor.x;
                dstY = pos.y + dstAnchor.y;
            } else if (targetKey === gateId) {
                const targetEl = document.querySelector(`[data-gate-id="${targetKey}"]`);
                const slot = pathHitbox.getAttribute('data-slot') || '';
                const dstAnchor = getInputLocalAnchor(targetEl, slot, offsetX, offsetY);
                dstX = newX + dstAnchor.x;
                dstY = newY + dstAnchor.y;

                const srcEl = document.querySelector(`[data-gate-id="${baseSrcKey}"]`);
                if (!srcEl) return;
                const srcAnchor = getOutputLocalAnchor(srcEl, srcKey);
                const pos = getGateCoordinates(srcEl);
                srcX = pos.x + srcAnchor.x;
                srcY = pos.y + srcAnchor.y;
            } else {
                return;
            }

            const customMidX = parseFloat(pathHitbox.getAttribute('data-mid-x'));
            const newPathStr = getOrthogonalPath(
                srcX, srcY, dstX, dstY,
                Number.isFinite(customMidX) ? customMidX : undefined
            );
            g.querySelectorAll('path').forEach(p => p.setAttribute('d', newPathStr));
        });
    }
    function dispatchProxyClick(btnId) {
        const btn = document.getElementById(btnId);
        if (btn) btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }

    function setupWorkspaceDrop() {
        const ws = document.getElementById("logic-workspace");
        if (ws) {
            const allowedGateTypes = new Set([
                "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
                "INPUT", "OUTPUT", "CLK", "SEVEN_SEG",
                "D_FF", "T_FF", "RS_FF", "JK_FF",
                "HALF_ADDER", "FULL_ADDER", "MUX_2_1", "DEMUX_1_2",
            "MUX_4_1", "DEMUX_1_4", "DECODER_2_4", "ENCODER_4_2"
            ]);

            ws.ondragover = e => {
                const types = Array.from(e.dataTransfer.types || []);
                if (types.includes("application/x-circuit-gate")) {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = "copy";
                }
            };

            ws.ondrop = e => {
                const gateType = e.dataTransfer.getData(
                    "application/x-circuit-gate"
                );
                if (!allowedGateTypes.has(gateType)) {
                    return;
                }

                e.preventDefault();
                e.stopPropagation();

                const rect = ws.getBoundingClientRect();
                const panX = parseFloat(
                    ws.getAttribute("data-pan-x")
                ) || 0;
                const panY = parseFloat(
                    ws.getAttribute("data-pan-y")
                ) || 0;
                const zoom = parseFloat(ws.getAttribute("data-zoom")) || 1;
                const rawX = (e.clientX - rect.left - panX) / zoom;
                const rawY = (e.clientY - rect.top - panY) / zoom;
                const snapX = Math.max(
                    40,
                    Math.round(
                        (rawX - (GATE_WIDTH / 2)) / GRID_SIZE
                    ) * GRID_SIZE
                );
                const snapY = Math.max(
                    20,
                    Math.round(
                        (rawY - 30) / GRID_SIZE
                    ) * GRID_SIZE
                );
                const dropBtn = document.getElementById(
                    "drop-trigger-btn"
                );
                if (dropBtn) {
                    dropBtn.setAttribute("data-type", gateType);
                    dropBtn.setAttribute("data-x", snapX);
                    dropBtn.setAttribute("data-y", snapY);
                    dispatchProxyClick("drop-trigger-btn");
                }
            };
        }
    }
    setupWorkspaceDrop();
    refreshConnectionTerminalVisibility();

    [50, 100, 250, 500, 1000, 2000].forEach(ms => {
        setTimeout(() => {
            setupWorkspaceDrop();
            refreshConnectionTerminalVisibility();
        }, ms);
    });

    if (window.__logicWorkspaceObserver) {
        window.__logicWorkspaceObserver.disconnect();
    }
    window.__logicWorkspaceObserver = new MutationObserver(() => {
        setupWorkspaceDrop();
        refreshConnectionTerminalVisibility();
    });
    const observerRoot = document.body || document.documentElement;
    if (observerRoot) {
        window.__logicWorkspaceObserver.observe(observerRoot, {
            childList: true,
            subtree: true
        });
    }

    window.__logicEnsureReady = () => {
        setupWorkspaceDrop();
        refreshConnectionTerminalVisibility();
        return !!(
            window.__logicListenersBound &&
            document.getElementById("logic-workspace")
        );
    };

    window.__getDroppedGate = () => {
        const btn = document.getElementById("drop-trigger-btn"); if (!btn) return null;
        const type = btn.getAttribute("data-type"), x = parseInt(btn.getAttribute("data-x")), y = parseInt(btn.getAttribute("data-y"));
        return (!type || isNaN(x) || isNaN(y)) ? null : { type, x, y };
    };
    window.__getDragEndData = () => {
        const btn = document.getElementById("drag-end-trigger-btn"); if (!btn) return null;
        const key = btn.getAttribute("data-key"), x = parseInt(btn.getAttribute("data-x")), y = parseInt(btn.getAttribute("data-y"));
        return (!key || isNaN(x) || isNaN(y)) ? null : { key, x, y };
    };
    window.__getViewChangeData = () => { const r = window.__pendingViewData; window.__pendingViewData = null; return r; };
    window.__getWireDragEndData = () => { const r = window.__pendingWireDragEnd; window.__pendingWireDragEnd = null; return r; };
    window.__getDeleteGateData = () => { const r = window.__pendingDeleteGate; window.__pendingDeleteGate = null; return r; };
    window.__getToggleInputData = () => { const r = window.__pendingToggleInput; window.__pendingToggleInput = null; return r; };
    window.__getSelectGateData = () => { const r = window.__pendingSelectGate; window.__pendingSelectGate = null; return r; };
    window.__getClockTickKey = () => { const r = window.__pendingClockTickKey; window.__pendingClockTickKey = null; return r; };

    const onKeyDown = e => {
        const ws = document.getElementById("logic-workspace");
        const activeEl = document.activeElement, isTyping = activeEl && (activeEl.tagName === "INPUT" || activeEl.tagName === "TEXTAREA" || activeEl.tagName === "SELECT") && !activeEl.readOnly;
        if (e.code === "Space" && !e.repeat && !isTyping) { window.__logicSpaceDown = true; if (ws) ws.style.cursor = ws.getAttribute("data-delete-mode") === "true" ? "crosshair" : "grab"; }
        if (isTyping) return;
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); dispatchProxyClick(e.shiftKey ? "redo-trigger-btn" : "undo-trigger-btn"); }
        else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') { e.preventDefault(); dispatchProxyClick("redo-trigger-btn"); }
        else if (e.key.toLowerCase() === 'x') { const btn = document.querySelector('button[title*="Delete Mode"]'); if (btn) btn.click(); }
        if (e.key === "Escape") { const p = document.getElementById("live-wire-preview"); if (p) p.style.display = "none"; dispatchProxyClick("cancel-action-trigger-btn"); }
    };
    const onKeyUp = e => { 
        const ws = document.getElementById("logic-workspace");
        if (e.code === "Space") { window.__logicSpaceDown = false; if (ws) ws.style.cursor = ws.getAttribute("data-delete-mode") === "true" ? "crosshair" : "default"; } 
    };

    const onPointerDown = e => {
        const ws = document.getElementById("logic-workspace");
        if (!ws || !ws.contains(e.target)) return;
        window.__lastClientX = e.clientX; window.__lastClientY = e.clientY; window.__wasDraggingGate = false;
        
        const wireSegment = e.target.closest('.wire-drag-segment');
        const pinBubble = e.target.closest('.input-pin-bubble, .output-pin-bubble');
        const isDeleteMode = ws.getAttribute("data-delete-mode") === "true";

        if (wireSegment && !isDeleteMode) {
            window.__draggedWire = { wire_id: wireSegment.getAttribute('data-wire-id'), element: wireSegment, startX: e.clientX, baseMidX: parseFloat(wireSegment.getAttribute('data-mid-x')) || 0, srcX: parseFloat(wireSegment.getAttribute('data-src-x')) || 0, srcY: parseFloat(wireSegment.getAttribute('data-src-y')) || 0, dstX: parseFloat(wireSegment.getAttribute('data-dst-x')) || 0, dstY: parseFloat(wireSegment.getAttribute('data-dst-y')) || 0, offsetDx: 0 };
            return;
        }
        if (pinBubble) return;

        let gateCard = e.target.closest('[data-gate-id]');
        if (isDeleteMode && gateCard) {
            // Single component-delete path:
            // let the existing Reflex gate-card on_click handler call
            // State.handle_gate_click(cell_key). Do not dispatch a second
            // JavaScript delete event here.
            window.__draggedGate = null;
            window.__selectedGateKey = gateCard.getAttribute('data-gate-id');
            return;
        }
        if (e.target.closest('.input-label-field') || e.target.tagName === 'SELECT' || (e.target.tagName === 'INPUT' && !e.target.readOnly)) return;
        
        const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
        if (e.button === 1 || (e.button === 0 && window.__logicSpaceDown === true) || !gateCard) {
            window.__isPanning = true; window.__startMouseX = e.clientX; window.__startMouseY = e.clientY; window.__startPanX = wsPanX; window.__startPanY = wsPanY; ws.style.cursor = isDeleteMode ? "crosshair" : "grabbing"; return;
        }
        if (gateCard && e.button === 0) {
            e.preventDefault();
            const gateId = gateCard.getAttribute('data-gate-id');
            window.__selectedGateKey = gateId;
            const zoom = parseFloat(ws.getAttribute("data-zoom")) || 1;
            const rect = ws.getBoundingClientRect(), mouseWorldX = ((e.clientX - rect.left) - wsPanX) / zoom, mouseWorldY = ((e.clientY - rect.top) - wsPanY) / zoom, pos = getGateCoordinates(gateCard);
            window.__draggedGate = { id: gateId, pointerId: e.pointerId, startX: mouseWorldX, startY: mouseWorldY, startClientX: e.clientX, startClientY: e.clientY, origX: pos.x, origY: pos.y, worldX: pos.x, worldY: pos.y };
            gateCard.style.zIndex = "100"; gateCard.style.cursor = isDeleteMode ? "crosshair" : "grabbing";
        }
    };

    const onPointerMove = e => {
        const ws = document.getElementById("logic-workspace");
        const vp = document.getElementById("logic-viewport");
        if (window.__draggedWire) {
            const dx = e.clientX - window.__draggedWire.startX; window.__draggedWire.offsetDx = Math.round(dx / GRID_SIZE) * GRID_SIZE;
            const newMidX = window.__draggedWire.baseMidX + dx, group = window.__draggedWire.element.closest('g');
            if (group) {
                const livePath = getOrthogonalPath(window.__draggedWire.srcX, window.__draggedWire.srcY, window.__draggedWire.dstX, window.__draggedWire.dstY, newMidX);
                group.querySelectorAll('path').forEach(p => p.setAttribute('d', livePath));
            }
            return;
        }
        if (window.__draggedGate && ws) {
            const rawDx = Math.abs(e.clientX - window.__draggedGate.startClientX);
            const rawDy = Math.abs(e.clientY - window.__draggedGate.startClientY);
            if (rawDx + rawDy > 4) window.__wasDraggingGate = true;

            const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
            const zoom = parseFloat(ws.getAttribute("data-zoom")) || 1;
            const rect = ws.getBoundingClientRect(), mouseWorldX = ((e.clientX - rect.left) - wsPanX) / zoom, mouseWorldY = ((e.clientY - rect.top) - wsPanY) / zoom;
            
            const dx = mouseWorldX - window.__draggedGate.startX;
            const dy = mouseWorldY - window.__draggedGate.startY;
            
            let newX = Math.round((window.__draggedGate.origX + dx) / GRID_SIZE) * GRID_SIZE;
            let newY = Math.round((window.__draggedGate.origY + dy) / GRID_SIZE) * GRID_SIZE;
            newX = Math.max(40, newX); newY = Math.max(20, newY);
            window.__draggedGate.worldX = newX; window.__draggedGate.worldY = newY;
            
            const gateEl = document.querySelector(`[data-gate-id="${window.__draggedGate.id}"]`);
            if (gateEl) {
                gateEl.style.left = `${newX}px`; gateEl.style.top = `${newY}px`;
            }
            updateAttachedWiresLive(window.__draggedGate.id, newX, newY);
            return;
        }
        const stateSource = ws ? ws.getAttribute("data-wiring-source") : null, previewPath = document.getElementById("live-wire-preview");
        if (stateSource && previewPath && ws) {
            const baseSrcKey = stateSource.includes(':') ? stateSource.split(':')[0] : stateSource;
            const srcEl = document.querySelector(`[data-gate-id="${baseSrcKey}"]`);
            if (srcEl) {
                const wsPanX = parseFloat(ws.getAttribute("data-pan-x")) || 0, wsPanY = parseFloat(ws.getAttribute("data-pan-y")) || 0;
                const zoom = parseFloat(ws.getAttribute("data-zoom")) || 1;
            const rect = ws.getBoundingClientRect(), mouseWorldX = ((e.clientX - rect.left) - wsPanX) / zoom, mouseWorldY = ((e.clientY - rect.top) - wsPanY) / zoom;
                const pos = getGateCoordinates(srcEl);
                const srcAnchor = getOutputLocalAnchor(srcEl, stateSource);
                previewPath.setAttribute(
                    'd',
                    getOrthogonalPath(
                        pos.x + srcAnchor.x,
                        pos.y + srcAnchor.y,
                        mouseWorldX,
                        mouseWorldY
                    )
                );
                previewPath.style.display = "block";
            }
        } else if (previewPath) { previewPath.style.display = "none"; }
        if (window.__isPanning && vp && ws) {
            const curPanX = window.__startPanX + (e.clientX - window.__startMouseX), curPanY = window.__startPanY + (e.clientY - window.__startMouseY);
            vp.style.transform = `translate(${curPanX}px, ${curPanY}px)`;
            ws.style.backgroundPosition = `${curPanX}px ${curPanY}px`;
            window.__currentPanX = curPanX; window.__currentPanY = curPanY; window.__wasPanning = true;
        }
    };

    const onPointerUp = e => {
        const ws = document.getElementById("logic-workspace");
        const isDeleteMode = ws ? ws.getAttribute("data-delete-mode") === "true" : false;
        if (window.__draggedWire) {
            if (window.__draggedWire.offsetDx !== 0) {
                window.__pendingWireDragEnd = { wire_id: window.__draggedWire.wire_id, offset_dx: window.__draggedWire.offsetDx };
                dispatchProxyClick("wire-drag-end-trigger-btn");
            }
            window.__draggedWire = null; return;
        }
        if (window.__draggedGate) {
            const gateEl = document.querySelector(`[data-gate-id="${window.__draggedGate.id}"]`);
            if (gateEl) {
                gateEl.style.zIndex = "10"; gateEl.style.cursor = isDeleteMode ? "crosshair" : "grab";
            }
            const deleteZone = document.getElementById("canvas-delete-zone");
            let droppedInDelete = false;
            if (deleteZone && gateEl) {
                const dzRect = deleteZone.getBoundingClientRect(), gateRect = gateEl.getBoundingClientRect();
                droppedInDelete = !(dzRect.right < gateRect.left || dzRect.left > gateRect.right || dzRect.bottom < gateRect.top || dzRect.bottom > gateRect.bottom);
            }
            if (droppedInDelete) {
                window.__pendingDeleteGate = { key: window.__draggedGate.id }; window.__draggedGate = null; dispatchProxyClick("delete-gate-trigger-btn"); return;
            }
            const gateId = window.__draggedGate.id, gateType = gateEl ? gateEl.getAttribute("data-gate-type") : "";
            if (window.__wasDraggingGate) {
                const dragEndBtn = document.getElementById("drag-end-trigger-btn");
                if (dragEndBtn) { dragEndBtn.setAttribute("data-key", gateId); dragEndBtn.setAttribute("data-x", window.__draggedGate.worldX); dragEndBtn.setAttribute("data-y", window.__draggedGate.worldY); dispatchProxyClick("drag-end-trigger-btn"); }
            } else {
                if (gateType === "INPUT" || gateType === "CLK") { window.__pendingToggleInput = { key: gateId }; dispatchProxyClick("toggle-input-trigger-btn"); }
                else { window.__pendingSelectGate = { key: gateId }; dispatchProxyClick("select-gate-trigger-btn"); }
            }
            window.__draggedGate = null;
        }
        if (window.__isPanning) {
            window.__isPanning = false; if (ws) ws.style.cursor = isDeleteMode ? "crosshair" : "default";
            if (window.__wasPanning) {
                window.__pendingPanData = { panX: window.__currentPanX, panY: window.__currentPanY };
            }
        }
    };

    function getViewData() {
        const ws = document.getElementById("logic-workspace");
        if (!ws) return null;
        return {
            panX: parseFloat(ws.getAttribute("data-pan-x")) || 0,
            panY: parseFloat(ws.getAttribute("data-pan-y")) || 0,
            zoom: parseFloat(ws.getAttribute("data-zoom")) || 1
        };
    }

    function applyView(panX, panY, zoom) {
        const ws = document.getElementById("logic-workspace");
        const vp = document.getElementById("logic-viewport");
        if (!ws || !vp) return null;
        zoom = Math.max(0.25, Math.min(2.0, zoom));
        vp.style.transform = `translate(${panX}px, ${panY}px) scale(${zoom})`;
        ws.setAttribute("data-pan-x", panX);
        ws.setAttribute("data-pan-y", panY);
        ws.setAttribute("data-zoom", zoom);
        ws.style.backgroundSize = `${20 * zoom}px ${20 * zoom}px`;
        ws.style.backgroundPosition = `${panX}px ${panY}px`;
        return { panX, panY, zoom };
    }

    window.__logicZoom = delta => {
        const ws = document.getElementById("logic-workspace");
        const v = getViewData();
        if (!ws || !v) return null;
        const rect = ws.getBoundingClientRect();
        const cx = rect.width / 2, cy = rect.height / 2;
        const worldX = (cx - v.panX) / v.zoom, worldY = (cy - v.panY) / v.zoom;
        const z = Math.round(Math.max(0.25, Math.min(2.0, v.zoom + delta)) * 100) / 100;
        return applyView(cx - worldX * z, cy - worldY * z, z);
    };
    window.__logicResetZoom = () => {
        const ws = document.getElementById("logic-workspace");
        const v = getViewData();
        if (!ws || !v) return null;
        const rect = ws.getBoundingClientRect(), cx = rect.width / 2, cy = rect.height / 2;
        const worldX = (cx - v.panX) / v.zoom, worldY = (cy - v.panY) / v.zoom;
        return applyView(cx - worldX, cy - worldY, 1);
    };
    window.__logicFit = () => {
        const ws = document.getElementById("logic-workspace");
        if (!ws) return null;
        const gates = Array.from(document.querySelectorAll('.schematic-gate-card'));
        const notes = Array.from(document.querySelectorAll('.canvas-text-box'));
        const els = gates.concat(notes);
        if (!els.length) return applyView(0, 0, 1);
        let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
        els.forEach(el => {
            const p=getGateCoordinates(el);
            const w=parseFloat(el.style.width)||el.offsetWidth||100;
            const h=parseFloat(el.style.height)||el.offsetHeight||70;
            minX=Math.min(minX,p.x); minY=Math.min(minY,p.y); maxX=Math.max(maxX,p.x+w); maxY=Math.max(maxY,p.y+h);
        });
        const r=ws.getBoundingClientRect(), pad=96;
        const contentW=Math.max(maxX-minX, 1), contentH=Math.max(maxY-minY, 1);
        const rawFit=Math.min((r.width-pad*2)/contentW,(r.height-pad*2)/contentH);
        // A tiny circuit should remain comfortably editable rather than becoming
        // either microscopic or comically oversized when Fit is pressed.
        const maxUsefulFit=(els.length <= 2) ? 1.15 : 1.35;
        const z=Math.max(0.55,Math.min(maxUsefulFit,rawFit));
        return applyView((r.width-(minX+maxX)*z)/2,(r.height-(minY+maxY)*z)/2,z);
    };
    const onWheel = e => {
        const ws=document.getElementById("logic-workspace");
        if (!ws || !ws.contains(e.target) || !(e.ctrlKey || e.metaKey)) return;
        e.preventDefault();
        const v=getViewData(), r=ws.getBoundingClientRect();
        const px=e.clientX-r.left, py=e.clientY-r.top;
        const wx=(px-v.panX)/v.zoom, wy=(py-v.panY)/v.zoom;
        const factor=e.deltaY<0?1.1:0.9;
        const z=Math.max(0.25,Math.min(2.0,v.zoom*factor));
        const result=applyView(px-wx*z,py-wy*z,z);
        window.__pendingViewData=result;
        dispatchProxyClick("view-change-trigger-btn");
    };

    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("keyup", onKeyUp);
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("pointermove", onPointerMove);
    document.addEventListener("pointerup", onPointerUp);
    document.addEventListener("wheel", onWheel, { passive: false });

    window.__logicHandlers = {
        onKeyDown,
        onKeyUp,
        onPointerDown,
        onPointerMove,
        onPointerUp,
        onWheel
    };
    window.__logicListenersBound = true;

    window.__calcCanvasClick = () => {
        const ws = document.getElementById("logic-workspace");
        if (window.__wasPanning) { window.__wasPanning = false; return null; }
        if (!ws) return null;
        const hit = document.elementFromPoint(window.__lastClientX, window.__lastClientY);
        if (hit && hit.closest('.canvas-text-box, .schematic-gate-card, textarea, .input-label-field, select, input, button, .input-pin-bubble, .output-pin-bubble')) return null;
        const rect = ws.getBoundingClientRect(), panX = parseFloat(ws.getAttribute("data-pan-x")) || 0, panY = parseFloat(ws.getAttribute("data-pan-y")) || 0, zoom = parseFloat(ws.getAttribute("data-zoom")) || 1;
        const rawX = (window.__lastClientX - rect.left - panX) / zoom, rawY = (window.__lastClientY - rect.top - panY) / zoom;
        return {
            x: Math.max(40, Math.round((rawX - (GATE_WIDTH / 2)) / GRID_SIZE) * GRID_SIZE),
            y: Math.max(20, Math.round((rawY - 30) / GRID_SIZE) * GRID_SIZE),
            text_x: Math.max(20, Math.round(rawX / GRID_SIZE) * GRID_SIZE),
            text_y: Math.max(20, Math.round(rawY / GRID_SIZE) * GRID_SIZE)
        };
    };
    window.__getPanData = () => { const r = window.__pendingPanData; window.__pendingPanData = null; return r; };
})();
