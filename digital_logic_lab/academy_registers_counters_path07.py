"""BoolNexa Academy Path 07 — Lessons 1–2: registers and shift-register foundations."""
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


class RegisterCounterPathState(rx.State):
    register_answer: str = ""
    register_feedback: str = ""
    width_answer: str = ""
    width_feedback: str = ""
    hold_answer: str = ""
    hold_feedback: str = ""
    shift_answer: str = ""
    shift_feedback: str = ""
    sipo_answer: str = ""
    sipo_feedback: str = ""
    piso_answer: str = ""
    piso_feedback: str = ""
    ripple_answer: str = ""
    ripple_feedback: str = ""
    divide_answer: str = ""
    divide_feedback: str = ""
    mod_answer: str = ""
    mod_feedback: str = ""
    sync_answer: str = ""
    sync_feedback: str = ""
    direction_answer: str = ""
    direction_feedback: str = ""
    load_answer: str = ""
    load_feedback: str = ""
    terminal_answer: str = ""
    terminal_feedback: str = ""
    sequence_answer: str = ""
    sequence_feedback: str = ""
    decode_answer: str = ""
    decode_feedback: str = ""
    capstone_answer: str = ""
    capstone_feedback: str = ""
    state_answer: str = ""
    state_feedback: str = ""

    def set_capstone_answer(self, value: str) -> None:
        self.capstone_answer = value

    def set_decode_answer(self, value: str) -> None:
        self.decode_answer = value

    def set_direction_answer(self, value: str) -> None:
        self.direction_answer = value

    def set_divide_answer(self, value: str) -> None:
        self.divide_answer = value

    def set_hold_answer(self, value: str) -> None:
        self.hold_answer = value

    def set_load_answer(self, value: str) -> None:
        self.load_answer = value

    def set_mod_answer(self, value: str) -> None:
        self.mod_answer = value

    def set_piso_answer(self, value: str) -> None:
        self.piso_answer = value

    def set_register_answer(self, value: str) -> None:
        self.register_answer = value

    def set_ripple_answer(self, value: str) -> None:
        self.ripple_answer = value

    def set_sequence_answer(self, value: str) -> None:
        self.sequence_answer = value

    def set_shift_answer(self, value: str) -> None:
        self.shift_answer = value

    def set_sipo_answer(self, value: str) -> None:
        self.sipo_answer = value

    def set_state_answer(self, value: str) -> None:
        self.state_answer = value

    def set_sync_answer(self, value: str) -> None:
        self.sync_answer = value

    def set_terminal_answer(self, value: str) -> None:
        self.terminal_answer = value

    def set_width_answer(self, value: str) -> None:
        self.width_answer = value

    def check_register(self) -> None:
        value = self.register_answer.strip().lower().replace(" ", "").replace("-", "")
        self.register_feedback = (
            "Correct. A register stores a multi-bit word using a group of storage elements, commonly flip-flops."
            if value in {"register", "registers"}
            else "What do we call a group of storage elements used to hold a multi-bit word?"
        )

    def check_width(self) -> None:
        value = self.width_answer.strip().lower().replace(" ", "")
        self.width_feedback = (
            "Correct. Eight one-bit storage stages can hold an 8-bit word."
            if value in {"8", "8bits", "8bit"}
            else "Count one storage stage for each bit in the word."
        )

    def check_hold(self) -> None:
        value = self.hold_answer.strip().lower().replace(" ", "")
        self.hold_feedback = (
            "Correct. With loading disabled, the register keeps its previously stored word until a permitted update occurs."
            if value in {"hold", "holds", "retain", "retains", "keep", "keeps"}
            else "What should the register do when loading is disabled?"
        )

    def check_shift(self) -> None:
        value = self.shift_answer.strip().lower().replace(" ", "").replace("-", "")
        self.shift_feedback = (
            "Correct. A shift register moves stored bits from one stage to an adjacent stage on active clock events."
            if value in {"shiftregister", "shiftregisters"}
            else "Which register structure moves stored bits between neighbouring stages?"
        )

    def check_sipo(self) -> None:
        value = self.sipo_answer.strip().lower().replace(" ", "").replace("-", "")
        self.sipo_feedback = (
            "Correct. SIPO means Serial-In Parallel-Out."
            if value in {"sipo", "serialinparallelout"}
            else "Enter the acronym for Serial-In Parallel-Out."
        )

    def check_piso(self) -> None:
        value = self.piso_answer.strip().lower().replace(" ", "").replace("-", "")
        self.piso_feedback = (
            "Correct. PISO means Parallel-In Serial-Out."
            if value in {"piso", "parallelinserialout"}
            else "Enter the acronym for Parallel-In Serial-Out."
        )


    def check_ripple(self) -> None:
        value = self.ripple_answer.strip().lower().replace(" ", "").replace("-", "")
        self.ripple_feedback = (
            "Correct. A ripple counter is asynchronous because later stages are triggered by earlier stage outputs rather than one common clock edge."
            if value in {"asynchronous", "asynchronouscounter", "ripple", "ripplecounter"}
            else "Is a ripple counter synchronous or asynchronous?"
        )

    def check_divide(self) -> None:
        value = self.divide_answer.strip().lower().replace(" ", "").replace("/", "")
        self.divide_feedback = (
            "Correct. One toggling stage divides the input clock frequency by 2."
            if value in {"2", "2x", "divideby2", "half", "f2"}
            else "A toggle stage changes state once for every active input event. What frequency division results?"
        )

    def check_mod(self) -> None:
        value = self.mod_answer.strip().lower().replace(" ", "").replace("-", "")
        self.mod_feedback = (
            "Correct. MOD-10 means the counter has ten distinct states before repeating."
            if value in {"10", "ten", "10states"}
            else "How many distinct states are in a MOD-10 counter?"
        )

    def check_sync(self) -> None:
        value = self.sync_answer.strip().lower().replace(" ", "").replace("-", "")
        self.sync_feedback = (
            "Correct. In a synchronous counter, all state flip-flops respond to the same clock event while combinational logic determines which stages toggle."
            if value in {"sameclock", "commonclock", "sharedclock", "oneclock"}
            else "What clocking feature distinguishes a synchronous counter from a ripple counter?"
        )


    def check_direction(self) -> None:
        value = self.direction_answer.strip().lower().replace(" ", "").replace("-", "")
        self.direction_feedback = (
            "Correct. An up/down counter can advance or reverse its state sequence under direction control."
            if value in {"updown", "updowncounter", "bidirectional", "bidirectionalcounter"}
            else "What counter type can count in both increasing and decreasing directions?"
        )

    def check_load(self) -> None:
        value = self.load_answer.strip().lower().replace(" ", "").replace("-", "")
        self.load_feedback = (
            "Correct. Parallel load forces a chosen starting count into the counter on the defined load event."
            if value in {"parallelload", "load", "preset"}
            else "Which feature allows a counter to start from a selected binary value?"
        )

    def check_terminal(self) -> None:
        value = self.terminal_answer.strip().lower().replace(" ", "").replace("-", "")
        self.terminal_feedback = (
            "Correct. Terminal-count or carry/borrow outputs indicate that a boundary state has been reached for cascading or control."
            if value in {"terminalcount", "terminal", "carry", "borrow", "carryborrow"}
            else "What output commonly indicates that the counter has reached an end state for cascading?"
        )

    def check_sequence(self) -> None:
        value = self.sequence_answer.strip().lower().replace(" ", "").replace("-", "")
        self.sequence_feedback = (
            "Correct. A decoded counter state can create a timing step or control phase."
            if value in {"decodedstate", "decode", "decoder", "counterdecode"}
            else "What converts a binary counter state into a specific timing/control step?"
        )

    def check_decode(self) -> None:
        value = self.decode_answer.strip().lower().replace(" ", "").replace("-", "")
        self.decode_feedback = (
            "Correct. One-hot decoding activates one output for the selected state, simplifying mutually exclusive timing steps."
            if value in {"onehot", "onehotdecode", "onehotdecoder"}
            else "What decoding style activates one output corresponding to one selected state?"
        )


    def check_capstone(self) -> None:
        value = self.capstone_answer.strip().lower().replace(" ", "").replace("-", "")
        self.capstone_feedback = (
            "Correct. A register stores the datapath word while a counter or state machine can control when operations occur."
            if value in {"register", "registers"}
            else "Which component should hold a multi-bit data word between clocked operations?"
        )

    def check_state(self) -> None:
        value = self.state_answer.strip().lower().replace(" ", "").replace("-", "")
        self.state_feedback = (
            "Correct. A finite-state machine is a natural next step when transitions depend on conditions rather than only a fixed count sequence."
            if value in {"fsm", "finitestatemachine", "statemachine"}
            else "What controller structure is normally used when next steps depend on conditions and present state?"
        )


def _section(number: str, title: str, *items: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(number, radius="full", color_scheme="teal"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *items,
            spacing="4",
            align="stretch",
        ),
        **PANEL,
    )


def _table(headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(*[rx.table.column_header_cell(h) for h in headers])
        ),
        rx.table.body(
            *[
                rx.table.row(*[rx.table.cell(cell) for cell in row])
                for row in rows
            ]
        ),
        width="100%",
    )


def registers_parallel_storage_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 01", color_scheme="teal"),
            rx.heading("Registers & Parallel Data Storage", size="8"),
            rx.text(
                "A register is a group of storage elements used to hold a binary word. "
                "Registers sit at the boundary between sequential logic and datapath design: "
                "they remember values while combinational logic transforms those values.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "From one stored bit to a word",
                rx.text(
                    "A flip-flop can store one binary state. Placing several one-bit storage "
                    "stages side by side creates a register able to hold a multi-bit word."
                ),
                rx.code_block(
                    """D3 ─► [FF] ─► Q3
D2 ─► [FF] ─► Q2
D1 ─► [FF] ─► Q1
D0 ─► [FF] ─► Q0
          ▲
       common CLK

Together: Q3 Q2 Q1 Q0 = one 4-bit register""",
                    language="markup",
                ),
                rx.text("What do we call this multi-bit storage structure?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.register_answer,
                        on_change=RegisterCounterPathState.set_register_answer,
                        placeholder="Answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_register),
                ),
                rx.cond(
                    RegisterCounterPathState.register_feedback != "",
                    rx.callout(RegisterCounterPathState.register_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "Register width",
                rx.text(
                    "Register width is the number of bits stored as one word. A 4-bit register "
                    "stores four bits at once; an 8-bit register stores eight bits; wider "
                    "registers follow the same idea."
                ),
                _table(
                    ("Register", "Storage stages", "Example word"),
                    (
                        ("4-bit", "4", "1011"),
                        ("8-bit", "8", "11001010"),
                        ("16-bit", "16", "16 binary positions"),
                    ),
                ),
                rx.text("How many one-bit stages are required for an 8-bit register?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.width_answer,
                        on_change=RegisterCounterPathState.set_width_answer,
                        placeholder="Number",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_width),
                ),
                rx.cond(
                    RegisterCounterPathState.width_feedback != "",
                    rx.callout(RegisterCounterPathState.width_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "3",
                "Parallel load",
                rx.text(
                    "With parallel loading, all bits of the new word are presented together. "
                    "On the active clock event, enabled stages capture their corresponding input "
                    "bits at the same logical update point."
                ),
                rx.code_block(
                    """Before clock: Q = 0011
Parallel D:     1010
LOAD = 1

active clock event
       │
       ▼
After clock:  Q = 1010""",
                    language="markup",
                ),
                rx.callout(
                    "Actual setup, hold and clock-to-output timing depend on the chosen device. "
                    "The Academy diagram shows the logical state transition, not a universal timing value.",
                    icon="info",
                ),
            ),
            _section(
                "4",
                "Load enable and hold",
                rx.text(
                    "A load-enable control decides whether the register accepts a new word or "
                    "keeps the old one. Conceptually, the data path can select either new input "
                    "data or feedback from the current output."
                ),
                rx.code_block(
                    """              ┌──────── new D
              ▼
Q feedback ─► [ select ] ─► register D
                 ▲
               LOAD

LOAD = 1 → capture selected new data
LOAD = 0 → feed back current data and retain state""",
                    language="markup",
                ),
                rx.text("What should the register do when LOAD is disabled?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.hold_answer,
                        on_change=RegisterCounterPathState.set_hold_answer,
                        placeholder="Answer",
                        max_width="180px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_hold),
                ),
                rx.cond(
                    RegisterCounterPathState.hold_feedback != "",
                    rx.callout(RegisterCounterPathState.hold_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Registers inside a datapath",
                rx.text(
                    "Registers separate operations across clocked stages. They can hold operands, "
                    "intermediate results, addresses, instruction fields, counters and control state."
                ),
                rx.code_block(
                    """Register A ──┐
             ├─► combinational logic ─► Result register
Register B ──┘                         ▲
                                      CLK""",
                    language="markup",
                ),
                rx.callout(
                    "A register is storage, not computation by itself. The combinational logic "
                    "between registers performs arithmetic, comparison, selection or other functions.",
                    icon="lightbulb",
                    color_scheme="teal",
                ),
            ),
            _section(
                "6",
                "Lesson mission",
                rx.text(
                    "Trace a 4-bit word through a parallel register: identify the D inputs, the "
                    "clock event, the load/hold decision and the stored Q outputs."
                ),
                rx.text(
                    "The important design rule is simple: determine what value should be stored, "
                    "when it may change, and when it must remain stable."
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(),
                rx.text("Path 07 · Lesson 1", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-7/shift-registers",
                ),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def shift_registers_data_movement_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 02", color_scheme="teal"),
            rx.heading("Shift Registers & Serial/Parallel Data Movement", size="8"),
            rx.text(
                "A shift register is a register whose stored bits can move between stages. "
                "This makes it useful for serial communication, data conversion, delay lines, "
                "sequence generation and many timing-oriented digital systems.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "What shifting means",
                rx.text(
                    "In a simple right-shifting register, each active clock event transfers the "
                    "previous value of one stage into the next stage to its right. A new serial bit "
                    "enters at one end while the bit at the opposite end can leave."
                ),
                rx.code_block(
                    """Serial In
    │
    ▼
 [Q3] ─► [Q2] ─► [Q1] ─► [Q0] ─► Serial Out
   ▲        ▲        ▲        ▲
             common clock

Example: 1011 → shift right with Serial In = 0 → 0101""",
                    language="markup",
                ),
                rx.text("What structure moves stored bits between neighbouring stages?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.shift_answer,
                        on_change=RegisterCounterPathState.set_shift_answer,
                        placeholder="Answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_shift),
                ),
                rx.cond(
                    RegisterCounterPathState.shift_feedback != "",
                    rx.callout(RegisterCounterPathState.shift_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "SISO, SIPO, PISO and PIPO",
                _table(
                    ("Mode", "Input", "Output", "Typical purpose"),
                    (
                        ("SISO", "Serial", "Serial", "Bit-stream delay / movement"),
                        ("SIPO", "Serial", "Parallel", "Serial-to-parallel conversion"),
                        ("PISO", "Parallel", "Serial", "Parallel-to-serial conversion"),
                        ("PIPO", "Parallel", "Parallel", "Ordinary parallel word storage"),
                    ),
                ),
                rx.callout(
                    "These names describe how data enters and leaves. A practical IC may support "
                    "more than one mode and may include reset, enable or direction controls.",
                    icon="info",
                ),
            ),
            _section(
                "3",
                "Serial-In Parallel-Out",
                rx.text(
                    "SIPO collects a stream of serial bits over several clock events. After enough "
                    "shifts, the stages collectively expose the received word in parallel."
                ),
                rx.code_block(
                    """serial stream: 1, 0, 1, 1

clock 1 → 1000
clock 2 → 0100
clock 3 → 1010
clock 4 → 1101

The exact left/right display depends on the chosen shift convention.""",
                    language="markup",
                ),
                rx.text("What acronym means Serial-In Parallel-Out?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.sipo_answer,
                        on_change=RegisterCounterPathState.set_sipo_answer,
                        placeholder="Acronym",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_sipo),
                ),
                rx.cond(
                    RegisterCounterPathState.sipo_feedback != "",
                    rx.callout(RegisterCounterPathState.sipo_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "4",
                "Parallel-In Serial-Out",
                rx.text(
                    "PISO first loads a complete word in parallel and then shifts one bit out per "
                    "active clock event. This is a common conceptual model for serialising a parallel word."
                ),
                rx.code_block(
                    """parallel load:  D3 D2 D1 D0 = 1 0 1 1
                           │
                           ▼
                     [ 1 0 1 1 ]
                           │ shift clocks
                           ▼
                    serial bit stream""",
                    language="markup",
                ),
                rx.text("What acronym means Parallel-In Serial-Out?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.piso_answer,
                        on_change=RegisterCounterPathState.set_piso_answer,
                        placeholder="Acronym",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_piso),
                ),
                rx.cond(
                    RegisterCounterPathState.piso_feedback != "",
                    rx.callout(RegisterCounterPathState.piso_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Bidirectional and universal shift registers",
                rx.text(
                    "A bidirectional shift register can move data left or right. A universal shift "
                    "register commonly combines hold, shift-left, shift-right and parallel-load "
                    "functions behind mode-control inputs."
                ),
                _table(
                    ("Mode", "Action"),
                    (
                        ("Hold", "Retain current word"),
                        ("Shift right", "Move each stage toward the right neighbour"),
                        ("Shift left", "Move each stage toward the left neighbour"),
                        ("Parallel load", "Capture a new word together"),
                    ),
                ),
                rx.callout(
                    "Mode encodings differ between devices; always use the truth/function table for "
                    "the actual register being designed with.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "Connect storage to movement",
                rx.code_block(
                    """ordinary register:  hold / parallel-load a word
shift register:     hold / move bits / often parallel-load too

Next:
registers + feedback + controlled next-state logic
                 ↓
              counters""",
                    language="markup",
                ),
                rx.text(
                    "You now have the storage and data-movement foundation needed to understand "
                    "how counters generate ordered state sequences."
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Registers", variant="soft"),
                    href="/academy/unit-7/registers-parallel-storage",
                ),
                rx.spacer(),
                rx.text("Path 07 · Lesson 2", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-7/ripple-counters"),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def ripple_counters_frequency_division_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 03", color_scheme="teal"),
            rx.heading("Ripple Counters & Frequency Division", size="8"),
            rx.text(
                "A ripple counter chains toggle-capable storage stages so the output transition of one stage clocks the next. "
                "This creates a compact binary counting sequence, but state changes do not occur everywhere at exactly the same instant.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "From toggling to counting",
                rx.text(
                    "A flip-flop configured to toggle changes state on each permitted active clock event. "
                    "Connecting several toggle stages produces a binary sequence."
                ),
                rx.code_block(
                    """input clock ─► [FF0] ─► [FF1] ─► [FF2]
                 Q0       Q1       Q2

Example stable count sequence:
000 → 001 → 010 → 011 → 100 → 101 → 110 → 111 → repeat""",
                    language="markup",
                ),
                rx.text("Is a ripple counter synchronous or asynchronous?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.ripple_answer,
                        on_change=RegisterCounterPathState.set_ripple_answer,
                        placeholder="Answer",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_ripple),
                ),
                rx.cond(
                    RegisterCounterPathState.ripple_feedback != "",
                    rx.callout(RegisterCounterPathState.ripple_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "Why it is called ripple",
                rx.text(
                    "Only the first stage receives the external clock directly. A transition then propagates through later stages. "
                    "Because real devices have propagation delay, intermediate output combinations can briefly appear while the new count settles."
                ),
                rx.code_block(
                    """external clock event
        │
        ▼
      Q0 changes
        │ propagation delay
        ▼
      Q1 may change
        │ propagation delay
        ▼
      Q2 may change""",
                    language="markup",
                ),
                rx.callout(
                    "The exact triggering edge and propagation times depend on the flip-flop implementation. "
                    "Always check the device timing specification before using ripple outputs as decode signals.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "3",
                "Frequency division",
                rx.text(
                    "Each ideal toggle stage changes output state at half the repetition rate of the signal driving it. "
                    "A cascade therefore provides successively divided clock-like outputs."
                ),
                _table(
                    ("Stage", "Ideal output frequency"),
                    (
                        ("Q0", "fCLK / 2"),
                        ("Q1", "fCLK / 4"),
                        ("Q2", "fCLK / 8"),
                        ("Q3", "fCLK / 16"),
                    ),
                ),
                rx.text("By what factor does one toggle stage divide its input frequency?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.divide_answer,
                        on_change=RegisterCounterPathState.set_divide_answer,
                        placeholder="Factor",
                        max_width="150px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_divide),
                ),
                rx.cond(
                    RegisterCounterPathState.divide_feedback != "",
                    rx.callout(RegisterCounterPathState.divide_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "4",
                "Counter modulus",
                rx.text(
                    "An n-bit binary counter has up to 2ⁿ distinct binary states before the natural sequence repeats. "
                    "The number of states in the repeating sequence is called the modulus."
                ),
                _table(
                    ("Bits", "Natural modulus", "State range"),
                    (
                        ("2", "4", "0 to 3"),
                        ("3", "8", "0 to 7"),
                        ("4", "16", "0 to 15"),
                    ),
                ),
                rx.callout(
                    "Counters can be deliberately shortened to a modulus smaller than 2ⁿ by detecting or controlling selected states.",
                    icon="info",
                ),
            ),
            _section(
                "5",
                "Ripple-counter timing caution",
                rx.text(
                    "Because outputs ripple rather than switch together, decoding a multi-bit ripple count can produce temporary glitches. "
                    "This is one reason synchronous counter structures are preferred when precise simultaneous state transitions matter."
                ),
                rx.code_block(
                    """desired stable transition: 011 → 100

physical ripple may briefly pass through
011 → 010 → 000 → 100
(depending on circuit polarity and propagation)

Do not assume every intermediate pattern is a valid stable count.""",
                    language="markup",
                ),
            ),
            _section(
                "6",
                "Applications",
                rx.text(
                    "Ripple counters are useful for simple event counting, clock division and low-complexity timing functions "
                    "when their asynchronous propagation behaviour is acceptable."
                ),
                rx.callout(
                    "Next, we redesign counting so every state flip-flop receives the same clock event.",
                    icon="arrow-right",
                    color_scheme="teal",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Shift registers", variant="soft"),
                    href="/academy/unit-7/shift-registers",
                ),
                rx.spacer(),
                rx.text("Path 07 · Lesson 3", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-7/synchronous-counters",
                ),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def synchronous_counters_modulo_n_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 04", color_scheme="teal"),
            rx.heading("Synchronous Counters & Modulo-N Design", size="8"),
            rx.text(
                "A synchronous counter drives all state flip-flops from a common clock. "
                "Combinational next-state logic decides which stages change on that clock event, "
                "reducing the stage-by-stage ripple of an asynchronous counter.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Common-clock architecture",
                rx.code_block(
                    """                 ┌──────── next-state logic ────────┐
                 │                                 │
CLK ─────────────┼──► [FF2]   [FF1]   [FF0] ◄─────┘
                 │      │        │       │
                 └──────┴────────┴───────┴── same clock event""",
                    language="markup",
                ),
                rx.text("What clocking feature distinguishes a synchronous counter?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.sync_answer,
                        on_change=RegisterCounterPathState.set_sync_answer,
                        placeholder="Answer",
                        max_width="210px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_sync),
                ),
                rx.cond(
                    RegisterCounterPathState.sync_feedback != "",
                    rx.callout(RegisterCounterPathState.sync_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "Binary synchronous up-counter idea",
                rx.text(
                    "For a simple binary up-counter, the least-significant stage toggles every count. "
                    "Higher stages toggle only when the required lower-order bits indicate a carry condition."
                ),
                _table(
                    ("Stage", "Conceptual toggle condition"),
                    (
                        ("Q0", "Every enabled count"),
                        ("Q1", "When Q0 = 1"),
                        ("Q2", "When Q1·Q0 = 1"),
                        ("Q3", "When Q2·Q1·Q0 = 1"),
                    ),
                ),
                rx.callout(
                    "The exact equations depend on flip-flop type and counter features such as enable, load, direction and reset.",
                    icon="info",
                ),
            ),
            _section(
                "3",
                "Modulo-N counters",
                rx.text(
                    "A modulo-N counter cycles through N defined states and then returns to the beginning of its sequence. "
                    "N does not need to equal a power of two."
                ),
                rx.code_block(
                    """MOD-6 example:
000 → 001 → 010 → 011 → 100 → 101 → 000 → ...

Six stable states are used.""",
                    language="markup",
                ),
                rx.text("How many distinct states are in a MOD-10 counter?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.mod_answer,
                        on_change=RegisterCounterPathState.set_mod_answer,
                        placeholder="Number",
                        max_width="150px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_mod),
                ),
                rx.cond(
                    RegisterCounterPathState.mod_feedback != "",
                    rx.callout(RegisterCounterPathState.mod_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "4",
                "How many flip-flops are required?",
                rx.text(
                    "Choose the smallest n such that 2ⁿ ≥ N. "
                    "For MOD-10, three bits are not enough because 2³ = 8, while four bits provide 16 possible encodings."
                ),
                _table(
                    ("Desired modulus", "Minimum bits", "Unused encodings if simple binary coding"),
                    (
                        ("6", "3", "2"),
                        ("10", "4", "6"),
                        ("16", "4", "0"),
                    ),
                ),
            ),
            _section(
                "5",
                "Designing the sequence",
                rx.text(
                    "A systematic synchronous-counter design starts from the desired state sequence, "
                    "builds a present-state/next-state table, derives flip-flop excitation or next-state equations, "
                    "then verifies reset and any unused-state behaviour."
                ),
                rx.code_block(
                    """1. Define required sequence
2. Assign binary state codes
3. Write present → next state table
4. Derive next-state / excitation logic
5. Implement common-clock storage
6. Verify legal and unused states""",
                    language="markup",
                ),
                rx.callout(
                    "Unused states should not be ignored in safety- or reliability-sensitive designs. "
                    "Define how the circuit behaves if an unexpected state is entered.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "Ripple vs synchronous",
                _table(
                    ("Feature", "Ripple counter", "Synchronous counter"),
                    (
                        ("Clocking", "Stage-to-stage", "Common clock"),
                        ("Propagation", "Ripples through stages", "State logic evaluated for one clock event"),
                        ("Complexity", "Usually simpler", "More next-state logic"),
                        ("High-speed decoding", "Timing caution required", "Generally easier to control"),
                    ),
                ),
                rx.text(
                    "Both structures count states; the engineering choice depends on speed, simplicity, timing discipline and required features."
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Ripple counters", variant="soft"),
                    href="/academy/unit-7/ripple-counters",
                ),
                rx.spacer(),
                rx.text("Path 07 · Lesson 4", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-7/up-down-programmable-counters"),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def up_down_programmable_counters_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 05", color_scheme="teal"),
            rx.heading("Up/Down & Programmable Counters", size="8"),
            rx.text(
                "Practical counters often need more than a fixed upward sequence. Direction control, enable, parallel load, "
                "reset and terminal-count outputs let a counter participate in larger control and datapath systems.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Bidirectional counting",
                rx.text(
                    "An up/down counter follows one state sequence when the direction input selects UP and the reverse sequence "
                    "when DOWN is selected."
                ),
                rx.code_block(
                    """UP:
000 → 001 → 010 → 011 → 100 → ...

DOWN:
100 → 011 → 010 → 001 → 000 → ...""",
                    language="markup",
                ),
                rx.text("What counter type can count in both directions?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.direction_answer,
                        on_change=RegisterCounterPathState.set_direction_answer,
                        placeholder="Answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_direction),
                ),
                rx.cond(
                    RegisterCounterPathState.direction_feedback != "",
                    rx.callout(RegisterCounterPathState.direction_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "Count enable",
                rx.text(
                    "A count-enable input lets the counter either advance according to its direction or hold its current state "
                    "on an active clock event."
                ),
                _table(
                    ("ENABLE", "Action"),
                    (
                        ("0", "Hold present count"),
                        ("1", "Perform selected count operation"),
                    ),
                ),
                rx.callout(
                    "The active level of enable is device-specific. Some ICs provide multiple enable inputs for cascading.",
                    icon="info",
                ),
            ),
            _section(
                "3",
                "Parallel load / preset",
                rx.text(
                    "Parallel load lets the designer place a selected binary word into the counter instead of incrementing or decrementing."
                ),
                rx.code_block(
                    """Current count: 0110
LOAD = active
Parallel input = 1010
clock/load event
      │
      ▼
New count: 1010""",
                    language="markup",
                ),
                rx.text("Which feature lets the counter start from a selected value?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.load_answer,
                        on_change=RegisterCounterPathState.set_load_answer,
                        placeholder="Answer",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_load),
                ),
                rx.cond(
                    RegisterCounterPathState.load_feedback != "",
                    rx.callout(RegisterCounterPathState.load_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "4",
                "Terminal count and cascading",
                rx.text(
                    "A terminal-count, carry or borrow indication tells other logic that the present counter has reached a boundary "
                    "relevant to extension or sequencing."
                ),
                rx.code_block(
                    """low-order counter ── terminal count ──► enable next counter
      Q[3:0]                              Q[7:4]

Together they can form a wider count word.""",
                    language="markup",
                ),
                rx.text("What kind of output indicates an end state for cascading?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.terminal_answer,
                        on_change=RegisterCounterPathState.set_terminal_answer,
                        placeholder="Answer",
                        max_width="210px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_terminal),
                ),
                rx.cond(
                    RegisterCounterPathState.terminal_feedback != "",
                    rx.callout(RegisterCounterPathState.terminal_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Control priority matters",
                rx.text(
                    "Counters can have reset, load, enable and direction controls. The implementation must define what happens "
                    "if more than one request is active at the same time."
                ),
                rx.code_block(
                    """Example conceptual priority:
RESET
  ↓
LOAD
  ↓
COUNT ENABLE
  ↓
HOLD""",
                    language="markup",
                ),
                rx.callout(
                    "Do not assume this priority for a real device. Read the function table and timing diagram for the exact IC or HDL design.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "Design use cases",
                rx.text(
                    "Programmable counters appear in address generation, digital timers, event measurement, frequency division, "
                    "motor-step sequencing and finite control systems."
                ),
                rx.callout(
                    "Next we use counter states as timing steps that drive control outputs.",
                    icon="arrow-right",
                    color_scheme="teal",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Synchronous counters", variant="soft"),
                    href="/academy/unit-7/synchronous-counters",
                ),
                rx.spacer(),
                rx.text("Path 07 · Lesson 5", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-7/timing-sequences",
                ),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def timing_sequences_counter_control_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 06", color_scheme="teal"),
            rx.heading("Timing Sequences & Counter-Based Control", size="8"),
            rx.text(
                "A counter can act as a time-step generator. By decoding selected counter states, a digital system can create "
                "ordered control phases for displays, communication, machines and datapaths.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Counter as a timing step generator",
                rx.text(
                    "Each stable counter state can represent one step in an operating sequence. A decoder converts the binary state "
                    "into individual control signals."
                ),
                rx.code_block(
                    """clock ─► counter ─► state decoder ─► T0
                                  │         ├─► T1
                                  │         ├─► T2
                                  │         └─► T3
                                  ▼
                             ordered phases""",
                    language="markup",
                ),
                rx.text("What converts a binary count state into a specific timing step?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.sequence_answer,
                        on_change=RegisterCounterPathState.set_sequence_answer,
                        placeholder="Answer",
                        max_width="210px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_sequence),
                ),
                rx.cond(
                    RegisterCounterPathState.sequence_feedback != "",
                    rx.callout(RegisterCounterPathState.sequence_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "One-hot timing outputs",
                rx.text(
                    "With one-hot decoding, one output corresponds to one selected state. This is convenient for mutually exclusive "
                    "time slots or control phases."
                ),
                _table(
                    ("Count", "T0", "T1", "T2", "T3"),
                    (
                        ("00", "1", "0", "0", "0"),
                        ("01", "0", "1", "0", "0"),
                        ("10", "0", "0", "1", "0"),
                        ("11", "0", "0", "0", "1"),
                    ),
                ),
                rx.text("What decoding style activates one selected output?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.decode_answer,
                        on_change=RegisterCounterPathState.set_decode_answer,
                        placeholder="Answer",
                        max_width="190px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_decode),
                ),
                rx.cond(
                    RegisterCounterPathState.decode_feedback != "",
                    rx.callout(RegisterCounterPathState.decode_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "3",
                "Sequence length and modulus",
                rx.text(
                    "The counter modulus determines how many timing steps repeat before the sequence starts again. "
                    "A MOD-6 timing counter can produce six repeating phases T0 through T5."
                ),
                rx.code_block(
                    """T0 → T1 → T2 → T3 → T4 → T5
▲                         │
└─────────────────────────┘ repeat""",
                    language="markup",
                ),
            ),
            _section(
                "4",
                "Generating control signals",
                rx.text(
                    "A timing step may directly enable an action or combine with conditions. For example, a register may load only "
                    "during T2 and only when READY is true."
                ),
                rx.code_block(
                    """LOAD_REGISTER = T2 · READY
WRITE_MEMORY  = T4 · ENABLE
DONE          = T5""",
                    language="markup",
                ),
                rx.callout(
                    "Counter-based sequencing is simple for fixed repetitive timing. More complex conditional behaviour is usually "
                    "easier to express with a finite-state machine.",
                    icon="lightbulb",
                    color_scheme="teal",
                ),
            ),
            _section(
                "5",
                "Timing hazards",
                rx.text(
                    "Decoded counter outputs must respect the timing behaviour of the source counter and decoder. Ripple counters can "
                    "briefly pass through intermediate states, while synchronous counters generally make state decoding easier to manage."
                ),
                rx.callout(
                    "Glitch-free control may require synchronous decoding, registered outputs, carefully constrained combinational logic "
                    "or other implementation-specific techniques.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "From counters to controllers",
                rx.code_block(
                    """fixed sequence:
clock → counter → decoder → control outputs

conditional sequence:
clock → state register → next-state logic → control outputs

The second structure is the foundation of an FSM.""",
                    language="markup",
                ),
                rx.text(
                    "You now know how registers hold data, shift registers move it, counters generate ordered states, "
                    "and decoded states can create timing/control phases."
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Programmable counters", variant="soft"),
                    href="/academy/unit-7/up-down-programmable-counters",
                ),
                rx.spacer(),
                rx.text("Path 07 · Lesson 6", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Final lesson →", variant="soft"), href="/academy/unit-7/register-counter-integration"),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )


def register_counter_integration_capstone_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 07 · LESSON 07 · PATH FINALE", color_scheme="green"),
            rx.heading("Register–Counter System Integration & Design Challenge", size="8"),
            rx.text(
                "The final Path 07 lesson combines storage and sequencing into one digital system. "
                "Registers hold working data, shift registers move it, counters create ordered events, "
                "and control logic decides when each operation is allowed to occur.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Build the full data-and-control picture",
                rx.code_block(
                    """                 CONTROL PATH
clock ─► counter / FSM ─► enables, loads, shifts, selects
              │
              ▼
       timing / state decode
              │
              ▼
                 DATA PATH
input ─► register ─► logic ─► shift register ─► output
             ▲                     │
             └──── stored data ────┘""",
                    language="markup",
                ),
                rx.text("Which component should hold a multi-bit data word between clocked operations?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.capstone_answer,
                        on_change=RegisterCounterPathState.set_capstone_answer,
                        placeholder="Answer",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_capstone),
                ),
                rx.cond(
                    RegisterCounterPathState.capstone_feedback != "",
                    rx.callout(RegisterCounterPathState.capstone_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "Capstone example: four-step data mover",
                rx.text(
                    "Imagine a controller that captures a 4-bit input word, shifts it once, presents it to an output register, "
                    "and then signals completion. A MOD-4 synchronous counter can provide four fixed time steps."
                ),
                _table(
                    ("Step", "Counter state", "Control action"),
                    (
                        ("T0", "00", "Load input register"),
                        ("T1", "01", "Shift data once"),
                        ("T2", "10", "Load output register"),
                        ("T3", "11", "Assert DONE, then restart"),
                    ),
                ),
                rx.code_block(
                    """T0: INPUT_REG_LOAD = 1
T1: SHIFT_ENABLE   = 1
T2: OUTPUT_LOAD    = 1
T3: DONE           = 1""",
                    language="markup",
                ),
            ),
            _section(
                "3",
                "Separate datapath from control",
                rx.text(
                    "A useful design discipline is to separate the datapath — where data is stored and transformed — "
                    "from the control path — which decides when those operations occur."
                ),
                _table(
                    ("Datapath elements", "Control elements"),
                    (
                        ("Registers", "Counters"),
                        ("Shift registers", "State decoder"),
                        ("MUX / arithmetic / logic", "Enable and load signals"),
                        ("Data buses", "FSM next-state logic"),
                    ),
                ),
                rx.callout(
                    "This separation is conceptual. In HDL or silicon, the blocks interact tightly, but the distinction makes design and verification easier.",
                    icon="info",
                ),
            ),
            _section(
                "4",
                "When a counter is enough — and when it is not",
                rx.text(
                    "A decoded counter is effective for a fixed repeating sequence. If the next action depends on inputs such as READY, ERROR, "
                    "EMPTY or DONE, a finite-state machine is usually a clearer controller."
                ),
                rx.code_block(
                    """fixed:
T0 → T1 → T2 → T3 → repeat

conditional:
IDLE ─start─► LOAD ─ready─► SHIFT
  ▲                         │
  └──────── done ◄──────── OUTPUT""",
                    language="markup",
                ),
                rx.text("What controller is normally used when next steps depend on conditions and present state?"),
                rx.hstack(
                    rx.input(
                        value=RegisterCounterPathState.state_answer,
                        on_change=RegisterCounterPathState.set_state_answer,
                        placeholder="Answer",
                        max_width="210px",
                    ),
                    rx.button("Check", on_click=RegisterCounterPathState.check_state),
                ),
                rx.cond(
                    RegisterCounterPathState.state_feedback != "",
                    rx.callout(RegisterCounterPathState.state_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Path 07 concept map",
                rx.code_block(
                    """registers
   │
   ├─ parallel load / hold
   └─ shift registers
          │
          ├─ SISO / SIPO / PISO / PIPO
          └─ serial / parallel data movement

counters
   │
   ├─ ripple / asynchronous
   ├─ synchronous
   ├─ modulo-N
   ├─ up/down + load + enable
   └─ timing-state decoding
              │
              ▼
      integrated controller/datapath""",
                    language="markup",
                ),
            ),
            _section(
                "6",
                "Engineering verification checklist",
                _table(
                    ("Check", "Question"),
                    (
                        ("Reset", "Does every storage element enter a defined starting state?"),
                        ("Clocking", "Which elements update on each active clock event?"),
                        ("Enable/load", "Can two controls conflict? What is the priority?"),
                        ("Counter sequence", "Are all intended states reached in the correct order?"),
                        ("Unused states", "What happens if an unexpected state is entered?"),
                        ("Timing", "Are setup, hold and propagation requirements respected?"),
                        ("Outputs", "Can decode glitches create unsafe control pulses?"),
                    ),
                ),
                rx.callout(
                    "Functional simulation is necessary but not sufficient for hardware sign-off. "
                    "Device-specific timing constraints and implementation checks are still required.",
                    icon="triangle-alert",
                    color_scheme="amber",
                ),
            ),
            _section(
                "7",
                "Path complete",
                rx.callout(
                    "Path 07 complete: you can now connect registers, shifting, counters and timing control into a structured sequential subsystem.",
                    icon="graduation-cap",
                    color_scheme="green",
                ),
                rx.text(
                    "This completes the Academy's Registers and Counters path and provides the foundation for larger datapaths, controllers and processor-style systems.",
                    font_weight="600",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Timing sequences", variant="soft"),
                    href="/academy/unit-7/timing-sequences",
                ),
                rx.spacer(),
                rx.text("Path 07 · Complete", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Return to Academy", color_scheme="green"),
                    href="/academy",
                ),
                width="100%",
                padding_y="16px",
            ),
            width="min(1180px, 94vw)",
            margin="0 auto",
            padding_y="28px",
            spacing="5",
            align="stretch",
        ),
    )
