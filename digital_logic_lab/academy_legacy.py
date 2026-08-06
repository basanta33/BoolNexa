"""BoolNexa Academy interactive learning page.

The Academy UI is intentionally separated from the main simulator so lessons,
visuals and learning activities can evolve without changing the CAD workbench.
"""
from __future__ import annotations

import reflex as rx

from .academy_content import ACADEMY_UNITS, LABS, LESSON_SECTIONS
from .lesson_content import UNIT_1_LESSONS


UNIT_ARTWORK = {
    1: "/academy/binary-systems.svg",
    2: "/academy/boolean-gates.svg",
    3: "/academy/kmap.svg",
    4: "/academy/combinational.svg",
    5: "/academy/msi-lsi.svg",
    6: "/academy/sequential.svg",
    7: "/academy/registers-counters.svg",
}


class AcademyState(rx.State):
    """Small, extensible state foundation for Academy navigation and progress."""

    selected_unit: int = 1
    completed_lessons: list[str] = []

    def select_unit(self, unit_number: int) -> None:
        self.selected_unit = unit_number

    def toggle_lesson(self, lesson_id: str) -> None:
        completed = list(self.completed_lessons)
        if lesson_id in completed:
            completed.remove(lesson_id)
        else:
            completed.append(lesson_id)
        self.completed_lessons = completed

    @rx.var
    def completed_count(self) -> int:
        return len(self.completed_lessons)

    @rx.var
    def progress_percent(self) -> int:
        total = sum(int(unit["lessons"]) for unit in ACADEMY_UNITS)
        return round((len(self.completed_lessons) / total) * 100) if total else 0


def _nav_button(label: str, href: str, active: bool = False) -> rx.Component:
    return rx.link(
        rx.button(
            label,
            variant="solid" if active else "soft",
            size="2",
            width="100%",
        ),
        href=href,
        width="100%",
        text_decoration="none",
    )


def _unit_card(unit: dict[str, object]) -> rx.Component:
    number = int(unit["number"])
    return rx.card(
        rx.vstack(
            rx.image(
                src=UNIT_ARTWORK[number],
                alt=f'{unit["title"]} concept illustration',
                width="100%",
                height="145px",
                object_fit="contain",
                border_radius="12px",
            ),
            rx.hstack(
                rx.badge(f"PATH {number:02d}", color_scheme="blue", variant="solid"),
                rx.spacer(),
                rx.badge(f'{unit["lessons"]} lessons', color_scheme="gray", variant="soft"),
                width="100%",
                align="center",
            ),
            rx.heading(str(unit["title"]), size="4", color="#0f172a"),
            rx.text(
                str(unit["summary"]),
                size="2",
                color="#475569",
                line_height="1.55",
            ),
            rx.progress(value=0, width="100%"),
            rx.hstack(
                rx.text("Ready to explore", size="1", color="#64748b"),
                rx.spacer(),
                rx.button(
                    "Explore path",
                    size="1",
                    variant="soft",
                    on_click=AcademyState.select_unit(number),
                ),
                width="100%",
                align="center",
            ),
            spacing="3",
            align="stretch",
        ),
        height="100%",
    )


def _lesson_card(lesson: dict[str, object]) -> rx.Component:
    is_available = str(lesson["status"]) == "available"
    action = (
        rx.link(
            rx.button("Start lesson", size="1", color_scheme="blue"),
            href="/academy/unit-1/why-computers-use-binary",
            text_decoration="none",
        )
        if is_available
        else rx.button("Coming soon", size="1", variant="soft", disabled=True)
    )

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(str(lesson["number"]), radius="full", color_scheme="blue"),
                rx.spacer(),
                rx.badge(
                    "Interactive" if is_available else "Planned",
                    color_scheme="green" if is_available else "gray",
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),
            rx.heading(str(lesson["title"]), size="3"),
            rx.text(
                str(lesson["simulator_activity"]),
                size="2",
                color="#64748b",
                line_height="1.5",
            ),
            rx.spacer(),
            action,
            spacing="3",
            align="stretch",
            min_height="180px",
        ),
        height="100%",
    )


def _continue_learning() -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.image(
                src="/academy/binary-systems.svg",
                alt="Binary learning illustration",
                width=rx.breakpoints(initial="100%", md="220px"),
                height="150px",
                object_fit="contain",
                border_radius="12px",
            ),
            rx.vstack(
                rx.badge("START HERE", color_scheme="green", variant="soft"),
                rx.heading("Why Computers Use Binary", size="5"),
                rx.text(
                    "Switch bits on and off, observe positional values and build the binary number 1010.",
                    color="#64748b",
                    line_height="1.55",
                ),
                rx.progress(value=0, width="100%"),
                rx.link(
                    rx.button("Begin lesson 1", color_scheme="blue"),
                    href="/academy/unit-1/why-computers-use-binary",
                    text_decoration="none",
                ),
                spacing="3",
                align="stretch",
                width="100%",
            ),
            width="100%",
            align="center",
            wrap="wrap",
            gap="5",
        )
    )


def _challenge_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge("TODAY'S CHALLENGE", color_scheme="amber"),
                rx.spacer(),
                rx.badge("10 min", color_scheme="gray", variant="soft"),
                width="100%",
            ),
            rx.image(
                src="/academy/boolean-gates.svg",
                alt="Logic gate challenge illustration",
                width="100%",
                height="145px",
                object_fit="contain",
                border_radius="12px",
            ),
            rx.heading("Build XOR using only NAND gates", size="4"),
            rx.text(
                "Use no more than four NAND gates and verify all four input combinations.",
                size="2",
                color="#64748b",
            ),
            rx.button("Challenge coming soon", variant="soft", disabled=True),
            spacing="3",
            align="stretch",
        ),
        height="100%",
    )


def _boolean_history() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.badge("FOUNDATION STORY", color_scheme="amber"),
            rx.heading("Boolean algebra made digital computing possible", size="5"),
            rx.text(
                "George Boole created an algebraic system for reasoning about logic. Claude Shannon later showed that Boolean expressions could describe switching and relay circuits.",
                color="#334155",
                line_height="1.65",
            ),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("George Boole", size="4"),
                        rx.text("Originator of Boolean algebra", size="2"),
                        rx.text(
                            "1815–1864 · English mathematician and logician",
                            size="1",
                            color="#64748b",
                        ),
                        align="start",
                    )
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Claude Shannon", size="4"),
                        rx.text("Connected Boolean algebra to switching circuits", size="2"),
                        rx.text(
                            "1916–2001 · American mathematician and electrical engineer",
                            size="1",
                            color="#64748b",
                        ),
                        align="start",
                    )
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                width="100%",
            ),
            rx.callout(
                "Every logic gate, processor, memory device and digital controller applies Boolean decisions through physical electronic switches.",
                icon="lightbulb",
                color_scheme="blue",
                width="100%",
            ),
            spacing="4",
            align="stretch",
        )
    )


def _unit_one_lessons() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.badge("UNIT 1", color_scheme="green"),
                rx.heading("Binary Systems", size="6"),
                rx.text(
                    "Learn each concept through visualisers, guided experiments and simulator challenges.",
                    color="#64748b",
                ),
                align="start",
                spacing="2",
            ),
            rx.spacer(),
            rx.link(
                rx.button("Begin lesson 1", color_scheme="blue"),
                href="/academy/unit-1/why-computers-use-binary",
                text_decoration="none",
            ),
            width="100%",
            align="center",
            wrap="wrap",
            gap="4",
        ),
        rx.grid(
            *[_lesson_card(lesson) for lesson in UNIT_1_LESSONS],
            columns=rx.breakpoints(initial="1", md="2", xl="3"),
            spacing="4",
            width="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


def _lesson_template() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("How every lesson works", size="5"),
            rx.text(
                "Each lesson follows a consistent learn–build–test journey.",
                color="#64748b",
            ),
            rx.grid(
                *[
                    rx.hstack(
                        rx.badge(str(index + 1), radius="full", color_scheme="blue"),
                        rx.text(section, size="2", font_weight="500"),
                        align="center",
                    )
                    for index, section in enumerate(LESSON_SECTIONS)
                ],
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                spacing="3",
                width="100%",
            ),
            spacing="4",
            align="stretch",
        )
    )


def academy() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.heading("BoolNexa", size="6", color="#0f172a"),
                        rx.text("Academy", color="#2563eb", font_weight="700"),
                        spacing="0",
                        align="start",
                    ),
                    _nav_button("Academy Home", "/academy", True),
                    _nav_button("Open Simulator", "/"),
                    rx.divider(),
                    rx.text("LEARNING PATH", size="1", color="#64748b", font_weight="700"),
                    *[
                        rx.button(
                            f'{unit["number"]}. {unit["title"]}',
                            variant="ghost",
                            size="1",
                            width="100%",
                            justify_content="flex-start",
                            on_click=AcademyState.select_unit(int(unit["number"])),
                        )
                        for unit in ACADEMY_UNITS
                    ],
                    rx.divider(),
                    rx.text("Progress", size="2", font_weight="700"),
                    rx.progress(value=AcademyState.progress_percent, width="100%"),
                    rx.text(
                        AcademyState.progress_percent.to_string() + "% complete",
                        size="1",
                        color="#64748b",
                    ),
                    spacing="3",
                    align="stretch",
                ),
                width="260px",
                min_width="260px",
                height="100vh",
                padding="24px 18px",
                border_right="1px solid #e2e8f0",
                background="#f8fafc",
                position="sticky",
                top="0",
                display=rx.breakpoints(initial="none", lg="block"),
            ),
            rx.box(
                rx.vstack(
                    rx.card(
                        rx.hstack(
                            rx.vstack(
                                rx.badge("BOOLNEXA ACADEMY", color_scheme="blue"),
                                rx.heading(
                                    "Learn digital logic by building real circuits",
                                    size="8",
                                    max_width="760px",
                                ),
                                rx.text(
                                    "From binary numbers to complete digital systems—every core concept is connected to an interactive activity, circuit or challenge.",
                                    size="4",
                                    color="#475569",
                                    max_width="760px",
                                    line_height="1.6",
                                ),
                                rx.hstack(
                                    rx.link(
                                        rx.button("Start learning", size="3", color_scheme="blue"),
                                        href="/academy/unit-1/why-computers-use-binary",
                                        text_decoration="none",
                                    ),
                                    rx.link(
                                        rx.button("Launch simulator", size="3", variant="soft"),
                                        href="/",
                                        text_decoration="none",
                                    ),
                                    wrap="wrap",
                                    gap="3",
                                ),
                                align="start",
                                spacing="4",
                                width="100%",
                            ),
                            rx.image(
                                src="/academy/logic-symbols-strip.svg",
                                alt="Logic gates connected to digital circuitry",
                                width=rx.breakpoints(initial="100%", lg="420px"),
                                max_height="260px",
                                object_fit="contain",
                            ),
                            width="100%",
                            align="center",
                            wrap="wrap",
                            gap="6",
                        )
                    ),
                    rx.grid(
                        _continue_learning(),
                        _challenge_card(),
                        columns=rx.breakpoints(initial="1", xl="2"),
                        spacing="4",
                        width="100%",
                    ),
                    _unit_one_lessons(),
                    rx.vstack(
                        rx.heading("Learning Path", size="6"),
                        rx.text(
                            "Choose a pathway, recognise its symbols and begin experimenting.",
                            color="#64748b",
                        ),
                        rx.grid(
                            *[_unit_card(unit) for unit in ACADEMY_UNITS],
                            columns=rx.breakpoints(initial="1", md="2", xl="3"),
                            spacing="4",
                            width="100%",
                        ),
                        align="stretch",
                        spacing="4",
                        width="100%",
                    ),
                    _boolean_history(),
                    _lesson_template(),
                    rx.card(
                        rx.vstack(
                            rx.heading("Practical and laboratory work", size="5"),
                            rx.text(
                                "Labs will combine objectives, predicted results, circuit construction, test cases, observations, debugging and viva questions.",
                                color="#64748b",
                            ),
                            rx.grid(
                                *[
                                    rx.hstack(
                                        rx.icon("flask-conical", size=17),
                                        rx.text(lab, size="2"),
                                        align="center",
                                    )
                                    for lab in LABS
                                ],
                                columns=rx.breakpoints(initial="1", md="2", xl="3"),
                                spacing="3",
                                width="100%",
                            ),
                            spacing="4",
                            align="stretch",
                        )
                    ),
                    rx.text(
                        "BoolNexa Academy · Learn, build, simulate, debug and master.",
                        size="1",
                        color="#94a3b8",
                        text_align="center",
                        padding_y="20px",
                    ),
                    spacing="6",
                    align="stretch",
                    width="100%",
                ),
                padding=rx.breakpoints(initial="20px", md="36px", xl="48px"),
                max_width="1500px",
                width="100%",
                margin="0 auto",
            ),
            width="100%",
            align="start",
        ),
        min_height="100vh",
        background="#ffffff",
    )
