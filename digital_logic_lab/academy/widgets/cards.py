"""Reusable Academy cards."""

from __future__ import annotations

import reflex as rx

from ..models import LabPreview, LearningPath
from ..state import AcademyState
from ..styles import CARD, MUTED


def path_card(path: LearningPath) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.image(
                src=path.artwork,
                alt=f"{path.title} illustration",
                width="100%",
                height="130px",
                object_fit="contain",
            ),
            rx.hstack(
                rx.badge(f"PATH {path.number:02d}", color_scheme="blue"),
                rx.spacer(),
                rx.text(
                    f"{path.lessons} lessons · {path.hours}h",
                    size="1",
                    color=MUTED,
                ),
                width="100%",
            ),
            rx.heading(path.title, size="4"),
            rx.text(path.summary, size="2", color=MUTED, line_height="1.55"),
            rx.hstack(
                rx.button(
                    "Select path",
                    size="2",
                    variant="soft",
                    on_click=AcademyState.select_path(path.number),
                ),
                rx.link(
                    rx.button(path.practice_label, size="2", color_scheme="blue"),
                    href=path.practice_href,
                    text_decoration="none",
                ),
                wrap="wrap",
                spacing="2",
            ),
            align="stretch",
            spacing="3",
        ),
        **CARD,
    )


def lab_card(lab: LabPreview) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(lab.icon, size=28),
                rx.spacer(),
                rx.badge("LIVE", color_scheme="green"),
                width="100%",
                align="center",
            ),
            rx.heading(lab.title, size="3"),
            rx.text(lab.description, size="2", color=MUTED, line_height="1.55"),
            rx.badge(lab.tool, variant="soft", color_scheme="blue"),
            rx.link(
                rx.button(lab.action, size="2", color_scheme="blue"),
                href=lab.href,
                text_decoration="none",
            ),
            align="start",
            spacing="3",
            min_height="15rem",
        ),
        **CARD,
    )
