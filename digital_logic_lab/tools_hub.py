"""BoolNexa autonomous tools discovery hub."""

from __future__ import annotations

import reflex as rx

from .ui import COLORS, app_header, page_intro, panel


TOOLS = [
    {
        "title": "Digital Logic Simulator",
        "description": (
            "Build and simulate logic gates, flip-flops, I/O devices and MSI/LSI "
            "components on an interactive circuit canvas."
        ),
        "href": "/",
        "badge": "SIMULATE",
        "action": "Open Simulator",
    },
    {
        "title": "Boolean Laboratory",
        "description": (
            "Analyse Boolean expressions, generate truth tables, derive canonical "
            "forms, simplify functions and solve Karnaugh maps."
        ),
        "href": "/tools/boolean",
        "badge": "ANALYSE",
        "action": "Open Boolean Lab",
    },
    {
        "title": "Logic Circuit Generator",
        "description": (
            "Convert a Boolean expression into an automatically laid-out gate-level "
            "circuit, then transfer the realization to the live simulator."
        ),
        "href": "/tools/circuit",
        "badge": "GENERATE",
        "action": "Open Circuit Generator",
    },
    {
        "title": "Number System Laboratory",
        "description": (
            "Convert integer and fractional values among binary, octal, decimal and "
            "hexadecimal with exact step-by-step explanations."
        ),
        "href": "/tools/number-systems",
        "badge": "CONVERT",
        "action": "Open Number Systems",
    },
    {
        "title": "BoolNexa Academy",
        "description": (
            "Learn digital logic through guided lessons and open the relevant "
            "BoolNexa tool whenever hands-on practice is useful."
        ),
        "href": "/academy",
        "badge": "LEARN",
        "action": "Open Academy",
    },
]


def _tool_card(tool: dict[str, str]) -> rx.Component:
    return panel(
        rx.vstack(
            rx.badge(
                tool["badge"],
                background=COLORS["primary_soft"],
                color=COLORS["primary"],
            ),
            rx.heading(tool["title"], size="5", color=COLORS["text"]),
            rx.text(
                tool["description"],
                color=COLORS["text_muted"],
                line_height="1.65",
                min_height="5.2rem",
            ),
            rx.spacer(),
            rx.link(
                rx.button(
                    tool["action"],
                    background=COLORS["primary"],
                    color="white",
                    cursor="pointer",
                ),
                href=tool["href"],
                text_decoration="none",
            ),
            align="start",
            spacing="3",
            min_height="17rem",
            width="100%",
        )
    )


def tools_hub() -> rx.Component:
    """Render the discovery hub; every linked module remains autonomous."""
    return rx.box(
        app_header("tools"),
        rx.box(
            rx.vstack(
                page_intro(
                    "BOOLNEXA · AUTONOMOUS MODULES",
                    "Digital Logic Tools",
                    "Use each BoolNexa module independently, or move between them "
                    "when a workflow naturally benefits from another tool.",
                ),
                rx.grid(
                    *[_tool_card(tool) for tool in TOOLS],
                    columns=rx.breakpoints(initial="1", md="2", xl="3"),
                    spacing="4",
                    width="100%",
                ),
                width="100%",
                spacing="5",
                align="stretch",
            ),
            max_width="82rem",
            margin="0 auto",
            padding="2rem 1.25rem 3rem",
        ),
        min_height="100vh",
        background=COLORS["page"],
    )
