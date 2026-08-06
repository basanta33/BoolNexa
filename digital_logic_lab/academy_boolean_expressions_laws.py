"""BoolNexa Academy Path 02 lessons 5 and 6."""

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


class BooleanExpressionsLawsState(rx.State):
    expression_answer: str = ""
    expression_feedback: str = ""
    precedence_answer: str = ""
    precedence_feedback: str = ""
    law_answer: str = ""
    law_feedback: str = ""
    simplify_answer: str = ""
    simplify_feedback: str = ""

    def set_expression_answer(self, value: str) -> None:
        self.expression_answer = value

    def set_law_answer(self, value: str) -> None:
        self.law_answer = value

    def set_precedence_answer(self, value: str) -> None:
        self.precedence_answer = value

    def set_simplify_answer(self, value: str) -> None:
        self.simplify_answer = value

    def check_expression(self):
        value = self.expression_answer.strip().upper().replace(" ", "")
        self.expression_feedback = (
            "Correct. NOT A is A', AND with B gives A'B, then OR C gives A'B + C."
            if value in {"A'B+C", "A̅B+C"}
            else "Build it operation by operation: NOT A → A', AND B → A'B, then OR C."
        )

    def check_precedence(self):
        value = self.precedence_answer.strip()
        self.precedence_feedback = (
            "Correct. Complement is evaluated before AND, and AND before OR."
            if value == "1"
            else "For A=0, B=1, C=0: A'=1, then A'B=1, then 1+C=1."
        )

    def check_law(self):
        value = self.law_answer.strip().upper().replace(" ", "")
        self.law_feedback = (
            "Correct. A + AB = A by the absorption law."
            if value == "A"
            else "Factor A: A + AB = A(1 + B) = A."
        )

    def check_simplify(self):
        value = self.simplify_answer.strip().upper().replace(" ", "")
        self.simplify_feedback = (
            "Correct. AB + AB' = A(B + B') = A."
            if value == "A"
            else "Factor A, then use the complement law B + B' = 1."
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children, align="stretch", spacing="3",
        ),
        **PANEL,
    )


def boolean_expressions_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 05", color_scheme="blue"),
            rx.heading("Reading & Writing Boolean Expressions", size="8"),
            rx.text(
                "Translate between words, Boolean notation and gate networks. "
                "A Boolean expression is a compact mathematical description of a digital circuit.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The notation",
                rx.code_block(
                    "NOT A       → A'\n"
                    "A AND B     → AB or A·B\n"
                    "A OR B      → A + B\n"
                    "A XOR B     → A ⊕ B\n\n"
                    "Example: Y = A'B + C",
                    language="markup",
                ),
                rx.text(
                    "Variables represent logic signals. A complement mark applies to the variable "
                    "or grouped expression immediately associated with it."
                ),
            ),
            _section(
                "2", "Order of operations",
                rx.text(
                    "Unless parentheses change the order, Boolean expressions are normally evaluated "
                    "with complement first, then AND, then OR."
                ),
                rx.code_block(
                    "Y = A'B + C\n\n"
                    "1. A'       → invert A\n"
                    "2. A'B      → AND A' with B\n"
                    "3. A'B + C  → OR that result with C",
                    language="markup",
                ),
                rx.callout(
                    "Parentheses make intent explicit: (A + B)C is different from A + BC.",
                    icon="info",
                ),
            ),
            _section(
                "3", "Words → expression",
                rx.text("Statement: 'Y is true when NOT A AND B is true, OR when C is true.'"),
                rx.code_block("NOT A → A'\nA' AND B → A'B\nA'B OR C → Y = A'B + C", language="markup"),
                rx.text("Now write the final expression yourself."),
                rx.hstack(
                    rx.input(
                        value=BooleanExpressionsLawsState.expression_answer,
                        on_change=BooleanExpressionsLawsState.set_expression_answer,
                        placeholder="Expression",
                        max_width="240px",
                    ),
                    rx.button("Check", on_click=BooleanExpressionsLawsState.check_expression),
                ),
                rx.cond(
                    BooleanExpressionsLawsState.expression_feedback != "",
                    rx.callout(BooleanExpressionsLawsState.expression_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "4", "Evaluate an expression",
                rx.text("For Y = A'B + C, calculate Y when A=0, B=1 and C=0."),
                rx.hstack(
                    rx.input(
                        value=BooleanExpressionsLawsState.precedence_answer,
                        on_change=BooleanExpressionsLawsState.set_precedence_answer,
                        placeholder="0 or 1",
                        max_width="150px",
                    ),
                    rx.button("Check", on_click=BooleanExpressionsLawsState.check_precedence),
                ),
                rx.cond(
                    BooleanExpressionsLawsState.precedence_feedback != "",
                    rx.callout(BooleanExpressionsLawsState.precedence_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Expression → circuit",
                rx.code_block(
                    "Y = A'B + C\n\n"
                    "A ─► NOT ─┐\n"
                    "          AND ─┐\n"
                    "B ─────────┘    OR ─► Y\n"
                    "C ──────────────┘",
                    language="markup",
                ),
                rx.text(
                    "Each operation becomes a gate or gate stage. More complex expressions are built "
                    "using exactly the same principle."
                ),
            ),
            _section(
                "6", "Use the real BoolNexa tools",
                rx.text(
                    "Enter A'B + C in Boolean Lab and inspect its truth table. Then send or recreate "
                    "the expression in Circuit Generator to compare the equation with its gate network."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← XOR & XNOR", variant="soft"), href="/academy/unit-2/xor-xnor"),
                rx.spacer(), rx.text("Path 02 · Lesson 5 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/boolean-laws"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def boolean_laws_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 02 · LESSON 06", color_scheme="blue"),
            rx.heading("Boolean Laws & Simplification", size="8"),
            rx.text(
                "Boolean laws let you rewrite a function without changing its truth table. "
                "Good simplification can reduce gate count, wiring and logic depth.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Core Boolean laws",
                rx.code_block(
                    "Identity:       A + 0 = A        A·1 = A\n"
                    "Null:           A + 1 = 1        A·0 = 0\n"
                    "Idempotent:     A + A = A        A·A = A\n"
                    "Complement:     A + A' = 1       A·A' = 0\n"
                    "Involution:     (A')' = A\n"
                    "Commutative:    A + B = B + A    AB = BA\n"
                    "Associative:    A+(B+C)=(A+B)+C  A(BC)=(AB)C\n"
                    "Distributive:   A(B+C)=AB+AC     A+BC=(A+B)(A+C)\n"
                    "Absorption:     A + AB = A       A(A+B) = A",
                    language="markup",
                ),
            ),
            _section(
                "2", "De Morgan's theorems",
                rx.text(
                    "De Morgan's theorems are especially important when converting between AND/OR "
                    "networks and NAND/NOR implementations."
                ),
                rx.code_block(
                    "(AB)' = A' + B'\n"
                    "(A + B)' = A'B'",
                    language="markup",
                ),
                rx.callout(
                    "When a complement crosses a grouping boundary, AND changes to OR and OR changes to AND.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "3", "Worked simplification",
                rx.code_block(
                    "F = A + AB\n"
                    "  = A(1 + B)      factor A\n"
                    "  = A·1           because 1 + B = 1\n"
                    "  = A",
                    language="markup",
                ),
                rx.text("Simplify A + AB."),
                rx.hstack(
                    rx.input(
                        value=BooleanExpressionsLawsState.law_answer,
                        on_change=BooleanExpressionsLawsState.set_law_answer,
                        placeholder="Simplified result",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=BooleanExpressionsLawsState.check_law),
                ),
                rx.cond(
                    BooleanExpressionsLawsState.law_feedback != "",
                    rx.callout(BooleanExpressionsLawsState.law_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "4", "Factor before simplifying",
                rx.code_block(
                    "F = AB + AB'\n"
                    "  = A(B + B')\n"
                    "  = A(1)\n"
                    "  = A",
                    language="markup",
                ),
                rx.text("Now simplify AB + AB'."),
                rx.hstack(
                    rx.input(
                        value=BooleanExpressionsLawsState.simplify_answer,
                        on_change=BooleanExpressionsLawsState.set_simplify_answer,
                        placeholder="Simplified result",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=BooleanExpressionsLawsState.check_simplify),
                ),
                rx.cond(
                    BooleanExpressionsLawsState.simplify_feedback != "",
                    rx.callout(BooleanExpressionsLawsState.simplify_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Why verify simplification?",
                rx.text(
                    "Two expressions are equivalent only if they produce the same output for every input combination. "
                    "A truth table provides a direct verification."
                ),
                rx.code_block(
                    "Original:   AB + AB'\n"
                    "Simplified: A\n\n"
                    "Both must produce identical outputs for every A,B combination.",
                    language="markup",
                ),
            ),
            _section(
                "6", "Simplify with BoolNexa",
                rx.text(
                    "Enter expressions such as A + AB and AB + AB' into Boolean Lab. Compare the original "
                    "truth table, simplified expression and K-map. Then inspect the simplified implementation "
                    "in Circuit Generator."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Boolean expressions", variant="soft"), href="/academy/unit-2/boolean-expressions"),
                rx.spacer(), rx.text("Path 02 · Lesson 6 of 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-2/truth-tables"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
