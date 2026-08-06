"""BoolNexa Academy Path 09 — Processor Architecture & CPU Datapath."""
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


class CpuPathState(rx.State):
    component_answer: str = ""
    component_feedback: str = ""
    pc_answer: str = ""
    pc_feedback: str = ""
    datapath_answer: str = ""
    datapath_feedback: str = ""
    fetch_answer: str = ""
    fetch_feedback: str = ""
    decode_answer: str = ""
    decode_feedback: str = ""
    execute_answer: str = ""
    execute_feedback: str = ""
    register_answer: str = ""
    register_feedback: str = ""
    bus_answer: str = ""
    bus_feedback: str = ""
    transfer_answer: str = ""
    transfer_feedback: str = ""
    format_answer: str = ""
    format_feedback: str = ""
    immediate_answer: str = ""
    immediate_feedback: str = ""
    loadstore_answer: str = ""
    loadstore_feedback: str = ""
    flow_answer: str = ""
    flow_feedback: str = ""
    control_answer: str = ""
    control_feedback: str = ""
    writeback_answer: str = ""
    writeback_feedback: str = ""
    branch_answer: str = ""
    branch_feedback: str = ""
    zero_answer: str = ""
    zero_feedback: str = ""
    pcsrc_answer: str = ""
    pcsrc_feedback: str = ""
    pipeline_answer: str = ""
    pipeline_feedback: str = ""
    stage_answer: str = ""
    stage_feedback: str = ""
    throughput_answer: str = ""
    throughput_feedback: str = ""
    hazard_answer: str = ""
    hazard_feedback: str = ""
    forwarding_answer: str = ""
    forwarding_feedback: str = ""
    controlhazard_answer: str = ""
    controlhazard_feedback: str = ""

    def set_component_answer(self, value: str) -> None:
        self.component_answer = value

    def set_pc_answer(self, value: str) -> None:
        self.pc_answer = value

    def set_datapath_answer(self, value: str) -> None:
        self.datapath_answer = value

    def set_fetch_answer(self, value: str) -> None:
        self.fetch_answer = value

    def set_decode_answer(self, value: str) -> None:
        self.decode_answer = value

    def set_execute_answer(self, value: str) -> None:
        self.execute_answer = value

    def set_register_answer(self, value: str) -> None:
        self.register_answer = value

    def set_bus_answer(self, value: str) -> None:
        self.bus_answer = value

    def set_transfer_answer(self, value: str) -> None:
        self.transfer_answer = value

    def set_format_answer(self, value: str) -> None:
        self.format_answer = value

    def set_immediate_answer(self, value: str) -> None:
        self.immediate_answer = value

    def set_loadstore_answer(self, value: str) -> None:
        self.loadstore_answer = value

    def set_flow_answer(self, value: str) -> None:
        self.flow_answer = value

    def set_control_answer(self, value: str) -> None:
        self.control_answer = value

    def set_writeback_answer(self, value: str) -> None:
        self.writeback_answer = value

    def set_branch_answer(self, value: str) -> None:
        self.branch_answer = value

    def set_zero_answer(self, value: str) -> None:
        self.zero_answer = value

    def set_pcsrc_answer(self, value: str) -> None:
        self.pcsrc_answer = value

    def set_pipeline_answer(self, value: str) -> None:
        self.pipeline_answer = value

    def set_stage_answer(self, value: str) -> None:
        self.stage_answer = value

    def set_throughput_answer(self, value: str) -> None:
        self.throughput_answer = value

    def set_hazard_answer(self, value: str) -> None:
        self.hazard_answer = value

    def set_forwarding_answer(self, value: str) -> None:
        self.forwarding_answer = value

    def set_controlhazard_answer(self, value: str) -> None:
        self.controlhazard_answer = value

    def check_component(self) -> None:
        value = self.component_answer.strip().lower().replace(" ", "").replace("-", "")
        self.component_feedback = (
            "Correct. The control unit interprets instruction information and coordinates the datapath."
            if value in {"controlunit", "controller", "control"}
            else "Which CPU block generates the signals that coordinate registers, ALU operations and data movement?"
        )

    def check_pc(self) -> None:
        value = self.pc_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pc_feedback = (
            "Correct. The Program Counter stores the address of the next instruction to fetch."
            if value in {"pc", "programcounter"}
            else "Which register normally holds the address of the next instruction?"
        )

    def check_datapath(self) -> None:
        value = self.datapath_answer.strip().lower().replace(" ", "").replace("-", "")
        self.datapath_feedback = (
            "Correct. The datapath is the collection of registers, buses, ALU and selection hardware that actually moves and transforms data."
            if value in {"datapath", "datapathhardware"}
            else "What name is given to the CPU hardware that stores, moves and transforms operands?"
        )

    def check_fetch(self) -> None:
        value = self.fetch_answer.strip().lower().replace(" ", "").replace("-", "")
        self.fetch_feedback = (
            "Correct. The PC supplies the address used to fetch the next instruction."
            if value in {"pc", "programcounter"}
            else "Which register supplies the instruction address during fetch?"
        )

    def check_decode(self) -> None:
        value = self.decode_answer.strip().lower().replace(" ", "").replace("-", "")
        self.decode_feedback = (
            "Correct. The opcode identifies the operation that the control logic must decode."
            if value in {"opcode", "operationcode"}
            else "Which instruction field identifies the requested operation?"
        )

    def check_execute(self) -> None:
        value = self.execute_answer.strip().lower().replace(" ", "").replace("-", "")
        self.execute_feedback = (
            "Correct. The ALU performs the selected arithmetic, logic or comparison operation."
            if value in {"alu", "arithmeticlogicunit"}
            else "Which CPU block normally performs arithmetic and logic during execute?"
        )

    def check_register(self) -> None:
        value = self.register_answer.strip().lower().replace(" ", "").replace("-", "")
        self.register_feedback = (
            "Correct. A register is fast CPU storage that holds a binary word for immediate use."
            if value in {"register", "registers"}
            else "What small, fast CPU storage element holds one binary word?"
        )

    def check_bus(self) -> None:
        value = self.bus_answer.strip().lower().replace(" ", "").replace("-", "")
        self.bus_feedback = (
            "Correct. A bus is a shared group of signal lines used to move a multi-bit value between CPU blocks."
            if value in {"bus", "databus", "internalbus"}
            else "What shared group of lines carries a multi-bit value between registers and other CPU blocks?"
        )

    def check_transfer(self) -> None:
        value = self.transfer_answer.strip().upper().replace(" ", "")
        self.transfer_feedback = (
            "Correct. R2 ← R1 means R2 receives a copy of the value currently stored in R1."
            if value in {"R2←R1", "R2<-R1", "R2=R1"}
            else "Write the register-transfer statement that copies the contents of R1 into R2."
        )

    def check_format(self) -> None:
        value = self.format_answer.strip().lower().replace(" ", "").replace("-", "")
        self.format_feedback = (
            "Correct. The opcode field tells the control unit which operation the instruction requests."
            if value in {"opcode", "operationcode"}
            else "Which instruction field identifies the operation?"
        )

    def check_immediate(self) -> None:
        value = self.immediate_answer.strip().lower().replace(" ", "").replace("-", "")
        self.immediate_feedback = (
            "Correct. Immediate data is a constant encoded directly inside the instruction."
            if value in {"immediate", "immediatedata", "constant", "literal"}
            else "What do we call a constant value encoded directly in an instruction?"
        )

    def check_loadstore(self) -> None:
        value = self.loadstore_answer.strip().lower().replace(" ", "").replace("-", "")
        self.loadstore_feedback = (
            "Correct. A load moves data from memory into a register; a store moves register data to memory."
            if value in {"load", "loadinstruction"}
            else "Which operation transfers a value from memory into a CPU register?"
        )

    def check_flow(self) -> None:
        value = self.flow_answer.strip().lower().replace(" ", "").replace("-", "")
        self.flow_feedback = (
            "Correct. The Program Counter supplies the instruction address at the start of the single-cycle datapath."
            if value in {"pc", "programcounter"}
            else "Which register supplies the address used to fetch the instruction?"
        )

    def check_control(self) -> None:
        value = self.control_answer.strip().lower().replace(" ", "").replace("-", "")
        self.control_feedback = (
            "Correct. The opcode is decoded to generate the control signals that steer the datapath."
            if value in {"opcode", "operationcode"}
            else "Which instruction field is decoded to generate the main control signals?"
        )

    def check_writeback(self) -> None:
        value = self.writeback_answer.strip().lower().replace(" ", "").replace("-", "")
        self.writeback_feedback = (
            "Correct. RegWrite enables the destination register to capture the selected result on the clock edge."
            if value in {"regwrite", "registerwrite", "writeenable"}
            else "Which control signal enables a result to be written into the register file?"
        )

    def check_branch(self) -> None:
        value = self.branch_answer.strip().lower().replace(" ", "").replace("-", "")
        self.branch_feedback = (
            "Correct. Branch marks a conditional control-flow instruction so its condition can influence the next PC."
            if value in {"branch", "branchenable", "branchcontrol"}
            else "Which main control signal identifies a conditional branch instruction?"
        )

    def check_zero(self) -> None:
        value = self.zero_answer.strip().lower().replace(" ", "").replace("-", "")
        self.zero_feedback = (
            "Correct. The ALU Zero flag is asserted when the comparison result is zero, such as when two operands are equal after subtraction."
            if value in {"zero", "zeroflag", "z"}
            else "Which ALU status output commonly reports equality for a branch-equal comparison?"
        )

    def check_pcsrc(self) -> None:
        value = self.pcsrc_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pcsrc_feedback = (
            "Correct. PCSrc selects whether the PC receives the sequential address or the branch target."
            if value in {"pcsrc", "pcsource", "nextpcselect"}
            else "Which select signal chooses the next value loaded into the Program Counter?"
        )


    def check_pipeline(self) -> None:
        value = self.pipeline_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pipeline_feedback = (
            "Correct. Pipelining overlaps different instructions in different execution stages."
            if value in {"pipeline", "pipelining", "instructionpipeline"}
            else "What technique overlaps the execution of several instructions by dividing work into stages?"
        )

    def check_stage(self) -> None:
        value = self.stage_answer.strip().lower().replace(" ", "").replace("-", "")
        self.stage_feedback = (
            "Correct. IF is the instruction-fetch stage; it uses the PC to obtain the next instruction."
            if value in {"if", "fetch", "instructionfetch", "ifstage"}
            else "Which pipeline stage fetches the instruction using the Program Counter?"
        )

    def check_throughput(self) -> None:
        value = self.throughput_answer.strip().lower().replace(" ", "").replace("-", "")
        self.throughput_feedback = (
            "Correct. Once a balanced pipeline is full, ideal throughput approaches one completed instruction per clock cycle."
            if value in {"one", "1", "oneinstructionpercycle", "1instructionpercycle", "onepercycle"}
            else "In an ideal filled pipeline, approximately how many instructions can complete per clock cycle?"
        )

    def check_hazard(self) -> None:
        value = self.hazard_answer.strip().lower().replace(" ", "").replace("-", "")
        self.hazard_feedback = (
            "Correct. A RAW data hazard occurs when a younger instruction tries to read a value before an older instruction has made that result available."
            if value in {"raw", "readafterwrite", "datahazard", "rawhazard"}
            else "Which dependency occurs when an instruction needs a value that an earlier instruction has not produced yet?"
        )

    def check_forwarding(self) -> None:
        value = self.forwarding_answer.strip().lower().replace(" ", "").replace("-", "")
        self.forwarding_feedback = (
            "Correct. Forwarding (bypassing) sends a newly produced result directly to a dependent stage instead of waiting for register-file write-back."
            if value in {"forwarding", "bypassing", "bypass", "operandforwarding"}
            else "What technique routes a result directly from a later pipeline stage to a dependent instruction?"
        )

    def check_controlhazard(self) -> None:
        value = self.controlhazard_answer.strip().lower().replace(" ", "").replace("-", "")
        self.controlhazard_feedback = (
            "Correct. A control hazard occurs when the correct next PC is not yet known because a branch or jump is unresolved."
            if value in {"controlhazard", "branchhazard", "control", "branch"}
            else "What hazard occurs when a branch leaves the correct next instruction address temporarily unknown?"
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


def _practice(
    prompt: str,
    value: rx.Var,
    setter,
    checker,
    feedback: rx.Var,
    placeholder: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(prompt, font_weight="700"),
            rx.hstack(
                rx.input(
                    value=value,
                    on_change=setter,
                    placeholder=placeholder,
                    width="100%",
                ),
                rx.button("Check", on_click=checker, color_scheme="teal"),
                width="100%",
            ),
            rx.cond(
                feedback != "",
                rx.callout(feedback, icon="lightbulb", size="1"),
                rx.fragment(),
            ),
            spacing="3",
            align="stretch",
        ),
        padding="16px",
        border="1px solid #99f6e4",
        border_radius="12px",
        background="#f0fdfa",
        width="100%",
    )


def cpu_architecture_foundations_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 01", color_scheme="teal"),
            rx.heading("CPU Architecture Foundations", size="8"),
            rx.text(
                "A processor brings together the ideas developed across earlier BoolNexa paths: "
                "registers store working values, the ALU transforms data, memory supplies instructions and operands, "
                "and a control unit coordinates each step.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "What a CPU actually does",
                rx.text(
                    "At a high level, a CPU repeatedly fetches an instruction, determines what that instruction means, "
                    "moves the required operands through its datapath, performs the requested operation and stores the result."
                ),
                rx.code_block(
                    "Fetch instruction\n"
                    "      ↓\n"
                    "Decode operation\n"
                    "      ↓\n"
                    "Read / select operands\n"
                    "      ↓\n"
                    "Execute in ALU / datapath\n"
                    "      ↓\n"
                    "Write result / update state",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "2",
                "Core processor blocks",
                rx.text(
                    "A basic educational CPU can be understood using a small set of cooperating blocks."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Block"),
                            rx.table.column_header_cell("Main role"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Register file"), rx.table.cell("Stores operands and intermediate values")),
                        rx.table.row(rx.table.cell("ALU"), rx.table.cell("Performs arithmetic, logic and comparisons")),
                        rx.table.row(rx.table.cell("Control unit"), rx.table.cell("Generates control signals from instruction information")),
                        rx.table.row(rx.table.cell("Program Counter (PC)"), rx.table.cell("Holds the next instruction address")),
                        rx.table.row(rx.table.cell("Instruction Register (IR)"), rx.table.cell("Holds the current instruction while it is decoded/executed")),
                        rx.table.row(rx.table.cell("Buses / multiplexers"), rx.table.cell("Route data between CPU blocks")),
                    ),
                    width="100%",
                ),
                _practice(
                    "Which block coordinates registers, ALU operations and internal data movement?",
                    CpuPathState.component_answer,
                    CpuPathState.set_component_answer,
                    CpuPathState.check_component,
                    CpuPathState.component_feedback,
                    "CPU block",
                ),
            ),
            _section(
                "3",
                "The Program Counter and Instruction Register",
                rx.text(
                    "The Program Counter does not normally store the instruction itself; it stores an address. "
                    "That address identifies where the next instruction is fetched from memory. "
                    "The fetched instruction is then held in an Instruction Register while control logic examines it."
                ),
                rx.code_block(
                    "PC ──address──→ Instruction memory\n"
                    "                  │\n"
                    "                  └── instruction ──→ IR ──→ decoder",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "Which register normally contains the address of the next instruction?",
                    CpuPathState.pc_answer,
                    CpuPathState.set_pc_answer,
                    CpuPathState.check_pc,
                    CpuPathState.pc_feedback,
                    "register",
                ),
            ),
            _section(
                "4",
                "Datapath versus control",
                rx.text(
                    "The datapath is the hardware that actually holds, routes and transforms values. "
                    "The control unit decides how that hardware should be configured for the current instruction."
                ),
                rx.code_block(
                    "CONTROL                          DATAPATH\n"
                    "instruction fields ─→ decoder ─→ register enables\n"
                    "                               → MUX selects\n"
                    "                               → ALU operation\n"
                    "                               → memory read/write\n\n"
                    "registers ↔ buses ↔ ALU ↔ memory interface",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "What is the CPU hardware that stores, routes and transforms operands called?",
                    CpuPathState.datapath_answer,
                    CpuPathState.set_datapath_answer,
                    CpuPathState.check_datapath,
                    CpuPathState.datapath_feedback,
                    "term",
                ),
            ),
            _section(
                "5",
                "Buses and multiplexers",
                rx.text(
                    "A CPU cannot dedicate a separate wire path for every possible source-to-destination transfer. "
                    "Shared buses and multiplexers let control signals choose which register or functional-unit output "
                    "drives a destination at a particular time."
                ),
                rx.callout(
                    "This is the same selection principle used inside the ALU, now applied to the complete processor datapath.",
                    icon="waypoints",
                ),
            ),
            _section(
                "6",
                "How earlier BoolNexa paths connect",
                rx.hstack(
                    rx.badge("Memory", color_scheme="blue"),
                    rx.text("→"),
                    rx.badge("Registers", color_scheme="indigo"),
                    rx.text("→"),
                    rx.badge("ALU", color_scheme="purple"),
                    rx.text("→"),
                    rx.badge("Control", color_scheme="orange"),
                    rx.text("→"),
                    rx.badge("CPU", color_scheme="teal"),
                    wrap="wrap",
                    spacing="2",
                ),
                rx.text(
                    "The CPU is not a completely new kind of circuit. It is an organized system built from the digital "
                    "building blocks you have already studied."
                ),
            ),
            _section(
                "7",
                "Preview of Path 09",
                rx.text(
                    "Path 09 will progress from CPU blocks to instruction fetch/decode/execute, register-transfer operations, "
                    "instruction formats, datapath control, branches and finally an integrated miniature processor."
                ),
                rx.code_block(
                    "Planned progression\n"
                    "1. CPU Architecture Foundations\n"
                    "2. Fetch, Decode and Execute\n"
                    "3. Registers, Buses and Register Transfer\n"
                    "4. Instruction Formats and Data Movement\n"
                    "5. Single-Cycle Datapath\n"
                    "6. Control Signals and Branching\n"
                    "7. Multi-Step CPU Control\n"
                    "8. Integrated Mini-CPU Design",
                    language="textile",
                    width="100%",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 01 COMPLETE", color_scheme="green"),
                    rx.heading("You now know the major blocks of a processor.", size="5"),
                    rx.text(
                        "Next: follow one instruction through the fetch, decode and execute cycle.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Fetch, Decode & Execute", color_scheme="teal"),
                        href="/academy/unit-9/fetch-decode-execute",
                        text_decoration="none",
                    ),
                    spacing="3",
                    align="start",
                ),
                width="100%",
            ),
            spacing="6",
            align="stretch",
            max_width="1050px",
            width="100%",
            margin="0 auto",
            padding="32px 20px 64px",
        ),
        min_height="100vh",
        background="#f8fafc",
    )


def fetch_decode_execute_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 02", color_scheme="teal"),
            rx.heading("Fetch, Decode & Execute", size="8"),
            rx.text(
                "Every instruction moves through an ordered sequence. The processor fetches the instruction, "
                "decodes what it requests, executes the required datapath operation, and commits any architectural result.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The instruction cycle",
                rx.code_block(
                    "FETCH → DECODE → EXECUTE → WRITE / UPDATE → next instruction\n\n"
                    "The exact hardware may overlap or subdivide these stages, but this sequence is the conceptual foundation.",
                    language="textile", width="100%",
                ),
                rx.text(
                    "The instruction cycle connects memory, the PC, the instruction register, control logic, registers and the ALU."
                ),
            ),
            _section(
                "2", "Fetch: obtain the instruction",
                rx.text(
                    "During fetch, the Program Counter supplies an instruction-memory address. "
                    "The instruction at that address is read and captured for decoding. "
                    "The PC is also prepared to identify the following instruction unless later control flow changes it."
                ),
                rx.code_block(
                    "PC ──→ instruction-memory address\n"
                    "memory[PC] ──→ IR\n"
                    "PC ──→ next sequential PC",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which register supplies the instruction address during the fetch stage?",
                    CpuPathState.fetch_answer, CpuPathState.set_fetch_answer,
                    CpuPathState.check_fetch, CpuPathState.fetch_feedback, "register",
                ),
            ),
            _section(
                "3", "Decode: understand the instruction",
                rx.text(
                    "The control unit examines instruction fields. An opcode identifies the operation, while other fields "
                    "may identify source registers, a destination register, an immediate constant or addressing information."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Field"),
                        rx.table.column_header_cell("Typical meaning"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Opcode"), rx.table.cell("Requested operation")),
                        rx.table.row(rx.table.cell("Source fields"), rx.table.cell("Where operands come from")),
                        rx.table.row(rx.table.cell("Destination field"), rx.table.cell("Where a result may be written")),
                        rx.table.row(rx.table.cell("Immediate"), rx.table.cell("Constant encoded in the instruction")),
                    ),
                    width="100%",
                ),
                _practice(
                    "Which instruction field normally identifies the operation to perform?",
                    CpuPathState.decode_answer, CpuPathState.set_decode_answer,
                    CpuPathState.check_decode, CpuPathState.decode_feedback, "field",
                ),
            ),
            _section(
                "4", "Execute: make the datapath act",
                rx.text(
                    "Control signals configure multiplexers, register reads and the ALU. "
                    "For an ADD instruction, source operands reach the ALU and the ALU performs addition. "
                    "For a logical instruction, the same datapath can select a different ALU function."
                ),
                rx.code_block(
                    "source registers ─→ operand MUXes ─→ ALU ─→ result\n"
                    "                         ↑            ↑\n"
                    "                    select bits    ALUCtrl\n"
                    "                         └──── control unit",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which CPU block normally performs arithmetic and logic during execute?",
                    CpuPathState.execute_answer, CpuPathState.set_execute_answer,
                    CpuPathState.check_execute, CpuPathState.execute_feedback, "block",
                ),
            ),
            _section(
                "5", "Write-back and architectural state",
                rx.text(
                    "If an instruction produces a register result, that value is written to the selected destination register. "
                    "Other instructions may update memory, status information or the PC instead. "
                    "These persistent values form the processor's architectural state."
                ),
                rx.callout(
                    "Not every instruction writes a general-purpose register. A branch may primarily change the PC; a store primarily changes memory.",
                    icon="info",
                ),
            ),
            _section(
                "6", "Walk through an example: ADD R3, R1, R2",
                rx.code_block(
                    "FETCH    : IR ← memory[PC], prepare next PC\n"
                    "DECODE   : opcode = ADD; sources = R1,R2; destination = R3\n"
                    "READ     : A ← R1, B ← R2\n"
                    "EXECUTE  : ALUOut ← A + B\n"
                    "WRITE    : R3 ← ALUOut",
                    language="textile", width="100%",
                ),
                rx.text(
                    "The notation uses ← to mean 'receives the value of'. It describes data movement without requiring a particular CPU implementation."
                ),
            ),
            _section(
                "7", "Control-flow instructions change the sequence",
                rx.text(
                    "Normally the CPU proceeds to the next sequential instruction. Branches and jumps can replace that next PC "
                    "with a target address. This is why the PC belongs to both the instruction-fetch path and the control-flow system."
                ),
                rx.code_block(
                    "condition false → next sequential PC\n"
                    "condition true  → branch target PC",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("PC", color_scheme="blue"), rx.text("→"),
                    rx.badge("Fetch", color_scheme="cyan"), rx.text("→"),
                    rx.badge("IR / Decode", color_scheme="orange"), rx.text("→"),
                    rx.badge("Datapath / Execute", color_scheme="purple"), rx.text("→"),
                    rx.badge("State update", color_scheme="green"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now trace an instruction from its address in the PC through decoding and datapath execution to a visible processor-state change."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 02 COMPLETE", color_scheme="green"),
                    rx.heading("The CPU instruction cycle is now connected end-to-end.", size="5"),
                    rx.text("Next: learn how registers and buses express data movement as register-transfer operations.", color="#475569"),
                    rx.link(
                        rx.button("Next · Registers, Buses & Register Transfer", color_scheme="teal"),
                        href="/academy/unit-9/register-transfer",
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


def registers_buses_register_transfer_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 03", color_scheme="teal"),
            rx.heading("Registers, Buses & Register Transfer", size="8"),
            rx.text(
                "A CPU performs useful work by moving binary words between registers and functional units. "
                "Register-transfer notation gives us a precise way to describe those movements before worrying about transistor-level detail.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Registers are the CPU's working storage",
                rx.text(
                    "A register is a small, fast storage element inside the processor. General-purpose registers hold operands and results, "
                    "while special-purpose registers such as the PC and IR hold values needed for control and instruction processing."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Register type"),
                        rx.table.column_header_cell("Typical purpose"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("General-purpose R0, R1, ..."), rx.table.cell("Operands, addresses and intermediate results")),
                        rx.table.row(rx.table.cell("PC"), rx.table.cell("Address of the next instruction")),
                        rx.table.row(rx.table.cell("IR"), rx.table.cell("Current instruction being decoded/executed")),
                        rx.table.row(rx.table.cell("Status / flags"), rx.table.cell("Condition information such as zero, carry or overflow")),
                    ),
                    width="100%",
                ),
                _practice(
                    "What small, fast CPU storage element holds one binary word for immediate use?",
                    CpuPathState.register_answer, CpuPathState.set_register_answer,
                    CpuPathState.check_register, CpuPathState.register_feedback, "storage element",
                ),
            ),
            _section(
                "2", "A register is a group of flip-flops",
                rx.text(
                    "An n-bit register stores n bits, so an 8-bit register stores one 8-bit word. Its storage bits share control signals "
                    "so the complete word can be loaded together on an active clock edge."
                ),
                rx.code_block(
                    "8-bit input word : D7 D6 D5 D4 D3 D2 D1 D0\n"
                    "                    │  │  │  │  │  │  │  │\n"
                    "                 [ eight clocked storage bits ]\n"
                    "                    │  │  │  │  │  │  │  │\n"
                    "8-bit stored word: Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Clocking determines when a register may capture a new word; an enable signal determines whether it should load or retain its old value.",
                    icon="info",
                ),
            ),
            _section(
                "3", "Buses move whole words",
                rx.text(
                    "A bus is a collection of parallel signal lines treated as one multi-bit path. Instead of drawing eight separate wires for an 8-bit value, "
                    "a datapath diagram can show one 8-bit bus connecting registers, multiplexers and the ALU."
                ),
                rx.code_block(
                    "R1 ──┐\n"
                    "R2 ──┼──→ source select ──→ 8-bit internal bus ──→ ALU / destination registers\n"
                    "R3 ──┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What shared group of lines carries a multi-bit value between CPU blocks?",
                    CpuPathState.bus_answer, CpuPathState.set_bus_answer,
                    CpuPathState.check_bus, CpuPathState.bus_feedback, "shared path",
                ),
            ),
            _section(
                "4", "Only one selected source should drive a shared bus",
                rx.text(
                    "If several registers connect to one shared bus, control hardware chooses which source places its value on that bus. "
                    "A multiplexer is a common implementation. The destination register loads the bus value only when its load-enable is asserted."
                ),
                rx.code_block(
                    "source select = R1\n"
                    "R1 = 10110110 ──→ BUS = 10110110\n"
                    "R2 load = 1     ──→ on clock edge, R2 captures BUS",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Two uncontrolled sources driving the same physical bus can cause contention. CPU control logic prevents incompatible bus drivers from being enabled together.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "5", "Register-transfer notation",
                rx.text(
                    "Register-transfer language (RTL) describes data movement and simple micro-operations. The left arrow means 'receives the value of'. "
                    "The source is read; the destination is updated. The source normally keeps its original value."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Notation"),
                        rx.table.column_header_cell("Meaning"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("R2 ← R1"), rx.table.cell("Copy R1 into R2")),
                        rx.table.row(rx.table.cell("R3 ← R1 + R2"), rx.table.cell("Add R1 and R2, then store the result in R3")),
                        rx.table.row(rx.table.cell("IR ← M[PC]"), rx.table.cell("Load the instruction at the address held in PC")),
                        rx.table.row(rx.table.cell("PC ← PC + 1"), rx.table.cell("Advance the Program Counter in this simplified model")),
                    ),
                    width="100%",
                ),
                _practice(
                    "Write the register-transfer statement that copies the contents of R1 into R2.",
                    CpuPathState.transfer_answer, CpuPathState.set_transfer_answer,
                    CpuPathState.check_transfer, CpuPathState.transfer_feedback, "for example R2 ← R1",
                ),
            ),
            _section(
                "6", "A transfer requires control and timing",
                rx.text(
                    "The statement R2 ← R1 looks simple, but hardware must coordinate several actions: select R1 as the bus source, "
                    "allow its value to propagate, assert R2's load enable, and capture the value at the correct clock event."
                ),
                rx.code_block(
                    "Micro-operation: R2 ← R1\n\n"
                    "1. Select R1 as source\n"
                    "2. R1 value appears on internal bus\n"
                    "3. Assert Load_R2\n"
                    "4. Active clock edge occurs\n"
                    "5. R2 stores the bus value",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Register transfer through the ALU",
                rx.text(
                    "Transfers do not have to be simple copies. Source registers can feed the ALU, the control unit can select an operation, "
                    "and the destination register can capture the ALU result."
                ),
                rx.code_block(
                    "R1 ──→ ALU input A ─┐\n"
                    "                    ├─ ADD ─→ result bus ─→ R3\n"
                    "R2 ──→ ALU input B ─┘\n\n"
                    "Register transfer: R3 ← R1 + R2",
                    language="textile", width="100%",
                ),
                rx.text(
                    "This connects Path 08's ALU to the CPU datapath: the ALU transforms values, while registers and buses make those values available and preserve the result."
                ),
            ),
            _section(
                "8", "Trace a complete micro-operation",
                rx.code_block(
                    "Before clock edge\n"
                    "R1 = 00110101\n"
                    "R2 = 11110000\n\n"
                    "Control: select R1; Load_R2 = 1\n"
                    "BUS = 00110101\n\n"
                    "After active clock edge\n"
                    "R1 = 00110101   (unchanged)\n"
                    "R2 = 00110101   (new copy)",
                    language="textile", width="100%",
                ),
                rx.text(
                    "A register transfer copies information unless the operation itself changes the source. This distinction is essential when tracing CPU state."
                ),
            ),
            _section(
                "9", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("Register", color_scheme="blue"), rx.text("→ stores word"),
                    rx.badge("Bus", color_scheme="cyan"), rx.text("→ moves word"),
                    rx.badge("Control", color_scheme="orange"), rx.text("→ selects source/destination"),
                    rx.badge("Clock", color_scheme="purple"), rx.text("→ commits transfer"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now read register-transfer notation and explain how registers, buses, selection logic, enables and clocking cooperate to move data through a processor."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 03 COMPLETE", color_scheme="green"),
                    rx.heading("You can now describe CPU data movement as register-transfer operations.", size="5"),
                    rx.text(
                        "Next: connect these transfers to instruction fields, load/store operations and immediate data.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Instruction Formats & Data Movement", color_scheme="teal"),
                        href="/academy/unit-9/instruction-formats",
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



def instruction_formats_data_movement_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 04", color_scheme="teal"),
            rx.heading("Instruction Formats & Data Movement", size="8"),
            rx.text(
                "An instruction is a binary word whose fields tell the CPU what operation to perform, where operands come from, "
                "where a result goes and, when needed, what constant or memory address information to use.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Why instructions need fields",
                rx.text(
                    "A processor must turn one binary instruction into several control decisions. An instruction format divides the word into fields so the decoder can interpret each part consistently."
                ),
                rx.code_block(
                    "Example 16-bit teaching format\n"
                    "+--------+--------+--------+--------+\n"
                    "| opcode |  Rd    |  Rs    | extra  |\n"
                    "+--------+--------+--------+--------+\n"
                    "   4 bits   4 bits   4 bits   4 bits",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Real processors use many different instruction widths and field layouts. This lesson uses simplified formats to make the datapath ideas visible.",
                    icon="info",
                ),
            ),
            _section(
                "2", "Opcode and register fields",
                rx.text(
                    "The opcode identifies the requested operation. Register fields identify source and destination registers. The same physical register file can therefore support many instructions simply by changing the encoded register numbers."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Field"),
                        rx.table.column_header_cell("Purpose"),
                        rx.table.column_header_cell("Example"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Opcode"), rx.table.cell("Select operation"), rx.table.cell("ADD")),
                        rx.table.row(rx.table.cell("Rd"), rx.table.cell("Destination register"), rx.table.cell("R3")),
                        rx.table.row(rx.table.cell("Rs1"), rx.table.cell("First source register"), rx.table.cell("R1")),
                        rx.table.row(rx.table.cell("Rs2"), rx.table.cell("Second source register"), rx.table.cell("R2")),
                    ), width="100%",
                ),
                _practice(
                    "Which instruction field tells the control unit which operation to perform?",
                    CpuPathState.format_answer, CpuPathState.set_format_answer,
                    CpuPathState.check_format, CpuPathState.format_feedback, "field",
                ),
            ),
            _section(
                "3", "Register-register data movement",
                rx.text(
                    "A register-register instruction obtains all of its main operands from registers. Decode selects the named registers, execute performs the operation, and write-back updates the destination."
                ),
                rx.code_block(
                    "ADD R3, R1, R2\n\n"
                    "Decode : source A = R1; source B = R2; destination = R3\n"
                    "Execute: ALUOut = R1 + R2\n"
                    "Write  : R3 ← ALUOut",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "4", "Immediate data travels with the instruction",
                rx.text(
                    "An immediate field stores a constant directly in the instruction. This avoids reading a second register when the required operand is a small fixed value."
                ),
                rx.code_block(
                    "ADDI R4, R1, #5\n\n"
                    "source register = R1\n"
                    "immediate field = 5\n"
                    "ALU inputs      = R1 and 5\n"
                    "result transfer = R4 ← R1 + 5",
                    language="textile", width="100%",
                ),
                _practice(
                    "What is a constant encoded directly inside an instruction called?",
                    CpuPathState.immediate_answer, CpuPathState.set_immediate_answer,
                    CpuPathState.check_immediate, CpuPathState.immediate_feedback, "term",
                ),
            ),
            _section(
                "5", "Immediate width, extension and range",
                rx.text(
                    "Instruction width is limited, so an immediate field usually has fewer bits than a CPU register. Hardware extends the encoded value to the datapath width before the ALU uses it."
                ),
                rx.code_block(
                    "8-bit immediate       1111 1010\n"
                    "sign-extend to 16 bit 1111 1111 1111 1010\n\n"
                    "zero extension is used when the encoded value is treated as unsigned; sign extension preserves a signed two's-complement value.",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Load and store connect registers to memory",
                rx.text(
                    "Arithmetic instructions mainly move values within the CPU. Load and store instructions cross the processor-memory boundary. A load reads memory and places the value in a register; a store writes a register value into memory."
                ),
                rx.code_block(
                    "LOAD R2, [R1 + 4]\n"
                    "address = R1 + 4\n"
                    "R2 ← memory[address]\n\n"
                    "STORE R2, [R1 + 4]\n"
                    "address = R1 + 4\n"
                    "memory[address] ← R2",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which operation moves a value from memory into a CPU register?",
                    CpuPathState.loadstore_answer, CpuPathState.set_loadstore_answer,
                    CpuPathState.check_loadstore, CpuPathState.loadstore_feedback, "operation",
                ),
            ),
            _section(
                "7", "Effective addresses combine fields and registers",
                rx.text(
                    "Many memory instructions do not encode a complete memory address. Instead, the CPU calculates an effective address from a base register and an offset carried in the instruction."
                ),
                rx.code_block(
                    "base register R1 = 0x1200\n"
                    "offset           = 0x000C\n"
                    "effective address = 0x120C\n\n"
                    "address ALU: R1 + offset → memory address",
                    language="textile", width="100%",
                ),
                rx.text(
                    "This is another register-transfer operation: instruction bits supply one operand, a register supplies another, and the ALU forms the address."
                ),
            ),
            _section(
                "8", "One instruction format drives several datapath choices",
                rx.code_block(
                    "instruction register (IR)\n"
                    "        │\n"
                    "        ├─ opcode ─────────→ control decoder ─→ ALUCtrl / MemRead / MemWrite\n"
                    "        ├─ source fields ──→ register-file read selects\n"
                    "        ├─ destination ─────→ register-file write select\n"
                    "        └─ immediate ───────→ extender ─→ operand/address MUX\n",
                    language="textile", width="100%",
                ),
                rx.text(
                    "The instruction therefore bridges control and datapath: encoded fields become select signals, operation controls and data values."
                ),
            ),
            _section(
                "9", "Trace three common instruction classes",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Class"),
                        rx.table.column_header_cell("Operands"),
                        rx.table.column_header_cell("Main data movement"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Register-register"), rx.table.cell("Registers"), rx.table.cell("Registers → ALU → register")),
                        rx.table.row(rx.table.cell("Immediate"), rx.table.cell("Register + encoded constant"), rx.table.cell("Register/immediate → ALU → register")),
                        rx.table.row(rx.table.cell("Load/store"), rx.table.cell("Register + offset + memory"), rx.table.cell("Register ↔ address ALU ↔ memory")),
                    ), width="100%",
                ),
                rx.text(
                    "Different instruction formats exist because different operations need different combinations of opcode bits, register identifiers, constants and address information."
                ),
            ),
            _section(
                "10", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("Opcode", color_scheme="blue"), rx.text("→ operation"),
                    rx.badge("Register fields", color_scheme="cyan"), rx.text("→ operands"),
                    rx.badge("Immediate", color_scheme="purple"), rx.text("→ encoded constant"),
                    rx.badge("Load/Store", color_scheme="orange"), rx.text("→ memory transfer"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now read a simplified instruction format and follow how its fields select registers, supply immediate data, calculate addresses and move values between the CPU and memory."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 04 COMPLETE", color_scheme="green"),
                    rx.heading("Instruction bits now connect directly to datapath movement.", size="5"),
                    rx.text(
                        "Next: combine these fields and transfers into a complete single-cycle processor datapath.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Single-Cycle Datapath", color_scheme="teal"),
                        href="/academy/unit-9/single-cycle-datapath",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )



def single_cycle_datapath_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 05", color_scheme="teal"),
            rx.heading("Single-Cycle Datapath", size="8"),
            rx.text(
                "A single-cycle processor completes the work of one instruction between two active clock edges. "
                "The datapath connects instruction memory, registers, the ALU, data memory and multiplexers so one "
                "instruction can flow from fetch to state update in a single coordinated path.",
                color="#334155", size="4",
            ),
            _section(
                "1", "One instruction, one clock interval",
                rx.text(
                    "In a single-cycle design, every instruction begins with the current PC and reaches its architectural "
                    "state update before the next active clock edge. Different instruction classes use different portions "
                    "of the datapath, but they share the same hardware structure."
                ),
                rx.code_block(
                    "clock edge n                                      clock edge n+1\
"
                    "    │                                                  │\
"
                    "    └─ PC → fetch → decode → execute → memory → write ─┘",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Single-cycle describes the timing model, not the number of internal hardware actions. Many combinational operations occur between the two clock edges.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "2", "The main datapath blocks",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Block"),
                        rx.table.column_header_cell("Role in the cycle"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("PC"), rx.table.cell("Holds the current instruction address")),
                        rx.table.row(rx.table.cell("Instruction memory"), rx.table.cell("Supplies the encoded instruction")),
                        rx.table.row(rx.table.cell("Register file"), rx.table.cell("Reads source operands and receives register results")),
                        rx.table.row(rx.table.cell("ALU"), rx.table.cell("Performs arithmetic/logic or forms an effective address")),
                        rx.table.row(rx.table.cell("Data memory"), rx.table.cell("Provides load data or accepts store data")),
                        rx.table.row(rx.table.cell("MUXes"), rx.table.cell("Choose among alternative sources and destinations")),
                    ), width="100%",
                ),
                _practice(
                    "Which register supplies the address used to fetch the instruction?",
                    CpuPathState.flow_answer, CpuPathState.set_flow_answer,
                    CpuPathState.check_flow, CpuPathState.flow_feedback, "register",
                ),
            ),
            _section(
                "3", "Follow the fetch path",
                rx.text(
                    "The PC fans out to instruction memory and to the next-PC adder. Instruction memory returns the instruction, "
                    "while the adder prepares the sequential address. In this simplified model, the next sequential PC is PC + 1."
                ),
                rx.code_block(
                    "                 ┌───────────────┐\
"
                    "PC ─────────────→│ Instruction   │──→ instruction bits\
"
                    "│                │ memory        │\
"
                    "└─→ +1 adder ─────────────────────→ sequential next PC",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "4", "Decode turns fields into selections",
                rx.text(
                    "The instruction register fields select source and destination registers. The opcode is decoded by the control "
                    "unit, which produces signals for the register file, ALU, memories and multiplexers."
                ),
                rx.code_block(
                    "instruction\
"
                    "   ├─ opcode ─────────→ control ─→ RegWrite / ALUSrc / MemRead / MemWrite / ResultSrc\
"
                    "   ├─ rs1, rs2 ───────→ register-file read ports\
"
                    "   ├─ rd ─────────────→ register-file write select\
"
                    "   └─ immediate ───────→ extender",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which instruction field is decoded to generate the main control signals?",
                    CpuPathState.control_answer, CpuPathState.set_control_answer,
                    CpuPathState.check_control, CpuPathState.control_feedback, "field",
                ),
            ),
            _section(
                "5", "Operand selection feeds the ALU",
                rx.text(
                    "The ALU's first input usually comes from a source register. A multiplexer chooses the second input: another "
                    "register for register-register operations, or an extended immediate for immediate arithmetic and address calculation."
                ),
                rx.code_block(
                    "R[rs1] ───────────────────────→ ALU input A\
"
                    "                                      ┌───────┐\
"
                    "R[rs2] ───────┐                     │       │\
"
                    "              ├─→ ALUSrc MUX ─────→│  ALU  │──→ ALUResult\
"
                    "immediate ────┘                     │       │\
"
                    "                                      └───────┘",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "6", "Load and store extend the path through data memory",
                rx.text(
                    "For a load or store, the ALU calculates the effective address. A load reads data memory and routes the returned "
                    "value toward the register file. A store sends a source-register value to memory and does not write a register result."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Instruction"),
                        rx.table.column_header_cell("ALU purpose"),
                        rx.table.column_header_cell("Memory"),
                        rx.table.column_header_cell("Register write"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("ADD"), rx.table.cell("R1 + R2"), rx.table.cell("none"), rx.table.cell("ALU result")),
                        rx.table.row(rx.table.cell("LOAD"), rx.table.cell("base + offset"), rx.table.cell("read"), rx.table.cell("memory data")),
                        rx.table.row(rx.table.cell("STORE"), rx.table.cell("base + offset"), rx.table.cell("write"), rx.table.cell("none")),
                    ), width="100%",
                ),
            ),
            _section(
                "7", "Write-back selects the architectural result",
                rx.text(
                    "A result multiplexer chooses what returns to the destination register. Arithmetic instructions select the ALU result; "
                    "loads select memory data. RegWrite is asserted only when the instruction is supposed to update the register file."
                ),
                rx.code_block(
                    "ALUResult ─────┐\
"
                    "               ├─→ ResultSrc MUX ─→ register-file write data\
"
                    "MemoryData ────┘                         │\
"
                    "                                      RegWrite",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which control signal enables a result to be written into the register file?",
                    CpuPathState.writeback_answer, CpuPathState.set_writeback_answer,
                    CpuPathState.check_writeback, CpuPathState.writeback_feedback, "control signal",
                ),
            ),
            _section(
                "8", "Trace an ADD instruction end-to-end",
                rx.code_block(
                    "Instruction: ADD R3, R1, R2\
\
"
                    "1. PC → instruction memory → instruction\
"
                    "2. register file reads R1 and R2\
"
                    "3. ALUSrc selects R2; ALU performs ADD\
"
                    "4. ResultSrc selects ALUResult\
"
                    "5. RegWrite = 1; R3 captures the result on the clock edge\
"
                    "6. PC captures the selected next address",
                    language="textile", width="100%",
                ),
                rx.text(
                    "No data-memory access is required for this register-register instruction. The combinational path is therefore fetch → register read → ALU → write-back."
                ),
            ),
            _section(
                "9", "Trace a LOAD instruction end-to-end",
                rx.code_block(
                    "Instruction: LOAD R3, [R1 + 8]\
\
"
                    "1. PC → instruction memory → instruction\
"
                    "2. register file reads base register R1\
"
                    "3. immediate 8 is extended; ALUSrc selects it\
"
                    "4. ALU forms effective address R1 + 8\
"
                    "5. MemRead supplies MemoryData\
"
                    "6. ResultSrc selects MemoryData\
"
                    "7. RegWrite = 1; R3 captures the loaded value",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "Why the longest path matters",
                rx.text(
                    "All instruction classes share one clock period in this design. The period must be long enough for the slowest legal "
                    "instruction path to settle before the next active edge. A load often exercises more blocks than a simple ALU instruction."
                ),
                rx.code_block(
                    "Typical long load path:\
"
                    "PC → instruction memory → register file → ALU → data memory → result MUX → destination register",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "This is the key trade-off of a single-cycle CPU: simple control and one-cycle instruction completion, but the clock must accommodate the longest combinational path.",
                    icon="clock", color_scheme="orange",
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("PC", color_scheme="blue"), rx.text("→ fetch address"),
                    rx.badge("Register file", color_scheme="cyan"), rx.text("→ operands/results"),
                    rx.badge("ALU", color_scheme="purple"), rx.text("→ operation/address"),
                    rx.badge("Memory", color_scheme="orange"), rx.text("→ load/store"),
                    rx.badge("MUX", color_scheme="green"), rx.text("→ selects paths"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now trace register-register and load/store instructions through a complete single-cycle datapath and explain how control signals steer shared hardware."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 05 COMPLETE", color_scheme="green"),
                    rx.heading("The complete single-cycle data path is now connected.", size="5"),
                    rx.text(
                        "Next: learn how control signals select datapath behavior and how branches choose a new PC.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Control Signals & Branching", color_scheme="teal"),
                        href="/academy/unit-9/control-signals-branching",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def control_signals_branching_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 06", color_scheme="teal", width="100%"),
            rx.heading("Control Signals & Branching", size="8"),
            rx.text(
                "A single-cycle datapath becomes a processor only when control logic selects the correct sources, operations, writes and next-PC path for every instruction."
            ),
            _section(
                "1", "Control turns an instruction into datapath decisions",
                rx.text(
                    "The opcode and function fields enter the control unit. The resulting signals configure multiplexers, the ALU, memories, register enables and the next-PC selector during the same clock interval."
                ),
                rx.code_block(
                    "instruction fields → main control → datapath controls\n"
                    "                         ├─ register write\n"
                    "                         ├─ memory read/write\n"
                    "                         ├─ ALU input and operation\n"
                    "                         └─ next-PC selection",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "2", "The main single-cycle control signals",
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Signal"), rx.table.column_header_cell("Purpose"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("RegWrite"), rx.table.cell("Enables a destination-register update")),
                        rx.table.row(rx.table.cell("ALUSrc"), rx.table.cell("Selects register or immediate as ALU input B")),
                        rx.table.row(rx.table.cell("ALUOp / ALUCtrl"), rx.table.cell("Chooses arithmetic, logic or comparison")),
                        rx.table.row(rx.table.cell("MemRead"), rx.table.cell("Enables a data-memory read")),
                        rx.table.row(rx.table.cell("MemWrite"), rx.table.cell("Enables a data-memory write")),
                        rx.table.row(rx.table.cell("MemToReg"), rx.table.cell("Selects memory data or ALU result for write-back")),
                        rx.table.row(rx.table.cell("Branch"), rx.table.cell("Enables conditional next-PC decision logic")),
                        rx.table.row(rx.table.cell("Jump"), rx.table.cell("Selects an unconditional target when supported")),
                        rx.table.row(rx.table.cell("PCSrc"), rx.table.cell("Selects the value loaded into the PC")),
                    ), width="100%",
                ),
                _practice(
                    "Which main control signal identifies a conditional branch instruction?",
                    CpuPathState.branch_answer, CpuPathState.set_branch_answer, CpuPathState.check_branch,
                    CpuPathState.branch_feedback, "control signal",
                ),
            ),
            _section(
                "3", "Opcode decoding creates a control word",
                rx.text(
                    "Each instruction class maps to a repeatable bundle of control values. A register ADD writes a register and uses two register operands; a LOAD also reads memory and selects memory data for write-back; a STORE writes memory but not the register file."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in ("Instruction", "RegWrite", "ALUSrc", "MemRead", "MemWrite", "MemToReg", "Branch")])),
                    rx.table.body(
                        rx.table.row(*[rx.table.cell(x) for x in ("ADD", "1", "0", "0", "0", "0", "0")]),
                        rx.table.row(*[rx.table.cell(x) for x in ("LOAD", "1", "1", "1", "0", "1", "0")]),
                        rx.table.row(*[rx.table.cell(x) for x in ("STORE", "0", "1", "0", "1", "X", "0")]),
                        rx.table.row(*[rx.table.cell(x) for x in ("BEQ", "0", "0", "0", "0", "X", "1")]),
                    ), width="100%",
                ),
                rx.callout("X means the signal is a don't-care for that instruction because its selected result is not committed.", icon="info", color_scheme="blue"),
            ),
            _section(
                "4", "ALU control refines the requested operation",
                rx.text(
                    "The main decoder can produce a compact ALUOp code, while a smaller ALU-control decoder combines ALUOp with function bits. Loads and stores request addition for address formation; a branch-equal instruction commonly requests subtraction for comparison."
                ),
                rx.code_block(
                    "LOAD / STORE → ALU ADD → base + extended offset\n"
                    "BEQ          → ALU SUB → test whether A - B = 0\n"
                    "register op  → function field selects ADD, SUB, AND, OR, ...",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Conditional branches combine control with a status result",
                rx.text(
                    "For branch-equal, the ALU subtracts the two source operands. Equal values produce zero, so the Zero flag becomes 1. Branch and Zero are then combined to decide whether the branch target should replace the sequential next PC."
                ),
                rx.code_block(
                    "comparison:  R[rs1] - R[rs2] → Zero\n"
                    "take_branch = Branch AND Zero\n"
                    "PCSrc       = take_branch",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which ALU status output commonly reports equality for a branch-equal comparison?",
                    CpuPathState.zero_answer, CpuPathState.set_zero_answer, CpuPathState.check_zero,
                    CpuPathState.zero_feedback, "status flag",
                ),
            ),
            _section(
                "6", "The branch target is formed in parallel",
                rx.text(
                    "While the register comparison is occurring, an adder forms the target from the sequential PC and a sign-extended displacement. Parallel work helps keep the path conceptually simple even though the final PC choice waits for the condition result."
                ),
                rx.code_block(
                    "sequential_next = PC + 1\n"
                    "branch_target  = sequential_next + sign_extend(offset)\n"
                    "next_PC        = PCSrc ? branch_target : sequential_next",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "PCSrc selects the next instruction address",
                rx.text(
                    "The next-PC multiplexer normally selects the sequential address. A taken conditional branch selects the branch target; an unconditional jump may use an additional target input and selection code."
                ),
                rx.code_block(
                    "                         ┌─ sequential PC\n"
                    "current PC → fetch ...  ├─ branch target  → next-PC MUX → PC\n"
                    "                         └─ jump target",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which select signal chooses the next value loaded into the Program Counter?",
                    CpuPathState.pcsrc_answer, CpuPathState.set_pcsrc_answer, CpuPathState.check_pcsrc,
                    CpuPathState.pcsrc_feedback, "select signal",
                ),
            ),
            _section(
                "8", "Trace a branch-equal instruction",
                rx.code_block(
                    "Instruction: BEQ R1, R2, +3\n"
                    "R1 = 01010110, R2 = 01010110\n\n"
                    "1. Decode sets Branch=1, ALUSrc=0 and RegWrite=0\n"
                    "2. Register file supplies R1 and R2\n"
                    "3. ALU performs R1 - R2 = 00000000, so Zero=1\n"
                    "4. Branch AND Zero = 1, therefore PCSrc=1\n"
                    "5. PC captures the computed branch target",
                    language="textile", width="100%",
                ),
                rx.text("No general-purpose register or data-memory location changes; the visible architectural result is the new PC."),
            ),
            _section(
                "9", "Not-taken branches and unconditional jumps",
                rx.text(
                    "If a branch condition is false, PCSrc keeps the sequential path selected. A jump does not depend on the ALU Zero flag: its decoded Jump control selects the jump target directly."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Control-flow case"), rx.table.column_header_cell("Next PC"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Ordinary instruction"), rx.table.cell("Sequential address")),
                        rx.table.row(rx.table.cell("Conditional branch, false"), rx.table.cell("Sequential address")),
                        rx.table.row(rx.table.cell("Conditional branch, true"), rx.table.cell("Branch target")),
                        rx.table.row(rx.table.cell("Jump"), rx.table.cell("Jump target")),
                    ), width="100%",
                ),
            ),
            _section(
                "10", "Safe control prevents unintended state changes",
                rx.text(
                    "Only explicit write enables should modify architectural state. Branches normally keep RegWrite and MemWrite deasserted. A mistaken write-enable value could corrupt a register or memory even when the next-PC decision is correct."
                ),
                rx.callout(
                    "Control signals are meaningful only when considered together: the full control word must describe one legal datapath action.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("Decode", color_scheme="blue"), rx.text("→ control word"),
                    rx.badge("ALU", color_scheme="purple"), rx.text("→ result / condition"),
                    rx.badge("Branch", color_scheme="orange"), rx.text("+ Zero → PCSrc"),
                    rx.badge("PC MUX", color_scheme="green"), rx.text("→ next address"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now derive the major control settings for arithmetic, load, store and branch instructions and trace how a condition changes the Program Counter."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 06 COMPLETE", color_scheme="green"),
                    rx.heading("Control and datapath now cooperate to execute branches.", size="5"),
                    rx.text("Next: divide instruction execution into overlapping pipeline stages.", color="#475569"),
                    rx.link(
                        rx.button("Next · Pipeline Fundamentals", color_scheme="teal"),
                        href="/academy/unit-9/pipeline-fundamentals",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def pipeline_fundamentals_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 07", color_scheme="teal", width="100%"),
            rx.heading("Pipeline Fundamentals", size="8"),
            rx.text(
                "Pipelining improves CPU throughput by dividing instruction execution into stages and overlapping several instructions in time. It does not make one instruction magically require less work; it allows different parts of the processor to work on different instructions at the same time."
            ),
            _section(
                "1", "Why processors use pipelining",
                rx.text(
                    "The single-cycle datapath waits for an entire instruction path to finish before beginning the next instruction. A pipeline inserts storage boundaries between useful portions of that path so the next instruction can begin before the previous one has fully completed."
                ),
                rx.code_block(
                    "single cycle:  [ instruction A: all work ] [ instruction B: all work ]\n\n"
                    "pipeline:      [A1][A2][A3][A4][A5]\n"
                    "                  [B1][B2][B3][B4][B5]\n"
                    "                     [C1][C2][C3][C4][C5]",
                    language="textile", width="100%",
                ),
                _practice(
                    "What technique overlaps the execution of several instructions by dividing work into stages?",
                    CpuPathState.pipeline_answer, CpuPathState.set_pipeline_answer, CpuPathState.check_pipeline,
                    CpuPathState.pipeline_feedback, "technique",
                ),
            ),
            _section(
                "2", "The classic five-stage instruction pipeline",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Stage"), rx.table.column_header_cell("Name"), rx.table.column_header_cell("Main work")
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("IF"), rx.table.cell("Instruction Fetch"), rx.table.cell("Use PC to read the instruction and form the next sequential PC")),
                        rx.table.row(rx.table.cell("ID"), rx.table.cell("Instruction Decode / Register Read"), rx.table.cell("Decode fields and read source registers")),
                        rx.table.row(rx.table.cell("EX"), rx.table.cell("Execute"), rx.table.cell("Perform ALU work, address calculation or branch comparison")),
                        rx.table.row(rx.table.cell("MEM"), rx.table.cell("Memory"), rx.table.cell("Read or write data memory when required")),
                        rx.table.row(rx.table.cell("WB"), rx.table.cell("Write Back"), rx.table.cell("Commit a selected result to the register file")),
                    ), width="100%",
                ),
                _practice(
                    "Which pipeline stage fetches the instruction using the Program Counter?",
                    CpuPathState.stage_answer, CpuPathState.set_stage_answer, CpuPathState.check_stage,
                    CpuPathState.stage_feedback, "stage",
                ),
            ),
            _section(
                "3", "Pipeline registers separate the stages",
                rx.text(
                    "Values produced by one stage must survive until the following stage uses them. Pipeline registers capture those values at the clock edge. They also carry instruction-specific control information so later stages know what action belongs to each instruction."
                ),
                rx.code_block(
                    "PC → IF → [IF/ID] → ID → [ID/EX] → EX → [EX/MEM] → MEM → [MEM/WB] → WB\n"
                    "             ↑             ↑              ↑                ↑\n"
                    "        stage values  operands/control  result/control   data/control",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "A pipeline register is not merely a delay: it preserves the exact data and control state required by the instruction advancing to the next stage.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "4", "Several instructions occupy the processor together",
                rx.text(
                    "After the pipeline begins filling, each clock edge advances every in-flight instruction by one stage. At a particular moment, one instruction may be writing back while a newer one accesses memory, another uses the ALU, another decodes, and another is fetched."
                ),
                rx.code_block(
                    "Cycle        1    2    3    4    5    6    7\n"
                    "Instruction A IF   ID   EX   MEM  WB\n"
                    "Instruction B      IF   ID   EX   MEM  WB\n"
                    "Instruction C           IF   ID   EX   MEM  WB",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Latency and throughput are different",
                rx.text(
                    "Latency is the time from the start of one instruction until that instruction completes. Throughput is the rate at which completed instructions emerge. A five-stage pipeline may still require roughly five stage intervals for one instruction, but after filling it can ideally complete one instruction every cycle."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Quantity"), rx.table.column_header_cell("Meaning"), rx.table.column_header_cell("Pipeline effect"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Latency"), rx.table.cell("Time for one instruction"), rx.table.cell("Not necessarily reduced by the stage count")),
                        rx.table.row(rx.table.cell("Throughput"), rx.table.cell("Instructions completed per unit time"), rx.table.cell("Can improve greatly after the pipeline fills")),
                    ), width="100%",
                ),
                _practice(
                    "In an ideal filled pipeline, approximately how many instructions can complete per clock cycle?",
                    CpuPathState.throughput_answer, CpuPathState.set_throughput_answer, CpuPathState.check_throughput,
                    CpuPathState.throughput_feedback, "for example: one",
                ),
            ),
            _section(
                "6", "The pipeline must first fill and finally drain",
                rx.text(
                    "The first instruction cannot complete until it has traversed all stages, so the first few cycles fill the pipeline. When instruction supply stops, the remaining in-flight instructions continue advancing until the pipeline drains."
                ),
                rx.code_block(
                    "fill → steady state → drain\n"
                    " 1       many          last few cycles\n\n"
                    "For k stages and n independent instructions, an ideal pipeline needs about k + n - 1 cycles.",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Stage balance determines the clock period",
                rx.text(
                    "The pipeline clock must be long enough for the slowest stage plus pipeline-register overhead. If one stage takes much longer than the others, the faster stages wait every cycle and much of the theoretical speedup is lost."
                ),
                rx.code_block(
                    "stage delays: IF=2 ns, ID=2 ns, EX=3 ns, MEM=2 ns, WB=1 ns\n"
                    "idealized pipeline clock ≥ 3 ns + register overhead",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Good pipeline design tries to divide the work into reasonably balanced stages rather than merely creating more stages.",
                    icon="clock", color_scheme="orange",
                ),
            ),
            _section(
                "8", "Ideal speedup has limits",
                rx.text(
                    "If k perfectly balanced stages replace one long datapath and a large stream of independent instructions is available, throughput can approach k times the unpipelined rate. Real processors fall short because stage delays differ, pipeline registers add overhead, and instructions sometimes interfere with one another."
                ),
                rx.code_block(
                    "ideal long-stream speedup ≈ unpipelined cycle time / pipelined cycle time\n"
                    "upper intuition for k equal stages: speedup approaches k",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Why perfect overlap is not always possible",
                rx.text(
                    "Instructions are not always independent. Two instructions may need the same hardware, one may depend on a result that an earlier instruction has not produced yet, or a branch may make the correct next instruction unknown. These situations are called pipeline hazards."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Hazard family"), rx.table.column_header_cell("Core problem"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Structural"), rx.table.cell("Two stages need the same resource at the same time")),
                        rx.table.row(rx.table.cell("Data"), rx.table.cell("An instruction needs a value that is not ready yet")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("The correct next instruction depends on unresolved control flow")),
                    ), width="100%",
                ),
            ),
            _section(
                "10", "Trace a three-instruction pipeline",
                rx.code_block(
                    "I1: ADD R3, R1, R2\n"
                    "I2: AND R6, R4, R5\n"
                    "I3: OR  R9, R7, R8\n\n"
                    "Cycle 1: I1=IF\n"
                    "Cycle 2: I1=ID,  I2=IF\n"
                    "Cycle 3: I1=EX,  I2=ID,  I3=IF\n"
                    "Cycle 4: I1=MEM, I2=EX,  I3=ID\n"
                    "Cycle 5: I1=WB,  I2=MEM, I3=EX",
                    language="textile", width="100%",
                ),
                rx.text(
                    "Because these example instructions are independent, the schedule shows the ideal overlap. Later lessons will examine what changes when dependencies or branches appear."
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.hstack(
                    rx.badge("IF", color_scheme="blue"), rx.text("→ fetch"),
                    rx.badge("ID", color_scheme="cyan"), rx.text("→ decode/read"),
                    rx.badge("EX", color_scheme="purple"), rx.text("→ execute"),
                    rx.badge("MEM", color_scheme="orange"), rx.text("→ memory"),
                    rx.badge("WB", color_scheme="green"), rx.text("→ write back"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now explain why pipelining improves throughput, identify the classic five stages and their pipeline registers, and distinguish ideal overlap from the hazards that disturb it."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 07 COMPLETE", color_scheme="green"),
                    rx.heading("The CPU can now overlap multiple instructions in a pipeline.", size="5"),
                    rx.text("Next: identify structural, data and control hazards and learn how a processor keeps the pipeline correct.", color="#475569"),
                    rx.link(
                        rx.button("Next · Pipeline Hazards", color_scheme="teal"),
                        href="/academy/unit-9/pipeline-hazards",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def pipeline_hazards_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 09 · LESSON 08", color_scheme="teal", width="100%"),
            rx.heading("Pipeline Hazards", size="8"),
            rx.text(
                "Pipelining improves instruction throughput only when overlapping instructions remain correct. Hazards are situations in which the next pipeline action cannot safely proceed as if every instruction were independent. This lesson identifies the three hazard families and shows the core hardware techniques used to resolve them.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A hazard is a threat to correct pipeline overlap",
                rx.text(
                    "A hazard does not automatically mean the processor has produced a wrong answer. It means the normal next-cycle advance would be unsafe unless the hardware delays, redirects or supplies additional information to the affected instruction."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Hazard"), rx.table.column_header_cell("Why it happens"), rx.table.column_header_cell("Typical response"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Structural"), rx.table.cell("Two stages request one resource at the same time"), rx.table.cell("Duplicate/schedule resource or stall")),
                        rx.table.row(rx.table.cell("Data"), rx.table.cell("An operand depends on an earlier in-flight result"), rx.table.cell("Forward, stall, or both")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("The correct next PC is not yet known"), rx.table.cell("Predict/redirect and flush if required")),
                    ), width="100%",
                ),
            ),
            _section(
                "2", "Structural hazards are resource conflicts",
                rx.text(
                    "A structural hazard appears when the datapath cannot support all simultaneous stage requests. For example, if instruction fetch and a load both require one single-ported memory in the same cycle, one request must wait."
                ),
                rx.code_block(
                    "same cycle:\n"
                    "I1 in MEM  ── needs memory ──┐\n"
                    "I2 in IF   ── needs memory ──┴─ conflict if only one port exists\n\n"
                    "common design response: separate instruction/data memories or add sufficient ports",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "A structural hazard is caused by insufficient hardware availability, not by a value dependency between the instructions.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "3", "RAW is the key data hazard in an in-order five-stage pipeline",
                rx.text(
                    "Read After Write (RAW) means a younger instruction wants to read a register that an older instruction will write. The architectural ordering requires the younger instruction to see the new value, not the old register-file contents."
                ),
                rx.code_block(
                    "I1: ADD R3, R1, R2     # produces R3\n"
                    "I2: SUB R5, R3, R4     # consumes new R3\n\n"
                    "I2 reaches EX before I1 would normally write R3 in WB → RAW dependency",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which dependency occurs when a younger instruction needs a value that an older instruction has not made available yet?",
                    CpuPathState.hazard_answer, CpuPathState.set_hazard_answer, CpuPathState.check_hazard,
                    CpuPathState.hazard_feedback, "hazard type",
                ),
            ),
            _section(
                "4", "Forwarding bypasses unnecessary waiting",
                rx.text(
                    "An ALU result often exists before it reaches the WB stage. Forwarding logic compares destination and source register numbers, then selects a newer result directly from a later pipeline register as an ALU input for the dependent instruction."
                ),
                rx.code_block(
                    "I1 result: EX ──→ [EX/MEM] ─────────────┐\n"
                    "                                      ▼\n"
                    "I2 operand: ID ──→ [ID/EX] ──→ input MUX ──→ EX\n"
                    "                               ▲\n"
                    "                         forwarding select",
                    language="textile", width="100%",
                ),
                _practice(
                    "What technique sends a newly produced value directly to a dependent stage instead of waiting for register-file write-back?",
                    CpuPathState.forwarding_answer, CpuPathState.set_forwarding_answer, CpuPathState.check_forwarding,
                    CpuPathState.forwarding_feedback, "technique",
                ),
            ),
            _section(
                "5", "A load-use dependency may still require a stall",
                rx.text(
                    "Forwarding cannot deliver a value before that value physically exists. In the classic five-stage pipeline, load data is returned near the end of MEM. An immediately following instruction normally needs its ALU operand at the start of EX, so one bubble is commonly inserted."
                ),
                rx.code_block(
                    "I1: LOAD R3, 0(R1)\n"
                    "I2: ADD  R5, R3, R4\n\n"
                    "Cycle:  1    2    3      4      5    6    7\n"
                    "I1      IF   ID   EX     MEM    WB\n"
                    "I2           IF   ID    STALL   EX   MEM  WB\n"
                    "                         ↑ one bubble lets load data become forwardable",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "A stall freezes the appropriate earlier pipeline state and injects a no-operation bubble so the dependent instruction executes only when its input can be supplied correctly.",
                    icon="pause", color_scheme="blue",
                ),
            ),
            _section(
                "6", "Hazard detection decides when the pipeline must wait",
                rx.text(
                    "A hazard-detection unit inspects register identifiers and control information carried by nearby pipeline stages. For a classic load-use case it detects that the instruction in EX is a load and that its destination matches a source needed by the instruction in ID."
                ),
                rx.code_block(
                    "if ID/EX.MemRead = 1\n"
                    "and ID/EX.destination matches IF/ID.source\n"
                    "then: hold PC, hold IF/ID, inject bubble into ID/EX",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Control hazards come from branches and jumps",
                rx.text(
                    "The fetch stage wants a next PC every cycle, but a conditional branch may not yet have determined whether execution continues sequentially or redirects to a target. Instructions fetched along the wrong path must never be allowed to change architectural state."
                ),
                rx.code_block(
                    "fetch assumes PC + 1 ──→ I2 ──→ I3 ...\n"
                    "              branch resolves TAKEN\n"
                    "                       └──→ target T\n\n"
                    "wrong-path I2/I3 must be discarded before they commit state",
                    language="textile", width="100%",
                ),
                _practice(
                    "What hazard occurs when a branch or jump leaves the correct next PC temporarily unknown?",
                    CpuPathState.controlhazard_answer, CpuPathState.set_controlhazard_answer, CpuPathState.check_controlhazard,
                    CpuPathState.controlhazard_feedback, "hazard family",
                ),
            ),
            _section(
                "8", "Flush and prediction protect control-flow correctness",
                rx.text(
                    "A simple processor can wait until a branch is resolved, but that wastes cycles. A more aggressive pipeline predicts a direction or target and keeps fetching. If the prediction is wrong, the PC is redirected and younger wrong-path instructions are flushed from the pipeline."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Technique"), rx.table.column_header_cell("Effect"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Stall until resolution"), rx.table.cell("Simple and correct, but loses fetch cycles")),
                        rx.table.row(rx.table.cell("Predict not taken / static prediction"), rx.table.cell("Continues fetch using a fixed rule")),
                        rx.table.row(rx.table.cell("Dynamic prediction"), rx.table.cell("Uses execution history to choose a likely path")),
                        rx.table.row(rx.table.cell("Flush"), rx.table.cell("Invalidates younger wrong-path instructions after a misprediction")),
                    ), width="100%",
                ),
            ),
            _section(
                "9", "Forwarding, stalling and flushing solve different problems",
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Mechanism"), rx.table.column_header_cell("What it changes"), rx.table.column_header_cell("Typical use"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Forward"), rx.table.cell("Operand source"), rx.table.cell("ALU-to-ALU RAW dependency")),
                        rx.table.row(rx.table.cell("Stall"), rx.table.cell("Instruction timing"), rx.table.cell("Value/resource not ready")),
                        rx.table.row(rx.table.cell("Flush"), rx.table.cell("Instruction validity"), rx.table.cell("Wrong-path control-flow instructions")),
                    ), width="100%",
                ),
                rx.text(
                    "These mechanisms can work together. A real pipeline continually decides whether each stage advances normally, receives forwarded data, waits, or discards invalid work."
                ),
            ),
            _section(
                "10", "Trace a dependent sequence",
                rx.code_block(
                    "I1: ADD  R3, R1, R2\n"
                    "I2: SUB  R6, R3, R5       # RAW: forward ADD result to I2 EX\n"
                    "I3: LOAD R7, 0(R6)        # R6 can also be forwarded\n"
                    "I4: AND  R8, R7, R9       # load-use: one stall, then forward load data\n"
                    "I5: BEQ  R8, R0, target   # control decision may redirect PC\n\n"
                    "Correct execution requires data availability AND correct-path instruction selection.",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Path 09 checkpoint",
                rx.hstack(
                    rx.badge("Structural", color_scheme="orange"), rx.text("→ resource conflict"),
                    rx.badge("Data", color_scheme="blue"), rx.text("→ operand dependency"),
                    rx.badge("Control", color_scheme="purple"), rx.text("→ next-PC uncertainty"),
                    wrap="wrap", spacing="2",
                ),
                rx.text(
                    "You can now connect CPU architecture, instruction execution, register transfer, control, single-cycle datapaths and pipelining into one processor model, then explain how forwarding, stalls and flushes preserve correctness when instructions overlap."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("PATH 09 COMPLETE", color_scheme="green"),
                    rx.heading("Processor Architecture & CPU Datapath is complete.", size="5"),
                    rx.text(
                        "You have progressed from the basic CPU blocks to a pipelined processor that detects and resolves the hazards created by overlapping instructions.",
                        color="#475569",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )
