from __future__ import annotations

import reflex as rx


def hero() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.badge("BOOLNEXA ACADEMY 2.0", color_scheme="blue"),
                rx.heading("Learn digital logic by building it", size="8"),
                rx.text(
                    "Learn the theory in Academy, then practise immediately in the "
                    "same BoolNexa tools used for real circuit simulation, Boolean "
                    "analysis, K-maps, circuit generation and number systems.",
                    size="4",
                    color="#cbd5e1",
                    line_height="1.6",
                    max_width="760px",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Start learning", size="3"),
                        href="/academy/unit-1/why-computers-use-binary",
                    ),
                    rx.link(
                        rx.button("Open tools", size="3", variant="soft"),
                        href="/tools",
                    ),
                    rx.link(
                        rx.button("Open simulator", size="3", variant="soft"),
                        href="/",
                    ),
                    wrap="wrap",
                ),
                align="start",
                spacing="4",
            ),
            rx.image(
                src="/academy/binary-lesson-hero.svg",
                alt="Digital logic learning",
                width=rx.breakpoints(initial="100%", lg="420px"),
                max_height="280px",
                object_fit="contain",
            ),
            width="100%",
            justify="between",
            align="center",
            wrap="wrap",
            gap="6",
        ),
        background="linear-gradient(135deg,#0f172a,#1e3a8a)",
        color="white",
        border_radius="24px",
        padding=rx.breakpoints(initial="24px", md="40px"),
        width="100%",
    )
