"""BoolNexa Academy Path 02 lessons 3 and 4."""

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


class UniversalXorState(rx.State):
    nand_answer: str = ""
    nand_feedback: str = ""
    nor_answer: str = ""
    nor_feedback: str = ""
    xor_answer: str = ""
    xor_feedback: str = ""
    xnor_answer: str = ""
    xnor_feedback: str = ""

    def set_nand_answer(self, value: str) -> None:
        self.nand_answer = value

    def set_nor_answer(self, value: str) -> None:
        self.nor_answer = value

    def set_xnor_answer(self, value: str) -> None:
        self.xnor_answer = value

    def set_xor_answer(self, value: str) -> None:
        self.xor_answer = value

    def check_nand(self):
        self.nand_feedback = (
            "Correct. NAND(1,1) = 0 because NAND is the complement of AND."
            if self.nand_answer.strip() == "0"
            else "Try again: first evaluate AND(1,1), then invert the result."
        )

    def check_nor(self):
        self.nor_feedback = (
            "Correct. Tying both NOR inputs to A gives NOT A."
            if self.nor_answer.strip().replace(" ", "").upper() in {"A'", "NOTA", "¬A"}
            else "Tie both inputs together: (A + A)' = A'."
        )

    def check_xor(self):
        self.xor_feedback = (
            "Correct. XOR is 1 when the two inputs are different."
            if self.xor_answer.strip() == "1"
            else "XOR(1,0) is 1 because exactly one input is HIGH."
        )

    def check_xnor(self):
        self.xnor_feedback = (
            "Correct. XNOR is 1 when the two inputs are equal."
            if self.xnor_answer.strip() == "1"
            else "XNOR(1,1) is 1 because both inputs have the same state."
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children, align="stretch", spacing="3",
        ),
        **PANEL,
    )


def _truth(headers, rows):
    return rx.table.root(
        rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),
        rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in row]) for row in rows]),
        width="100%", variant="surface",
    )


def nand_nor_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 03", color_scheme="blue"),
            rx.heading("NAND & NOR — Universal Gates", size="8"),
            rx.text(
                "NAND and NOR are complemented versions of AND and OR. More importantly, "
                "either gate type can be used by itself to construct every Boolean function.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "NAND gate",
                rx.text("NAND means NOT-AND. Its output is 0 only when every input is 1."),
                rx.code_block("Y = (AB)'", language="markup"),
                _truth(
                    ("A", "B", "AND", "NAND"),
                    (("0","0","0","1"),("0","1","0","1"),("1","0","0","1"),("1","1","1","0")),
                ),
            ),
            _section(
                "2", "NOR gate",
                rx.text("NOR means NOT-OR. Its output is 1 only when every input is 0."),
                rx.code_block("Y = (A + B)'", language="markup"),
                _truth(
                    ("A", "B", "OR", "NOR"),
                    (("0","0","0","1"),("0","1","1","0"),("1","0","1","0"),("1","1","1","0")),
                ),
            ),
            _section(
                "3", "Why are they universal?",
                rx.text(
                    "A gate is functionally complete when we can build NOT, AND and OR from that gate alone. "
                    "Because NOT, AND and OR can express any Boolean function, NAND alone or NOR alone can "
                    "implement any combinational Boolean circuit."
                ),
                rx.code_block(
                    "NAND-only:\n"
                    "NOT A = (AA)'\n"
                    "A AND B = [(AB)'(AB)']'\n"
                    "A OR B = (AA)' NAND (BB)'\n\n"
                    "NOR-only:\n"
                    "NOT A = (A + A)'\n"
                    "A OR B = [(A+B)' + (A+B)']'\n"
                    "A AND B = (A+A)' NOR (B+B)'",
                    language="markup",
                ),
                rx.callout(
                    "Universal-gate implementations are important when a design must use a restricted gate family.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "4", "Interactive check",
                rx.text("What is NAND(1,1)?"),
                rx.hstack(
                    rx.input(value=UniversalXorState.nand_answer, on_change=UniversalXorState.set_nand_answer,
                             placeholder="0 or 1", max_width="150px"),
                    rx.button("Check NAND", on_click=UniversalXorState.check_nand),
                ),
                rx.cond(UniversalXorState.nand_feedback != "",
                        rx.callout(UniversalXorState.nand_feedback, icon="brain"), rx.box()),
                rx.text("If both inputs of a NOR gate are connected to A, what Boolean result is produced?"),
                rx.hstack(
                    rx.input(value=UniversalXorState.nor_answer, on_change=UniversalXorState.set_nor_answer,
                             placeholder="e.g. A'", max_width="180px"),
                    rx.button("Check NOR", on_click=UniversalXorState.check_nor),
                ),
                rx.cond(UniversalXorState.nor_feedback != "",
                        rx.callout(UniversalXorState.nor_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Build it in BoolNexa",
                rx.text(
                    "Use the Simulator to construct a NOT gate using only NAND, then repeat using only NOR. "
                    "Use Boolean Lab to compare the resulting truth tables."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← AND, OR & NOT", variant="soft"), href="/academy/unit-2/and-or-not"),
                rx.spacer(), rx.text("Path 02 · Lesson 3 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/xor-xnor"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def xor_xnor_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 04", color_scheme="blue"),
            rx.heading("XOR & XNOR Gates", size="8"),
            rx.text(
                "XOR detects difference and XNOR detects equality. These gates are central to arithmetic, "
                "comparison and parity circuits.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Exclusive-OR (XOR)",
                rx.text("For two inputs, XOR outputs 1 when the inputs are different."),
                rx.code_block("Y = A ⊕ B = A'B + AB'", language="markup"),
                _truth(
                    ("A","B","A ⊕ B"),
                    (("0","0","0"),("0","1","1"),("1","0","1"),("1","1","0")),
                ),
                rx.text("A two-input XOR can therefore be read as a 'different?' detector."),
            ),
            _section(
                "2", "Exclusive-NOR (XNOR)",
                rx.text("XNOR is the complement of XOR and outputs 1 when the inputs are equal."),
                rx.code_block("Y = (A ⊕ B)' = AB + A'B'", language="markup"),
                _truth(
                    ("A","B","A XNOR B"),
                    (("0","0","1"),("0","1","0"),("1","0","0"),("1","1","1")),
                ),
                rx.text("A two-input XNOR can therefore be used as a one-bit equality detector."),
            ),
            _section(
                "3", "XOR in binary arithmetic",
                rx.text(
                    "A half adder adds two one-bit numbers. Its SUM output is XOR and its CARRY output is AND."
                ),
                rx.code_block(
                    "SUM   = A ⊕ B\n"
                    "CARRY = AB\n\n"
                    "A B | SUM CARRY\n"
                    "0 0 |  0    0\n"
                    "0 1 |  1    0\n"
                    "1 0 |  1    0\n"
                    "1 1 |  0    1",
                    language="markup",
                ),
            ),
            _section(
                "4", "XOR and parity",
                rx.text(
                    "XOR chains are useful for parity because the output tracks whether an odd number "
                    "of input bits are 1. Parity can help detect certain transmission or storage errors."
                ),
                rx.callout(
                    "Parity can detect errors, but a single parity bit cannot identify which bit changed "
                    "and cannot detect every possible multi-bit error.",
                    icon="info",
                ),
            ),
            _section(
                "5", "Interactive check",
                rx.text("What is XOR(1,0)?"),
                rx.hstack(
                    rx.input(value=UniversalXorState.xor_answer, on_change=UniversalXorState.set_xor_answer,
                             placeholder="0 or 1", max_width="150px"),
                    rx.button("Check XOR", on_click=UniversalXorState.check_xor),
                ),
                rx.cond(UniversalXorState.xor_feedback != "",
                        rx.callout(UniversalXorState.xor_feedback, icon="calculator"), rx.box()),
                rx.text("What is XNOR(1,1)?"),
                rx.hstack(
                    rx.input(value=UniversalXorState.xnor_answer, on_change=UniversalXorState.set_xnor_answer,
                             placeholder="0 or 1", max_width="150px"),
                    rx.button("Check XNOR", on_click=UniversalXorState.check_xnor),
                ),
                rx.cond(UniversalXorState.xnor_feedback != "",
                        rx.callout(UniversalXorState.xnor_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "6", "Practise with the real tools",
                rx.text(
                    "Build XOR/XNOR examples in the Simulator, then enter A'B + AB' in Boolean Lab and "
                    "confirm that its truth table matches XOR."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← NAND & NOR", variant="soft"), href="/academy/unit-2/nand-nor"),
                rx.spacer(), rx.text("Path 02 · Lesson 4 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/boolean-expressions"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
