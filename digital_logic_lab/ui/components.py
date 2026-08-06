"""Reusable BoolNexa UI components."""

from __future__ import annotations

import reflex as rx

from .theme import COLORS, RADIUS, SHADOW


def app_header(active: str = "") -> rx.Component:
    def nav_link(label: str, href: str, key: str) -> rx.Component:
        selected = active == key
        return rx.link(
            rx.text(
                label,
                font_size="0.9rem",
                font_weight="700" if selected else "600",
                color=COLORS["primary"] if selected else COLORS["text_muted"],
            ),
            href=href,
            text_decoration="none",
            padding="0.55rem 0.75rem",
            border_radius="9px",
            background=COLORS["primary_soft"] if selected else "transparent",
        )

    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.box(
                        "B",
                        width="2rem",
                        height="2rem",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        border_radius="9px",
                        background=COLORS["accent"],
                        color="white",
                        font_weight="900",
                    ),
                    rx.text(
                        "BoolNexa",
                        color=COLORS["text"],
                        font_size="1.05rem",
                        font_weight="850",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            rx.spacer(),
            nav_link("Simulator", "/", "simulator"),
            nav_link("Academy", "/academy", "academy"),
            nav_link("Tools", "/tools", "tools"),
            nav_link("Number Systems", "/tools/number-systems", "numbers"),
            nav_link("Boolean Lab", "/tools/boolean", "boolean"),
            nav_link("Circuit Generator", "/tools/circuit", "circuit"),
            width="100%",
            align="center",
            spacing="2",
        ),
        width="100%",
        background=COLORS["surface"],
        border_bottom=f"1px solid {COLORS['border']}",
        padding="0.7rem 1.2rem",
        position="sticky",
        top="0",
        z_index="20",
    )


def page_intro(eyebrow: str, title: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.badge(
            eyebrow,
            background=COLORS["primary_soft"],
            color=COLORS["primary"],
            border=f"1px solid {COLORS['border']}",
        ),
        rx.heading(
            title,
            size="8",
            color=COLORS["text"],
            letter_spacing="-0.035em",
            line_height="1.08",
        ),
        rx.text(
            description,
            color=COLORS["text_muted"],
            line_height="1.7",
            max_width="62rem",
        ),
        width="100%",
        align="start",
        spacing="3",
    )


def panel(*children: rx.Component, padding: str = "1.15rem") -> rx.Component:
    return rx.box(
        *children,
        background=COLORS["surface"],
        border=f"1px solid {COLORS['border']}",
        border_radius=RADIUS,
        box_shadow=SHADOW,
        padding=padding,
        width="100%",
    )


def metric_card(title: str, value, compact: bool = False) -> rx.Component:
    return rx.box(
        rx.text(
            title,
            color=COLORS["text_muted"],
            font_size="0.7rem",
            font_weight="800",
            letter_spacing="0.05em",
        ),
        rx.text(
            value,
            color=COLORS["text"],
            font_family="monospace",
            font_weight="750",
            font_size="0.88rem" if compact else "0.96rem",
            margin_top="0.35rem",
            overflow_wrap="anywhere",
            line_height="1.45",
        ),
        background=COLORS["surface_soft"],
        border=f"1px solid {COLORS['border']}",
        border_radius="11px",
        padding="0.75rem",
        min_height="4.4rem" if compact else "5.2rem",
        width="100%",
    )


def primary_button(label: str, on_click) -> rx.Component:
    return rx.button(
        label,
        on_click=on_click,
        background=COLORS["primary"],
        color="white",
        border_radius="10px",
        cursor="pointer",
        font_weight="750",
        _hover={"background": "#2949AE"},
    )


def secondary_button(label: str, on_click) -> rx.Component:
    return rx.button(
        label,
        on_click=on_click,
        background=COLORS["surface_soft"],
        color=COLORS["text"],
        border=f"1px solid {COLORS['border_strong']}",
        border_radius="10px",
        cursor="pointer",
        _hover={"background": COLORS["primary_soft"]},
    )
