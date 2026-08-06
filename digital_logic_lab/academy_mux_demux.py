"""BoolNexa Academy Path 04 lessons 5 and 6: multiplexers and demultiplexers."""

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


class MuxDemuxState(rx.State):
    mux_select: str = ""
    mux_feedback: str = ""
    mux_output: str = ""
    mux_output_feedback: str = ""
    demux_selects: str = ""
    demux_feedback: str = ""
    demux_output: str = ""
    demux_output_feedback: str = ""

    def set_demux_output(self, value: str) -> None:
        self.demux_output = value

    def set_demux_selects(self, value: str) -> None:
        self.demux_selects = value

    def set_mux_output(self, value: str) -> None:
        self.mux_output = value

    def set_mux_select(self, value: str) -> None:
        self.mux_select = value

    def check_mux_select(self):
        self.mux_feedback = (
            "Correct. A 4-to-1 MUX needs log₂(4) = 2 select lines."
            if self.mux_select.strip() == "2"
            else "Use n select bits to choose among 2ⁿ inputs."
        )

    def check_mux_output(self):
        value = self.mux_output.strip()
        self.mux_output_feedback = (
            "Correct. S=1 selects I1, so Y=0."
            if value == "0"
            else "For a 2-to-1 MUX, S=1 routes I1 to Y."
        )

    def check_demux_selects(self):
        self.demux_feedback = (
            "Correct. A 1-to-4 DEMUX needs 2 select lines."
            if self.demux_selects.strip() == "2"
            else "Two select bits provide four destination codes: 00, 01, 10 and 11."
        )

    def check_demux_output(self):
        value = self.demux_output.strip().upper().replace(" ", "")
        self.demux_output_feedback = (
            "Correct. With S1S0=10, input D is routed to Y2."
            if value in {"Y2", "2"}
            else "Read 10₂ as output index 2."
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


def multiplexers_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 05", color_scheme="blue"),
            rx.heading("Multiplexers: Digital Data Selectors", size="8"),
            rx.text(
                "A multiplexer, or MUX, selects one of several input signals and forwards the selected input "
                "to a single output. Think of it as a digitally controlled switch.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The 2-to-1 multiplexer",
                rx.text("A 2-to-1 MUX has data inputs I0 and I1, one select input S, and one output Y."),
                _table(
                    ("S", "Selected input", "Y"),
                    (("0", "I0", "I0"), ("1", "I1", "I1")),
                ),
                rx.code_block("Y = S'I0 + SI1", language="markup"),
                rx.text(
                    "When S=0, the S'I0 term passes I0. When S=1, the SI1 term passes I1."
                ),
            ),
            _section(
                "2", "Interactive selection",
                rx.text("Suppose I0=1, I1=0 and S=1. What is Y?"),
                rx.hstack(
                    rx.input(value=MuxDemuxState.mux_output,
                             on_change=MuxDemuxState.set_mux_output,
                             placeholder="Y", max_width="120px"),
                    rx.button("Check", on_click=MuxDemuxState.check_mux_output),
                ),
                rx.cond(MuxDemuxState.mux_output_feedback != "",
                        rx.callout(MuxDemuxState.mux_output_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "The 4-to-1 multiplexer",
                _table(
                    ("S1", "S0", "Selected input"),
                    (
                        ("0", "0", "I0"),
                        ("0", "1", "I1"),
                        ("1", "0", "I2"),
                        ("1", "1", "I3"),
                    ),
                ),
                rx.code_block(
                    "Y = S1'S0'I0 + S1'S0I1 + S1S0'I2 + S1S0I3",
                    language="markup",
                ),
                rx.text("How many select lines does a 4-to-1 MUX need?"),
                rx.hstack(
                    rx.input(value=MuxDemuxState.mux_select,
                             on_change=MuxDemuxState.set_mux_select,
                             placeholder="Select lines", max_width="160px"),
                    rx.button("Check", on_click=MuxDemuxState.check_mux_select),
                ),
                rx.cond(MuxDemuxState.mux_feedback != "",
                        rx.callout(MuxDemuxState.mux_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "General selection rule",
                rx.text(
                    "With n select lines, a conventional multiplexer can select among up to 2ⁿ data inputs."
                ),
                rx.code_block(
                    "1 select bit  → 2 inputs\n"
                    "2 select bits → 4 inputs\n"
                    "3 select bits → 8 inputs\n"
                    "4 select bits → 16 inputs",
                    language="markup",
                ),
            ),
            _section(
                "5", "MUX as a Boolean-function generator",
                rx.text(
                    "A MUX can implement Boolean functions by using variables as select lines and connecting "
                    "data inputs to 0, 1, another variable, or its complement."
                ),
                rx.code_block(
                    "Example: F(A,B) = Σm(1,2)\n"
                    "Use A,B as the select lines of a 4:1 MUX\n"
                    "I0=0, I1=1, I2=1, I3=0\n"
                    "→ F = A ⊕ B",
                    language="markup",
                ),
                rx.callout(
                    "This is why multiplexers are not merely routing devices—they are universal building blocks for combinational design.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Build and verify",
                rx.text(
                    "Use Circuit Generator for Y=S'I0+SI1 and verify that changing S switches the output between I0 and I1."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Circuit Generator", color_scheme="blue"), href="/tools/circuit"),
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Comparators", variant="soft"), href="/academy/unit-4/comparators"),
                rx.spacer(), rx.text("Path 04 · Lesson 5", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/demultiplexers"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def demultiplexers_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 06", color_scheme="blue"),
            rx.heading("Demultiplexers: Digital Data Distributors", size="8"),
            rx.text(
                "A demultiplexer, or DEMUX, takes one data input and routes it to one selected output. "
                "It performs the complementary routing role to a multiplexer.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The 1-to-2 DEMUX",
                rx.text("A 1-to-2 DEMUX has data input D, select S, and outputs Y0 and Y1."),
                _table(
                    ("S", "Y0", "Y1"),
                    (
                        ("0", "D", "0"),
                        ("1", "0", "D"),
                    ),
                ),
                rx.code_block("Y0 = DS'\nY1 = DS", language="markup"),
            ),
            _section(
                "2", "The 1-to-4 DEMUX",
                _table(
                    ("S1", "S0", "Active destination"),
                    (
                        ("0", "0", "Y0"),
                        ("0", "1", "Y1"),
                        ("1", "0", "Y2"),
                        ("1", "1", "Y3"),
                    ),
                ),
                rx.code_block(
                    "Y0 = D S1' S0'\n"
                    "Y1 = D S1' S0\n"
                    "Y2 = D S1  S0'\n"
                    "Y3 = D S1  S0",
                    language="markup",
                ),
                rx.text("How many select lines does a 1-to-4 DEMUX require?"),
                rx.hstack(
                    rx.input(value=MuxDemuxState.demux_selects,
                             on_change=MuxDemuxState.set_demux_selects,
                             placeholder="Select lines", max_width="160px"),
                    rx.button("Check", on_click=MuxDemuxState.check_demux_selects),
                ),
                rx.cond(MuxDemuxState.demux_feedback != "",
                        rx.callout(MuxDemuxState.demux_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "Route the data",
                rx.text("For a 1-to-4 DEMUX with D=1 and S1S0=10, which output receives the 1?"),
                rx.hstack(
                    rx.input(value=MuxDemuxState.demux_output,
                             on_change=MuxDemuxState.set_demux_output,
                             placeholder="Y0–Y3", max_width="160px"),
                    rx.button("Check", on_click=MuxDemuxState.check_demux_output),
                ),
                rx.cond(MuxDemuxState.demux_output_feedback != "",
                        rx.callout(MuxDemuxState.demux_output_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "MUX versus DEMUX",
                _table(
                    ("Feature", "MUX", "DEMUX"),
                    (
                        ("Data flow", "Many inputs → one output", "One input → many outputs"),
                        ("Control", "Selects source", "Selects destination"),
                        ("Example", "4-to-1", "1-to-4"),
                        ("Typical role", "Data selection", "Data distribution"),
                    ),
                ),
            ),
            _section(
                "5", "Where DEMUX circuits are useful",
                rx.unordered_list(
                    rx.list_item("Routing a shared data signal to one selected destination."),
                    rx.list_item("Communication and channel-selection systems."),
                    rx.list_item("Control-signal distribution."),
                    rx.list_item("Serial-to-parallel style routing when combined with timing/control logic."),
                ),
                rx.callout(
                    "A DEMUX routes a data signal. A decoder, studied next, instead decodes an input code into an active output; the concepts are closely related but not identical.",
                    icon="info",
                ),
            ),
            _section(
                "6", "Explore the gate equations",
                rx.text(
                    "Generate the four 1-to-4 DEMUX output equations and confirm that for a fixed select code only the selected path can carry D."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Multiplexers", variant="soft"), href="/academy/unit-4/multiplexers"),
                rx.spacer(), rx.text("Path 04 · Lesson 6", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/decoders"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
