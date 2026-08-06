"""BoolNexa Academy Path 04 lessons 9 and 10: integrated design and mastery."""

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


class CombinationalMasteryState(rx.State):
    workflow_answer: str = ""
    workflow_feedback: str = ""
    block_answer: str = ""
    block_feedback: str = ""
    q1: str = ""
    q2: str = ""
    q3: str = ""
    q4: str = ""
    mastery_score: int = 0
    mastery_feedback: str = ""

    def set_block_answer(self, value: str) -> None:
        self.block_answer = value

    def set_q1(self, value: str) -> None:
        self.q1 = value

    def set_q2(self, value: str) -> None:
        self.q2 = value

    def set_q3(self, value: str) -> None:
        self.q3 = value

    def set_q4(self, value: str) -> None:
        self.q4 = value

    def set_workflow_answer(self, value: str) -> None:
        self.workflow_answer = value

    def check_workflow(self):
        value = self.workflow_answer.strip().lower().replace(" ", "")
        self.workflow_feedback = (
            "Correct. Define the required behaviour before choosing gates or building blocks."
            if value in {"specification", "requirements", "problemstatement", "behaviour", "behavior"}
            else "Start by stating exactly what the system must do."
        )

    def check_block(self):
        value = self.block_answer.strip().lower().replace(" ", "")
        self.block_feedback = (
            "Correct. A multiplexer is the natural building block when one of several data sources must be selected."
            if value in {"mux", "multiplexer"}
            else "Which component selects one of many inputs and forwards it to one output?"
        )

    def grade_mastery(self):
        score = 0
        if self.q1.strip().lower().replace(" ", "") in {"fulladder", "fa"}:
            score += 1
        if self.q2.strip().lower().replace(" ", "") in {"mux", "multiplexer"}:
            score += 1
        if self.q3.strip().lower().replace(" ", "") in {"xnor", "xnorand", "xnor+and"}:
            score += 1
        if self.q4.strip().lower().replace(" ", "") in {"priorityencoder", "priority"}:
            score += 1
        self.mastery_score = score
        if score == 4:
            self.mastery_feedback = "Mastery achieved: 4/4. You are ready to progress beyond combinational building blocks."
        elif score == 3:
            self.mastery_feedback = "Strong result: 3/4. Review the missed building block, then verify it in BoolNexa."
        else:
            self.mastery_feedback = f"Score: {score}/4. Revisit the relevant Path 04 lessons and try again."


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


def integrated_combinational_design_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 09", color_scheme="blue"),
            rx.heading("Integrated Combinational Design", size="8"),
            rx.text(
                "Real digital systems combine arithmetic, comparison, selection and decoding. "
                "This lesson turns individual building blocks into a disciplined engineering design process.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Begin with the specification",
                rx.text(
                    "Do not begin by placing gates. First define inputs, outputs, required behaviour, invalid conditions "
                    "and any assumptions such as active-high signals or unsigned numbers."
                ),
                rx.text("What should come first in a digital design: gates or the specification?"),
                rx.hstack(
                    rx.input(value=CombinationalMasteryState.workflow_answer,
                             on_change=CombinationalMasteryState.set_workflow_answer,
                             placeholder="Answer", max_width="220px"),
                    rx.button("Check", on_click=CombinationalMasteryState.check_workflow),
                ),
                rx.cond(CombinationalMasteryState.workflow_feedback != "",
                        rx.callout(CombinationalMasteryState.workflow_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "Choose the right abstraction",
                _table(
                    ("Design need", "Useful building block"),
                    (
                        ("Add binary values", "Adder"),
                        ("Subtract values", "Subtractor / adder-subtractor"),
                        ("Compare magnitudes", "Comparator"),
                        ("Choose one data source", "Multiplexer"),
                        ("Route data to one destination", "Demultiplexer"),
                        ("Decode an address/code", "Decoder"),
                        ("Encode an active request", "Encoder / priority encoder"),
                    ),
                ),
                rx.text("Which block naturally selects one of several data inputs?"),
                rx.hstack(
                    rx.input(value=CombinationalMasteryState.block_answer,
                             on_change=CombinationalMasteryState.set_block_answer,
                             placeholder="Building block", max_width="220px"),
                    rx.button("Check", on_click=CombinationalMasteryState.check_block),
                ),
                rx.cond(CombinationalMasteryState.block_feedback != "",
                        rx.callout(CombinationalMasteryState.block_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "Worked system: a tiny arithmetic selector",
                rx.text(
                    "Design a one-bit unit with inputs A, B and operation select M. "
                    "When M=0 it adds A+B. When M=1 it subtracts A−B."
                ),
                rx.code_block(
                    "M=0 → select ADD result\n"
                    "M=1 → select SUBTRACT result\n\n"
                    "Adder ───────┐\n"
                    "             ├─► MUX ─► selected result\n"
                    "Subtractor ──┘\n"
                    "              ▲\n"
                    "              M",
                    language="markup",
                ),
                rx.text(
                    "This hierarchical approach is easier to reason about than immediately expanding everything into individual gates."
                ),
            ),
            _section(
                "4", "Optimise after correctness",
                rx.text(
                    "Once the design is functionally correct, simplify equations, reuse shared terms and consider whether a standard "
                    "building block reduces complexity. Optimisation must preserve the specified behaviour."
                ),
                rx.code_block(
                    "Specification → architecture → equations → verify\n"
                    "                         ↓\n"
                    "                 simplify / optimise\n"
                    "                         ↓\n"
                    "                     verify again",
                    language="markup",
                ),
                rx.callout(
                    "Never accept a smaller circuit merely because it looks simpler. Equivalence must be verified.",
                    icon="info",
                ),
            ),
            _section(
                "5", "Engineering considerations",
                rx.unordered_list(
                    rx.list_item("Propagation delay: long logic or carry chains respond more slowly."),
                    rx.list_item("Fan-in/fan-out: physical gates have electrical limits."),
                    rx.list_item("Active-high/active-low conventions must be interpreted correctly."),
                    rx.list_item("Unused or invalid input combinations should be deliberately handled."),
                    rx.list_item("Modular designs are easier to test, explain and reuse."),
                ),
            ),
            _section(
                "6", "Use BoolNexa as a verification environment",
                rx.text(
                    "Move between Boolean Lab, Circuit Generator and the simulator. Predict first, build second, "
                    "then compare every relevant input combination with the specification."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    rx.link(rx.button("Open Simulator", variant="soft"), href="/"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Encoders", variant="soft"), href="/academy/unit-4/encoders"),
                rx.spacer(), rx.text("Path 04 · Lesson 9", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Mastery challenge →", variant="soft"), href="/academy/unit-4/mastery-challenge"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def combinational_mastery_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 10", color_scheme="blue"),
            rx.heading("Combinational Logic Mastery Challenge", size="8"),
            rx.text(
                "Finish Path 04 by identifying the correct building blocks and designing a small system from requirements.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Rapid knowledge check",
                rx.text("Q1. Which block adds A, B and a carry-in?"),
                rx.input(value=CombinationalMasteryState.q1, on_change=CombinationalMasteryState.set_q1,
                         placeholder="Answer", max_width="260px"),
                rx.text("Q2. Which block selects one of several data inputs?"),
                rx.input(value=CombinationalMasteryState.q2, on_change=CombinationalMasteryState.set_q2,
                         placeholder="Answer", max_width="260px"),
                rx.text("Q3. Which gate is naturally used to test equality of two individual bits?"),
                rx.input(value=CombinationalMasteryState.q3, on_change=CombinationalMasteryState.set_q3,
                         placeholder="Answer", max_width="260px"),
                rx.text("Q4. Which block resolves simultaneous requests according to importance?"),
                rx.input(value=CombinationalMasteryState.q4, on_change=CombinationalMasteryState.set_q4,
                         placeholder="Answer", max_width="260px"),
                rx.button("Grade challenge", on_click=CombinationalMasteryState.grade_mastery, color_scheme="blue"),
                rx.cond(CombinationalMasteryState.mastery_feedback != "",
                        rx.callout(CombinationalMasteryState.mastery_feedback, icon="graduation-cap"), rx.box()),
            ),
            _section(
                "2", "Capstone: two-input decision unit",
                rx.text(
                    "Design a two-bit unsigned system with inputs A=A1A0 and B=B1B0 and mode M."
                ),
                rx.code_block(
                    "Required behaviour:\n"
                    "M=0 → output the 2-bit value A\n"
                    "M=1 → output the 2-bit value B\n"
                    "Also produce EQ=1 when A=B\n\n"
                    "Think before building:\n"
                    "• What selects A or B?\n"
                    "• What determines equality?\n"
                    "• Can each output bit use the same repeated structure?",
                    language="markup",
                ),
            ),
            _section(
                "3", "Expected architecture",
                rx.text(
                    "Use one 2-to-1 MUX per data bit. For equality, XNOR corresponding bits and AND the equality results."
                ),
                rx.code_block(
                    "Y1 = M'A1 + MB1\n"
                    "Y0 = M'A0 + MB0\n\n"
                    "EQ = (A1 XNOR B1)(A0 XNOR B0)",
                    language="markup",
                ),
                rx.callout(
                    "The important result is not only the equations. Notice the reusable structure: two identical selection channels plus one comparator path.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "4", "Verification checklist",
                rx.unordered_list(
                    rx.list_item("For M=0, confirm Y=A for all A and B."),
                    rx.list_item("For M=1, confirm Y=B for all A and B."),
                    rx.list_item("Confirm EQ=1 only when both two-bit values are identical."),
                    rx.list_item("Test boundary patterns such as 00, 01, 10 and 11."),
                    rx.list_item("Explain each subcircuit before considering the design complete."),
                ),
                rx.hstack(
                    rx.link(rx.button("Verify in Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Build in Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            _section(
                "5", "Path 04 complete",
                rx.callout(
                    "You can now move from a behavioural requirement to truth tables, Boolean equations, simplification, "
                    "standard combinational blocks, gate-level implementation and verification.",
                    icon="graduation-cap", color_scheme="green",
                ),
                rx.text(
                    "These skills form the bridge from Boolean algebra to larger digital architectures."
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Integrated design", variant="soft"), href="/academy/unit-4/integrated-design"),
                rx.spacer(), rx.text("Path 04 · Lesson 10", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Return to Academy", color_scheme="blue"), href="/academy"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
