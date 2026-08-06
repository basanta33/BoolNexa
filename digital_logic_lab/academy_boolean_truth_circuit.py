"""BoolNexa Academy Path 02 lessons 7 and 8."""

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


class TruthCircuitState(rx.State):
    rows_answer: str = ""
    rows_feedback: str = ""
    output_answer: str = ""
    output_feedback: str = ""
    gate_answer: str = ""
    gate_feedback: str = ""
    stage_answer: str = ""
    stage_feedback: str = ""

    def set_gate_answer(self, value: str) -> None:
        self.gate_answer = value

    def set_output_answer(self, value: str) -> None:
        self.output_answer = value

    def set_rows_answer(self, value: str) -> None:
        self.rows_answer = value

    def set_stage_answer(self, value: str) -> None:
        self.stage_answer = value

    def check_rows(self):
        self.rows_feedback = (
            "Correct. Three variables give 2³ = 8 input combinations."
            if self.rows_answer.strip() == "8"
            else "Use 2ⁿ combinations for n Boolean variables."
        )

    def check_output(self):
        self.output_feedback = (
            "Correct. For A=1, B=0, C=1: AB=0 and A'C=0, so F=0."
            if self.output_answer.strip() == "0"
            else "Evaluate each product term first: AB and A'C, then OR the results."
        )

    def check_gate(self):
        value = self.gate_answer.strip().upper().replace(" ", "")
        self.gate_feedback = (
            "Correct. A' requires a NOT gate before the AND stage."
            if value in {"NOT", "NOTGATE", "INVERTER"}
            else "Look at A'. The complement mark tells you which operation must happen first."
        )

    def check_stage(self):
        value = self.stage_answer.strip().upper().replace(" ", "")
        self.stage_feedback = (
            "Correct. The two product terms are combined by an OR gate."
            if value in {"OR", "ORGATE"}
            else "The '+' in AB + A'C represents Boolean OR."
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


def truth_tables_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 07", color_scheme="blue"),
            rx.heading("Truth Tables & Function Analysis", size="8"),
            rx.text(
                "A truth table is a complete behavioural specification of a Boolean function. "
                "Learn how to construct one systematically and use it to verify expressions.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "How many rows?",
                rx.text(
                    "For n input variables there are 2ⁿ possible binary input combinations. "
                    "Every combination must appear exactly once."
                ),
                rx.code_block(
                    "1 variable  → 2¹ = 2 rows\n"
                    "2 variables → 2² = 4 rows\n"
                    "3 variables → 2³ = 8 rows\n"
                    "4 variables → 2⁴ = 16 rows",
                    language="markup",
                ),
                rx.text("How many input rows are required for A, B and C?"),
                rx.hstack(
                    rx.input(value=TruthCircuitState.rows_answer, on_change=TruthCircuitState.set_rows_answer,
                             placeholder="Rows", max_width="150px"),
                    rx.button("Check", on_click=TruthCircuitState.check_rows),
                ),
                rx.cond(TruthCircuitState.rows_feedback != "",
                        rx.callout(TruthCircuitState.rows_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "Build a table systematically",
                rx.text("For three variables, count from binary 000 through 111."),
                _truth(
                    ("A","B","C"),
                    (("0","0","0"),("0","0","1"),("0","1","0"),("0","1","1"),
                     ("1","0","0"),("1","0","1"),("1","1","0"),("1","1","1")),
                ),
                rx.callout(
                    "Using binary counting prevents missing or duplicating an input combination.",
                    icon="info",
                ),
            ),
            _section(
                "3", "Analyse F = AB + A'C",
                rx.text("Create intermediate columns before calculating the final OR."),
                _truth(
                    ("A","B","C","AB","A'","A'C","F"),
                    (
                        ("0","0","0","0","1","0","0"),
                        ("0","0","1","0","1","1","1"),
                        ("0","1","0","0","1","0","0"),
                        ("0","1","1","0","1","1","1"),
                        ("1","0","0","0","0","0","0"),
                        ("1","0","1","0","0","0","0"),
                        ("1","1","0","1","0","0","1"),
                        ("1","1","1","1","0","0","1"),
                    ),
                ),
                rx.text("For A=1, B=0, C=1, what is F?"),
                rx.hstack(
                    rx.input(value=TruthCircuitState.output_answer, on_change=TruthCircuitState.set_output_answer,
                             placeholder="0 or 1", max_width="150px"),
                    rx.button("Check", on_click=TruthCircuitState.check_output),
                ),
                rx.cond(TruthCircuitState.output_feedback != "",
                        rx.callout(TruthCircuitState.output_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "What can a truth table prove?",
                rx.text(
                    "If two Boolean expressions have identical output columns for every possible input, "
                    "they are logically equivalent. This is a powerful way to verify algebraic simplification."
                ),
                rx.code_block(
                    "Example:\n"
                    "F₁ = A + AB\n"
                    "F₂ = A\n\n"
                    "If F₁ and F₂ match on every row, the expressions are equivalent.",
                    language="markup",
                ),
            ),
            _section(
                "5", "From output rows to minterms",
                rx.text(
                    "Rows where F=1 identify the input combinations that make the function true. "
                    "These rows can be written as minterms and later placed on a Karnaugh map."
                ),
                rx.code_block(
                    "For A,B,C = 0,0,1:\n"
                    "minterm = A'B'C\n\n"
                    "For A,B,C = 1,1,0:\n"
                    "minterm = ABC'",
                    language="markup",
                ),
            ),
            _section(
                "6", "Generate and verify in BoolNexa",
                rx.text(
                    "Enter AB + A'C in Boolean Lab and compare BoolNexa's generated truth table "
                    "with the manual table above. Then inspect its K-map and simplified result."
                ),
                rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
            ),
            rx.hstack(
                rx.link(rx.button("← Boolean laws", variant="soft"), href="/academy/unit-2/boolean-laws"),
                rx.spacer(), rx.text("Path 02 · Lesson 7 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/expression-to-circuit"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def expression_to_circuit_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 08", color_scheme="blue"),
            rx.heading("Expression-to-Circuit Design", size="8"),
            rx.text(
                "Turn Boolean algebra into a gate network methodically. "
                "The safest approach is to translate the expression one operation at a time.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Design workflow",
                rx.code_block(
                    "1. Identify every input variable.\n"
                    "2. Generate required complements with NOT gates.\n"
                    "3. Build AND/product terms.\n"
                    "4. Build OR/sum stages.\n"
                    "5. Connect the final output.\n"
                    "6. Verify the circuit against the truth table.",
                    language="markup",
                ),
            ),
            _section(
                "2", "Worked design: F = AB + A'C",
                rx.text("First identify the operations embedded in the expression."),
                rx.code_block(
                    "A'       → NOT A\n"
                    "AB       → AND(A,B)\n"
                    "A'C      → AND(A',C)\n"
                    "AB+A'C   → OR(the two product terms)",
                    language="markup",
                ),
                rx.code_block(
                    "A ──────────► AND ─────┐\n"
                    "B ──────────►     AB   │\n"
                    "                       ├─► OR ─► F\n"
                    "A ─► NOT ─► AND ───────┘\n"
                    "C ─────────►     A'C",
                    language="markup",
                ),
            ),
            _section(
                "3", "Identify the gates",
                rx.text("Which gate is needed first to create A' in F = AB + A'C?"),
                rx.hstack(
                    rx.input(value=TruthCircuitState.gate_answer, on_change=TruthCircuitState.set_gate_answer,
                             placeholder="Gate", max_width="180px"),
                    rx.button("Check", on_click=TruthCircuitState.check_gate),
                ),
                rx.cond(TruthCircuitState.gate_feedback != "",
                        rx.callout(TruthCircuitState.gate_feedback, icon="brain"), rx.box()),
                rx.text("Which gate combines AB and A'C at the final stage?"),
                rx.hstack(
                    rx.input(value=TruthCircuitState.stage_answer, on_change=TruthCircuitState.set_stage_answer,
                             placeholder="Gate", max_width="180px"),
                    rx.button("Check", on_click=TruthCircuitState.check_stage),
                ),
                rx.cond(TruthCircuitState.stage_feedback != "",
                        rx.callout(TruthCircuitState.stage_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "4", "Simplify before building",
                rx.text(
                    "A logically equivalent simplified expression can require fewer gates. "
                    "For example, A + AB simplifies to A, eliminating the unnecessary AND and OR network."
                ),
                rx.code_block(
                    "Before: F = A + AB\n"
                    "Boolean law: A + AB = A\n"
                    "After:  F = A",
                    language="markup",
                ),
                rx.callout(
                    "Always verify that the simplified expression has the same truth table before replacing the original circuit.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "5", "Generate the circuit automatically",
                rx.text(
                    "Use BoolNexa Circuit Generator with AB + A'C. Compare the generated network with "
                    "the manual design, and inspect how each expression term maps to gates."
                ),
                rx.link(
                    rx.button("Open Circuit Generator", color_scheme="blue"),
                    href="/tools/circuit",
                    align_self="flex-start",
                ),
            ),
            _section(
                "6", "Then test it as a circuit",
                rx.text(
                    "Recreate the network in the Simulator using switches, NOT/AND/OR gates and an output indicator. "
                    "Test all eight A,B,C combinations and compare them with the truth table from Lesson 7."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Truth tables", variant="soft"), href="/academy/unit-2/truth-tables"),
                rx.spacer(), rx.text("Path 02 · Lesson 8 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/universal-implementation"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
