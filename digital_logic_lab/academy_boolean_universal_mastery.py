"""BoolNexa Academy Path 02 lessons 9 and 10."""

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


class BooleanUniversalMasteryState(rx.State):
    nand_not_answer: str = ""
    nand_not_feedback: str = ""
    nor_not_answer: str = ""
    nor_not_feedback: str = ""
    mastery_gate: str = ""
    mastery_simplify: str = ""
    mastery_rows: str = ""
    mastery_score: str = ""

    def set_mastery_gate(self, value: str) -> None:
        self.mastery_gate = value

    def set_mastery_rows(self, value: str) -> None:
        self.mastery_rows = value

    def set_mastery_simplify(self, value: str) -> None:
        self.mastery_simplify = value

    def set_nand_not_answer(self, value: str) -> None:
        self.nand_not_answer = value

    def set_nor_not_answer(self, value: str) -> None:
        self.nor_not_answer = value

    def check_nand_not(self):
        value = self.nand_not_answer.strip().upper().replace(" ", "")
        self.nand_not_feedback = (
            "Correct. NAND(A,A) = (AA)' = A'."
            if value in {"A'", "NOTA", "¬A"}
            else "Tie both NAND inputs to A: (AA)' = A'."
        )

    def check_nor_not(self):
        value = self.nor_not_answer.strip().upper().replace(" ", "")
        self.nor_not_feedback = (
            "Correct. NOR(A,A) = (A+A)' = A'."
            if value in {"A'", "NOTA", "¬A"}
            else "Tie both NOR inputs to A: (A+A)' = A'."
        )

    def check_mastery(self):
        score = 0
        if self.mastery_gate.strip().upper().replace(" ", "") in {"XOR", "XORGATE"}:
            score += 1
        if self.mastery_simplify.strip().upper().replace(" ", "") == "A":
            score += 1
        if self.mastery_rows.strip() == "16":
            score += 1

        if score == 3:
            self.mastery_score = "3/3 — Excellent. Path 02 mastery check complete."
        elif score == 2:
            self.mastery_score = "2/3 — Good. Review the one concept that needs correction."
        else:
            self.mastery_score = f"{score}/3 — Revisit the relevant lesson and try again."


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children, align="stretch", spacing="3",
        ),
        **PANEL,
    )


def universal_implementation_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 09", color_scheme="blue"),
            rx.heading("Universal-Gate Implementation", size="8"),
            rx.text(
                "Convert ordinary AND/OR/NOT networks into NAND-only or NOR-only implementations "
                "without changing the Boolean function.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Functional completeness",
                rx.text(
                    "NAND and NOR are universal because either gate family can reproduce NOT, AND and OR. "
                    "Once those operations are available, any Boolean function can be implemented."
                ),
                rx.code_block(
                    "NAND inverter: A NAND A = (AA)' = A'\n"
                    "NOR inverter:  A NOR A  = (A+A)' = A'",
                    language="markup",
                ),
            ),
            _section(
                "2", "NAND-only building blocks",
                rx.code_block(
                    "NOT:\n"
                    "A' = NAND(A,A)\n\n"
                    "AND:\n"
                    "AB = NAND(NAND(A,B), NAND(A,B))\n\n"
                    "OR (using De Morgan):\n"
                    "A+B = (A'B')'\n"
                    "    = NAND(NAND(A,A), NAND(B,B))",
                    language="markup",
                ),
                rx.callout(
                    "A NAND-NAND structure naturally implements many sum-of-products expressions.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "3", "NOR-only building blocks",
                rx.code_block(
                    "NOT:\n"
                    "A' = NOR(A,A)\n\n"
                    "OR:\n"
                    "A+B = NOR(NOR(A,B), NOR(A,B))\n\n"
                    "AND (using De Morgan):\n"
                    "AB = (A' + B')'\n"
                    "   = NOR(NOR(A,A), NOR(B,B))",
                    language="markup",
                ),
                rx.callout(
                    "A NOR-NOR structure naturally implements many product-of-sums expressions.",
                    icon="info",
                ),
            ),
            _section(
                "4", "De Morgan transformation",
                rx.text(
                    "De Morgan's theorems explain why complemented AND and OR structures can be exchanged."
                ),
                rx.code_block(
                    "(AB)' = A' + B'\n"
                    "(A+B)' = A'B'\n\n"
                    "When the complement crosses the operator, AND ↔ OR and each input is complemented.",
                    language="markup",
                ),
            ),
            _section(
                "5", "Interactive universal-gate check",
                rx.text("If both inputs of a NAND gate are connected to A, what is the output?"),
                rx.hstack(
                    rx.input(
                        value=BooleanUniversalMasteryState.nand_not_answer,
                        on_change=BooleanUniversalMasteryState.set_nand_not_answer,
                        placeholder="Expression", max_width="190px",
                    ),
                    rx.button("Check NAND", on_click=BooleanUniversalMasteryState.check_nand_not),
                ),
                rx.cond(
                    BooleanUniversalMasteryState.nand_not_feedback != "",
                    rx.callout(BooleanUniversalMasteryState.nand_not_feedback, icon="brain"),
                    rx.box(),
                ),
                rx.text("If both inputs of a NOR gate are connected to A, what is the output?"),
                rx.hstack(
                    rx.input(
                        value=BooleanUniversalMasteryState.nor_not_answer,
                        on_change=BooleanUniversalMasteryState.set_nor_not_answer,
                        placeholder="Expression", max_width="190px",
                    ),
                    rx.button("Check NOR", on_click=BooleanUniversalMasteryState.check_nor_not),
                ),
                rx.cond(
                    BooleanUniversalMasteryState.nor_not_feedback != "",
                    rx.callout(BooleanUniversalMasteryState.nor_not_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "Build and verify",
                rx.text(
                    "Choose a simple AND/OR/NOT function in Boolean Lab, verify its truth table, then recreate "
                    "the same function in the Simulator using only NAND gates. Repeat with NOR gates."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Simulator", variant="soft"), href="/"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Expression-to-circuit", variant="soft"),
                    href="/academy/unit-2/expression-to-circuit",
                ),
                rx.spacer(), rx.text("Path 02 · Lesson 9 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Final challenge →", variant="soft"), href="/academy/unit-2/mastery-challenge"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def boolean_mastery_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 10", color_scheme="green"),
            rx.heading("Boolean Algebra & Logic Gates Mastery", size="8"),
            rx.text(
                "Bring the entire Path 02 together: gate behaviour, Boolean algebra, truth tables, "
                "simplification and circuit design.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Path 02 review",
                rx.grid(
                    rx.callout("Logic states and truth tables", icon="circle-check"),
                    rx.callout("AND, OR, NOT, NAND and NOR", icon="circle-check"),
                    rx.callout("XOR, XNOR and parity", icon="circle-check"),
                    rx.callout("Boolean expressions and laws", icon="circle-check"),
                    rx.callout("De Morgan and simplification", icon="circle-check"),
                    rx.callout("Expression-to-circuit design", icon="circle-check"),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3",
                ),
            ),
            _section(
                "2", "Mastery challenge",
                rx.text("Answer these without opening the tools first."),
                rx.vstack(
                    rx.text("A. Which gate outputs 1 when two inputs are different?"),
                    rx.input(
                        value=BooleanUniversalMasteryState.mastery_gate,
                        on_change=BooleanUniversalMasteryState.set_mastery_gate,
                        placeholder="Gate name", max_width="260px",
                    ),
                    rx.text("B. Simplify A + AB."),
                    rx.input(
                        value=BooleanUniversalMasteryState.mastery_simplify,
                        on_change=BooleanUniversalMasteryState.set_mastery_simplify,
                        placeholder="Simplified expression", max_width="260px",
                    ),
                    rx.text("C. How many rows does a four-variable truth table contain?"),
                    rx.input(
                        value=BooleanUniversalMasteryState.mastery_rows,
                        on_change=BooleanUniversalMasteryState.set_mastery_rows,
                        placeholder="Rows", max_width="260px",
                    ),
                    rx.button("Check mastery score", on_click=BooleanUniversalMasteryState.check_mastery),
                    rx.cond(
                        BooleanUniversalMasteryState.mastery_score != "",
                        rx.callout(BooleanUniversalMasteryState.mastery_score, icon="trophy"),
                        rx.box(),
                    ),
                    align="start", spacing="3",
                ),
            ),
            _section(
                "3", "Practical challenge",
                rx.text(
                    "Design F = A'B + AC. First predict its truth table manually. Then use Boolean Lab "
                    "to verify the function and Circuit Generator to inspect the gate network."
                ),
                rx.hstack(
                    rx.link(rx.button("Verify in Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Generate Circuit", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            _section(
                "4", "Hardware challenge",
                rx.text(
                    "Recreate the same function in the Simulator. Test every A,B,C combination and make sure "
                    "the simulated output agrees with the truth table."
                ),
                rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
            ),
            _section(
                "5", "Path 02 complete",
                rx.callout(
                    "You have completed Boolean Algebra & Logic Gates. You can now describe logic as equations, "
                    "analyse it with truth tables, simplify it and turn it into circuits.",
                    icon="graduation-cap", color_scheme="green",
                ),
                rx.text(
                    "The next Academy path can build on this foundation with combinational logic design, "
                    "including adders, subtractors, multiplexers, decoders and comparators."
                ),
                rx.link(
                    rx.button("Return to Academy →", size="3", color_scheme="blue"),
                    href="/academy",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Universal gates", variant="soft"),
                    href="/academy/unit-2/universal-implementation",
                ),
                rx.spacer(), rx.text("Path 02 · Lesson 10 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Academy home", variant="soft"), href="/academy"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
