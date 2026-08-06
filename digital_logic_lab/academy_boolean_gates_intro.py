"""BoolNexa Academy Path 02 lessons 1 and 2."""

from __future__ import annotations

import reflex as rx

from .ui import app_header


PANEL = {
    "border": "1px solid #e2e8f0",
    "border_radius": "16px",
    "padding": "22px",
    "background": "white",
    "width": "100%",
}


class BooleanGateIntroState(rx.State):
    logic_answer: str = ""
    logic_feedback: str = ""
    and_answer: str = ""
    and_feedback: str = ""
    or_answer: str = ""
    or_feedback: str = ""
    not_answer: str = ""
    not_feedback: str = ""

    def set_and_answer(self, value: str) -> None:
        self.and_answer = value

    def set_logic_answer(self, value: str) -> None:
        self.logic_answer = value

    def set_not_answer(self, value: str) -> None:
        self.not_answer = value

    def set_or_answer(self, value: str) -> None:
        self.or_answer = value

    def check_logic_state(self):
        value = self.logic_answer.strip()
        self.logic_feedback = (
            "Correct. In positive logic, HIGH is represented by logic 1."
            if value == "1"
            else "Try again. Positive logic normally maps the HIGH state to 1."
        )

    def check_and(self):
        value = self.and_answer.strip()
        self.and_feedback = (
            "Correct. AND is 1 only when both inputs are 1."
            if value == "1"
            else "AND requires A = 1 and B = 1 before the output becomes 1."
        )

    def check_or(self):
        value = self.or_answer.strip()
        self.or_feedback = (
            "Correct. OR is 1 when at least one input is 1."
            if value == "1"
            else "OR becomes 1 if A, B, or both are 1."
        )

    def check_not(self):
        value = self.not_answer.strip()
        self.not_feedback = (
            "Correct. NOT inverts 0 to 1."
            if value == "1"
            else "A NOT gate outputs the opposite logic state."
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(number, color_scheme="blue"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            align="stretch",
            spacing="3",
        ),
        **PANEL,
    )


def _truth_table(headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(*[rx.table.column_header_cell(item) for item in headers])
        ),
        rx.table.body(
            *[
                rx.table.row(*[rx.table.cell(item) for item in row])
                for row in rows
            ]
        ),
        width="100%",
        variant="surface",
    )


def logic_states_gates_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 01", color_scheme="blue"),
            rx.heading("Digital Logic States & Gate Fundamentals", size="8"),
            rx.text(
                "Move from binary numbers to digital decisions. Learn what logic 0 and logic 1 "
                "mean and how logic gates transform input states into output states.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Learning objectives",
                rx.unordered_list(
                    rx.list_item("distinguish a binary digit from a physical logic state;"),
                    rx.list_item("interpret LOW/HIGH as logic 0/1 in positive logic;"),
                    rx.list_item("explain the input → gate → output model;"),
                    rx.list_item("read a simple truth table."),
                ),
            ),
            _section(
                "2", "Logic 0 and logic 1",
                rx.text(
                    "A digital circuit works with ranges of electrical conditions rather than "
                    "perfect mathematical numbers. Designers interpret those conditions as two "
                    "logical states: LOW and HIGH."
                ),
                rx.hstack(
                    rx.card(
                        rx.vstack(
                            rx.heading("0", size="7"),
                            rx.text("LOW", weight="bold"),
                            rx.text("False · OFF", color="#64748b"),
                            align="center",
                        )
                    ),
                    rx.card(
                        rx.vstack(
                            rx.heading("1", size="7"),
                            rx.text("HIGH", weight="bold"),
                            rx.text("True · ON", color="#64748b"),
                            align="center",
                        )
                    ),
                    wrap="wrap",
                    spacing="4",
                ),
                rx.callout(
                    "Exact voltage thresholds depend on the logic family and device. "
                    "Do not assume that every digital circuit uses the same voltage.",
                    icon="info",
                ),
            ),
            _section(
                "3", "The gate model",
                rx.code_block(
                    "INPUT(S)  ─────►  LOGIC GATE  ─────►  OUTPUT\n\n"
                    "A gate applies a Boolean rule to one or more input states.",
                    language="markup",
                ),
                rx.text(
                    "A truth table lists every possible input combination and the corresponding output."
                ),
                _truth_table(
                    ("A", "B", "Example output Y"),
                    (
                        ("0", "0", "0"),
                        ("0", "1", "1"),
                        ("1", "0", "1"),
                        ("1", "1", "1"),
                    ),
                ),
                rx.text(
                    "This example happens to match an OR gate. You will formally study AND, OR and NOT next."
                ),
            ),
            _section(
                "4", "Quick check",
                rx.text("In positive logic, which binary value normally represents HIGH?"),
                rx.hstack(
                    rx.input(
                        value=BooleanGateIntroState.logic_answer,
                        on_change=BooleanGateIntroState.set_logic_answer,
                        placeholder="0 or 1",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=BooleanGateIntroState.check_logic_state),
                ),
                rx.cond(
                    BooleanGateIntroState.logic_feedback != "",
                    rx.callout(BooleanGateIntroState.logic_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Explore the real BoolNexa Simulator",
                rx.text(
                    "Open the Simulator, place input switches and an output indicator, then inspect "
                    "how logic states change as you interact with the circuit."
                ),
                rx.link(
                    rx.button("Open Simulator", color_scheme="blue"),
                    href="/",
                    align_self="flex-start",
                ),
            ),
            _section(
                "6", "Bridge from binary to Boolean logic",
                rx.text(
                    "Binary Systems taught you how 0 and 1 represent information. Boolean algebra "
                    "now gives us rules for processing those states. In the next lesson, the first "
                    "three gates become Boolean operations."
                ),
                rx.link(
                    rx.button("Open Boolean Lab", variant="soft"),
                    href="/tools/boolean",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(),
                rx.text("Path 02 · Lesson 1 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-2/and-or-not",
                ),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def and_or_not_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 02", color_scheme="blue"),
            rx.heading("AND, OR & NOT Gates", size="8"),
            rx.text(
                "Learn the three fundamental Boolean operations through equations, truth tables "
                "and practical gate behaviour.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "AND gate",
                rx.text(
                    "AND outputs 1 only when every required input is 1. In Boolean algebra, "
                    "AND is commonly written using multiplication or adjacency."
                ),
                rx.code_block("Y = A·B = AB", language="markup"),
                _truth_table(
                    ("A", "B", "Y = AB"),
                    (("0", "0", "0"), ("0", "1", "0"), ("1", "0", "0"), ("1", "1", "1")),
                ),
                rx.text("Example: a machine runs only when POWER = 1 AND ENABLE = 1."),
            ),
            _section(
                "2", "OR gate",
                rx.text(
                    "OR outputs 1 when at least one input is 1. Boolean OR is written with +."
                ),
                rx.code_block("Y = A + B", language="markup"),
                _truth_table(
                    ("A", "B", "Y = A + B"),
                    (("0", "0", "0"), ("0", "1", "1"), ("1", "0", "1"), ("1", "1", "1")),
                ),
                rx.text("Example: an alarm activates if SENSOR_A = 1 OR SENSOR_B = 1."),
            ),
            _section(
                "3", "NOT gate",
                rx.text(
                    "NOT has one input and produces its complement: 0 becomes 1 and 1 becomes 0."
                ),
                rx.code_block("Y = A'   (also written ¬A or A̅)", language="markup"),
                _truth_table(("A", "Y = A'"), (("0", "1"), ("1", "0"))),
                rx.text("Example: NOT READY becomes true whenever READY is false."),
            ),
            _section(
                "4", "Interactive gate check",
                rx.text("A = 1 and B = 1. What is AND output AB?"),
                rx.hstack(
                    rx.input(
                        value=BooleanGateIntroState.and_answer,
                        on_change=BooleanGateIntroState.set_and_answer,
                        placeholder="0 or 1", max_width="150px",
                    ),
                    rx.button("Check AND", on_click=BooleanGateIntroState.check_and),
                ),
                rx.cond(
                    BooleanGateIntroState.and_feedback != "",
                    rx.callout(BooleanGateIntroState.and_feedback, icon="calculator"),
                    rx.box(),
                ),
                rx.text("A = 0 and B = 1. What is OR output A + B?"),
                rx.hstack(
                    rx.input(
                        value=BooleanGateIntroState.or_answer,
                        on_change=BooleanGateIntroState.set_or_answer,
                        placeholder="0 or 1", max_width="150px",
                    ),
                    rx.button("Check OR", on_click=BooleanGateIntroState.check_or),
                ),
                rx.cond(
                    BooleanGateIntroState.or_feedback != "",
                    rx.callout(BooleanGateIntroState.or_feedback, icon="calculator"),
                    rx.box(),
                ),
                rx.text("A = 0. What is NOT output A'?"),
                rx.hstack(
                    rx.input(
                        value=BooleanGateIntroState.not_answer,
                        on_change=BooleanGateIntroState.set_not_answer,
                        placeholder="0 or 1", max_width="150px",
                    ),
                    rx.button("Check NOT", on_click=BooleanGateIntroState.check_not),
                ),
                rx.cond(
                    BooleanGateIntroState.not_feedback != "",
                    rx.callout(BooleanGateIntroState.not_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "From gates to Boolean expressions",
                rx.text(
                    "A circuit can combine operations. For example, Y = A'B + C means: invert A, "
                    "AND A' with B, then OR that result with C."
                ),
                rx.code_block(
                    "A ─► NOT ─┐\n"
                    "          AND ─┐\n"
                    "B ─────────┘    OR ─► Y\n"
                    "C ──────────────┘",
                    language="markup",
                ),
                rx.callout(
                    "The expression and the circuit describe the same logical function.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Practise in BoolNexa",
                rx.text(
                    "Use the Simulator to test physical gate behaviour, then use Boolean Lab to "
                    "enter expressions and generate their truth tables."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Logic states", variant="soft"),
                    href="/academy/unit-2/logic-states-and-gates",
                ),
                rx.spacer(),
                rx.text("Path 02 · Lesson 2 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-2/nand-nor",
                ),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
