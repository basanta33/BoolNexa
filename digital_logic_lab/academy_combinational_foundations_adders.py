"""BoolNexa Academy Path 04 lessons 1 and 2: combinational foundations and adders."""

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


class CombinationalFoundationsState(rx.State):
    memory_answer: str = ""
    memory_feedback: str = ""
    half_sum: str = ""
    half_carry: str = ""
    half_feedback: str = ""
    full_inputs: str = ""
    full_feedback: str = ""

    def set_full_inputs(self, value: str) -> None:
        self.full_inputs = value

    def set_half_carry(self, value: str) -> None:
        self.half_carry = value

    def set_half_sum(self, value: str) -> None:
        self.half_sum = value

    def set_memory_answer(self, value: str) -> None:
        self.memory_answer = value

    def check_memory(self):
        value = self.memory_answer.strip().lower().replace(" ", "")
        self.memory_feedback = (
            "Correct. A combinational circuit has no stored state; its outputs depend on the current inputs."
            if value in {"no", "none", "nomemory", "false"}
            else "Combinational logic does not remember an earlier input."
        )

    def check_half_adder(self):
        s = self.half_sum.strip()
        c = self.half_carry.strip()
        if s == "0" and c == "1":
            self.half_feedback = "Correct. 1 + 1 = binary 10, so Sum=0 and Carry=1."
        else:
            self.half_feedback = "Add the two input bits: binary 1 + 1 equals 10."

    def check_full_inputs(self):
        self.full_feedback = (
            "Correct. A full adder accepts A, B and carry-in: three one-bit inputs."
            if self.full_inputs.strip() == "3"
            else "Count A, B and Cin."
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


def combinational_foundations_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 01", color_scheme="blue"),
            rx.heading("Introduction to Combinational Logic", size="8"),
            rx.text(
                "Now turn Boolean expressions into useful digital systems. In combinational logic, "
                "the output is determined by the inputs that are present right now.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "What makes a circuit combinational?",
                rx.text(
                    "A combinational circuit has no stored state. For the same current input combination, "
                    "an ideal combinational circuit produces the same output combination."
                ),
                rx.code_block(
                    "Current inputs ──► Combinational logic ──► Current outputs\n\n"
                    "No clock required\nNo previous-state memory required",
                    language="markup",
                ),
                rx.text("Does a purely combinational circuit need to remember a previous input?"),
                rx.hstack(
                    rx.input(value=CombinationalFoundationsState.memory_answer,
                             on_change=CombinationalFoundationsState.set_memory_answer,
                             placeholder="yes / no", max_width="180px"),
                    rx.button("Check", on_click=CombinationalFoundationsState.check_memory),
                ),
                rx.cond(CombinationalFoundationsState.memory_feedback != "",
                        rx.callout(CombinationalFoundationsState.memory_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "From specification to circuit",
                rx.code_block(
                    "Problem statement\n"
                    "      ↓\n"
                    "Inputs and outputs\n"
                    "      ↓\n"
                    "Truth table\n"
                    "      ↓\n"
                    "Boolean expression\n"
                    "      ↓\n"
                    "Simplification / K-map\n"
                    "      ↓\n"
                    "Gate-level circuit\n"
                    "      ↓\n"
                    "Simulation and verification",
                    language="markup",
                ),
                rx.text(
                    "This workflow connects Paths 02 and 03 directly to practical digital design."
                ),
            ),
            _section(
                "3", "Common combinational building blocks",
                rx.unordered_list(
                    rx.list_item("Adders and subtractors perform binary arithmetic."),
                    rx.list_item("Comparators determine equality or relative magnitude."),
                    rx.list_item("Multiplexers select one data source."),
                    rx.list_item("Demultiplexers route one source to a selected destination."),
                    rx.list_item("Encoders compress an active input into a code."),
                    rx.list_item("Decoders activate outputs from an input code."),
                ),
            ),
            _section(
                "4", "Example: a simple decision circuit",
                rx.text(
                    "Suppose an alarm should turn on only when Enable E is 1 and either sensor A or sensor B is active."
                ),
                rx.code_block(
                    "Specification: Alarm when E AND (A OR B)\n"
                    "Boolean form: Y = E(A + B)\n"
                    "Gate structure: OR(A,B) → AND with E",
                    language="markup",
                ),
                rx.text(
                    "A design begins with behaviour, not with randomly placing gates."
                ),
            ),
            _section(
                "5", "Combinational versus sequential",
                _table(
                    ("Feature", "Combinational", "Sequential"),
                    (
                        ("Output depends on", "Current inputs", "Current inputs + stored state"),
                        ("Memory/state", "No", "Yes"),
                        ("Typical examples", "Adder, MUX, decoder", "Counter, register, FSM"),
                    ),
                ),
                rx.callout(
                    "Sequential logic comes later. Path 04 deliberately builds a strong combinational foundation first.",
                    icon="info",
                ),
            ),
            _section(
                "6", "Build the example in BoolNexa",
                rx.text(
                    "Use Circuit Generator for Y = E(A + B), then use the simulator to test different input combinations."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Circuit Generator", color_scheme="blue"), href="/tools/circuit"),
                    rx.link(rx.button("Open Simulator", variant="soft"), href="/"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(), rx.text("Path 04 · Lesson 1", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/adders"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def adders_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 02", color_scheme="blue"),
            rx.heading("Half Adders & Full Adders", size="8"),
            rx.text(
                "Binary addition is one of the foundations of digital arithmetic. Start with two bits, "
                "then include a carry-in so addition can be chained across many bit positions.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Half adder",
                rx.text("A half adder adds two one-bit inputs A and B."),
                _table(
                    ("A", "B", "Sum S", "Carry C"),
                    (
                        ("0", "0", "0", "0"),
                        ("0", "1", "1", "0"),
                        ("1", "0", "1", "0"),
                        ("1", "1", "0", "1"),
                    ),
                ),
                rx.code_block("S = A ⊕ B\nC = AB", language="markup"),
            ),
            _section(
                "2", "Check binary 1 + 1",
                rx.text("For A=1 and B=1, enter the Sum bit and Carry bit."),
                rx.hstack(
                    rx.input(value=CombinationalFoundationsState.half_sum,
                             on_change=CombinationalFoundationsState.set_half_sum,
                             placeholder="Sum", max_width="120px"),
                    rx.input(value=CombinationalFoundationsState.half_carry,
                             on_change=CombinationalFoundationsState.set_half_carry,
                             placeholder="Carry", max_width="120px"),
                    rx.button("Check", on_click=CombinationalFoundationsState.check_half_adder),
                    wrap="wrap",
                ),
                rx.cond(CombinationalFoundationsState.half_feedback != "",
                        rx.callout(CombinationalFoundationsState.half_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "3", "Why a half adder is not enough",
                rx.text(
                    "When adding multi-bit numbers, a bit position may receive a carry from the position to its right. "
                    "A half adder has no carry-in input, so we need a full adder."
                ),
            ),
            _section(
                "4", "Full adder",
                rx.text("A full adder accepts A, B and carry-in Cin, and produces Sum S and carry-out Cout."),
                _table(
                    ("A","B","Cin","S","Cout"),
                    (
                        ("0","0","0","0","0"),
                        ("0","0","1","1","0"),
                        ("0","1","0","1","0"),
                        ("0","1","1","0","1"),
                        ("1","0","0","1","0"),
                        ("1","0","1","0","1"),
                        ("1","1","0","0","1"),
                        ("1","1","1","1","1"),
                    ),
                ),
                rx.code_block(
                    "S = A ⊕ B ⊕ Cin\n"
                    "Cout = AB + ACin + BCin\n\n"
                    "Equivalent carry form:\n"
                    "Cout = AB + Cin(A ⊕ B)",
                    language="markup",
                ),
                rx.text("How many one-bit inputs does a full adder have?"),
                rx.hstack(
                    rx.input(value=CombinationalFoundationsState.full_inputs,
                             on_change=CombinationalFoundationsState.set_full_inputs,
                             placeholder="Inputs", max_width="140px"),
                    rx.button("Check", on_click=CombinationalFoundationsState.check_full_inputs),
                ),
                rx.cond(CombinationalFoundationsState.full_feedback != "",
                        rx.callout(CombinationalFoundationsState.full_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Build larger adders",
                rx.text(
                    "Full adders can be cascaded: each stage's Cout feeds the next stage's Cin. "
                    "This forms a ripple-carry adder for multi-bit binary numbers."
                ),
                rx.code_block(
                    "LSB                                      MSB\n"
                    "[FA0] ─Cout→ [FA1] ─Cout→ [FA2] ─Cout→ [FA3]\n"
                    "  ↑            ↑            ↑            ↑\n"
                    " A0,B0        A1,B1        A2,B2        A3,B3",
                    language="markup",
                ),
                rx.callout(
                    "The carry must propagate through stages, so larger ripple-carry adders have increasing propagation delay.",
                    icon="info",
                ),
            ),
            _section(
                "6", "Design and verify",
                rx.text(
                    "Use BoolNexa to create the half-adder equations, generate the circuit, and verify all four input combinations. "
                    "Then examine how the full-adder equations extend the same idea."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Combinational foundations", variant="soft"),
                        href="/academy/unit-4/combinational-foundations"),
                rx.spacer(), rx.text("Path 04 · Lesson 2", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Academy", variant="soft"), href="/academy"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
