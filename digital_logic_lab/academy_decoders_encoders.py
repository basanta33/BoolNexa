"""BoolNexa Academy Path 04 lessons 7 and 8: decoders, encoders and priority encoders."""

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


class DecoderEncoderState(rx.State):
    decoder_outputs: str = ""
    decoder_outputs_feedback: str = ""
    decoder_active: str = ""
    decoder_active_feedback: str = ""
    encoder_bits: str = ""
    encoder_bits_feedback: str = ""
    priority_answer: str = ""
    priority_feedback: str = ""

    def set_decoder_active(self, value: str) -> None:
        self.decoder_active = value

    def set_decoder_outputs(self, value: str) -> None:
        self.decoder_outputs = value

    def set_encoder_bits(self, value: str) -> None:
        self.encoder_bits = value

    def set_priority_answer(self, value: str) -> None:
        self.priority_answer = value

    def check_decoder_outputs(self):
        self.decoder_outputs_feedback = (
            "Correct. Three input bits represent 2³ = 8 codes, so a 3-to-8 decoder has eight decoded outputs."
            if self.decoder_outputs.strip() == "8"
            else "Use 2ⁿ outputs for an n-bit binary decoder."
        )

    def check_decoder_active(self):
        value = self.decoder_active.strip().upper().replace(" ", "")
        self.decoder_active_feedback = (
            "Correct. Input 10₂ selects output Y2."
            if value in {"Y2", "2"}
            else "Interpret 10₂ as decimal index 2."
        )

    def check_encoder_bits(self):
        self.encoder_bits_feedback = (
            "Correct. Eight one-hot input choices require a 3-bit binary code."
            if self.encoder_bits.strip() == "3"
            else "Find n such that 2ⁿ = 8."
        )

    def check_priority(self):
        value = self.priority_answer.strip().upper().replace(" ", "")
        self.priority_feedback = (
            "Correct. With D3 highest priority, D3 wins even when D1 is also active."
            if value in {"D3", "3", "11"}
            else "A priority encoder reports the highest-priority asserted input."
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


def decoders_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 07", color_scheme="blue"),
            rx.heading("Binary Decoders", size="8"),
            rx.text(
                "A decoder converts an n-bit input code into one of up to 2ⁿ output selections. "
                "It is a fundamental building block for address selection, instruction decoding and display/control systems.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The 2-to-4 decoder",
                rx.text(
                    "A basic active-high 2-to-4 decoder has inputs A and B. Exactly one output is high for each input code."
                ),
                _table(
                    ("A", "B", "Y0", "Y1", "Y2", "Y3"),
                    (
                        ("0","0","1","0","0","0"),
                        ("0","1","0","1","0","0"),
                        ("1","0","0","0","1","0"),
                        ("1","1","0","0","0","1"),
                    ),
                ),
                rx.code_block(
                    "Y0 = A'B'\n"
                    "Y1 = A'B\n"
                    "Y2 = AB'\n"
                    "Y3 = AB",
                    language="markup",
                ),
            ),
            _section(
                "2", "Decode a binary input",
                rx.text("For a 2-to-4 active-high decoder, which output is selected by AB=10?"),
                rx.hstack(
                    rx.input(value=DecoderEncoderState.decoder_active,
                             on_change=DecoderEncoderState.set_decoder_active,
                             placeholder="Y0–Y3", max_width="160px"),
                    rx.button("Check", on_click=DecoderEncoderState.check_decoder_active),
                ),
                rx.cond(DecoderEncoderState.decoder_active_feedback != "",
                        rx.callout(DecoderEncoderState.decoder_active_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "The n-to-2ⁿ rule",
                rx.text(
                    "An n-bit binary decoder can distinguish 2ⁿ binary input combinations, so a full decoder provides up to 2ⁿ outputs."
                ),
                rx.code_block(
                    "2 inputs → 4 outputs\n"
                    "3 inputs → 8 outputs\n"
                    "4 inputs → 16 outputs",
                    language="markup",
                ),
                rx.text("How many outputs does a full 3-to-8 decoder have?"),
                rx.hstack(
                    rx.input(value=DecoderEncoderState.decoder_outputs,
                             on_change=DecoderEncoderState.set_decoder_outputs,
                             placeholder="Outputs", max_width="150px"),
                    rx.button("Check", on_click=DecoderEncoderState.check_decoder_outputs),
                ),
                rx.cond(DecoderEncoderState.decoder_outputs_feedback != "",
                        rx.callout(DecoderEncoderState.decoder_outputs_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "Enable inputs",
                rx.text(
                    "Many practical decoder ICs include an Enable input. When disabled, the decoder does not perform its normal one-of-N selection. "
                    "Enable pins also make it possible to cascade smaller decoders into larger decoding systems."
                ),
                rx.callout(
                    "Always check whether a real device uses active-high or active-low enable and output signals; bubble notation and datasheets matter.",
                    icon="info",
                ),
            ),
            _section(
                "5", "Decoder as a minterm generator",
                rx.text(
                    "Each output of a full binary decoder corresponds to one minterm. "
                    "This means Boolean functions can be implemented by OR-ing the decoder outputs associated with the function's required minterms."
                ),
                rx.code_block(
                    "F(A,B) = Σm(1,2)\n"
                    "2-to-4 decoder generates Y0..Y3\n"
                    "F = Y1 + Y2",
                    language="markup",
                ),
                rx.callout(
                    "This connects canonical SOP notation directly to practical combinational hardware.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Build the decoder equations",
                rx.text(
                    "Use BoolNexa to generate the four 2-to-4 decoder output circuits and verify that only the selected minterm output is active."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Demultiplexers", variant="soft"), href="/academy/unit-4/demultiplexers"),
                rx.spacer(), rx.text("Path 04 · Lesson 7", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/encoders"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def encoders_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 04 · LESSON 08", color_scheme="blue"),
            rx.heading("Encoders & Priority Encoders", size="8"),
            rx.text(
                "An encoder performs the reverse coding idea of a decoder: it converts an active input line into a compact binary code. "
                "Priority encoders resolve the important real-world case where several inputs may be active simultaneously.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The 4-to-2 encoder",
                rx.text(
                    "For a simple one-hot 4-to-2 encoder, exactly one of D0–D3 is assumed active."
                ),
                _table(
                    ("Active input", "Y1", "Y0", "Binary code"),
                    (
                        ("D0","0","0","00"),
                        ("D1","0","1","01"),
                        ("D2","1","0","10"),
                        ("D3","1","1","11"),
                    ),
                ),
                rx.code_block(
                    "Y1 = D2 + D3\n"
                    "Y0 = D1 + D3",
                    language="markup",
                ),
            ),
            _section(
                "2", "Compression rule",
                rx.text(
                    "A conventional 2ⁿ-to-n encoder represents one of 2ⁿ input positions using n output bits."
                ),
                rx.text("How many output bits are needed to encode one of eight one-hot inputs?"),
                rx.hstack(
                    rx.input(value=DecoderEncoderState.encoder_bits,
                             on_change=DecoderEncoderState.set_encoder_bits,
                             placeholder="Bits", max_width="140px"),
                    rx.button("Check", on_click=DecoderEncoderState.check_encoder_bits),
                ),
                rx.cond(DecoderEncoderState.encoder_bits_feedback != "",
                        rx.callout(DecoderEncoderState.encoder_bits_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "3", "The ambiguity problem",
                rx.text(
                    "A simple encoder assumes only one input is active. If D1 and D3 are both 1, the ordinary equations no longer describe "
                    "a unique input position. Real systems therefore often need a priority rule."
                ),
                rx.callout(
                    "One-hot assumptions must be stated explicitly. Without them, a basic encoder can produce an ambiguous code.",
                    icon="info",
                ),
            ),
            _section(
                "4", "Priority encoder",
                rx.text(
                    "A priority encoder assigns an order of importance. For a 4-to-2 priority encoder with D3 highest priority, "
                    "D3 overrides D2, D1 and D0 whenever D3 is asserted."
                ),
                _table(
                    ("D3","D2","D1","D0","Encoded source"),
                    (
                        ("1","X","X","X","D3 → 11"),
                        ("0","1","X","X","D2 → 10"),
                        ("0","0","1","X","D1 → 01"),
                        ("0","0","0","1","D0 → 00"),
                    ),
                ),
                rx.text("If D3=1 and D1=1, which input wins?"),
                rx.hstack(
                    rx.input(value=DecoderEncoderState.priority_answer,
                             on_change=DecoderEncoderState.set_priority_answer,
                             placeholder="Input", max_width="160px"),
                    rx.button("Check", on_click=DecoderEncoderState.check_priority),
                ),
                rx.cond(DecoderEncoderState.priority_feedback != "",
                        rx.callout(DecoderEncoderState.priority_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Valid-output signal",
                rx.text(
                    "A useful priority encoder often includes a Valid output to distinguish 'D0 is selected' from 'no input is active', "
                    "because both situations could otherwise produce code 00."
                ),
                rx.code_block(
                    "No active input → V=0\n"
                    "Any valid active input → V=1",
                    language="markup",
                ),
                rx.unordered_list(
                    rx.list_item("Interrupt controllers use priority encoding."),
                    rx.list_item("Arbitration logic chooses among simultaneous requests."),
                    rx.list_item("Keyboards and input systems encode active positions."),
                ),
            ),
            _section(
                "6", "Explore the equations",
                rx.text(
                    "Use Boolean Lab to inspect Y1=D2+D3 and Y0=D1+D3 for the simple one-hot encoder, then generate their circuits."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Decoders", variant="soft"), href="/academy/unit-4/decoders"),
                rx.spacer(), rx.text("Path 04 · Lesson 8", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-4/integrated-design"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
