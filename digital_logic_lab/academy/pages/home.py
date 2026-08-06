"""Academy home page."""

from __future__ import annotations

import reflex as rx

from ...ui import app_header
from ..models import LAB_PREVIEWS, LEARNING_PATHS, TOTAL_LESSONS
from ..state import AcademyState
from ..styles import CARD, MUTED, PAGE_BG, SECTION
from ..widgets.cards import lab_card, path_card
from ..widgets.hero import hero


def _metric(label: str, value, icon: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.icon(icon, size=24),
            rx.vstack(
                rx.text(label, size="1", color=MUTED),
                rx.heading(value, size="5"),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
        ),
        **CARD,
    )


def academy() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.box(hero(), **SECTION),
            rx.box(
                rx.grid(
                    _metric(
                        "Course progress",
                        AcademyState.progress_percent.to_string() + "%",
                        "chart-no-axes-column-increasing",
                    ),
                    _metric(
                        "Lessons completed",
                        AcademyState.completed_count,
                        "circle-check",
                    ),
                    _metric("XP earned", AcademyState.xp, "sparkles"),
                    _metric(
                        "Learning streak",
                        AcademyState.streak_days.to_string() + " day",
                        "flame",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                    spacing="4",
                    width="100%",
                ),
                **SECTION,
            ),
            rx.box(
                rx.card(
                    rx.hstack(
                        rx.vstack(
                            rx.badge("CONTINUE LEARNING", color_scheme="green"),
                            rx.heading("Why Computers Use Binary", size="5"),
                            rx.text(
                                "Control a four-bit input bank and build decimal 10 "
                                "from positional weights.",
                                color=MUTED,
                            ),
                            rx.progress(
                                value=AcademyState.progress_percent,
                                width="100%",
                            ),
                            rx.hstack(
                                rx.link(
                                    rx.button("Begin lesson 1"),
                                    href="/academy/unit-1/why-computers-use-binary",
                                ),
                                rx.link(
                                    rx.button(
                                        "Practice conversions",
                                        variant="soft",
                                    ),
                                    href="/tools/number-systems",
                                ),
                                wrap="wrap",
                            ),
                            align="stretch",
                            spacing="3",
                            width="100%",
                        ),
                        rx.image(
                            src="/academy/binary-systems.svg",
                            width="220px",
                            height="150px",
                            object_fit="contain",
                        ),
                        wrap="wrap",
                        width="100%",
                        align="center",
                    ),
                    **CARD,
                ),
                **SECTION,
            ),
            rx.box(
                rx.vstack(
                    rx.heading("Learning paths", size="6"),
                    rx.text(
                        f"A complete {TOTAL_LESSONS}-lesson journey from binary "
                        "to counters and memory. Every path now links directly to "
                        "the relevant autonomous BoolNexa tool.",
                        color=MUTED,
                    ),
                    rx.grid(
                        *[path_card(path) for path in LEARNING_PATHS],
                        columns=rx.breakpoints(initial="1", md="2", xl="3"),
                        spacing="5",
                        width="100%",
                    ),
                    align="stretch",
                    spacing="4",
                ),
                **SECTION,
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Virtual laboratory", size="6"),
                            rx.text(
                                "These are live laboratories backed by the real "
                                "BoolNexa tools—not duplicate Academy demos.",
                                color=MUTED,
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.link(
                            rx.button("View all tools", variant="soft"),
                            href="/tools",
                        ),
                        width="100%",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.grid(
                        *[lab_card(lab) for lab in LAB_PREVIEWS],
                        columns=rx.breakpoints(initial="1", md="2", xl="3"),
                        spacing="4",
                        width="100%",
                    ),
                    align="stretch",
                    spacing="4",
                ),
                **SECTION,
            ),
            spacing="7",
            align="stretch",
            padding_bottom="60px",
        ),
        background=PAGE_BG,
        min_height="100vh",
        width="100%",
    )
