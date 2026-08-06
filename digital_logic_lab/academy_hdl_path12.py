"""BoolNexa Academy Path 12 — HDL, FPGA & Digital System Design."""
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


class HDLFPGAState(rx.State):
    hdl_answer: str = ""
    hdl_feedback: str = ""
    fpga_answer: str = ""
    fpga_feedback: str = ""
    synth_answer: str = ""
    synth_feedback: str = ""
    comb_answer: str = ""
    comb_feedback: str = ""
    module_answer: str = ""
    module_feedback: str = ""
    blocking_answer: str = ""
    blocking_feedback: str = ""
    register_answer: str = ""
    register_feedback: str = ""
    edge_answer: str = ""
    edge_feedback: str = ""
    nonblocking_answer: str = ""
    nonblocking_feedback: str = ""
    fsm_answer: str = ""
    fsm_feedback: str = ""
    moore_answer: str = ""
    moore_feedback: str = ""
    mealy_answer: str = ""
    mealy_feedback: str = ""
    testbench_answer: str = ""
    testbench_feedback: str = ""
    dut_answer: str = ""
    dut_feedback: str = ""
    assertion_answer: str = ""
    assertion_feedback: str = ""
    constraint_answer: str = ""
    constraint_feedback: str = ""
    slack_answer: str = ""
    slack_feedback: str = ""
    critical_answer: str = ""
    critical_feedback: str = ""
    bram_answer: str = ""
    bram_feedback: str = ""
    dsp_answer: str = ""
    dsp_feedback: str = ""
    pipeline_answer: str = ""
    pipeline_feedback: str = ""
    bitstream_answer: str = ""
    bitstream_feedback: str = ""
    io_answer: str = ""
    io_feedback: str = ""
    ila_answer: str = ""
    ila_feedback: str = ""

    def set_hdl_answer(self, value: str) -> None:
        self.hdl_answer = value

    def set_fpga_answer(self, value: str) -> None:
        self.fpga_answer = value

    def set_synth_answer(self, value: str) -> None:
        self.synth_answer = value

    def set_comb_answer(self, value: str) -> None:
        self.comb_answer = value

    def set_module_answer(self, value: str) -> None:
        self.module_answer = value

    def set_blocking_answer(self, value: str) -> None:
        self.blocking_answer = value

    def set_register_answer(self, value: str) -> None:
        self.register_answer = value

    def set_edge_answer(self, value: str) -> None:
        self.edge_answer = value

    def set_nonblocking_answer(self, value: str) -> None:
        self.nonblocking_answer = value

    def set_fsm_answer(self, value: str) -> None:
        self.fsm_answer = value

    def set_moore_answer(self, value: str) -> None:
        self.moore_answer = value

    def set_mealy_answer(self, value: str) -> None:
        self.mealy_answer = value

    def set_testbench_answer(self, value: str) -> None:
        self.testbench_answer = value

    def set_dut_answer(self, value: str) -> None:
        self.dut_answer = value

    def set_assertion_answer(self, value: str) -> None:
        self.assertion_answer = value

    def set_constraint_answer(self, value: str) -> None:
        self.constraint_answer = value

    def set_slack_answer(self, value: str) -> None:
        self.slack_answer = value

    def set_critical_answer(self, value: str) -> None:
        self.critical_answer = value

    def set_bram_answer(self, value: str) -> None:
        self.bram_answer = value

    def set_dsp_answer(self, value: str) -> None:
        self.dsp_answer = value

    def set_pipeline_answer(self, value: str) -> None:
        self.pipeline_answer = value

    def set_bitstream_answer(self, value: str) -> None:
        self.bitstream_answer = value

    def set_io_answer(self, value: str) -> None:
        self.io_answer = value

    def set_ila_answer(self, value: str) -> None:
        self.ila_answer = value

    def check_bitstream(self) -> None:
        value = self.bitstream_answer.strip().lower().replace(" ", "").replace("-", "")
        self.bitstream_feedback = (
            "Correct. The bitstream configures the FPGA fabric to implement the compiled design."
            if value in {"bitstream", "configurationbitstream", "configbitstream"}
            else "What generated configuration file programs the FPGA fabric?"
        )

    def check_io(self) -> None:
        value = self.io_answer.strip().lower().replace(" ", "").replace("-", "")
        self.io_feedback = (
            "Correct. Pin/I/O constraints assign logical ports to physical device pins and electrical standards."
            if value in {"ioconstraint", "pinconstraint", "ioconstraints", "pinconstraints", "xdc", "qsf"}
            else "What constraints connect logical HDL ports to physical FPGA pins and electrical standards?"
        )

    def check_ila(self) -> None:
        value = self.ila_answer.strip().lower().replace(" ", "").replace("-", "")
        self.ila_feedback = (
            "Correct. An integrated logic analyzer captures internal FPGA signals while the design runs in hardware."
            if value in {"ila", "integratedlogicanalyzer", "logic analyzer", "logicanalyzer"}
            else "What embedded FPGA debug instrument captures internal signals in real hardware?"
        )

    def check_bram(self) -> None:
        value = self.bram_answer.strip().lower().replace(" ", "").replace("-", "")
        self.bram_feedback = (
            "Correct. Block RAM is dedicated on-chip memory inside many FPGAs."
            if value in {"blockram", "bram", "blockmemory"}
            else "What dedicated FPGA resource stores larger on-chip memories more efficiently than individual flip-flops?"
        )

    def check_dsp(self) -> None:
        value = self.dsp_answer.strip().lower().replace(" ", "").replace("-", "")
        self.dsp_feedback = (
            "Correct. DSP blocks provide dedicated arithmetic resources such as multipliers and multiply-accumulate datapaths."
            if value in {"dsp", "dspblock", "digitalsignalprocessingblock"}
            else "What FPGA resource is optimized for arithmetic such as multiplication and multiply-accumulate operations?"
        )

    def check_pipeline(self) -> None:
        value = self.pipeline_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pipeline_feedback = (
            "Correct. Pipelining inserts registers between stages so each cycle contains less combinational work."
            if value in {"pipeline", "pipelining", "registerpipeline"}
            else "What design technique inserts registers between datapath stages to improve clock frequency?"
        )

    def check_constraint(self) -> None:
        value = self.constraint_answer.strip().lower().replace(" ", "").replace("-", "")
        self.constraint_feedback = (
            "Correct. Timing constraints tell the implementation tools what timing requirements the design must satisfy."
            if value in {"constraint", "timingconstraint", "constraints"}
            else "What specification tells FPGA tools the required clocks and timing limits?"
        )

    def check_slack(self) -> None:
        value = self.slack_answer.strip().lower().replace(" ", "").replace("-", "")
        self.slack_feedback = (
            "Correct. Slack is the margin between required and achieved timing."
            if value in {"slack", "timingslack"}
            else "What timing-analysis term describes the margin between required time and actual path timing?"
        )

    def check_critical(self) -> None:
        value = self.critical_answer.strip().lower().replace(" ", "").replace("-", "")
        self.critical_feedback = (
            "Correct. The critical path is the path with the tightest/longest timing delay that limits achievable clock speed."
            if value in {"criticalpath", "critical"}
            else "What do we call the timing path that most limits the maximum clock frequency?"
        )

    def check_testbench(self) -> None:
        value = self.testbench_answer.strip().lower().replace(" ", "").replace("-", "")
        self.testbench_feedback = (
            "Correct. A testbench provides stimulus and checks the design during simulation."
            if value in {"testbench", "tb"}
            else "What HDL verification environment drives inputs and observes a design during simulation?"
        )

    def check_dut(self) -> None:
        value = self.dut_answer.strip().lower().replace(" ", "").replace("-", "")
        self.dut_feedback = (
            "Correct. DUT means design under test."
            if value in {"dut", "designundertest"}
            else "What does DUT stand for?"
        )

    def check_assertion(self) -> None:
        value = self.assertion_answer.strip().lower().replace(" ", "").replace("-", "")
        self.assertion_feedback = (
            "Correct. An assertion automatically checks that a required property holds."
            if value in {"assertion", "assert", "property"}
            else "What verification construct automatically checks a required behaviour or property?"
        )

    def check_fsm(self) -> None:
        value = self.fsm_answer.strip().lower().replace(" ", "").replace("-", "")
        self.fsm_feedback = (
            "Correct. FSM means finite-state machine."
            if value in {"fsm", "finitestatemachine"}
            else "What does FSM stand for?"
        )

    def check_moore(self) -> None:
        value = self.moore_answer.strip().lower().replace(" ", "").replace("-", "")
        self.moore_feedback = (
            "Correct. In a Moore machine, outputs depend on the current state."
            if value in {"moore", "mooremachine"}
            else "Which FSM style makes outputs depend on state rather than directly on current inputs?"
        )

    def check_mealy(self) -> None:
        value = self.mealy_answer.strip().lower().replace(" ", "").replace("-", "")
        self.mealy_feedback = (
            "Correct. In a Mealy machine, outputs can depend on both state and current inputs."
            if value in {"mealy", "mealymachine"}
            else "Which FSM style can make outputs depend on both current state and current inputs?"
        )

    def check_register(self) -> None:
        value = self.register_answer.strip().lower().replace(" ", "").replace("-", "")
        self.register_feedback = (
            "Correct. A register stores state using flip-flops."
            if value in {"register", "flipflopregister", "reg"}
            else "What hardware structure stores a multi-bit value across clock cycles?"
        )

    def check_edge(self) -> None:
        value = self.edge_answer.strip().lower().replace(" ", "").replace("-", "")
        self.edge_feedback = (
            "Correct. Sequential logic commonly updates state on a clock edge."
            if value in {"clockedge", "risingedge", "fallingedge", "edge"}
            else "What clock event commonly causes a synchronous register to update?"
        )

    def check_nonblocking(self) -> None:
        value = self.nonblocking_answer.strip().lower().replace(" ", "").replace("-", "")
        self.nonblocking_feedback = (
            "Correct. Non-blocking assignment is typically used for clocked sequential logic in Verilog-style HDL."
            if value in {"nonblocking", "nonblockingassignment", "<="}
            else "Which assignment style is typically used in Verilog-style clocked sequential blocks?"
        )

    def check_comb(self) -> None:
        value = self.comb_answer.strip().lower().replace(" ", "").replace("-", "")
        self.comb_feedback = (
            "Correct. Combinational logic depends on current inputs and does not intentionally store state."
            if value in {"combinational", "combinationallogic", "comblogic"}
            else "What kind of logic produces outputs from current inputs without storing state?"
        )

    def check_module(self) -> None:
        value = self.module_answer.strip().lower().replace(" ", "").replace("-", "")
        self.module_feedback = (
            "Correct. A module/entity is a reusable hierarchical HDL design block."
            if value in {"module", "entity", "moduleentity", "hierarchicalblock"}
            else "What HDL construct represents a reusable hardware block with ports?"
        )

    def check_blocking(self) -> None:
        value = self.blocking_answer.strip().lower().replace(" ", "").replace("-", "")
        self.blocking_feedback = (
            "Correct. Blocking assignment is commonly used inside combinational procedural logic because statements take effect in order during simulation of that process."
            if value in {"blocking", "blockingassignment", "="}
            else "Which assignment style is typically used inside Verilog-style combinational procedural blocks?"
        )

    def check_hdl(self) -> None:
        value = self.hdl_answer.strip().lower().replace(" ", "").replace("-", "")
        self.hdl_feedback = (
            "Correct. HDL means hardware description language."
            if value in {"hdl", "hardwaredescriptionlanguage"}
            else "What does HDL stand for?"
        )

    def check_fpga(self) -> None:
        value = self.fpga_answer.strip().lower().replace(" ", "").replace("-", "")
        self.fpga_feedback = (
            "Correct. FPGA means field-programmable gate array."
            if value in {"fpga", "fieldprogrammablegatearray"}
            else "What does FPGA stand for?"
        )

    def check_synth(self) -> None:
        value = self.synth_answer.strip().lower().replace(" ", "").replace("-", "")
        self.synth_feedback = (
            "Correct. Synthesis converts synthesizable HDL into a hardware implementation/netlist."
            if value in {"synthesis", "synthesizer", "synth"}
            else "What process converts synthesizable HDL into a gate/register-level hardware implementation?"
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(number, color_scheme="teal"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            spacing="4",
            align="stretch",
        ),
        style=PANEL,
    )


def _practice(question, value, setter, checker, feedback, placeholder) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(question, weight="bold"),
            rx.hstack(
                rx.input(value=value, on_change=setter, placeholder=placeholder, width="100%"),
                rx.button("Check", on_click=checker, color_scheme="teal"),
                width="100%",
            ),
            rx.cond(feedback != "", rx.text(feedback, size="2", color="#0f766e")),
            spacing="2",
            align="stretch",
        ),
        padding="14px",
        border="1px solid #5eead4",
        border_radius="12px",
        background="#f0fdfa",
        width="100%",
    )


def hdl_fpga_foundations_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 01", color_scheme="teal", width="100%"),
            rx.heading("HDL & FPGA Foundations", size="8"),
            rx.text(
                "Digital logic can be drawn as gates, but real designs quickly become too large to manage schematically. Hardware description languages (HDLs) let engineers describe structure and behaviour in text, then synthesize that description into programmable FPGA hardware.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "HDLs describe hardware, not a sequence of software instructions",
                rx.text(
                    "A hardware description language expresses signals, combinational relationships, registers and timing-sensitive behaviour. Multiple described hardware blocks can operate concurrently because the final result is circuitry, not one CPU executing statements one after another."
                ),
                rx.code_block(
                    "software idea: execute instruction A, then B, then C\n\n"
                    "HDL idea:      block A ─┐\n"
                    "               block B ─┼─ all exist and operate as hardware\n"
                    "               block C ─┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What does HDL stand for?",
                    HDLFPGAState.hdl_answer,
                    HDLFPGAState.set_hdl_answer,
                    HDLFPGAState.check_hdl,
                    HDLFPGAState.hdl_feedback,
                    "abbreviation",
                ),
            ),
            _section(
                "2", "Common HDLs include Verilog/SystemVerilog and VHDL",
                rx.text(
                    "Different HDLs use different syntax, but the fundamental digital concepts remain the same: inputs, outputs, signals, logic equations, clocked registers, hierarchy and verification."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Concept"),
                        rx.table.column_header_cell("Hardware meaning"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Input/output port"), rx.table.cell("Connection to another hardware block")),
                        rx.table.row(rx.table.cell("Signal/net"), rx.table.cell("Value carried between logic elements")),
                        rx.table.row(rx.table.cell("Combinational assignment"), rx.table.cell("Logic function without stored state")),
                        rx.table.row(rx.table.cell("Clocked process/block"), rx.table.cell("Registers/state updated on clock events")),
                        rx.table.row(rx.table.cell("Module/entity"), rx.table.cell("Reusable hierarchical hardware block")),
                    ), width="100%",
                ),
            ),
            _section(
                "3", "An FPGA is reconfigurable digital hardware",
                rx.text(
                    "A field-programmable gate array contains configurable logic, routing and I/O resources. A configuration bitstream programs those resources so the chip implements the required circuit."
                ),
                rx.code_block(
                    "HDL design → synthesis/place/route → bitstream → FPGA\n"
                    "                                              │\n"
                    "                           configurable logic + routing + I/O",
                    language="textile", width="100%",
                ),
                _practice(
                    "What does FPGA stand for?",
                    HDLFPGAState.fpga_answer,
                    HDLFPGAState.set_fpga_answer,
                    HDLFPGAState.check_fpga,
                    HDLFPGAState.fpga_feedback,
                    "programmable device",
                ),
            ),
            _section(
                "4", "FPGA logic is built from configurable resources",
                rx.text(
                    "Modern FPGAs commonly include lookup tables (LUTs), flip-flops, programmable routing, I/O blocks, block RAM, clock-management resources and often dedicated arithmetic/DSP blocks."
                ),
                rx.code_block(
                    "inputs → LUT/combinational logic → optional flip-flop → routing → next block\n"
                    "                ↑                                  │\n"
                    "              logic                           programmable fabric",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "A LUT implements small Boolean functions",
                rx.text(
                    "A lookup table stores the truth-table result for a small number of inputs. Configuration bits therefore let the same physical LUT implement AND, OR, XOR or a much more complex Boolean expression within its input capacity."
                ),
                rx.code_block(
                    "A B C → LUT address → stored result → F\n\n"
                    "configuration contents = truth table for desired F(A,B,C)",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Synthesis translates HDL into implementable hardware",
                rx.text(
                    "Synthesis analyzes synthesizable HDL and maps the described logic into gates, registers and technology-oriented resources. Not every statement that can be simulated is necessarily synthesizable."
                ),
                rx.code_block(
                    "HDL source\n"
                    "   ↓\n"
                    "parse/elaborate\n"
                    "   ↓\n"
                    "synthesis + optimization\n"
                    "   ↓\n"
                    "logical netlist / mapped resources",
                    language="textile", width="100%",
                ),
                _practice(
                    "What process converts synthesizable HDL into a gate/register-level hardware implementation?",
                    HDLFPGAState.synth_answer,
                    HDLFPGAState.set_synth_answer,
                    HDLFPGAState.check_synth,
                    HDLFPGAState.synth_feedback,
                    "design process",
                ),
            ),
            _section(
                "7", "Implementation assigns logic to physical FPGA resources",
                rx.text(
                    "After synthesis, implementation places logic into physical blocks and routes connections through the FPGA fabric. Timing analysis checks whether signal paths satisfy the required clock constraints."
                ),
                rx.code_block(
                    "synthesized netlist → place → route → timing analysis → bitstream",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "A design that is logically correct can still fail in hardware if timing constraints are not met.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "8", "Simulation verifies behaviour before programming hardware",
                rx.text(
                    "A testbench drives inputs into the HDL design and observes outputs. Simulation catches functional errors quickly and can test corner cases that would be inconvenient to reproduce manually on a board."
                ),
                rx.code_block(
                    "testbench → stimulus → design-under-test → outputs/assertions\n"
                    "                   simulated time →",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Combinational and sequential HDL describe different hardware",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Description"),
                        rx.table.column_header_cell("Implied hardware"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Output depends only on current inputs"), rx.table.cell("Combinational logic")),
                        rx.table.row(rx.table.cell("State changes on clock edge"), rx.table.cell("Flip-flops/registers")),
                        rx.table.row(rx.table.cell("Feedback plus registers"), rx.table.cell("State machine / sequential datapath")),
                    ), width="100%",
                ),
            ),
            _section(
                "10", "Parallel hardware is the key FPGA advantage",
                rx.text(
                    "An FPGA can contain many datapaths operating in parallel. Instead of time-sharing one processor ALU across every operation, a design can instantiate several arithmetic or logic blocks when resources permit."
                ),
                rx.code_block(
                    "stream A → processing block A ─┐\n"
                    "stream B → processing block B ─┼→ parallel hardware\n"
                    "stream C → processing block C ─┘",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace the FPGA design flow",
                rx.code_block(
                    "1. define hardware requirements\n"
                    "2. write HDL modules/entities\n"
                    "3. create simulation testbench\n"
                    "4. simulate and correct functional errors\n"
                    "5. synthesize HDL\n"
                    "6. review warnings/resource use\n"
                    "7. place and route\n"
                    "8. run timing analysis\n"
                    "9. generate programming bitstream\n"
                    "10. configure FPGA\n"
                    "11. verify behaviour on hardware",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now explain what an HDL describes, define an FPGA, identify LUTs and registers, distinguish simulation from synthesis, describe placement/routing and timing analysis, and trace the complete FPGA implementation flow."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 01 COMPLETE", color_scheme="green"),
                    rx.heading("Gate-level knowledge now scales into programmable digital hardware.", size="5"),
                    rx.text(
                        "Next: learn combinational HDL modelling, modules, operators and synthesis-safe coding.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Combinational HDL Design & Modules", color_scheme="teal"),
                        href="/academy/unit-12/combinational-hdl-design-modules",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def combinational_hdl_design_modules_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 02", color_scheme="teal", width="100%"),
            rx.heading("Combinational HDL Design & Modules", size="8"),
            rx.text(
                "Combinational HDL describes logic whose outputs are functions of current inputs. This lesson connects Boolean expressions, modules, operators, procedural combinational blocks and hierarchy to synthesizable hardware.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Combinational HDL maps directly from Boolean relationships",
                rx.text(
                    "A simple Boolean equation can be written as a continuous HDL assignment. Synthesis turns the expression into logic resources that implement the same truth table."
                ),
                rx.code_block(
                    "Boolean:   F = (A AND B) OR (NOT C)\n\n"
                    "HDL idea:  assign F = (A & B) | ~C;\n\n"
                    "hardware:  A ─┐\n"
                    "             AND ─┐\n"
                    "           B ─┘    OR ─→ F\n"
                    "           C ─NOT─┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What kind of logic produces outputs from current inputs without storing state?",
                    HDLFPGAState.comb_answer,
                    HDLFPGAState.set_comb_answer,
                    HDLFPGAState.check_comb,
                    HDLFPGAState.comb_feedback,
                    "logic type",
                ),
            ),
            _section(
                "2", "Ports define the module boundary",
                rx.text(
                    "A module or entity exposes input and output ports. Internal implementation can change while the external interface remains stable, which supports reuse and hierarchical design."
                ),
                rx.code_block(
                    "module ALU_slice\n"
                    " inputs : A, B, SEL\n"
                    " outputs: Y\n\n"
                    "external logic ↔ ports ↔ internal implementation",
                    language="textile", width="100%",
                ),
                _practice(
                    "What HDL construct represents a reusable hardware block with ports?",
                    HDLFPGAState.module_answer,
                    HDLFPGAState.set_module_answer,
                    HDLFPGAState.check_module,
                    HDLFPGAState.module_feedback,
                    "hierarchical block",
                ),
            ),
            _section(
                "3", "Bitwise operators build gate-level logic",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("HDL operator idea"),
                        rx.table.column_header_cell("Hardware meaning"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("~A"), rx.table.cell("bitwise NOT")),
                        rx.table.row(rx.table.cell("A & B"), rx.table.cell("bitwise AND")),
                        rx.table.row(rx.table.cell("A | B"), rx.table.cell("bitwise OR")),
                        rx.table.row(rx.table.cell("A ^ B"), rx.table.cell("bitwise XOR")),
                    ),
                    width="100%",
                ),
                rx.text(
                    "Bit width matters: vector operators apply to corresponding bits unless the language/operator specifies another interpretation."
                ),
            ),
            _section(
                "4", "Vectors represent multi-bit buses",
                rx.text(
                    "HDL signals can contain several bits. Vectors represent buses, registers, addresses and datapaths. Slices and concatenation help select or combine groups of bits."
                ),
                rx.code_block(
                    "8-bit bus: data[7:0]\n\n"
                    "upper nibble = data[7:4]\n"
                    "lower nibble = data[3:0]\n"
                    "combined     = {upper, lower}",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Conditional operators infer multiplexers",
                rx.text(
                    "Selecting one of several values based on a control signal produces multiplexer hardware. HDL conditional expressions make this compact."
                ),
                rx.code_block(
                    "Y = SEL ? B : A\n\n"
                    "A ─┐\n"
                    "   MUX ─→ Y\n"
                    "B ─┘\n"
                    "   ↑\n"
                    "  SEL",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Procedural combinational blocks describe decisions",
                rx.text(
                    "Combinational processes/always blocks are useful for multi-branch logic such as decoders, ALUs and priority logic. Every output must receive a value for every possible path to avoid unintended storage."
                ),
                rx.code_block(
                    "combinational block:\n"
                    "  default Y = 0\n"
                    "  if SEL == 0: Y = A\n"
                    "  else:        Y = B\n\n"
                    "all paths assign Y → combinational hardware",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which assignment style is typically used inside Verilog-style combinational procedural blocks?",
                    HDLFPGAState.blocking_answer,
                    HDLFPGAState.set_blocking_answer,
                    HDLFPGAState.check_blocking,
                    HDLFPGAState.blocking_feedback,
                    "assignment style",
                ),
            ),
            _section(
                "7", "Incomplete assignments can infer latches",
                rx.text(
                    "If a procedural combinational block leaves an output unchanged on some control path, synthesis may infer a level-sensitive latch so the old value can be remembered."
                ),
                rx.code_block(
                    "bad pattern:\n"
                    "if EN: Y = A\n"
                    "# no assignment when EN=0\n\n"
                    "hardware must remember old Y → latch inferred",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Use explicit defaults or complete branch coverage in combinational logic unless a latch is intentionally required.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "8", "Case statements describe decoders and selectors",
                rx.text(
                    "A case-style construct maps control patterns to outputs. It is well suited to instruction decoders, operation selectors and finite lookup structures."
                ),
                rx.code_block(
                    "case opcode:\n"
                    "  00 → Y = A & B\n"
                    "  01 → Y = A | B\n"
                    "  10 → Y = A ^ B\n"
                    "  11 → Y = ~A",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Hierarchy scales large designs",
                rx.text(
                    "A larger system instantiates smaller verified modules. Ports connect modules through named signals, allowing a top-level design to describe system structure clearly."
                ),
                rx.code_block(
                    "top_level\n"
                    " ├─ decoder\n"
                    " ├─ alu\n"
                    " ├─ comparator\n"
                    " └─ output_mux",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "Synthesis sees hardware, not source-code cleverness",
                rx.text(
                    "Two pieces of HDL that look different can synthesize into equivalent hardware, while a compact expression can still infer a large circuit. Designers should reason about resulting logic depth, fan-in, resource use and timing."
                ),
                rx.callout(
                    "Readable HDL that makes the intended hardware obvious is usually easier to verify and optimize than overly compressed source code.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "11", "Trace a 4-to-1 multiplexer design",
                rx.code_block(
                    "1. define inputs D0..D3 and select S[1:0]\n"
                    "2. define output Y\n"
                    "3. write complete case on S\n"
                    "4. assign Y for 00,01,10,11\n"
                    "5. simulate all select values\n"
                    "6. synthesize\n"
                    "7. inspect inferred mux/LUT structure\n"
                    "8. verify no unintended latch warnings\n"
                    "9. integrate module into top-level design",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now write combinational HDL from Boolean equations, define modules and ports, use vectors and operators, describe multiplexers and decoders, avoid unintended latch inference and assemble hierarchy from reusable modules."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 02 COMPLETE", color_scheme="green"),
                    rx.heading("Boolean logic can now be expressed as reusable synthesizable HDL.", size="5"),
                    rx.text(
                        "Next: learn sequential HDL, registers, clocks and reset behaviour.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Sequential HDL, Registers & Clocks", color_scheme="teal"),
                        href="/academy/unit-12/sequential-hdl-registers-clocks",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def sequential_hdl_registers_clocks_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 03", color_scheme="teal", width="100%"),
            rx.heading("Sequential HDL, Registers & Clocks", size="8"),
            rx.text(
                "Sequential HDL describes hardware that remembers state. Registers update on clock events, resets establish known startup values, and carefully written clocked processes ensure that synthesized hardware behaves predictably across cycles.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Sequential logic stores state across time",
                rx.text(
                    "Unlike combinational logic, sequential logic can produce different outputs for the same current inputs because previous state matters. Flip-flops and registers provide that memory."
                ),
                rx.code_block(
                    "current inputs + previous state → next-state logic → register → new state\n"
                    "                                      ↑           │\n"
                    "                                      └── clock ──┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What hardware structure stores a multi-bit value across clock cycles?",
                    HDLFPGAState.register_answer,
                    HDLFPGAState.set_register_answer,
                    HDLFPGAState.check_register,
                    HDLFPGAState.register_feedback,
                    "state element",
                ),
            ),
            _section(
                "2", "Clock edges define synchronous update moments",
                rx.text(
                    "A synchronous design commonly uses rising or falling clock edges as the moments when registers capture their next values. Between active edges, the stored state remains stable."
                ),
                rx.code_block(
                    "clock:  __/‾‾\\__/‾‾\\__/‾‾\\__\n"
                    "          ↑       ↑       ↑\n"
                    "        update  update  update",
                    language="textile", width="100%",
                ),
                _practice(
                    "What clock event commonly causes a synchronous register to update?",
                    HDLFPGAState.edge_answer,
                    HDLFPGAState.set_edge_answer,
                    HDLFPGAState.check_edge,
                    HDLFPGAState.edge_feedback,
                    "clock event",
                ),
            ),
            _section(
                "3", "Clocked HDL infers flip-flops",
                rx.text(
                    "When a synthesizable process updates a signal on an explicit clock edge, synthesis normally infers flip-flops or register resources."
                ),
                rx.code_block(
                    "on rising clock edge:\n"
                    "    Q <= D\n\n"
                    "hardware: D → flip-flop → Q\n"
                    "                    ↑\n"
                    "                   CLK",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "4", "Non-blocking assignment models simultaneous register updates",
                rx.text(
                    "In Verilog-style sequential code, non-blocking assignments let several registers conceptually capture old-state inputs at the same clock edge before their new values become visible."
                ),
                rx.code_block(
                    "on clock edge:\n"
                    "    A <= B\n"
                    "    B <= A\n\n"
                    "result: A and B swap old values simultaneously",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which assignment style is typically used in Verilog-style clocked sequential blocks?",
                    HDLFPGAState.nonblocking_answer,
                    HDLFPGAState.set_nonblocking_answer,
                    HDLFPGAState.check_nonblocking,
                    HDLFPGAState.nonblocking_feedback,
                    "assignment style",
                ),
            ),
            _section(
                "5", "Registers can include enables",
                rx.text(
                    "A clock enable allows a register to update only when a control condition is true. Otherwise the register retains its previous state."
                ),
                rx.code_block(
                    "on clock edge:\n"
                    "    if EN:\n"
                    "        Q <= D\n"
                    "    else:\n"
                    "        Q keeps previous value",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Reset establishes a defined initial state",
                rx.text(
                    "Reset logic places registers into known values. Synchronous reset is sampled on the active clock edge; asynchronous reset can affect registers independently of the clock, depending on device resources and coding style."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Reset style"),
                        rx.table.column_header_cell("Key behaviour"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Synchronous"), rx.table.cell("Register responds to reset at clock edge")),
                        rx.table.row(rx.table.cell("Asynchronous"), rx.table.cell("Register can enter reset state without waiting for clock edge")),
                    ),
                    width="100%",
                ),
                rx.callout(
                    "Reset strategy should match the target FPGA/device architecture and timing methodology.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "7", "Counters are simple sequential systems",
                rx.text(
                    "A binary counter stores a value and computes the next value from the current one. Each active clock edge loads the incremented result."
                ),
                rx.code_block(
                    "Q_next = Q + 1\n\n"
                    "clock edges:  0000 → 0001 → 0010 → 0011 → 0100 ...",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "Shift registers move data through stages",
                rx.text(
                    "A shift register is a chain of flip-flops where each stage captures the previous stage's value. It can delay data, serialize/deserialize streams or implement pipelines."
                ),
                rx.code_block(
                    "serial_in → [FF0] → [FF1] → [FF2] → [FF3] → serial_out\n"
                    "                  shared clock",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Clock-domain boundaries require care",
                rx.text(
                    "Signals that cross between unrelated clock domains can violate setup/hold assumptions and become metastable. Synchronizers, handshakes or asynchronous FIFOs are used depending on the data type and throughput requirement."
                ),
                rx.callout(
                    "Do not directly sample an arbitrary asynchronous control signal into logic and assume it is safe. Clock-domain crossing requires explicit design.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "10", "Timing constraints define required performance",
                rx.text(
                    "Synthesis and implementation need accurate clock constraints. Static timing analysis checks whether combinational paths between registers complete within the required timing window."
                ),
                rx.code_block(
                    "source register → combinational path → destination register\n"
                    "       ↑                                 ↑\n"
                    "     clock                             next edge\n\n"
                    "path delay must satisfy timing requirement",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace a 4-bit synchronous counter",
                rx.code_block(
                    "1. define 4-bit register Q\n"
                    "2. define clock and reset inputs\n"
                    "3. on active clock edge, check reset\n"
                    "4. if reset: Q <= 0000\n"
                    "5. else: Q <= Q + 1\n"
                    "6. simulate reset and several clock cycles\n"
                    "7. synthesize\n"
                    "8. verify four flip-flops plus increment logic\n"
                    "9. constrain clock\n"
                    "10. run timing analysis",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now describe registers in HDL, explain edge-triggered state updates, use non-blocking assignments for clocked logic, add enables and resets, build counters and shift registers, and recognize clock-domain and timing constraints."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 03 COMPLETE", color_scheme="green"),
                    rx.heading("Your HDL can now describe stateful synchronous hardware.", size="5"),
                    rx.text(
                        "Next: learn finite-state machines and control-path design.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Finite-State Machines & Control Logic", color_scheme="teal"),
                        href="/academy/unit-12/finite-state-machines-control-logic",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def finite_state_machines_control_logic_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 04", color_scheme="teal", width="100%"),
            rx.heading("Finite-State Machines & Control Logic", size="8"),
            rx.text(
                "Finite-state machines (FSMs) turn sequential logic into understandable control behaviour. By separating stored state, next-state decisions and outputs, HDL can describe controllers that react to events over multiple clock cycles.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "An FSM stores one of a finite set of states",
                rx.text(
                    "A finite-state machine represents the current phase of a control process using a state register. Combinational logic examines the current state and inputs to determine what happens next."
                ),
                rx.code_block(
                    "inputs ─→ next-state logic ─→ state register ─→ output logic ─→ outputs\n"
                    "              ↑                    │\n"
                    "              └──── current state ─┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What does FSM stand for?",
                    HDLFPGAState.fsm_answer,
                    HDLFPGAState.set_fsm_answer,
                    HDLFPGAState.check_fsm,
                    HDLFPGAState.fsm_feedback,
                    "abbreviation",
                ),
            ),
            _section(
                "2", "States represent meaningful control phases",
                rx.text(
                    "Good state names describe behaviour rather than raw binary codes. A traffic controller might use RED, GREEN and AMBER; a protocol controller might use IDLE, START, TRANSFER and DONE."
                ),
                rx.code_block(
                    "IDLE → LOAD → PROCESS → DONE → IDLE",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Transitions define when the controller moves",
                rx.text(
                    "A state transition occurs when a specified condition is true. The transition relationship can be written as a diagram, a table or next-state HDL."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Current state"),
                        rx.table.column_header_cell("Condition"),
                        rx.table.column_header_cell("Next state"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("IDLE"), rx.table.cell("start=0"), rx.table.cell("IDLE")),
                        rx.table.row(rx.table.cell("IDLE"), rx.table.cell("start=1"), rx.table.cell("RUN")),
                        rx.table.row(rx.table.cell("RUN"), rx.table.cell("done=0"), rx.table.cell("RUN")),
                        rx.table.row(rx.table.cell("RUN"), rx.table.cell("done=1"), rx.table.cell("DONE")),
                        rx.table.row(rx.table.cell("DONE"), rx.table.cell("ack=1"), rx.table.cell("IDLE")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "4", "Moore outputs depend on state",
                rx.text(
                    "In a Moore FSM, outputs are functions of the registered state. This often makes output timing easier to reason about because output changes are tied to state changes."
                ),
                rx.code_block(
                    "state register → Moore output logic → outputs\n"
                    "inputs affect outputs indirectly through future state",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which FSM style makes outputs depend on state rather than directly on current inputs?",
                    HDLFPGAState.moore_answer,
                    HDLFPGAState.set_moore_answer,
                    HDLFPGAState.check_moore,
                    HDLFPGAState.moore_feedback,
                    "FSM style",
                ),
            ),
            _section(
                "5", "Mealy outputs can respond to inputs immediately",
                rx.text(
                    "In a Mealy FSM, outputs can depend on both current state and current inputs. This can reduce latency or state count, but output timing must account for combinational input paths."
                ),
                rx.code_block(
                    "current state ─┐\n"
                    "               ├→ Mealy output logic → outputs\n"
                    "current inputs ─┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which FSM style can make outputs depend on both current state and current inputs?",
                    HDLFPGAState.mealy_answer,
                    HDLFPGAState.set_mealy_answer,
                    HDLFPGAState.check_mealy,
                    HDLFPGAState.mealy_feedback,
                    "FSM style",
                ),
            ),
            _section(
                "6", "A common HDL FSM structure separates three concerns",
                rx.text(
                    "Many designers separate the state register, next-state logic and output logic. This makes the intended hardware and verification responsibilities clear."
                ),
                rx.code_block(
                    "1. clocked block:      state <= next_state\n"
                    "2. combinational block: next_state = f(state, inputs)\n"
                    "3. output block:        outputs = g(state[, inputs])",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Default assignments prevent unintended storage",
                rx.text(
                    "Next-state combinational logic should assign a value on every path. A common pattern begins with next_state = state, then overrides it only when transition conditions are met."
                ),
                rx.code_block(
                    "next_state = state\n"
                    "case state:\n"
                    "  IDLE: if start: next_state = RUN\n"
                    "  RUN:  if done:  next_state = DONE\n"
                    "  DONE: if ack:   next_state = IDLE",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Incomplete next-state assignment can infer latches or create difficult-to-debug behaviour.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "8", "State encoding maps symbolic states into bits",
                rx.text(
                    "The symbolic states eventually need binary representation. Common strategies include binary encoding, one-hot encoding and tool-selected encoding."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Encoding"),
                        rx.table.column_header_cell("Typical characteristic"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Binary"), rx.table.cell("Uses about log2(N) state bits")),
                        rx.table.row(rx.table.cell("One-hot"), rx.table.cell("Uses one state bit per state; simple decode, more flip-flops")),
                        rx.table.row(rx.table.cell("Automatic"), rx.table.cell("Synthesis tool chooses based on target/optimization")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "9", "Illegal-state recovery improves robustness",
                rx.text(
                    "An FSM can include a default recovery path so unexpected encoded states return to a safe state. Reset should also place the machine into a known valid state."
                ),
                rx.code_block(
                    "reset → IDLE\n\n"
                    "default/illegal state → SAFE or IDLE",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "FSMs coordinate datapaths",
                rx.text(
                    "Control logic often directs a separate datapath containing registers, counters, ALUs and memories. The FSM issues enables, selects and operation codes while the datapath returns status conditions."
                ),
                rx.code_block(
                    "        status flags\n"
                    "datapath ─────────────→ FSM control\n"
                    "   ↑                      │\n"
                    "   └── enables/selects ───┘",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace a simple transaction controller",
                rx.code_block(
                    "1. RESET places state in IDLE\n"
                    "2. IDLE waits for start=1\n"
                    "3. transition to LOAD\n"
                    "4. LOAD asserts capture_enable for one cycle\n"
                    "5. transition to RUN\n"
                    "6. RUN waits for datapath done=1\n"
                    "7. transition to DONE\n"
                    "8. DONE asserts complete=1\n"
                    "9. ack=1 returns machine to IDLE\n"
                    "10. simulation verifies legal and unexpected paths",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now describe FSM state, transitions and outputs, compare Moore and Mealy machines, structure HDL into state/next-state/output logic, choose state encoding, provide illegal-state recovery and coordinate a controller with a datapath."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 04 COMPLETE", color_scheme="green"),
                    rx.heading("Your HDL can now express structured multi-cycle control behaviour.", size="5"),
                    rx.text(
                        "Next: learn testbenches, simulation and assertion-based verification.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Testbenches, Simulation & Verification", color_scheme="teal"),
                        href="/academy/unit-12/testbenches-simulation-verification",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def testbenches_simulation_verification_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 05", color_scheme="teal", width="100%"),
            rx.heading("Testbenches, Simulation & Verification", size="8"),
            rx.text(
                "HDL is not finished when it compiles. Verification asks whether the described hardware actually satisfies its specification. Testbenches generate stimulus, simulation exposes behaviour over time, and automated checks catch failures before an FPGA is programmed.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A testbench surrounds the design under test",
                rx.text(
                    "A testbench is verification HDL that instantiates the design, drives its inputs and observes outputs. Testbench-only constructs do not need to synthesize because the testbench itself is not implemented as FPGA hardware."
                ),
                rx.code_block(
                    "testbench\n"
                    " ├─ stimulus generator ─→ DUT inputs\n"
                    " ├─ DUT (design under test)\n"
                    " └─ checker/monitor ←── DUT outputs",
                    language="textile", width="100%",
                ),
                _practice(
                    "What HDL verification environment drives inputs and observes a design during simulation?",
                    HDLFPGAState.testbench_answer,
                    HDLFPGAState.set_testbench_answer,
                    HDLFPGAState.check_testbench,
                    HDLFPGAState.testbench_feedback,
                    "verification environment",
                ),
            ),
            _section(
                "2", "DUT identifies the hardware being verified",
                rx.text(
                    "The design under test may be one module, a subsystem or the complete top-level design. Keeping a clear DUT boundary makes stimulus, expected behaviour and failures easier to understand."
                ),
                _practice(
                    "What does DUT stand for?",
                    HDLFPGAState.dut_answer,
                    HDLFPGAState.set_dut_answer,
                    HDLFPGAState.check_dut,
                    HDLFPGAState.dut_feedback,
                    "abbreviation",
                ),
            ),
            _section(
                "3", "Stimulus explores normal and corner-case behaviour",
                rx.text(
                    "Verification should test more than the most obvious input. Useful stimulus includes boundary values, reset sequences, simultaneous controls, illegal combinations when relevant, and transitions around important clock events."
                ),
                rx.code_block(
                    "stimulus plan:\n"
                    "  reset → normal case → boundary case → back-to-back case\n"
                    "        → invalid/ignored case → recovery → repeat",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "4", "Clock and reset generation establish simulation timing",
                rx.text(
                    "Sequential DUTs need a testbench clock and deliberate reset sequence. Stimulus should be scheduled so the intended relationship to active clock edges is unambiguous."
                ),
                rx.code_block(
                    "CLK:   __/‾\\__/‾\\__/‾\\__/‾\\__\n"
                    "RESET: ‾‾‾‾\\___________________\n"
                    "DATA:       01    10    11",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Waveforms expose signal behaviour over time",
                rx.text(
                    "A waveform viewer displays clocks, inputs, state and outputs against simulated time. It is valuable for debugging ordering, state transitions, latency and unexpected unknown values."
                ),
                rx.code_block(
                    "time →   0   10  20  30  40 ns\n"
                    "clk      0 1 0 1 0 1 0 1\n"
                    "state    IDLE  LOAD  RUN  DONE\n"
                    "valid    0      0     0    1",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Self-checking testbenches compare actual and expected results",
                rx.text(
                    "A self-checking testbench computes or stores the expected result and automatically reports a mismatch. This is more scalable and repeatable than visually inspecting every waveform."
                ),
                rx.code_block(
                    "apply input vector\n"
                    "      ↓\n"
                    "DUT output ─────┐\n"
                    "expected value ─┼→ compare → PASS / FAIL\n"
                    "                ┘",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Assertions turn requirements into executable checks",
                rx.text(
                    "Assertions state properties that must hold during simulation. They can detect protocol violations, impossible state combinations, incorrect latency or outputs that appear at the wrong time."
                ),
                rx.code_block(
                    "example property idea:\n"
                    "if request is accepted,\n"
                    "then done must become true within N cycles",
                    language="textile", width="100%",
                ),
                _practice(
                    "What verification construct automatically checks a required behaviour or property?",
                    HDLFPGAState.assertion_answer,
                    HDLFPGAState.set_assertion_answer,
                    HDLFPGAState.check_assertion,
                    HDLFPGAState.assertion_feedback,
                    "automatic check",
                ),
            ),
            _section(
                "8", "Directed and randomized tests serve different purposes",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Approach"),
                        rx.table.column_header_cell("Strength"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Directed"), rx.table.cell("Targets known requirements and corner cases precisely")),
                        rx.table.row(rx.table.cell("Randomized"), rx.table.cell("Explores combinations a designer may not manually anticipate")),
                        rx.table.row(rx.table.cell("Constrained-random"), rx.table.cell("Randomizes within legal/useful scenario rules")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "9", "Coverage asks what has actually been exercised",
                rx.text(
                    "Passing tests do not prove completeness. Coverage metrics can track whether code branches, conditions, states, transitions or defined functional scenarios have been exercised."
                ),
                rx.callout(
                    "High coverage is evidence of test activity, not proof that the specification is correct or that every bug has been found.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "10", "Verification should include failure and recovery paths",
                rx.text(
                    "Controllers and interfaces should be tested when inputs arrive too early, too late, simultaneously or unexpectedly. Reset and recovery behaviour deserve explicit verification rather than being assumed."
                ),
                rx.code_block(
                    "normal transaction → PASS\n"
                    "timeout path       → expected error response\n"
                    "reset during work  → known reset state\n"
                    "illegal request    → safe handling",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace verification of a 4-to-1 multiplexer",
                rx.code_block(
                    "1. instantiate the 4:1 mux DUT\n"
                    "2. assign distinct values to D0..D3\n"
                    "3. drive select=00 and check Y=D0\n"
                    "4. drive select=01 and check Y=D1\n"
                    "5. drive select=10 and check Y=D2\n"
                    "6. drive select=11 and check Y=D3\n"
                    "7. repeat with different data patterns\n"
                    "8. automatically report mismatches\n"
                    "9. inspect waveform only when debugging a failure",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now define a testbench and DUT, generate clocks and stimulus, interpret waveforms, create self-checking tests and assertions, compare directed and randomized testing, understand coverage, and verify both normal and recovery behaviour."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 05 COMPLETE", color_scheme="green"),
                    rx.heading("Your HDL designs can now be tested systematically before hardware deployment.", size="5"),
                    rx.text(
                        "Next: learn FPGA synthesis, implementation, constraints and timing closure.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · FPGA Synthesis, Constraints & Timing", color_scheme="teal"),
                        href="/academy/unit-12/fpga-synthesis-constraints-timing",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def fpga_synthesis_constraints_timing_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 06", color_scheme="teal", width="100%"),
            rx.heading("FPGA Synthesis, Constraints & Timing", size="8"),
            rx.text(
                "A functionally correct HDL design still has to fit into the FPGA and meet timing. Synthesis, placement, routing and static timing analysis turn RTL into physical hardware while checking whether every required path can complete within its specified time.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Synthesis converts RTL into a technology-aware implementation",
                rx.text(
                    "The synthesis tool elaborates hierarchy, infers arithmetic and memory structures, simplifies Boolean logic and maps the RTL toward resources available in the target FPGA."
                ),
                rx.code_block(
                    "RTL HDL\n"
                    "  ↓ elaborate\n"
                    "logical operators/registers\n"
                    "  ↓ optimize\n"
                    "mapped LUTs / FFs / RAM / DSP resources",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "2", "Resource reports reveal what the design consumes",
                rx.text(
                    "Post-synthesis reports show how many LUTs, flip-flops, block RAMs, DSP blocks and I/O resources are required. Unexpected usage can reveal inefficient coding or unintended hardware inference."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Resource"),
                        rx.table.column_header_cell("Typical role"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("LUT"), rx.table.cell("Combinational logic")),
                        rx.table.row(rx.table.cell("Flip-flop"), rx.table.cell("Registered state")),
                        rx.table.row(rx.table.cell("Block RAM"), rx.table.cell("On-chip memory")),
                        rx.table.row(rx.table.cell("DSP block"), rx.table.cell("Fast arithmetic / multiply-accumulate")),
                        rx.table.row(rx.table.cell("I/O block"), rx.table.cell("External pin interface")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "3", "Timing constraints define the performance target",
                rx.text(
                    "Implementation tools cannot infer the intended clock period from wishful thinking. Designers must declare clocks and relevant timing relationships so static timing analysis knows the required arrival times."
                ),
                rx.code_block(
                    "example intent:\n"
                    "clock period = 10 ns  → target frequency = 100 MHz\n\n"
                    "constraint tells tools: register-to-register paths must fit within required timing",
                    language="textile", width="100%",
                ),
                _practice(
                    "What specification tells FPGA tools the required clocks and timing limits?",
                    HDLFPGAState.constraint_answer,
                    HDLFPGAState.set_constraint_answer,
                    HDLFPGAState.check_constraint,
                    HDLFPGAState.constraint_feedback,
                    "timing requirement",
                ),
            ),
            _section(
                "4", "Static timing analysis checks paths without input vectors",
                rx.text(
                    "Static timing analysis (STA) examines timing paths mathematically rather than simulating every possible data pattern. It computes path delays and compares them with timing requirements."
                ),
                rx.code_block(
                    "launch FF → combinational logic → capture FF\n"
                    "    |             delay             |\n"
                    "    └──── checked against clock requirement ────┘",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Slack tells whether timing passes or fails",
                rx.text(
                    "Slack is the difference between required timing and achieved arrival timing. Positive slack means the path meets the requirement; negative slack means the design violates it."
                ),
                rx.code_block(
                    "required arrival = 10.0 ns\n"
                    "actual arrival   =  8.7 ns\n"
                    "slack            = +1.3 ns  → PASS\n\n"
                    "actual arrival   = 10.8 ns\n"
                    "slack            = -0.8 ns  → FAIL",
                    language="textile", width="100%",
                ),
                _practice(
                    "What timing-analysis term describes the margin between required time and actual path timing?",
                    HDLFPGAState.slack_answer,
                    HDLFPGAState.set_slack_answer,
                    HDLFPGAState.check_slack,
                    HDLFPGAState.slack_feedback,
                    "timing margin",
                ),
            ),
            _section(
                "6", "The critical path limits maximum clock frequency",
                rx.text(
                    "The slowest relevant timing path often sets the highest safe clock frequency. Reducing combinational depth, improving placement or adding pipeline registers can shorten that path."
                ),
                rx.code_block(
                    "short path: FF → LUT → FF\n"
                    "long path : FF → LUT → LUT → LUT → carry chain → FF\n"
                    "                                      ↑\n"
                    "                                likely critical path",
                    language="textile", width="100%",
                ),
                _practice(
                    "What do we call the timing path that most limits the maximum clock frequency?",
                    HDLFPGAState.critical_answer,
                    HDLFPGAState.set_critical_answer,
                    HDLFPGAState.check_critical,
                    HDLFPGAState.critical_feedback,
                    "limiting path",
                ),
            ),
            _section(
                "7", "Placement and routing affect real delays",
                rx.text(
                    "After synthesis, placement chooses physical FPGA locations for logic and routing connects them. Two logically identical designs can have different timing because physical distance and routing congestion change interconnect delay."
                ),
                rx.callout(
                    "Post-route timing is the meaningful implementation result; synthesis estimates alone are not the final word.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "8", "Pipelining trades latency for clock speed",
                rx.text(
                    "A long combinational path can be split by inserting registers. Each stage then performs less work per cycle, improving maximum clock frequency at the cost of additional cycle latency."
                ),
                rx.code_block(
                    "before:\n"
                    "FF → logic A → logic B → logic C → FF\n\n"
                    "pipelined:\n"
                    "FF → logic A → FF → logic B → FF → logic C → FF",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "I/O timing also needs constraints",
                rx.text(
                    "Signals entering and leaving the FPGA interact with external devices. Input and output delay constraints describe external timing relationships so the tool can analyze paths between pins and internal registers."
                ),
                rx.code_block(
                    "external device → FPGA input pin → input register\n"
                    "FPGA output register → output pin → external device",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "False and multicycle paths must be declared carefully",
                rx.text(
                    "Some paths are not required to meet the default single-cycle relationship. Exceptions such as false paths or multicycle paths can be valid, but incorrect exceptions can hide real timing failures."
                ),
                rx.callout(
                    "Timing exceptions should reflect real architectural behaviour, not be used simply to silence failing reports.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "11", "Trace a timing-closure workflow",
                rx.code_block(
                    "1. define accurate clocks and I/O constraints\n"
                    "2. synthesize RTL\n"
                    "3. inspect inferred resources and warnings\n"
                    "4. place and route\n"
                    "5. run static timing analysis\n"
                    "6. locate worst negative-slack paths\n"
                    "7. identify logic depth / fanout / routing issue\n"
                    "8. optimize RTL, pipeline or adjust architecture\n"
                    "9. rebuild implementation\n"
                    "10. repeat until all required timing paths pass",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now explain synthesis mapping, interpret FPGA resource usage, define timing constraints, read slack, identify critical paths, understand placement/routing effects, use pipelining for timing closure and treat timing exceptions carefully."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 06 COMPLETE", color_scheme="green"),
                    rx.heading("Your HDL can now be judged against real FPGA resource and timing limits.", size="5"),
                    rx.text(
                        "Next: learn FPGA memories, DSP blocks and pipelined datapaths.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · FPGA Memories, DSP Blocks & Pipelining", color_scheme="teal"),
                        href="/academy/unit-12/fpga-memories-dsp-pipelining",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def fpga_memories_dsp_pipelining_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 07", color_scheme="teal", width="100%"),
            rx.heading("FPGA Memories, DSP Blocks & Pipelining", size="8"),
            rx.text(
                "Modern FPGAs include specialized hardware beyond LUTs and flip-flops. Block memories store data efficiently, DSP blocks accelerate arithmetic, and pipelines turn long datapaths into high-throughput hardware.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Large storage should use dedicated memory resources",
                rx.text(
                    "Small state values fit naturally in flip-flops, but deeper memories would consume too many registers. FPGA block RAM provides dense on-chip storage with configurable width, depth and port structure."
                ),
                rx.code_block(
                    "logic fabric registers → small state / short shift chains\n"
                    "block RAM           → deeper tables / buffers / FIFOs / memories",
                    language="textile", width="100%",
                ),
                _practice(
                    "What dedicated FPGA resource stores larger on-chip memories more efficiently than individual flip-flops?",
                    HDLFPGAState.bram_answer,
                    HDLFPGAState.set_bram_answer,
                    HDLFPGAState.check_bram,
                    HDLFPGAState.bram_feedback,
                    "memory resource",
                ),
            ),
            _section(
                "2", "Memory dimensions trade width for depth",
                rx.text(
                    "A fixed amount of memory can often be configured as many narrow words or fewer wide words. The HDL array shape and access style influence how synthesis infers the memory."
                ),
                rx.code_block(
                    "same total capacity idea:\n"
                    "1024 × 8 bits\n"
                    " 512 × 16 bits\n"
                    " 256 × 32 bits",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Single-port and dual-port memories support different access patterns",
                rx.text(
                    "Single-port RAM provides one access interface. Dual-port memories can support two independent accesses under device-specific rules, enabling producer/consumer buffers, frame stores and lookup structures."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Memory style"),
                        rx.table.column_header_cell("Typical use"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Single-port"), rx.table.cell("One read/write access path")),
                        rx.table.row(rx.table.cell("Simple dual-port"), rx.table.cell("One write port plus one read port")),
                        rx.table.row(rx.table.cell("True dual-port"), rx.table.cell("Two independently configurable ports")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "4", "Synchronous memory adds cycle latency",
                rx.text(
                    "Many FPGA block memories register their addresses or outputs. A read request may therefore produce data one or more clock cycles later, and downstream logic must account for that latency."
                ),
                rx.code_block(
                    "cycle N:     present address\n"
                    "cycle N+1:   memory output valid\n"
                    "cycle N+2:   downstream pipeline continues",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "DSP blocks accelerate arithmetic",
                rx.text(
                    "Dedicated DSP resources commonly contain multipliers, adders, accumulators and pipeline registers. Mapping arithmetic into these blocks saves LUTs and can improve speed and power efficiency."
                ),
                rx.code_block(
                    "A × B → multiplier ─┐\n"
                    "                   adder/accumulator → P\n"
                    "C ─────────────────┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What FPGA resource is optimized for arithmetic such as multiplication and multiply-accumulate operations?",
                    HDLFPGAState.dsp_answer,
                    HDLFPGAState.set_dsp_answer,
                    HDLFPGAState.check_dsp,
                    HDLFPGAState.dsp_feedback,
                    "arithmetic resource",
                ),
            ),
            _section(
                "6", "Coding style influences DSP inference",
                rx.text(
                    "Synthesis recognizes arithmetic patterns. Expressions that clearly describe multiplication, addition and accumulation are more likely to map into dedicated resources than obscure equivalent logic."
                ),
                rx.callout(
                    "Inference rules vary by FPGA family and synthesis tool. Review the synthesis report instead of assuming a DSP block was used.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "7", "Pipelining increases throughput",
                rx.text(
                    "A long arithmetic chain can miss timing because too much logic lies between registers. Pipelining inserts registers between stages so each stage completes less work per clock cycle."
                ),
                rx.code_block(
                    "un-pipelined:\n"
                    "FF → multiply → add → scale → compare → FF\n\n"
                    "pipelined:\n"
                    "FF → multiply → FF → add → FF → scale → FF → compare → FF",
                    language="textile", width="100%",
                ),
                _practice(
                    "What design technique inserts registers between datapath stages to improve clock frequency?",
                    HDLFPGAState.pipeline_answer,
                    HDLFPGAState.set_pipeline_answer,
                    HDLFPGAState.check_pipeline,
                    HDLFPGAState.pipeline_feedback,
                    "timing technique",
                ),
            ),
            _section(
                "8", "Latency and throughput are different metrics",
                rx.text(
                    "A pipeline may take several cycles before the first result emerges, increasing latency. Once full, however, it can often accept new data every cycle and produce one result per cycle."
                ),
                rx.code_block(
                    "cycle:    1   2   3   4   5   6\n"
                    "input A:  S1  S2  S3  OUT\n"
                    "input B:      S1  S2  S3  OUT\n"
                    "input C:          S1  S2  S3  OUT",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Valid signals keep pipeline data aligned",
                rx.text(
                    "When data may be absent or stalled, a valid bit can travel alongside each pipeline stage. Control metadata such as packet IDs or operation types may also need matching pipeline delays."
                ),
                rx.code_block(
                    "data0 ─→ [stage1] ─→ [stage2] ─→ [stage3] ─→ result\n"
                    "valid ─→ [  v1  ] ─→ [  v2  ] ─→ [  v3  ] ─→ result_valid",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "FIFOs decouple producers and consumers",
                rx.text(
                    "First-in, first-out buffers absorb bursts and allow connected blocks to operate with temporary rate differences. FPGA FIFOs are often implemented using block RAM plus read/write pointers and status logic."
                ),
                rx.code_block(
                    "producer → FIFO memory → consumer\n"
                    "            ↑      ↑\n"
                    "          write   read\n"
                    "          ptr     ptr\n\n"
                    "status: empty / full / level",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace a pipelined multiply-accumulate datapath",
                rx.code_block(
                    "1. accept input A, B and C with valid=1\n"
                    "2. stage 1 registers A×B using DSP multiplier\n"
                    "3. stage 2 adds registered product + C\n"
                    "4. valid bit advances with each stage\n"
                    "5. output result becomes valid after pipeline latency\n"
                    "6. next input can enter every cycle once pipeline is flowing\n"
                    "7. synthesis report confirms DSP usage\n"
                    "8. timing report checks every stage\n"
                    "9. simulation verifies value/valid alignment",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now distinguish register storage from block RAM, reason about memory ports and latency, use dedicated DSP arithmetic, explain pipeline latency versus throughput, align valid/control signals and use FIFOs to buffer streaming datapaths."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 07 COMPLETE", color_scheme="green"),
                    rx.heading("Your FPGA designs can now exploit dedicated memory and arithmetic hardware efficiently.", size="5"),
                    rx.text(
                        "Next: integrate the complete HDL-to-FPGA design workflow.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Complete FPGA System Design & Deployment", color_scheme="teal"),
                        href="/academy/unit-12/complete-fpga-system-design-deployment",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def complete_fpga_system_design_deployment_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 12 · LESSON 08", color_scheme="teal", width="100%"),
            rx.heading("Complete FPGA System Design & Deployment", size="8"),
            rx.text(
                "The final FPGA workflow integrates specification, RTL, verification, constraints, implementation, programming and hardware debug into one disciplined engineering process. A deployed design must be logically correct, meet timing, use legal pins, configure reliably and behave correctly on the physical board.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "System design starts from measurable requirements",
                rx.text(
                    "Before writing HDL, define interfaces, clock rates, throughput, latency, reset behaviour, data widths, resource limits and external electrical requirements."
                ),
                rx.code_block(
                    "requirements → architecture → modules/datapaths/FSMs → verification plan\n\n"
                    "example: 100 MHz clock • 1 sample/cycle • 16-bit input • fixed latency",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "2", "Top-level architecture connects reusable blocks",
                rx.text(
                    "The top-level module instantiates verified submodules and defines how clocks, resets, buses and data streams connect. Clear hierarchy makes integration and timing analysis easier."
                ),
                rx.code_block(
                    "top_level\n"
                    " ├─ input_interface\n"
                    " ├─ control_fsm\n"
                    " ├─ pipelined_datapath\n"
                    " ├─ block_ram_buffer\n"
                    " └─ output_interface",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Clock and reset architecture must be deliberate",
                rx.text(
                    "Multiple clocks, generated clocks and reset distribution affect the whole design. Clock resources should use dedicated FPGA clocking networks, and reset release should be compatible with each clock domain."
                ),
                rx.callout(
                    "Treat clock-domain crossings and reset-domain crossings as explicit architecture topics, not afterthoughts.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "4", "Pin and I/O constraints connect HDL to the board",
                rx.text(
                    "Logical ports must be assigned to physical FPGA pins. Constraints also specify I/O standards and may include drive strength, slew behaviour or other device-specific electrical settings."
                ),
                rx.code_block(
                    "HDL port led[0] ── constraint ──→ FPGA package pin P17\n"
                    "HDL port clk    ── constraint ──→ board oscillator pin",
                    language="textile", width="100%",
                ),
                _practice(
                    "What constraints connect logical HDL ports to physical FPGA pins and electrical standards?",
                    HDLFPGAState.io_answer,
                    HDLFPGAState.set_io_answer,
                    HDLFPGAState.check_io,
                    HDLFPGAState.io_feedback,
                    "constraint type",
                ),
            ),
            _section(
                "5", "Implementation must satisfy both resource and timing limits",
                rx.text(
                    "A successful build must fit the device and meet required timing. Resource utilization, timing slack, clocking resources, I/O placement and routing congestion should all be reviewed before programming hardware."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Report"),
                        rx.table.column_header_cell("Question"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Utilization"), rx.table.cell("Does the design fit available LUT/FF/RAM/DSP resources?")),
                        rx.table.row(rx.table.cell("Timing"), rx.table.cell("Do all required paths meet constraints?")),
                        rx.table.row(rx.table.cell("DRC"), rx.table.cell("Are implementation/device rules violated?")),
                        rx.table.row(rx.table.cell("Clocking"), rx.table.cell("Are clocks routed and constrained correctly?")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "6", "The bitstream configures the FPGA fabric",
                rx.text(
                    "After implementation succeeds, the tool generates a configuration bitstream. Programming transfers that configuration into the FPGA so its LUTs, routing, memories and other resources implement the compiled design."
                ),
                rx.code_block(
                    "implemented design → bitstream generation → programmer/JTAG → FPGA configuration",
                    language="textile", width="100%",
                ),
                _practice(
                    "What generated configuration file programs the FPGA fabric?",
                    HDLFPGAState.bitstream_answer,
                    HDLFPGAState.set_bitstream_answer,
                    HDLFPGAState.check_bitstream,
                    HDLFPGAState.bitstream_feedback,
                    "configuration file",
                ),
            ),
            _section(
                "7", "Volatile configuration may require boot storage",
                rx.text(
                    "Many SRAM-based FPGAs lose configuration when power is removed. Boards therefore often use external nonvolatile configuration memory or a processor that reloads the FPGA during startup."
                ),
                rx.code_block(
                    "power-on → configuration source → FPGA loads bitstream → user design starts",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "Hardware bring-up verifies the real board",
                rx.text(
                    "Initial hardware testing should begin with simple, observable behaviour: clocks present, reset released, known LEDs or outputs toggling, then progressively enable more subsystems."
                ),
                rx.code_block(
                    "bring-up order:\n"
                    "1. power / clock\n"
                    "2. configuration success\n"
                    "3. reset behaviour\n"
                    "4. simple GPIO\n"
                    "5. internal datapath\n"
                    "6. external interfaces\n"
                    "7. full application",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Integrated logic analyzers expose internal signals",
                rx.text(
                    "An embedded logic analyzer can sample selected internal FPGA signals and store captures in on-chip memory. This makes otherwise invisible state, buses and control events observable while the design runs."
                ),
                rx.code_block(
                    "internal signals → trigger/capture core → block RAM → debug link → waveform viewer",
                    language="textile", width="100%",
                ),
                _practice(
                    "What embedded FPGA debug instrument captures internal signals in real hardware?",
                    HDLFPGAState.ila_answer,
                    HDLFPGAState.set_ila_answer,
                    HDLFPGAState.check_ila,
                    HDLFPGAState.ila_feedback,
                    "debug instrument",
                ),
            ),
            _section(
                "10", "Simulation and hardware debug complement each other",
                rx.text(
                    "Simulation gives complete visibility and repeatable stimulus, while hardware testing reveals board-level effects, clocking issues, external-device interactions and real implementation behaviour."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Method"),
                        rx.table.column_header_cell("Best strength"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Simulation"), rx.table.cell("Deterministic verification and full internal visibility")),
                        rx.table.row(rx.table.cell("On-chip logic analyzer"), rx.table.cell("Internal signal capture in deployed hardware")),
                        rx.table.row(rx.table.cell("Oscilloscope"), rx.table.cell("Analog/electrical timing at physical pins")),
                        rx.table.row(rx.table.cell("External logic analyzer"), rx.table.cell("Digital protocol and pin-level timing")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "11", "Trace a complete FPGA deployment workflow",
                rx.code_block(
                    "1. define system requirements\n"
                    "2. create top-level architecture\n"
                    "3. write reusable RTL modules\n"
                    "4. verify modules and integrated design in simulation\n"
                    "5. add clock, I/O and timing constraints\n"
                    "6. synthesize and inspect resources/warnings\n"
                    "7. place and route\n"
                    "8. close timing and clear implementation-rule errors\n"
                    "9. generate bitstream\n"
                    "10. program/configure FPGA\n"
                    "11. perform staged board bring-up\n"
                    "12. use on-chip/external instruments to debug remaining issues\n"
                    "13. archive source, constraints, tool version and known-good build artifacts",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Path 12 integration checkpoint",
                rx.text(
                    "You can now progress from Boolean logic to synthesizable HDL, sequential design, FSMs, verification, timing closure, FPGA memories/DSP pipelines and finally a programmed, debugged physical FPGA system."
                ),
                rx.code_block(
                    "specification\n"
                    "   ↓\n"
                    "RTL + hierarchy\n"
                    "   ↓\n"
                    "simulation / assertions\n"
                    "   ↓\n"
                    "synthesis\n"
                    "   ↓\n"
                    "constraints + place/route + timing closure\n"
                    "   ↓\n"
                    "bitstream\n"
                    "   ↓\n"
                    "FPGA board\n"
                    "   ↓\n"
                    "hardware verification / debug",
                    language="textile", width="100%",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("PATH 12 COMPLETE", color_scheme="green"),
                    rx.heading("HDL, FPGA & Digital System Design is complete.", size="5"),
                    rx.text(
                        "You can now describe, verify, synthesize, time, deploy and debug complete programmable digital hardware.",
                        color="#475569",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )
