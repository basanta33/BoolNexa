"""Standalone BoolNexa Logic Circuit Laboratory page."""

from __future__ import annotations

from typing import TypedDict
from urllib.parse import quote

import reflex as rx

from .boolean_engine import BooleanExpressionError, parse_expression
from .circuit_svg_renderer import render_circuit_graph_svg
from .realization_policy import (
    OptimizationObjective,
    RealizationPreset,
)
from .realization_strategy import realize_preset
from .ui import (
    COLORS,
    app_header,
    metric_card,
    page_intro,
    panel,
    primary_button,
    secondary_button,
)


class GateCountView(TypedDict):
    kind: str
    count: str


class CircuitLabState(rx.State):
    expression: str = "AB + AC'"
    realization_mode: str = "AUTO"
    normalized: str = ""
    svg_markup: str = ""
    total_gates: int = 0
    logic_depth: int = 0
    inputs: int = 0
    gate_counts: list[GateCountView] = []
    gates_used_text: str = ""
    preferred_used_text: str = ""
    realization_note: str = ""
    strict_text: str = "No"
    error_message: str = ""

    def on_load(self) -> None:
        self.generate()

    def set_expression(self, value: str) -> None:
        self.expression = value

    def load_example(self, value: str) -> None:
        self.expression = value
        self.generate()

    def choose_realization(self, mode: str) -> None:
        self.realization_mode = mode
        self.generate()

    def _preset(self) -> RealizationPreset:
        mapping = {
            "AUTO": RealizationPreset.AUTO,
            "BASIC_ONLY": RealizationPreset.BASIC_ONLY,
            "NAND_ONLY": RealizationPreset.NAND_ONLY,
            "NOR_ONLY": RealizationPreset.NOR_ONLY,
        }
        return mapping[self.realization_mode]

    def simulate_circuit(self):
        """Open this exact generated realization in a new simulator tab."""
        # Keep the URL payload intentionally small. The simulator recreates the
        # same realization graph, then transfers that graph into its live model.
        # Opening a new tab keeps the generated reference circuit available.
        expression = quote(self.expression, safe="")
        mode = quote(self.realization_mode, safe="")
        url = f"/?generated_expression={expression}&generated_mode={mode}"
        return rx.call_script(
            f"window.open({url!r}, '_blank', 'noopener,noreferrer')"
        )

    def generate(self) -> None:
        try:
            result = realize_preset(
                self.expression,
                self._preset(),
                objective=OptimizationObjective.BALANCED,
            )
            graph = result.graph
            summary = result.summary
            svg = render_circuit_graph_svg(graph)
        except (BooleanExpressionError, ValueError) as exc:
            self.error_message = str(exc)
            self.normalized = ""
            self.svg_markup = ""
            self.total_gates = 0
            self.logic_depth = 0
            self.inputs = 0
            self.gate_counts = []
            self.gates_used_text = ""
            self.preferred_used_text = ""
            self.realization_note = ""
            self.strict_text = "No"
            return

        self.error_message = ""
        self.normalized = parse_expression(self.expression).display().replace("·", "")
        self.svg_markup = svg
        self.total_gates = graph.statistics.total_gates
        self.logic_depth = graph.statistics.logic_depth
        self.inputs = graph.statistics.inputs
        self.gate_counts = [
            {"kind": kind, "count": str(count)}
            for kind, count in graph.statistics.counts.items()
        ]
        self.gates_used_text = ", ".join(summary.gates_used) or "None"
        self.preferred_used_text = (
            ", ".join(summary.preferred_gates_used) or "None"
        )
        self.realization_note = summary.note
        self.strict_text = "Yes" if summary.strict else "No"


def _mode_button(label: str, mode: str) -> rx.Component:
    return rx.button(
        label,
        on_click=lambda: CircuitLabState.choose_realization(mode),
        variant="soft",
        size="2",
        cursor="pointer",
    )


def logic_circuit_lab() -> rx.Component:
    return rx.box(
        app_header("boolean"),
        rx.box(
            rx.vstack(
                page_intro(
                    "TOOLS LAB · CIRCUIT GENERATOR",
                    "Logic Circuit Generator",
                    "Convert a Boolean expression into a gate-level circuit "
                    "and choose how BoolNexa should realize the logic.",
                ),
                rx.grid(
                    panel(
                        rx.vstack(
                            rx.heading(
                                "Boolean expression",
                                size="4",
                                color=COLORS["text"],
                            ),
                            rx.input(
                                value=CircuitLabState.expression,
                                on_change=CircuitLabState.set_expression,
                                placeholder="Example: AB + AC'",
                                width="100%",
                                font_family="monospace",
                                background=COLORS["surface_soft"],
                            ),
                            primary_button(
                                "Generate circuit",
                                CircuitLabState.generate,
                            ),
                            rx.separator(),
                            rx.text(
                                "Realization",
                                font_size="0.75rem",
                                font_weight="800",
                                color=COLORS["text_muted"],
                            ),
                            rx.flex(
                                _mode_button("Auto", "AUTO"),
                                _mode_button("Basic", "BASIC_ONLY"),
                                _mode_button("NAND Only", "NAND_ONLY"),
                                _mode_button("NOR Only", "NOR_ONLY"),
                                wrap="wrap",
                                gap="0.45rem",
                            ),
                            rx.text(
                                "Selected: ",
                                CircuitLabState.realization_mode,
                                font_size="0.78rem",
                                color=COLORS["text_muted"],
                            ),
                            rx.separator(),
                            rx.text(
                                "Examples",
                                font_size="0.75rem",
                                font_weight="800",
                                color=COLORS["text_muted"],
                            ),
                            rx.flex(
                                secondary_button(
                                    "AB + AC'",
                                    lambda: CircuitLabState.load_example(
                                        "AB + AC'"
                                    ),
                                ),
                                secondary_button(
                                    "A(B+C')",
                                    lambda: CircuitLabState.load_example(
                                        "A(B+C')"
                                    ),
                                ),
                                secondary_button(
                                    "AB + CD",
                                    lambda: CircuitLabState.load_example(
                                        "AB + CD"
                                    ),
                                ),
                                secondary_button(
                                    "A ⊕ B",
                                    lambda: CircuitLabState.load_example(
                                        "A ⊕ B"
                                    ),
                                ),
                                wrap="wrap",
                                gap="0.45rem",
                            ),
                            rx.cond(
                                CircuitLabState.error_message != "",
                                rx.callout(
                                    CircuitLabState.error_message,
                                    icon="triangle-alert",
                                    color_scheme="red",
                                    width="100%",
                                ),
                            ),
                            width="100%",
                            spacing="3",
                            align="stretch",
                        )
                    ),
                    rx.vstack(
                        rx.grid(
                            metric_card(
                                "NORMALIZED",
                                CircuitLabState.normalized,
                                compact=True,
                            ),
                            metric_card(
                                "INPUTS",
                                CircuitLabState.inputs,
                                compact=True,
                            ),
                            metric_card(
                                "TOTAL GATES",
                                CircuitLabState.total_gates,
                                compact=True,
                            ),
                            metric_card(
                                "LOGIC DEPTH",
                                CircuitLabState.logic_depth,
                                compact=True,
                            ),
                            columns=rx.breakpoints(
                                initial="1",
                                sm="2",
                                xl="4",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        panel(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Generated circuit",
                                        size="4",
                                        color=COLORS["text"],
                                    ),
                                    rx.spacer(),
                                    rx.badge(
                                        CircuitLabState.realization_mode,
                                        background=COLORS["primary_soft"],
                                        color=COLORS["primary"],
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                rx.box(
                                    rx.html(CircuitLabState.svg_markup),
                                    width="100%",
                                    min_height="360px",
                                    overflow_x="auto",
                                    background="#FFFFFF",
                                    border=(
                                        f"1px solid {COLORS['border']}"
                                    ),
                                    border_radius="10px",
                                    padding="1rem",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    primary_button(
                                        "Simulate circuit",
                                        CircuitLabState.simulate_circuit,
                                    ),
                                    width="100%",
                                ),
                                width="100%",
                                spacing="3",
                                align="stretch",
                            )
                        ),
                        panel(
                            rx.vstack(
                                rx.heading(
                                    "Realization summary",
                                    size="4",
                                    color=COLORS["text"],
                                ),
                                rx.text(
                                    "Gates used: ",
                                    CircuitLabState.gates_used_text,
                                ),
                                rx.text(
                                    "Preferred gates used: ",
                                    CircuitLabState.preferred_used_text,
                                ),
                                rx.text(
                                    "Strict realization: ",
                                    CircuitLabState.strict_text,
                                ),
                                rx.text(
                                    CircuitLabState.realization_note,
                                    color=COLORS["text_muted"],
                                ),
                                rx.flex(
                                    rx.foreach(
                                        CircuitLabState.gate_counts,
                                        lambda item: rx.badge(
                                            item["kind"]
                                            + " · "
                                            + item["count"],
                                            background=COLORS[
                                                "surface_soft"
                                            ],
                                            color=COLORS["text"],
                                        ),
                                    ),
                                    wrap="wrap",
                                    gap="0.55rem",
                                ),
                                width="100%",
                                spacing="2",
                                align="stretch",
                            )
                        ),
                        width="100%",
                        spacing="4",
                        align="stretch",
                    ),
                    columns=rx.breakpoints(
                        initial="1",
                        lg="290px 1fr",
                    ),
                    spacing="4",
                    width="100%",
                    align_items="start",
                ),
                width="100%",
                spacing="5",
                align="stretch",
            ),
            max_width="88rem",
            margin="0 auto",
            padding="2rem 1.25rem 3rem",
        ),
        min_height="100vh",
        background=COLORS["page"],
        on_mount=CircuitLabState.on_load,
    )
