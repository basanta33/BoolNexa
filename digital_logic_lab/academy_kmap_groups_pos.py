"""BoolNexa Academy Path 03 lessons 5 and 6."""

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


class KMapGroupsPosState(rx.State):
    prime_answer: str = ""
    prime_feedback: str = ""
    essential_answer: str = ""
    essential_feedback: str = ""
    pos_answer: str = ""
    pos_feedback: str = ""
    dontcare_answer: str = ""
    dontcare_feedback: str = ""

    def set_dontcare_answer(self, value: str) -> None:
        self.dontcare_answer = value

    def set_essential_answer(self, value: str) -> None:
        self.essential_answer = value

    def set_pos_answer(self, value: str) -> None:
        self.pos_answer = value

    def set_prime_answer(self, value: str) -> None:
        self.prime_answer = value

    def check_prime(self):
        value = self.prime_answer.strip().lower().replace(" ", "")
        self.prime_feedback = (
            "Correct. A prime implicant cannot be combined into a larger valid group."
            if value in {"cannotbecombined", "cannotgrow", "maximalgroup", "largestpossiblegroup"}
            else "Think of a valid group that cannot be enlarged without including an invalid cell."
        )

    def check_essential(self):
        value = self.essential_answer.strip().lower().replace(" ", "")
        self.essential_feedback = (
            "Correct. An essential prime implicant covers at least one required 1 not covered by any other prime implicant."
            if value in {"unique1", "uniqueminterm", "oneuniqueminterm", "coversaunique1"}
            else "Look for a required 1 that has only one possible prime-implicant cover."
        )

    def check_pos(self):
        value = self.pos_answer.strip().upper().replace(" ", "")
        self.pos_feedback = (
            "Correct. Grouping 0s produces a POS/maxterm form."
            if value in {"POS", "PRODUCTOFSUMS"}
            else "For POS minimisation, group the 0s instead of the 1s."
        )

    def check_dontcare(self):
        value = self.dontcare_answer.strip().lower().replace(" ", "")
        self.dontcare_feedback = (
            "Correct. A don't-care may be treated as 0 or 1—whichever helps create the simpler valid result."
            if value in {"0or1", "either", "whicheverhelps", "both"}
            else "A don't-care is optional: include it in a group only when doing so simplifies the function."
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children,
            align="stretch",
            spacing="3",
        ),
        **PANEL,
    )


def prime_implicants_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 05", color_scheme="blue"),
            rx.heading("Prime Implicants, Essential Groups & Overlap", size="8"),
            rx.text(
                "Good K-map simplification is not only about drawing loops. Learn how to identify "
                "maximal groups, essential coverage and useful overlap so that every required minterm is covered efficiently.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Prime implicants",
                rx.text(
                    "A prime implicant is a valid power-of-two group that cannot be enlarged into a bigger valid group. "
                    "Single cells, pairs and quads can all be prime implicants if no larger valid group contains them."
                ),
                rx.code_block(
                    "Valid group → try to expand it\n"
                    "If it can grow, it is not yet prime\n"
                    "If it cannot grow, it is a prime implicant",
                    language="markup",
                ),
                rx.text("In your own words, what makes a group a prime implicant?"),
                rx.hstack(
                    rx.input(
                        value=KMapGroupsPosState.prime_answer,
                        on_change=KMapGroupsPosState.set_prime_answer,
                        placeholder="Short answer",
                        max_width="320px",
                    ),
                    rx.button("Check", on_click=KMapGroupsPosState.check_prime),
                    wrap="wrap",
                ),
                rx.cond(
                    KMapGroupsPosState.prime_feedback != "",
                    rx.callout(KMapGroupsPosState.prime_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2", "Essential prime implicants",
                rx.text(
                    "A prime implicant is essential when it covers at least one required 1 that no other prime implicant covers. "
                    "That group must appear in the final SOP solution."
                ),
                rx.code_block(
                    "Required 1 covered by only G2\n"
                    "→ G2 is essential\n"
                    "→ G2 must be selected",
                    language="markup",
                ),
                rx.text("What clue tells you that a prime implicant is essential?"),
                rx.hstack(
                    rx.input(
                        value=KMapGroupsPosState.essential_answer,
                        on_change=KMapGroupsPosState.set_essential_answer,
                        placeholder="Short answer",
                        max_width="320px",
                    ),
                    rx.button("Check", on_click=KMapGroupsPosState.check_essential),
                    wrap="wrap",
                ),
                rx.cond(
                    KMapGroupsPosState.essential_feedback != "",
                    rx.callout(KMapGroupsPosState.essential_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "3", "Why overlap is allowed",
                rx.text(
                    "A required 1 may be included in more than one group. Overlap is useful when reusing a cell allows "
                    "another larger group or avoids a smaller, more expensive implicant."
                ),
                rx.callout(
                    "Do not avoid overlap just because loops cross. Judge the Boolean result, not the visual neatness alone.",
                    icon="lightbulb",
                    color_scheme="amber",
                ),
            ),
            _section(
                "4", "Coverage strategy",
                rx.code_block(
                    "1. List the largest valid groups.\n"
                    "2. Mark essential prime implicants first.\n"
                    "3. Cover any remaining required 1s.\n"
                    "4. Prefer the choice with fewer terms/literals.\n"
                    "5. Verify that every required 1 is covered and no forbidden 0 is included.",
                    language="markup",
                ),
            ),
            _section(
                "5", "Worked idea",
                rx.text(
                    "Suppose one quad covers m0,m1,m4,m5 and another quad covers m1,m3,m5,m7. "
                    "The cells m1 and m5 appear in both groups. That overlap is valid because each quad represents a different "
                    "useful implicant."
                ),
                rx.code_block(
                    "G1 = {m0,m1,m4,m5}\n"
                    "G2 = {m1,m3,m5,m7}\n\n"
                    "Overlap: m1 and m5\n"
                    "Both groups may still be needed.",
                    language="markup",
                ),
            ),
            _section(
                "6", "Inspect groups in BoolNexa",
                rx.text(
                    "Use a four-variable expression with several 1s in Boolean Lab. Identify prime and essential groups yourself, "
                    "then compare your choices with BoolNexa's coloured group outlines and simplified expression."
                ),
                rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
            ),
            rx.hstack(
                rx.link(rx.button("← Four-variable K-maps", variant="soft"),
                        href="/academy/unit-3/four-variable-kmaps"),
                rx.spacer(),
                rx.text("Path 03 · Lesson 5", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"),
                        href="/academy/unit-3/sop-pos-dont-cares"),
                width="100%",
                padding_y="16px",
            ),
            spacing="5",
            align="stretch",
            max_width="1100px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh",
        background="#f8fafc",
    )


def sop_pos_dont_cares_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 06", color_scheme="blue"),
            rx.heading("SOP, POS & Don't-Care Conditions", size="8"),
            rx.text(
                "K-maps can minimise both sum-of-products and product-of-sums forms. "
                "Don't-care conditions can also be used strategically when certain input combinations never occur or do not matter.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "SOP: group the 1s",
                rx.text(
                    "For sum-of-products minimisation, place 1s for the minterms where the function is true. "
                    "Each selected group produces one product term."
                ),
                rx.code_block(
                    "F(A,B,C) = Σm(1,3,5,7)\n"
                    "Group all four 1s where C = 1\n"
                    "→ F = C",
                    language="markup",
                ),
            ),
            _section(
                "2", "POS: group the 0s",
                rx.text(
                    "For product-of-sums minimisation, focus on cells where F=0. "
                    "Each group of 0s produces a sum term, and the final result is the product of those sums."
                ),
                rx.text("Which form do you obtain by grouping 0s?"),
                rx.hstack(
                    rx.input(
                        value=KMapGroupsPosState.pos_answer,
                        on_change=KMapGroupsPosState.set_pos_answer,
                        placeholder="SOP or POS",
                        max_width="180px",
                    ),
                    rx.button("Check", on_click=KMapGroupsPosState.check_pos),
                ),
                rx.cond(
                    KMapGroupsPosState.pos_feedback != "",
                    rx.callout(KMapGroupsPosState.pos_feedback, icon="brain"),
                    rx.box(),
                ),
                rx.callout(
                    "SOP and POS can describe the same function using different gate structures.",
                    icon="info",
                ),
            ),
            _section(
                "3", "How a POS group becomes a term",
                rx.text(
                    "For a 0-group, keep only variables that remain constant. The polarity is opposite to the SOP rule: "
                    "a variable fixed at 0 appears uncomplemented in the sum term, while a variable fixed at 1 appears complemented."
                ),
                rx.code_block(
                    "Example zero-group with A=0 and B=1 constant\n"
                    "→ sum term = (A + B')",
                    language="markup",
                ),
            ),
            _section(
                "4", "Don't-care conditions",
                rx.text(
                    "A don't-care cell is usually marked X. It represents an input combination for which the output is irrelevant "
                    "or the combination is not used in the intended system."
                ),
                rx.code_block(
                    "Required 1 → must be covered\n"
                    "Required 0 → must not be included in SOP groups\n"
                    "Don't-care X → may act as 0 or 1 when useful",
                    language="markup",
                ),
                rx.text("How may a don't-care be treated during simplification?"),
                rx.hstack(
                    rx.input(
                        value=KMapGroupsPosState.dontcare_answer,
                        on_change=KMapGroupsPosState.set_dontcare_answer,
                        placeholder="Short answer",
                        max_width="300px",
                    ),
                    rx.button("Check", on_click=KMapGroupsPosState.check_dontcare),
                    wrap="wrap",
                ),
                rx.cond(
                    KMapGroupsPosState.dontcare_feedback != "",
                    rx.callout(KMapGroupsPosState.dontcare_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Use don't-cares only when they help",
                rx.text(
                    "You are not required to include every X in a group. Use a don't-care only if it creates a larger valid group "
                    "or otherwise reduces the final expression."
                ),
                rx.code_block(
                    "Without X: pair of 2 → 3 literals\n"
                    "Using useful X: quad of 4 → 2 literals\n\n"
                    "Choose the quad.",
                    language="markup",
                ),
            ),
            _section(
                "6", "Compare forms with BoolNexa",
                rx.text(
                    "Use Boolean Lab to explore a function in canonical SOP form, inspect its K-map, and compare the simplified expression "
                    "with the circuit generated from that result."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Prime implicants", variant="soft"),
                        href="/academy/unit-3/prime-implicants"),
                rx.spacer(),
                rx.text("Path 03 · Lesson 6", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-3/five-variable-kmaps"),
                width="100%",
                padding_y="16px",
            ),
            spacing="5",
            align="stretch",
            max_width="1100px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh",
        background="#f8fafc",
    )
