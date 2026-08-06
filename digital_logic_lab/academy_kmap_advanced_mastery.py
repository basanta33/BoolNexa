"""BoolNexa Academy Path 03 lessons 9 and 10: advanced strategy and mastery."""

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


class KMapMasteryState(rx.State):
    strategy_answer: str = ""
    strategy_feedback: str = ""
    hazard_answer: str = ""
    hazard_feedback: str = ""
    mastery_score: int = 0
    mastery_feedback: str = ""
    q1: str = ""
    q2: str = ""
    q3: str = ""
    q4: str = ""

    def set_hazard_answer(self, value: str) -> None:
        self.hazard_answer = value

    def set_q1(self, value: str) -> None:
        self.q1 = value

    def set_q2(self, value: str) -> None:
        self.q2 = value

    def set_q3(self, value: str) -> None:
        self.q3 = value

    def set_q4(self, value: str) -> None:
        self.q4 = value

    def set_strategy_answer(self, value: str) -> None:
        self.strategy_answer = value

    def check_strategy(self):
        value = self.strategy_answer.strip().lower().replace(" ", "")
        self.strategy_feedback = (
            "Correct. Start with essential prime implicants, then cover remaining required cells efficiently."
            if value in {"essential", "essentialprimeimplicants", "essentialgroups"}
            else "First identify groups that uniquely cover a required minterm."
        )

    def check_hazard(self):
        value = self.hazard_answer.strip().lower().replace(" ", "")
        self.hazard_feedback = (
            "Correct. A redundant consensus group can remove a static-1 hazard in an SOP implementation."
            if value in {"consensus", "consensusterm", "redundantgroup", "overlap"}
            else "Think about adding an overlapping group that bridges the transition."
        )

    def grade_mastery(self):
        score = 0
        if self.q1.strip() == "16":
            score += 1
        if self.q2.strip().upper().replace(" ", "") in {"POS", "PRODUCTOFSUMS"}:
            score += 1
        if self.q3.strip().lower().replace(" ", "") in {"poweroftwo", "powersoftwo", "1,2,4,8", "1248"}:
            score += 1
        if self.q4.strip().lower().replace(" ", "") in {"yes", "y", "true"}:
            score += 1
        self.mastery_score = score
        if score == 4:
            self.mastery_feedback = "Mastery achieved: 4/4. You are ready to apply K-maps to real circuit design."
        elif score >= 3:
            self.mastery_feedback = f"Strong result: {score}/4. Review the missed idea, then verify it in Boolean Lab."
        else:
            self.mastery_feedback = f"Score: {score}/4. Revisit the earlier Path 03 lessons before moving on."


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="blue"), rx.heading(title, size="5"), align="center"),
            *children, align="stretch", spacing="3",
        ),
        **PANEL,
    )


def advanced_kmap_strategy_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 09", color_scheme="blue"),
            rx.heading("Advanced K-map Strategy", size="8"),
            rx.text(
                "Move from simply finding valid groups to choosing efficient covers, comparing alternatives "
                "and understanding why a deliberately redundant group can sometimes improve real hardware behaviour.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A disciplined minimisation workflow",
                rx.code_block(
                    "1. Map every required 1, 0 and don't-care correctly.\n"
                    "2. Find the largest valid prime implicants.\n"
                    "3. Select essential prime implicants first.\n"
                    "4. Cover remaining required cells with the cheapest useful groups.\n"
                    "5. Compare term count and literal count.\n"
                    "6. Verify the result against the truth table.",
                    language="markup",
                ),
                rx.text("Which groups should normally be selected first?"),
                rx.hstack(
                    rx.input(value=KMapMasteryState.strategy_answer,
                             on_change=KMapMasteryState.set_strategy_answer,
                             placeholder="Short answer", max_width="300px"),
                    rx.button("Check", on_click=KMapMasteryState.check_strategy),
                    wrap="wrap",
                ),
                rx.cond(KMapMasteryState.strategy_feedback != "",
                        rx.callout(KMapMasteryState.strategy_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "When several covers are correct",
                rx.text(
                    "A K-map can have more than one correct minimal cover. Compare alternatives by the number of product terms "
                    "and total literals, while remembering that the best physical implementation may also depend on the available gates."
                ),
                rx.callout(
                    "Minimal Boolean form and best hardware implementation are related, but they are not always identical engineering goals.",
                    icon="info",
                ),
            ),
            _section(
                "3", "From simplification to hazards",
                rx.text(
                    "Real gates have propagation delay. In an SOP circuit, two adjacent 1-cells may be covered by different implicants. "
                    "During a one-variable input transition, unequal delays can briefly make the output fall to 0 even though the ideal "
                    "Boolean function should remain 1. This is a static-1 hazard."
                ),
                rx.code_block(
                    "F = AB + A'C\n"
                    "Potential transition in A when B=C=1\n"
                    "Consensus term BC bridges the adjacent 1-cells\n\n"
                    "Hazard-reduced implementation:\n"
                    "F = AB + A'C + BC",
                    language="markup",
                ),
            ),
            _section(
                "4", "Redundancy can be useful",
                rx.text(
                    "The consensus term BC is Boolean-redundant for the steady-state function, but physically useful because it provides "
                    "continuous coverage during the transition. On a K-map, this appears as an overlapping group connecting the two regions."
                ),
                rx.text("What kind of added group can help remove a static-1 hazard?"),
                rx.hstack(
                    rx.input(value=KMapMasteryState.hazard_answer,
                             on_change=KMapMasteryState.set_hazard_answer,
                             placeholder="Short answer", max_width="300px"),
                    rx.button("Check", on_click=KMapMasteryState.check_hazard),
                    wrap="wrap",
                ),
                rx.cond(KMapMasteryState.hazard_feedback != "",
                        rx.callout(KMapMasteryState.hazard_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Know the practical limit",
                rx.text(
                    "K-maps are excellent teaching and manual-design tools for a modest number of variables. "
                    "As variable count grows, algorithmic minimisation and synthesis tools become more practical than manual grouping."
                ),
                rx.callout(
                    "The important transferable skill is understanding adjacency, implicants and minimisation—not memorising ever-larger drawings.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Verify with BoolNexa",
                rx.text(
                    "Use Boolean Lab to simplify a function, inspect the selected groups, then use Circuit Generator to compare the "
                    "original and reduced implementations. Treat the software result as something to verify, not merely copy."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Six-variable K-maps", variant="soft"),
                        href="/academy/unit-3/six-variable-kmaps"),
                rx.spacer(), rx.text("Path 03 · Lesson 9", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Mastery challenge →", variant="soft"),
                        href="/academy/unit-3/mastery-challenge"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def kmap_mastery_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 10", color_scheme="blue"),
            rx.heading("Karnaugh Map Mastery Challenge", size="8"),
            rx.text(
                "Finish Path 03 by recalling the core rules and then applying the complete workflow using BoolNexa's real tools.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Rapid knowledge check",
                rx.text("Q1. How many cells are in a four-variable K-map?"),
                rx.input(value=KMapMasteryState.q1, on_change=KMapMasteryState.set_q1,
                         placeholder="Answer", max_width="240px"),
                rx.text("Q2. Which normal form is produced by grouping 0s?"),
                rx.input(value=KMapMasteryState.q2, on_change=KMapMasteryState.set_q2,
                         placeholder="Answer", max_width="240px"),
                rx.text("Q3. Valid K-map group sizes follow what numerical rule?"),
                rx.input(value=KMapMasteryState.q3, on_change=KMapMasteryState.set_q3,
                         placeholder="Answer", max_width="300px"),
                rx.text("Q4. Can opposite K-map edges be adjacent?"),
                rx.input(value=KMapMasteryState.q4, on_change=KMapMasteryState.set_q4,
                         placeholder="yes / no", max_width="240px"),
                rx.button("Grade challenge", on_click=KMapMasteryState.grade_mastery, color_scheme="blue"),
                rx.cond(KMapMasteryState.mastery_feedback != "",
                        rx.callout(KMapMasteryState.mastery_feedback, icon="graduation-cap"), rx.box()),
            ),
            _section(
                "2", "Design challenge",
                rx.text(
                    "Use F(A,B,C,D)=Σm(0,2,5,7,8,10,13,15). Do not begin by asking the software for the answer."
                ),
                rx.code_block(
                    "Your task:\n"
                    "• Place all eight minterms correctly.\n"
                    "• Find the largest valid groups.\n"
                    "• Write a minimal SOP expression.\n"
                    "• Verify every truth-table row.\n"
                    "• Generate the corresponding circuit.",
                    language="markup",
                ),
            ),
            _section(
                "3", "Tool-assisted verification",
                rx.text(
                    "Now open Boolean Lab and enter the challenge function. Compare its map and simplification with your own work. "
                    "Then open Circuit Generator and inspect the implementation."
                ),
                rx.hstack(
                    rx.link(rx.button("Verify in Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Build the Circuit", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            _section(
                "4", "Explain, don't just calculate",
                rx.text(
                    "A student has mastered K-maps when they can explain why cells are adjacent, why a variable disappears, "
                    "why a group is essential, and why the final expression is equivalent—not only produce an answer."
                ),
            ),
            _section(
                "5", "Path 03 completion",
                rx.callout(
                    "You have progressed from 2-variable maps through higher-variable Gray-code maps, SOP/POS, don't-cares, "
                    "prime implicants, overlap, advanced cover selection and practical hazard awareness.",
                    icon="graduation-cap", color_scheme="green",
                ),
                rx.text(
                    "Next, apply this minimisation skill to combinational logic design, where Boolean expressions become useful digital systems."
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Advanced strategy", variant="soft"),
                        href="/academy/unit-3/advanced-strategy"),
                rx.spacer(), rx.text("Path 03 · Lesson 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Return to Academy", color_scheme="blue"), href="/academy"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
