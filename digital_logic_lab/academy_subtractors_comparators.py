"""BoolNexa Academy Path 04 lessons 3 and 4: subtractors and comparators."""

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


class SubtractorComparatorState(rx.State):
    half_d: str = ""
    half_b: str = ""
    half_feedback: str = ""
    full_inputs: str = ""
    full_feedback: str = ""
    compare_answer: str = ""
    compare_feedback: str = ""
    equality_answer: str = ""
    equality_feedback: str = ""

    def set_compare_answer(self, value: str) -> None:
        self.compare_answer = value

    def set_equality_answer(self, value: str) -> None:
        self.equality_answer = value

    def set_full_inputs(self, value: str) -> None:
        self.full_inputs = value

    def set_half_b(self, value: str) -> None:
        self.half_b = value

    def set_half_d(self, value: str) -> None:
        self.half_d = value

    def check_half_subtractor(self):
        if self.half_d.strip() == "1" and self.half_b.strip() == "1":
            self.half_feedback = "Correct. 0 − 1 needs a borrow: Difference=1 and Borrow=1."
        else:
            self.half_feedback = "For 0 − 1, borrow from the next higher bit: binary 10 − 1 = 1."

    def check_full_inputs(self):
        self.full_feedback = (
            "Correct. A full subtractor uses A, B and borrow-in Bin."
            if self.full_inputs.strip() == "3"
            else "Count A, B and Bin."
        )

    def check_compare(self):
        value = self.compare_answer.strip().replace(" ", "")
        self.compare_feedback = (
            "Correct. Binary 101 (5) is greater than 011 (3), so A>B."
            if value in {"A>B", ">", "Aisgreater"}
            else "Convert or compare from the most significant bit: 101₂=5 and 011₂=3."
        )

    def check_equality(self):
        value = self.equality_answer.strip().lower().replace(" ", "")
        self.equality_feedback = (
            "Correct. XNOR is 1 when its two input bits are equal."
            if value in {"xnor", "equivalence", "equivalencegate"}
            else "Which gate outputs 1 for 00 and 11?"
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children, align="stretch", spacing="3",
        ),
        **PANEL,
    )


def _table(headers, rows):
    return rx.table.root(
        rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),
        rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in row]) for row in rows]),
        width="100%", variant="surface",
    )


def subtractors_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 03", color_scheme="blue"),
            rx.heading("Half Subtractors & Full Subtractors", size="8"),
            rx.text(
                "Subtraction circuits calculate a difference and, when necessary, a borrow. "
                "Their structure mirrors the progression from half adders to full adders.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Half subtractor",
                rx.text("A half subtractor computes A − B using two one-bit inputs."),
                _table(
                    ("A", "B", "Difference D", "Borrow Bout"),
                    (
                        ("0", "0", "0", "0"),
                        ("0", "1", "1", "1"),
                        ("1", "0", "1", "0"),
                        ("1", "1", "0", "0"),
                    ),
                ),
                rx.code_block("D = A ⊕ B\nBout = A'B", language="markup"),
            ),
            _section(
                "2", "Why borrowing occurs",
                rx.text(
                    "When A=0 and B=1, the current bit cannot subtract 1 directly. "
                    "It borrows one unit from the next higher binary position."
                ),
                rx.code_block("0 − 1  → borrow\n10₂ − 1₂ = 1₂\nDifference=1, Borrow=1", language="markup"),
                rx.text("For A=0 and B=1, enter Difference and Borrow."),
                rx.hstack(
                    rx.input(value=SubtractorComparatorState.half_d,
                             on_change=SubtractorComparatorState.set_half_d,
                             placeholder="Difference", max_width="140px"),
                    rx.input(value=SubtractorComparatorState.half_b,
                             on_change=SubtractorComparatorState.set_half_b,
                             placeholder="Borrow", max_width="140px"),
                    rx.button("Check", on_click=SubtractorComparatorState.check_half_subtractor),
                    wrap="wrap",
                ),
                rx.cond(SubtractorComparatorState.half_feedback != "",
                        rx.callout(SubtractorComparatorState.half_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "3", "Full subtractor",
                rx.text(
                    "A full subtractor includes borrow-in Bin from a less-significant stage. "
                    "It produces Difference D and borrow-out Bout."
                ),
                _table(
                    ("A","B","Bin","D","Bout"),
                    (
                        ("0","0","0","0","0"),
                        ("0","0","1","1","1"),
                        ("0","1","0","1","1"),
                        ("0","1","1","0","1"),
                        ("1","0","0","1","0"),
                        ("1","0","1","0","0"),
                        ("1","1","0","0","0"),
                        ("1","1","1","1","1"),
                    ),
                ),
                rx.code_block(
                    "D = A ⊕ B ⊕ Bin\n"
                    "Bout = A'B + A'Bin + B·Bin",
                    language="markup",
                ),
                rx.text("How many one-bit inputs does a full subtractor have?"),
                rx.hstack(
                    rx.input(value=SubtractorComparatorState.full_inputs,
                             on_change=SubtractorComparatorState.set_full_inputs,
                             placeholder="Inputs", max_width="140px"),
                    rx.button("Check", on_click=SubtractorComparatorState.check_full_inputs),
                ),
                rx.cond(SubtractorComparatorState.full_feedback != "",
                        rx.callout(SubtractorComparatorState.full_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "4", "Multi-bit subtraction",
                rx.text(
                    "Full subtractors can be cascaded. Each stage's borrow-out feeds the next more-significant stage's borrow-in."
                ),
                rx.code_block(
                    "LSB                                      MSB\n"
                    "[FS0] ─Bout→ [FS1] ─Bout→ [FS2] ─Bout→ [FS3]\n"
                    "  ↑             ↑             ↑             ↑\n"
                    " A0,B0         A1,B1         A2,B2         A3,B3",
                    language="markup",
                ),
            ),
            _section(
                "5", "Adder-subtractor idea",
                rx.text(
                    "Practical arithmetic units often reuse adder hardware for subtraction by using two's-complement arithmetic: "
                    "A − B = A + (B' + 1). XOR gates can conditionally invert B while the initial carry-in supplies the +1."
                ),
                rx.code_block(
                    "Mode M=0: A + B\n"
                    "Mode M=1: A + B' + 1\n\n"
                    "B input to adder = B ⊕ M\n"
                    "Initial Cin = M",
                    language="markup",
                ),
                rx.callout(
                    "This reuse of hardware is an important step toward understanding arithmetic logic units (ALUs).",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Verify with BoolNexa",
                rx.text("Generate the half-subtractor equations and verify the four input combinations."),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Adders", variant="soft"), href="/academy/unit-4/adders"),
                rx.spacer(), rx.text("Path 04 · Lesson 3", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/comparators"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def comparators_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 04", color_scheme="blue"),
            rx.heading("Digital Comparators", size="8"),
            rx.text(
                "A magnitude comparator determines whether one binary value is greater than, equal to or less than another.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "One-bit comparison",
                _table(
                    ("A","B","A>B","A=B","A<B"),
                    (
                        ("0","0","0","1","0"),
                        ("0","1","0","0","1"),
                        ("1","0","1","0","0"),
                        ("1","1","0","1","0"),
                    ),
                ),
                rx.code_block(
                    "A > B : G = AB'\n"
                    "A = B : E = A XNOR B = A'B' + AB\n"
                    "A < B : L = A'B",
                    language="markup",
                ),
            ),
            _section(
                "2", "Equality uses XNOR",
                rx.text(
                    "Two bits are equal when they are both 0 or both 1. XNOR captures exactly this behaviour."
                ),
                rx.text("Which gate is naturally used for bit equality?"),
                rx.hstack(
                    rx.input(value=SubtractorComparatorState.equality_answer,
                             on_change=SubtractorComparatorState.set_equality_answer,
                             placeholder="Gate", max_width="180px"),
                    rx.button("Check", on_click=SubtractorComparatorState.check_equality),
                ),
                rx.cond(SubtractorComparatorState.equality_feedback != "",
                        rx.callout(SubtractorComparatorState.equality_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "Multi-bit comparison starts at the MSB",
                rx.text(
                    "For unsigned binary numbers, compare the most significant bits first. "
                    "Only when those bits are equal do lower positions decide the result."
                ),
                rx.code_block(
                    "A = 101₂\nB = 011₂\n\n"
                    "MSB: A2=1, B2=0\n"
                    "Decision is immediate: A > B",
                    language="markup",
                ),
                rx.text("Compare A=101₂ and B=011₂. Enter A>B, A=B or A<B."),
                rx.hstack(
                    rx.input(value=SubtractorComparatorState.compare_answer,
                             on_change=SubtractorComparatorState.set_compare_answer,
                             placeholder="Relationship", max_width="180px"),
                    rx.button("Check", on_click=SubtractorComparatorState.check_compare),
                ),
                rx.cond(SubtractorComparatorState.compare_feedback != "",
                        rx.callout(SubtractorComparatorState.compare_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "Two-bit equality",
                rx.text(
                    "For A=A1A0 and B=B1B0, both corresponding bit pairs must match."
                ),
                rx.code_block(
                    "E1 = A1 XNOR B1\n"
                    "E0 = A0 XNOR B0\n"
                    "A = B when E = E1·E0",
                    language="markup",
                ),
            ),
            _section(
                "5", "Where comparators are used",
                rx.unordered_list(
                    rx.list_item("Processors and ALUs for conditional decisions."),
                    rx.list_item("Digital control systems for thresholds and limits."),
                    rx.list_item("Address/tag matching and equality detection."),
                    rx.list_item("Sorting, priority and measurement systems."),
                ),
                rx.callout(
                    "Unsigned and signed comparison are not always identical. Signed two's-complement values require correct sign-aware interpretation.",
                    icon="info",
                ),
            ),
            _section(
                "6", "Build the one-bit comparator",
                rx.text(
                    "Use the three comparator equations in BoolNexa and verify that exactly one of G, E or L is active for each input pair."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Subtractors", variant="soft"), href="/academy/unit-4/subtractors"),
                rx.spacer(), rx.text("Path 04 · Lesson 4", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/multiplexers"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
