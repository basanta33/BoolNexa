"""First interactive BoolNexa Academy lesson."""
from __future__ import annotations

import reflex as rx


class BinaryLessonState(rx.State):
    """Interactive state for the first Academy lesson."""

    bit_3: int = 0
    bit_2: int = 0
    bit_1: int = 0
    bit_0: int = 0
    quiz_answer: str = ""
    quiz_submitted: bool = False
    challenge_target: int = 10

    def toggle_bit_3(self) -> None:
        self.bit_3 = 0 if self.bit_3 else 1

    def toggle_bit_2(self) -> None:
        self.bit_2 = 0 if self.bit_2 else 1

    def toggle_bit_1(self) -> None:
        self.bit_1 = 0 if self.bit_1 else 1

    def toggle_bit_0(self) -> None:
        self.bit_0 = 0 if self.bit_0 else 1

    def reset_bits(self) -> None:
        self.bit_3 = self.bit_2 = self.bit_1 = self.bit_0 = 0

    def set_quiz_answer(self, answer: str) -> None:
        self.quiz_answer = answer
        self.quiz_submitted = False

    def submit_quiz(self) -> None:
        self.quiz_submitted = True

    @rx.var
    def decimal_value(self) -> int:
        return self.bit_3 * 8 + self.bit_2 * 4 + self.bit_1 * 2 + self.bit_0

    @rx.var
    def binary_text(self) -> str:
        return f"{self.bit_3}{self.bit_2}{self.bit_1}{self.bit_0}"

    @rx.var
    def weighted_expression(self) -> str:
        return (
            f"({self.bit_3} × 8) + ({self.bit_2} × 4) + "
            f"({self.bit_1} × 2) + ({self.bit_0} × 1)"
        )

    @rx.var
    def challenge_complete(self) -> bool:
        return self.decimal_value == self.challenge_target

    @rx.var
    def quiz_correct(self) -> bool:
        return self.quiz_answer == "They allow stable states with useful noise tolerance"


def _bit_switch(label: str, weight: int, value: rx.Var, handler) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(label, size="1", color="#64748b", weight="bold"),
            rx.button(
                value.to_string(),
                on_click=handler,
                size="4",
                width="72px",
                height="72px",
                color_scheme="blue",
                variant="solid",
            ),
            rx.text(f"Weight {weight}", size="1", color="#64748b"),
            spacing="2",
            align="center",
        )
    )


def _section(number: str, title: str, *children: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(number, radius="full", color_scheme="blue"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            spacing="4",
            align="stretch",
        )
    )


def binary_intro_lesson() -> rx.Component:
    """Render the first complete, simulation-led lesson."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(),
                rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                width="100%",
            ),
            rx.image(
                src="/academy/binary-lesson-hero.svg",
                alt="Four binary switches forming 1010, equal to decimal 10",
                width="100%",
                max_height="330px",
                object_fit="contain",
            ),
            rx.vstack(
                rx.badge("UNIT 01 · LESSON 01", color_scheme="blue"),
                rx.heading("Why Computers Use Binary", size="8"),
                rx.text(
                    "Learn why digital systems use two logic states, then control a four-bit "
                    "binary input bank and prove your understanding through a live challenge.",
                    size="4",
                    color="#475569",
                    max_width="900px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.badge("20 minutes", color_scheme="gray"),
                    rx.badge("Beginner", color_scheme="green"),
                    rx.badge("Interactive", color_scheme="amber"),
                    wrap="wrap",
                ),
                align="start",
                spacing="3",
            ),
            _section(
                "1",
                "Learning objectives",
                rx.vstack(
                    rx.text("By the end of this lesson, you will be able to:"),
                    rx.text("• Explain why two-state signals are reliable for digital systems."),
                    rx.text("• Read a four-bit binary number using positional weights."),
                    rx.text("• Create a target decimal value using binary switches."),
                    rx.text("• Connect binary digits to logic LOW and logic HIGH."),
                    align="start",
                    spacing="2",
                ),
            ),
            _section(
                "2",
                "The central idea",
                rx.text(
                    "A digital circuit distinguishes between two ranges of electrical conditions. "
                    "We describe them as logic LOW and logic HIGH, and represent them with the digits "
                    "0 and 1. Two well-separated states are easier to regenerate and interpret reliably "
                    "than many closely spaced levels.",
                    line_height="1.7",
                    color="#334155",
                ),
                rx.grid(
                    rx.card(
                        rx.vstack(
                            rx.badge("0", radius="full", color_scheme="gray"),
                            rx.heading("Logic LOW", size="4"),
                            rx.text("An interpreted low signal range", size="2", color="#64748b"),
                            align="center",
                        )
                    ),
                    rx.card(
                        rx.vstack(
                            rx.badge("1", radius="full", color_scheme="blue"),
                            rx.heading("Logic HIGH", size="4"),
                            rx.text("An interpreted high signal range", size="2", color="#64748b"),
                            align="center",
                        )
                    ),
                    columns=rx.breakpoints(initial="1", sm="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.callout(
                    "Binary is not the same as electricity itself. The digits 0 and 1 are symbols used to represent two interpreted logic states.",
                    icon="info",
                    color_scheme="blue",
                ),
            ),
            _section(
                "3",
                "Interactive four-bit simulator",
                rx.text(
                    "Select each bit. The leftmost bit has the greatest weight. Watch the binary word, weighted expression and decimal value update immediately.",
                    color="#475569",
                ),
                rx.flex(
                    _bit_switch("Most significant bit", 8, BinaryLessonState.bit_3, BinaryLessonState.toggle_bit_3),
                    _bit_switch("Bit 2", 4, BinaryLessonState.bit_2, BinaryLessonState.toggle_bit_2),
                    _bit_switch("Bit 1", 2, BinaryLessonState.bit_1, BinaryLessonState.toggle_bit_1),
                    _bit_switch("Least significant bit", 1, BinaryLessonState.bit_0, BinaryLessonState.toggle_bit_0),
                    gap="4",
                    wrap="wrap",
                    justify="center",
                    width="100%",
                ),
                rx.grid(
                    rx.card(rx.vstack(rx.text("Binary word", color="#64748b"), rx.heading(BinaryLessonState.binary_text, size="7"))),
                    rx.card(rx.vstack(rx.text("Decimal value", color="#64748b"), rx.heading(BinaryLessonState.decimal_value, size="7"))),
                    columns=rx.breakpoints(initial="1", sm="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.callout(BinaryLessonState.weighted_expression, icon="calculator", width="100%"),
                rx.hstack(
                    rx.button(
                        "Reset bits",
                        on_click=BinaryLessonState.reset_bits,
                        variant="soft",
                    ),
                    rx.link(
                        rx.button(
                            "Practice in Number Systems",
                            color_scheme="blue",
                            variant="soft",
                        ),
                        href="/tools/number-systems",
                    ),
                    wrap="wrap",
                    align_self="flex-start",
                ),
            ),
            _section(
                "4",
                "Build challenge",
                rx.text("Set the switches so that the four-bit input represents decimal 10."),
                rx.cond(
                    BinaryLessonState.challenge_complete,
                    rx.callout(
                        "Challenge passed: 1010₂ = 10₁₀. You combined weights 8 and 2.",
                        icon="circle-check",
                        color_scheme="green",
                        width="100%",
                    ),
                    rx.callout(
                        "Not yet. Keep changing the bits until the decimal display reaches 10.",
                        icon="target",
                        color_scheme="amber",
                        width="100%",
                    ),
                ),
            ),
            _section(
                "5",
                "Knowledge check",
                rx.text("Why are two logic states useful in digital systems?"),
                rx.radio(
                    [
                        "They allow stable states with useful noise tolerance",
                        "They make every calculation use only two transistors",
                        "They eliminate all timing delays",
                    ],
                    value=BinaryLessonState.quiz_answer,
                    on_change=BinaryLessonState.set_quiz_answer,
                    direction="column",
                ),
                rx.button("Submit answer", on_click=BinaryLessonState.submit_quiz, color_scheme="blue", align_self="flex-start"),
                rx.cond(
                    BinaryLessonState.quiz_submitted,
                    rx.cond(
                        BinaryLessonState.quiz_correct,
                        rx.callout("Correct. Reliable separation between interpreted states is the key idea.", icon="circle-check", color_scheme="green"),
                        rx.callout("Review the central idea: binary uses two well-separated interpreted states.", icon="circle-alert", color_scheme="red"),
                    ),
                    rx.box(),
                ),
            ),
            _section(
                "6",
                "Simulator connection",
                rx.text(
                    "In the main BoolNexa simulator, INPUT components behave like the switches above. "
                    "Their values propagate through gates, allowing larger binary systems to be built and tested.",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.link(rx.button("Build with INPUT gates", color_scheme="blue"), href="/"),
                    rx.link(rx.button("Return to Academy", variant="soft"), href="/academy"),
                    wrap="wrap",
                ),
            ),
            rx.text(
                "BoolNexa Academy · Learn → Visualise → Build → Simulate → Test",
                size="1",
                color="#94a3b8",
                text_align="center",
                padding_y="20px",
            ),
            spacing="6",
            align="stretch",
            max_width="1100px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px", xl="48px"),
        ),
        min_height="100vh",
        background="#ffffff",
    )
