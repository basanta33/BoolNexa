"""BoolNexa Academy Path 08 — Computer Arithmetic & ALU Design."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class AluPathState(rx.State):
    add_answer:str=""; add_feedback:str=""
    subtract_answer:str=""; subtract_feedback:str=""
    carry_answer:str=""; carry_feedback:str=""
    overflow_answer:str=""; overflow_feedback:str=""
    zero_flag_answer:str=""; zero_flag_feedback:str=""
    negative_flag_answer:str=""; negative_flag_feedback:str=""
    ripple_delay_answer:str=""; ripple_delay_feedback:str=""
    cla_answer:str=""; cla_feedback:str=""
    prefix_answer:str=""; prefix_feedback:str=""
    datapath_answer:str=""; datapath_feedback:str=""
    increment_answer:str=""; increment_feedback:str=""
    transfer_answer:str=""; transfer_feedback:str=""
    bitwise_answer:str=""; bitwise_feedback:str=""
    xor_answer:str=""; xor_feedback:str=""
    logic_select_answer:str=""; logic_select_feedback:str=""
    opcode_answer:str=""; opcode_feedback:str=""
    control_width_answer:str=""; control_width_feedback:str=""
    illegal_code_answer:str=""; illegal_code_feedback:str=""
    equality_answer:str=""; equality_feedback:str=""
    signed_compare_answer:str=""; signed_compare_feedback:str=""
    unsigned_compare_answer:str=""; unsigned_compare_feedback:str=""
    capstone_control_answer:str=""; capstone_control_feedback:str=""
    capstone_flag_answer:str=""; capstone_flag_feedback:str=""
    capstone_verify_answer:str=""; capstone_verify_feedback:str=""
    def set_add_answer(self,value:str)->None:self.add_answer=value
    def set_subtract_answer(self,value:str)->None:self.subtract_answer=value
    def set_carry_answer(self,value:str)->None:self.carry_answer=value
    def set_overflow_answer(self,value:str)->None:self.overflow_answer=value
    def set_zero_flag_answer(self,value:str)->None:self.zero_flag_answer=value
    def set_negative_flag_answer(self,value:str)->None:self.negative_flag_answer=value
    def set_ripple_delay_answer(self,value:str)->None:self.ripple_delay_answer=value
    def set_cla_answer(self,value:str)->None:self.cla_answer=value
    def set_prefix_answer(self,value:str)->None:self.prefix_answer=value
    def set_datapath_answer(self,value:str)->None:self.datapath_answer=value
    def set_increment_answer(self,value:str)->None:self.increment_answer=value
    def set_transfer_answer(self,value:str)->None:self.transfer_answer=value
    def set_bitwise_answer(self,value:str)->None:self.bitwise_answer=value
    def set_xor_answer(self,value:str)->None:self.xor_answer=value
    def set_logic_select_answer(self,value:str)->None:self.logic_select_answer=value
    def set_opcode_answer(self,value:str)->None:self.opcode_answer=value
    def set_control_width_answer(self,value:str)->None:self.control_width_answer=value
    def set_illegal_code_answer(self,value:str)->None:self.illegal_code_answer=value
    def set_equality_answer(self,value:str)->None:self.equality_answer=value
    def set_signed_compare_answer(self,value:str)->None:self.signed_compare_answer=value
    def set_unsigned_compare_answer(self,value:str)->None:self.unsigned_compare_answer=value
    def set_capstone_control_answer(self,value:str)->None:self.capstone_control_answer=value
    def set_capstone_flag_answer(self,value:str)->None:self.capstone_flag_answer=value
    def set_capstone_verify_answer(self,value:str)->None:self.capstone_verify_answer=value
    def check_add(self)->None:
        v=self.add_answer.strip().lower().replace(" ","")
        self.add_feedback="Correct. 1011₂ + 0110₂ = 10001₂." if v in {"10001","10001₂","17"} else "Add from the least-significant bit and carry into the next column when a column total reaches 2."
    def check_subtract(self)->None:
        v=self.subtract_answer.strip().lower().replace(" ","").replace("-","")
        self.subtract_feedback="Correct. In fixed-width hardware, A − B can be performed as A + two's-complement(B)." if v in {"twoscomplement","2scomplement","two'scomplement","complement"} else "Which signed-binary representation lets an adder perform subtraction by complementing B and adding one?"
    def check_carry(self)->None:
        v=self.carry_answer.strip().lower().replace(" ","")
        self.carry_feedback="Correct. The carry-out is 1 because the 4-bit sum exceeds 1111₂." if v in {"1","one","high"} else "1011₂ + 0110₂ is 10001₂. What bit lies beyond the four-bit result field?"
    def check_overflow(self)->None:
        v=self.overflow_answer.strip().lower().replace(" ","").replace("-","")
        self.overflow_feedback=("Correct. In 4-bit two's-complement, 7 + 3 cannot be represented because the valid range is −8 to +7, so signed overflow occurs." if v in {"1","yes","true","overflow","occurs"} else "Both operands are positive, but the 4-bit result appears negative. What signed arithmetic condition does that indicate?")
    def check_zero_flag(self)->None:
        v=self.zero_flag_answer.strip().lower().replace(" ","").replace("-","")
        self.zero_flag_feedback=("Correct. The Zero flag is asserted when every result bit is 0." if v in {"1","yes","true","set","asserted"} else "If the ALU result word is 0000, should the Zero flag be asserted?")
    def check_negative_flag(self)->None:
        v=self.negative_flag_answer.strip().lower().replace(" ","").replace("-","")
        self.negative_flag_feedback=("Correct. In two's-complement arithmetic, the most-significant result bit is the sign bit, so N follows the MSB." if v in {"msb","mostsignificantbit","signbit","resultmsb"} else "Which result bit normally drives the Negative flag in two's-complement arithmetic?")
    def check_ripple_delay(self)->None:
        v=self.ripple_delay_answer.strip().lower().replace(" ","").replace("-","")
        self.ripple_delay_feedback=(
            "Correct. In a ripple-carry adder, each stage may wait for the previous stage's carry, so worst-case delay grows roughly with word width."
            if v in {"carry","carrypropagation","ripplecarry","carrychain"}
            else "Which signal must move through successive full-adder stages before the most-significant sum can settle?"
        )
    def check_cla(self)->None:
        v=self.cla_answer.strip().lower().replace(" ","").replace("-","")
        self.cla_feedback=(
            "Correct. Carry-lookahead logic forms generate and propagate terms so carries can be predicted in parallel rather than waiting for a full ripple."
            if v in {"generateandpropagate","generatepropagate","gandp","gp","lookahead"}
            else "Which two per-bit concepts are combined to predict carries in a carry-lookahead adder?"
        )
    def check_prefix(self)->None:
        v=self.prefix_answer.strip().lower().replace(" ","").replace("-","")
        self.prefix_feedback=(
            "Correct. Parallel-prefix adders organize carry computation as a tree, reducing logic depth compared with a long serial carry chain."
            if v in {"tree","prefix","paralleltree","logarithmic","logarithmictree"}
            else "What structural idea lets parallel-prefix adders combine carry information over groups in only a few logic levels?"
        )
    def check_datapath(self)->None:
        v=self.datapath_answer.strip().lower().replace(" ","").replace("-","")
        self.datapath_feedback=("Correct. A multiplexer selects which source or transformed operand reaches the shared arithmetic hardware." if v in {"mux","multiplexer","selector"} else "Which combinational component selects one of several candidate operand paths?")
    def check_increment(self)->None:
        v=self.increment_answer.strip().lower().replace(" ","")
        self.increment_feedback=("Correct. Incrementing A is simply A + 1." if v in {"1","one","+1"} else "What constant must be added to A to increment it?")
    def check_transfer(self)->None:
        v=self.transfer_answer.strip().lower().replace(" ","").replace("-","")
        self.transfer_feedback=("Correct. A transfer operation passes an operand to the result without changing its value." if v in {"unchanged","same","pass","passthrough","transfer"} else "Does a transfer operation numerically modify the selected operand?")
    def check_bitwise(self)->None:
        v=self.bitwise_answer.strip().lower().replace(" ","").replace("_","")
        self.bitwise_feedback=("Correct. 1010 AND 1100 = 1000 because AND is applied independently to each bit position." if v in {"1000","1000₂"} else "Apply AND independently to each aligned pair of bits.")
    def check_xor(self)->None:
        v=self.xor_answer.strip().lower().replace(" ","").replace("_","")
        self.xor_feedback=("Correct. 1010 XOR 1100 = 0110." if v in {"0110","110","0110₂"} else "XOR is 1 where the two aligned input bits differ.")
    def check_logic_select(self)->None:
        v=self.logic_select_answer.strip().lower().replace(" ","").replace("-","")
        self.logic_select_feedback=("Correct. A multiplexer can select which precomputed logic function reaches the ALU output." if v in {"mux","multiplexer","selector"} else "Which component selects one result from several simultaneously computed logic functions?")
    def check_opcode(self)->None:
        v=self.opcode_answer.strip().lower().replace(" ","").replace("-","")
        self.opcode_feedback=("Correct. An operation code (opcode / ALU control code) tells the ALU which function to perform." if v in {"opcode","operationcode","alucontrol","controlcode"} else "What encoded field tells the ALU which operation to perform?")
    def check_control_width(self)->None:
        v=self.control_width_answer.strip().lower().replace(" ","")
        self.control_width_feedback=("Correct. Three control bits provide 2³ = 8 distinct binary codes." if v in {"3","three","3bits","3bit"} else "How many binary control bits are required to encode up to eight unique operations?")
    def check_illegal_code(self)->None:
        v=self.illegal_code_answer.strip().lower().replace(" ","").replace("-","")
        self.illegal_code_feedback=("Correct. Unused or illegal control codes should have documented deterministic behaviour rather than an accidental result." if v in {"defined","deterministic","safe","documented","trap","reserved"} else "Should an unused ALU control code have undefined accidental behaviour, or a specified safe behaviour?")
    def check_equality(self)->None:
        v=self.equality_answer.strip().lower().replace(" ","").replace("-","")
        self.equality_feedback=("Correct. Subtracting equal operands produces zero, so Z = 1 can indicate equality." if v in {"z","zero","zeroflag","zflag","1"} else "Which status flag becomes asserted when A − B produces 0?")
    def check_signed_compare(self)->None:
        v=self.signed_compare_answer.strip().lower().replace(" ","").replace("-","").replace("xor","^")
        self.signed_compare_feedback=("Correct. Signed less-than can be derived from N XOR V after A − B." if v in {"n^v","nv","n⊕v","negative^overflow","negativeoverflow"} else "For signed A < B after subtraction, which combination of N and V corrects the sign when overflow occurs?")
    def check_unsigned_compare(self)->None:
        v=self.unsigned_compare_answer.strip().lower().replace(" ","").replace("-","")
        self.unsigned_compare_feedback=("Correct. With the no-borrow carry convention, A < B unsigned is indicated when C = 0 after A − B." if v in {"c=0","c0","0","carry0","nocarry"} else "Using the lesson's no-borrow carry convention, what value of C indicates A < B after A − B?")
    def check_capstone_control(self)->None:
        v=self.capstone_control_answer.strip().lower().replace(" ","").replace("-","")
        self.capstone_control_feedback=("Correct. The control decoder translates ALU control bits into internal select signals." if v in {"decoder","controldecoder","controlunit","aludecoder"} else "Which block converts the encoded ALU control field into internal selection signals?")
    def check_capstone_flag(self)->None:
        v=self.capstone_flag_answer.strip().lower().replace(" ","").replace("-","")
        self.capstone_flag_feedback=("Correct. Z is asserted whenever every bit of the selected ALU result is zero." if v in {"z","zero","zeroflag","zflag"} else "Which flag must reflect an all-zero selected ALU result?")
    def check_capstone_verify(self)->None:
        v=self.capstone_verify_answer.strip().lower().replace(" ","").replace("-","")
        self.capstone_verify_feedback=("Correct. A complete ALU should be verified with a structured control/operation table and representative test vectors." if v in {"truthtable","testvectors","verificationtable","controltable","testbench","testcases"} else "Name a structured verification method for checking ALU operations and flags.")

def _section(n:str,title:str,*items:rx.Component)->rx.Component:
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,radius="full",color_scheme="indigo"),rx.heading(title,size="5"),align="center"),*items,spacing="4",align="stretch"),**PANEL)

def _practice(prompt:str,value:rx.Var,setter,checker,feedback:rx.Var,placeholder:str)->rx.Component:
    return rx.box(rx.vstack(rx.text(prompt,font_weight="700"),rx.hstack(rx.input(value=value,on_change=setter,placeholder=placeholder,width="100%"),rx.button("Check",on_click=checker,color_scheme="indigo"),width="100%"),rx.cond(feedback!="",rx.callout(feedback,icon="lightbulb",size="1"),rx.fragment()),spacing="3",align="stretch"),padding="16px",border="1px solid #c7d2fe",border_radius="12px",background="#eef2ff",width="100%")

def binary_addition_subtraction_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 01",color_scheme="indigo"),
            rx.heading("Binary Addition, Subtraction & Arithmetic Hardware",size="8"),
            rx.text("Computer arithmetic begins with familiar binary rules, but now we examine how real digital hardware performs those operations using adders, carry paths and two's-complement subtraction.",size="4",color="#475569",line_height="1.6"),
            _section("1","Binary addition as a hardware operation",
                rx.text("Each bit position combines operand bits and, except at the least-significant stage, a carry from the previous position. A full adder therefore accepts A, B and Cin and produces Sum and Cout."),
                rx.code_block("0 + 0 = 0\n0 + 1 = 1\n1 + 0 = 1\n1 + 1 = 10₂\n1 + 1 + 1 = 11₂",language="textile",width="100%"),
                rx.callout("For an n-bit ripple adder, one full-adder stage is used per bit. Carry-out from a lower stage becomes carry-in to the next stage.",icon="cpu")),
            _section("2","Worked 4-bit example",
                rx.code_block("   1011   (11)\n + 0110   ( 6)\n -------\n  10001   (17)",language="textile",width="100%"),
                rx.text("A four-bit datapath keeps the low four result bits (0001) and exposes the extra most-significant bit as carry-out. Whether that carry means overflow depends on whether the operands are interpreted as unsigned or signed."),
                _practice("Calculate 1011₂ + 0110₂.",AluPathState.add_answer,AluPathState.set_add_answer,AluPathState.check_add,AluPathState.add_feedback,"Binary result")),
            _section("3","Subtraction with the same adder",
                rx.text("Digital systems normally avoid a completely separate subtractor. For fixed-width two's-complement arithmetic, A − B is formed as A + (~B) + 1. An XOR-controlled B input and the adder carry-in can therefore switch one arithmetic datapath between ADD and SUBTRACT."),
                rx.code_block("ADD mode:  B passes unchanged, Cin = 0\nSUB mode:  B is complemented, Cin = 1\nResult:    A + B        or        A + (~B) + 1",language="textile",width="100%"),
                _practice("What representation makes A − B possible by adding the complemented B plus 1?",AluPathState.subtract_answer,AluPathState.set_subtract_answer,AluPathState.check_subtract,AluPathState.subtract_feedback,"Representation")),
            _section("4","Carry-out is not signed overflow",
                rx.text("Carry-out is essential for unsigned arithmetic and multiword addition. Signed two's-complement overflow is a different condition: it occurs when the mathematical signed result cannot be represented in the available width. Path 08 Lesson 2 will examine carry, borrow and overflow flags in detail."),
                _practice("For 4-bit 1011₂ + 0110₂, what is Cout?",AluPathState.carry_answer,AluPathState.set_carry_answer,AluPathState.check_carry,AluPathState.carry_feedback,"0 or 1")),
            _section("5","From arithmetic to an ALU",
                rx.text("An arithmetic logic unit combines arithmetic operations with logic operations such as AND, OR and XOR. Control bits select which operation reaches the output. During Path 08 we will progressively build the ideas needed for a complete ALU."),
                rx.hstack(rx.badge("Operands A, B",color_scheme="blue"),rx.text("→"),rx.badge("Arithmetic / Logic blocks",color_scheme="indigo"),rx.text("→"),rx.badge("Operation selector",color_scheme="purple"),rx.text("→"),rx.badge("Result + flags",color_scheme="green"),wrap="wrap",spacing="2")),
            rx.card(rx.vstack(rx.badge("LESSON 01 COMPLETE",color_scheme="green"),rx.heading("You now have the arithmetic foundation for an ALU.",size="5"),rx.text("Next: carry, borrow, signed overflow and processor status flags.",color="#475569"),rx.link(rx.button("Next · Carry, Overflow & Status Flags",color_scheme="indigo"),href="/academy/unit-8/carry-overflow-flags",text_decoration="none"),spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def carry_overflow_status_flags_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 02",color_scheme="indigo"),
            rx.heading("Carry, Overflow & Status Flags",size="8"),
            rx.text("Arithmetic hardware also produces status information describing the result: unsigned carry, signed overflow, zero and negative state.",size="4",color="#475569",line_height="1.6"),
            _section("1","Carry flag for unsigned arithmetic",
                rx.text("For unsigned addition, Cout from the most-significant stage indicates that the mathematical sum exceeded the available word width. Processors commonly copy this event into a Carry flag C."),
                rx.code_block("4-bit unsigned example\n1111₂ + 0001₂ = 1 0000₂\nstored result = 0000₂\nCarry C = 1",language="textile",width="100%"),
                rx.callout("Carry is essential for multiword arithmetic because one word's carry can feed the next word.",icon="cpu")),
            _section("2","Signed overflow is different",
                rx.text("Two's-complement signed overflow is not the same as carry-out. Overflow V occurs when the true signed result lies outside the representable range. A common hardware test is that the carry into the sign bit differs from the carry out of the sign bit."),
                rx.code_block("4-bit signed range: −8 … +7\n0111₂ (+7)\n+0011₂ (+3)\n-----------\n1010₂ (looks like −6)\nV = 1",language="textile",width="100%"),
                _practice("For 4-bit signed 0111₂ + 0011₂, does overflow occur?",AluPathState.overflow_answer,AluPathState.set_overflow_answer,AluPathState.check_overflow,AluPathState.overflow_feedback,"yes / no")),
            _section("3","Zero and Negative flags",
                rx.text("The Zero flag Z is asserted when every result bit is 0. The Negative flag N normally copies the most-significant result bit when the result is interpreted as two's-complement."),
                rx.code_block("Result = 0000₂  →  Z = 1\nResult = 0101₂  →  Z = 0, N = 0\nResult = 1011₂  →  Z = 0, N = 1",language="textile",width="100%"),
                _practice("If the ALU result is 0000₂, should Z be asserted?",AluPathState.zero_flag_answer,AluPathState.set_zero_flag_answer,AluPathState.check_zero_flag,AluPathState.zero_flag_feedback,"yes / no"),
                _practice("Which result bit normally drives N?",AluPathState.negative_flag_answer,AluPathState.set_negative_flag_answer,AluPathState.check_negative_flag,AluPathState.negative_flag_feedback,"bit name")),
            _section("4","Borrow and subtraction",
                rx.text("Subtraction flag conventions differ by architecture. Some processors define C after subtraction as no-borrow, while others expose borrow differently."),
                rx.callout("Engineering rule: document whether C means carry, no-borrow or borrow after subtraction.",icon="triangle-alert")),
            _section("5","Status register concept",
                rx.text("Flags are often collected into a status or condition-code register so branches and later instructions can test the previous arithmetic result."),
                rx.code_block("C = Carry / architecture-defined subtraction carry\nV = Signed overflow\nZ = Result is zero\nN = Result sign bit",language="textile",width="100%"),
                rx.hstack(rx.badge("C",color_scheme="blue"),rx.badge("V",color_scheme="red"),rx.badge("Z",color_scheme="green"),rx.badge("N",color_scheme="purple"),spacing="2")),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 02 COMPLETE",color_scheme="green"),
                    rx.heading("You can now distinguish arithmetic results from status flags.",size="5"),
                    rx.text("Next: ripple carry versus faster adder architectures and the performance cost of carry propagation.",color="#475569"),
                    rx.link(rx.button("Next · Fast Adder Architectures",color_scheme="indigo"),href="/academy/unit-8/fast-adders",text_decoration="none"),
                    spacing="3",align="start"),
                width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def fast_adder_architectures_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 03",color_scheme="indigo"),
            rx.heading("Fast Adder Architectures",size="8"),
            rx.text(
                "Addition is simple logically but can become a timing bottleneck as word width grows. "
                "This lesson compares ripple-carry adders with faster carry-lookahead and parallel-prefix structures.",
                size="4",color="#475569",line_height="1.6"),
            _section("1","Why ripple carry becomes slow",
                rx.text(
                    "A ripple-carry adder chains full-adder stages. The sum at a high-order bit may depend on a carry "
                    "that must propagate through every lower stage first. For an n-bit adder, worst-case carry delay "
                    "therefore grows approximately with n."
                ),
                rx.code_block(
                    "bit 0 carry → bit 1 carry → bit 2 carry → bit 3 carry → ...\n"
                    "Simple hardware, but a long serial dependency chain.",
                    language="textile",width="100%"),
                _practice(
                    "What signal causes the main serial delay in a ripple-carry adder?",
                    AluPathState.ripple_delay_answer,
                    AluPathState.set_ripple_delay_answer,
                    AluPathState.check_ripple_delay,
                    AluPathState.ripple_delay_feedback,
                    "signal / mechanism")),
            _section("2","Generate and propagate",
                rx.text(
                    "Carry-lookahead starts by describing each bit with two local terms. Generate Gi means that bit "
                    "creates a carry regardless of Cin. Propagate Pi means an incoming carry will pass through that bit."
                ),
                rx.code_block(
                    "Gi = Ai · Bi\n"
                    "Pi = Ai ⊕ Bi\n"
                    "Ci+1 = Gi + Pi·Ci",
                    language="textile",width="100%"),
                rx.callout(
                    "The key advantage is that several carry equations can be expanded and evaluated in parallel.",
                    icon="zap"),
                _practice(
                    "Which two concepts are used by carry-lookahead logic?",
                    AluPathState.cla_answer,
                    AluPathState.set_cla_answer,
                    AluPathState.check_cla,
                    AluPathState.cla_feedback,
                    "two concepts")),
            _section("3","Carry-lookahead adder",
                rx.text(
                    "A carry-lookahead adder computes group carry conditions with extra logic. This reduces the number "
                    "of serial carry steps, trading additional gates and wiring for lower arithmetic latency."
                ),
                rx.code_block(
                    "C1 = G0 + P0·C0\n"
                    "C2 = G1 + P1·G0 + P1·P0·C0\n"
                    "C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0",
                    language="textile",width="100%"),
                rx.text(
                    "Large flat lookahead equations become expensive, so practical designs use grouped or hierarchical lookahead."
                )),
            _section("4","Parallel-prefix adders",
                rx.text(
                    "Parallel-prefix adders combine generate/propagate information using a tree of prefix cells. "
                    "Families such as Kogge–Stone and Brent–Kung differ in wiring density, fan-out, area and logic depth."
                ),
                rx.code_block(
                    "local G/P\n"
                    "   ↓\n"
                    "group pairs combined in parallel\n"
                    "   ↓\n"
                    "larger groups\n"
                    "   ↓\n"
                    "all carries become available",
                    language="textile",width="100%"),
                _practice(
                    "What structural idea gives parallel-prefix adders low carry depth?",
                    AluPathState.prefix_answer,
                    AluPathState.set_prefix_answer,
                    AluPathState.check_prefix,
                    AluPathState.prefix_feedback,
                    "structure")),
            _section("5","Architecture trade-offs",
                rx.text(
                    "There is no single best adder. Ripple carry is compact and easy to implement. Carry-lookahead "
                    "reduces delay with extra logic. Parallel-prefix designs can achieve very low depth but may consume "
                    "substantial wiring and area."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Architecture"),
                            rx.table.column_header_cell("Delay"),
                            rx.table.column_header_cell("Area / wiring"),
                            rx.table.column_header_cell("Typical role"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Ripple carry"),rx.table.cell("Higher"),rx.table.cell("Low"),rx.table.cell("Small / simple datapaths")),
                        rx.table.row(rx.table.cell("Carry lookahead"),rx.table.cell("Lower"),rx.table.cell("Moderate"),rx.table.cell("Medium-width fast arithmetic")),
                        rx.table.row(rx.table.cell("Parallel prefix"),rx.table.cell("Very low"),rx.table.cell("Higher"),rx.table.cell("High-performance ALUs")),
                    ),
                    width="100%")),
            _section("6","From fast addition to ALU timing",
                rx.text(
                    "In many ALUs, addition and subtraction share the same carry network, so improving the adder improves "
                    "both operations. The adder's delay often contributes strongly to the processor's arithmetic critical path."
                ),
                rx.callout(
                    "Design rule: choose the adder architecture by balancing timing target, silicon area, power and routing complexity.",
                    icon="gauge")),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 03 COMPLETE",color_scheme="green"),
                    rx.heading("You now understand why adder architecture matters for ALU performance.",size="5"),
                    rx.text(
                        "Next: organize add, subtract, increment, decrement and transfer operations inside an arithmetic datapath.",
                        color="#475569"),
                    rx.link(rx.button("Next · Arithmetic Operations & Datapaths",color_scheme="indigo"),href="/academy/unit-8/arithmetic-datapaths",text_decoration="none"),
                    spacing="3",align="start"),
                width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def arithmetic_operations_datapaths_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 04",color_scheme="indigo"),
            rx.heading("Arithmetic Operations & Datapaths",size="8"),
            rx.text("An ALU becomes useful when one arithmetic core can perform several operations. Multiplexers, operand conditioning and control signals let the same adder implement add, subtract, increment, decrement and transfer functions.",size="4",color="#475569",line_height="1.6"),
            _section("1","What is a datapath?",
                rx.text("A datapath is the hardware route through which operands and results move. It combines registers, buses, multiplexers, arithmetic blocks and control points."),
                rx.code_block("Register A ─┐\n            ├─ operand selection ─ arithmetic core ─ result bus\nRegister B ─┘",language="textile",width="100%"),
                _practice("Which component commonly selects one of several operand paths?",AluPathState.datapath_answer,AluPathState.set_datapath_answer,AluPathState.check_datapath,AluPathState.datapath_feedback,"component")),
            _section("2","Reusing one adder",
                rx.text("Instead of dedicating separate hardware to every arithmetic instruction, operand-selection logic changes what enters a shared adder."),
                rx.code_block("ADD:       A + B\nSUBTRACT:  A + (~B) + 1\nINCREMENT: A + 1\nDECREMENT: A + (−1)\nTRANSFER:  pass selected operand",language="textile",width="100%"),
                rx.callout("Hardware reuse reduces duplicated logic and makes the control word responsible for selecting the desired arithmetic function.",icon="cpu")),
            _section("3","Increment and decrement",
                rx.text("Incrementers and decrementers appear in program counters, stack pointers, address generators and loop-control hardware. A general ALU can usually perform these operations through its existing adder."),
                _practice("What constant is added to A to perform A + 1?",AluPathState.increment_answer,AluPathState.set_increment_answer,AluPathState.check_increment,AluPathState.increment_feedback,"constant")),
            _section("4","Operand conditioning",
                rx.text("Before an operand reaches the adder it may be passed unchanged, complemented, forced to zero or forced to one. A small selector network can therefore create many arithmetic behaviours from the same core."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Selected B path"),rx.table.column_header_cell("Cin"),rx.table.column_header_cell("Example result"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("B"),rx.table.cell("0"),rx.table.cell("A + B")),
                        rx.table.row(rx.table.cell("~B"),rx.table.cell("1"),rx.table.cell("A − B")),
                        rx.table.row(rx.table.cell("0"),rx.table.cell("1"),rx.table.cell("A + 1")),
                        rx.table.row(rx.table.cell("all 1s"),rx.table.cell("0"),rx.table.cell("A − 1")),
                    ),width="100%")),
            _section("5","Transfer operations",
                rx.text("A transfer function routes a selected operand to the result bus without changing its numeric value. This is useful for register moves and datapath routing even though no arithmetic transformation is required."),
                _practice("What happens numerically to an operand during a transfer operation?",AluPathState.transfer_answer,AluPathState.set_transfer_answer,AluPathState.check_transfer,AluPathState.transfer_feedback,"answer")),
            _section("6","Control word idea",
                rx.text("The datapath is controlled by encoded signals. Some bits choose the B transformation, another may choose Cin, and later ALU control bits will select between arithmetic and logic results."),
                rx.code_block("Control bits → operand MUX / conditioning → shared adder → arithmetic result\n                    ↑\n                 A and B",language="textile",width="100%"),
                rx.callout("Separating datapath from control is a fundamental digital-system design pattern.",icon="waypoints")),
            rx.card(rx.vstack(
                rx.badge("LESSON 04 COMPLETE",color_scheme="green"),
                rx.heading("You can now see how one arithmetic core supports many operations.",size="5"),
                rx.text("Next: add bitwise AND, OR, XOR and NOT functions and select between logic results.",color="#475569"),
                rx.link(rx.button("Next · Logic Operations & Function Selection",color_scheme="indigo"),href="/academy/unit-8/logic-function-selection",text_decoration="none"),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def logic_operations_function_selection_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 05",color_scheme="indigo"),
            rx.heading("Logic Operations & Function Selection",size="8"),
            rx.text("An ALU is not only an arithmetic unit. It also performs bitwise logic on entire words. Each bit position can run AND, OR, XOR or inversion in parallel, and selection logic chooses the requested function.",size="4",color="#475569",line_height="1.6"),
            _section("1","Bitwise logic across a word",
                rx.text("For an n-bit ALU, a logic operation is replicated across all n bit positions. There is no carry dependency between neighbouring bits."),
                rx.code_block("A = 1010\nB = 1100\n\nA AND B = 1000\nA OR  B = 1110\nA XOR B = 0110",language="textile",width="100%"),
                _practice("Calculate 1010 AND 1100.",AluPathState.bitwise_answer,AluPathState.set_bitwise_answer,AluPathState.check_bitwise,AluPathState.bitwise_feedback,"4-bit result")),
            _section("2","AND, OR, XOR and NOT",
                rx.text("AND is useful for masking bits, OR for setting or combining bits, XOR for toggling and difference detection, and NOT for complementing every bit."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Function"),rx.table.column_header_cell("Typical use"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("AND"),rx.table.cell("Mask / clear selected bits")),
                        rx.table.row(rx.table.cell("OR"),rx.table.cell("Set / combine selected bits")),
                        rx.table.row(rx.table.cell("XOR"),rx.table.cell("Toggle / compare bit differences")),
                        rx.table.row(rx.table.cell("NOT"),rx.table.cell("Invert all bits")),
                    ),width="100%"),
                _practice("Calculate 1010 XOR 1100.",AluPathState.xor_answer,AluPathState.set_xor_answer,AluPathState.check_xor,AluPathState.xor_feedback,"4-bit result")),
            _section("3","Parallel logic hardware",
                rx.text("A straightforward logic unit may compute several functions at the same time. A function selector then forwards only the requested result."),
                rx.code_block("A,B ──→ AND ─┐\n     ──→ OR  ─┤\n     ──→ XOR ─┼─→ function MUX → LogicResult\nA    ──→ NOT ─┘",language="textile",width="100%"),
                _practice("Which component can select one precomputed logic result?",AluPathState.logic_select_answer,AluPathState.set_logic_select_answer,AluPathState.check_logic_select,AluPathState.logic_select_feedback,"component")),
            _section("4","Function selection codes",
                rx.text("Control bits encode the requested operation. With two selector bits, four logic functions can be selected."),
                rx.code_block("S1 S0 | Logic function\n0  0  | AND\n0  1  | OR\n1  0  | XOR\n1  1  | NOT A",language="textile",width="100%"),
                rx.callout("The exact encoding is a design choice. What matters is that the control specification and hardware agree.",icon="binary")),
            _section("5","Arithmetic versus logic result",
                rx.text("The arithmetic datapath from Lesson 4 and the logic unit can operate as separate internal blocks. A final ALU multiplexer chooses which block drives the result bus."),
                rx.code_block("             ┌─ Arithmetic unit ─┐\nA,B,control ─┤                   ├─→ ALU result\n             └─ Logic unit ──────┘\n                    ↑ final mode select",language="textile",width="100%"),
                rx.callout("This hierarchy makes the ALU easier to reason about: first choose an operation inside a block, then choose the block result.",icon="layers")),
            _section("6","Logic operations and flags",
                rx.text("Zero and Negative flags can be derived from logic results just as they are from arithmetic results. Carry and signed overflow usually belong to arithmetic operations and must follow the ALU's documented flag rules.")),
            rx.card(rx.vstack(
                rx.badge("LESSON 05 COMPLETE",color_scheme="green"),
                rx.heading("You can now build the logic half of an ALU.",size="5"),
                rx.text("Next: encode arithmetic and logic choices into a unified ALU control word.",color="#475569"),
                rx.link(rx.button("Next · ALU Control & Operation Encoding",color_scheme="indigo"),href="/academy/unit-8/alu-control",text_decoration="none"),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def alu_control_operation_encoding_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 06",color_scheme="indigo"),
            rx.heading("ALU Control & Operation Encoding",size="8"),
            rx.text("The ALU contains many possible functions, but only one should be selected for a given instruction. A compact control field encodes the requested operation and drives operand conditioning, internal selectors and the final result multiplexer.",size="4",color="#475569",line_height="1.6"),
            _section("1","From instruction to ALU operation",
                rx.text("A processor instruction may contain an opcode, function field or decoded control signals. The control unit translates that information into an ALU control code."),
                rx.code_block("Instruction bits\n     ↓\nControl decoder\n     ↓\nALU control code\n     ↓\nADD / SUB / AND / OR / XOR / ...",language="textile",width="100%"),
                _practice("What encoded field tells the ALU which function to perform?",AluPathState.opcode_answer,AluPathState.set_opcode_answer,AluPathState.check_opcode,AluPathState.opcode_feedback,"field name")),
            _section("2","How many control bits?",
                rx.text("With k control bits, up to 2ᵏ unique binary codes are available. The encoding width should cover the required ALU functions while leaving room for reserved operations when useful."),
                rx.code_block("2 bits → 4 codes\n3 bits → 8 codes\n4 bits → 16 codes",language="textile",width="100%"),
                _practice("How many control bits are needed to encode up to 8 operations?",AluPathState.control_width_answer,AluPathState.set_control_width_answer,AluPathState.check_control_width,AluPathState.control_width_feedback,"number")),
            _section("3","Example ALU control table",
                rx.text("One possible 3-bit encoding is shown below. The exact mapping is a design choice; consistency between decoder, datapath and documentation is what matters."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("ALUCtrl"),rx.table.column_header_cell("Operation"),rx.table.column_header_cell("Result source"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("000"),rx.table.cell("ADD"),rx.table.cell("Arithmetic")),
                        rx.table.row(rx.table.cell("001"),rx.table.cell("SUB"),rx.table.cell("Arithmetic")),
                        rx.table.row(rx.table.cell("010"),rx.table.cell("AND"),rx.table.cell("Logic")),
                        rx.table.row(rx.table.cell("011"),rx.table.cell("OR"),rx.table.cell("Logic")),
                        rx.table.row(rx.table.cell("100"),rx.table.cell("XOR"),rx.table.cell("Logic")),
                        rx.table.row(rx.table.cell("101"),rx.table.cell("TRANSFER A"),rx.table.cell("Datapath")),
                        rx.table.row(rx.table.cell("110"),rx.table.cell("INC A"),rx.table.cell("Arithmetic")),
                        rx.table.row(rx.table.cell("111"),rx.table.cell("Reserved / defined behaviour"),rx.table.cell("Specified")),
                    ),width="100%")),
            _section("4","Control signals inside the ALU",
                rx.text("A single ALU control code can be decoded into several internal control signals: B complement, Cin selection, arithmetic/logic mode, function selector and output selection."),
                rx.code_block("ALUCtrl\n  ├─→ B_invert\n  ├─→ Cin_select\n  ├─→ LogicFn[1:0]\n  ├─→ ArithFn[1:0]\n  └─→ ResultSelect",language="textile",width="100%"),
                rx.callout("Control encoding reduces external wiring while a decoder recreates the detailed internal control signals.",icon="split")),
            _section("5","Reserved and illegal codes",
                rx.text("Not every possible binary pattern must represent a useful ALU operation. Unused codes may be reserved, mapped to a safe default, or detected as illegal—depending on the architecture."),
                _practice("Should an unused ALU control code have a documented deterministic behaviour?",AluPathState.illegal_code_answer,AluPathState.set_illegal_code_answer,AluPathState.check_illegal_code,AluPathState.illegal_code_feedback,"yes / behaviour")),
            _section("6","Decoder design and verification",
                rx.text("The control decoder is combinational logic, so every valid code must produce exactly the intended internal selections. A control truth table is therefore one of the most important verification artifacts for an ALU."),
                rx.code_block("Verification checklist\n✓ every legal code maps to one intended function\n✓ operand conditioning matches the operation\n✓ exactly one result source is selected\n✓ reserved codes behave predictably\n✓ flags follow the selected operation",language="textile",width="100%")),
            rx.card(rx.vstack(
                rx.badge("LESSON 06 COMPLETE",color_scheme="green"),
                rx.heading("You can now translate operation codes into ALU behaviour.",size="5"),
                rx.text("Next: combine result flags with comparison operations such as equality, signed less-than and unsigned less-than.",color="#475569"),
                rx.link(rx.button("Next · ALU Flags & Comparisons",color_scheme="indigo"),href="/academy/unit-8/alu-flags-comparisons",text_decoration="none"),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def alu_flags_comparisons_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 07",color_scheme="indigo"),
            rx.heading("ALU Flags & Comparisons",size="8"),
            rx.text("Comparison hardware often reuses subtraction and the ALU's status flags. Equality, signed ordering and unsigned ordering can therefore be derived without building a second arithmetic engine.",size="4",color="#475569",line_height="1.6"),
            _section("1","Equality from subtraction",
                rx.text("To test A = B, compute A − B. Equal operands produce an all-zero result, so the Zero flag provides a direct equality condition."),
                rx.code_block("A = 0101\nB = 0101\nA − B = 0000\nZ = 1  →  A = B",language="textile",width="100%"),
                _practice("Which flag can indicate equality after computing A − B?",AluPathState.equality_answer,AluPathState.set_equality_answer,AluPathState.check_equality,AluPathState.equality_feedback,"flag")),
            _section("2","Signed less-than",
                rx.text("For two's-complement signed numbers, the subtraction result sign alone is not always safe because overflow can invert the apparent sign. A standard signed less-than condition is N XOR V."),
                rx.code_block("Compute A − B\nSignedLess = N ⊕ V\n\nN = result sign flag\nV = signed overflow flag",language="textile",width="100%"),
                _practice("Which flag expression is commonly used for signed A < B after A − B?",AluPathState.signed_compare_answer,AluPathState.set_signed_compare_answer,AluPathState.check_signed_compare,AluPathState.signed_compare_feedback,"expression")),
            _section("3","Why overflow matters",
                rx.text("If the true signed subtraction result lies outside the representable range, the stored sign bit may disagree with the true mathematical ordering. XORing N with V compensates for that overflow condition."),
                rx.callout("Signed comparison interprets the bit pattern using two's-complement rules, not unsigned magnitude rules.",icon="triangle-alert")),
            _section("4","Unsigned less-than",
                rx.text("Unsigned comparison uses carry/borrow information rather than signed overflow. With the convention used here, subtraction sets C when no borrow is required; therefore C = 0 means A < B unsigned."),
                rx.code_block("Compute A − B\nC = 1 → no borrow → A ≥ B unsigned\nC = 0 → borrow required → A < B unsigned",language="textile",width="100%"),
                _practice("With this no-borrow convention, what C value indicates A < B unsigned?",AluPathState.unsigned_compare_answer,AluPathState.set_unsigned_compare_answer,AluPathState.check_unsigned_compare,AluPathState.unsigned_compare_feedback,"C value")),
            _section("5","One subtraction, many conditions",
                rx.text("A single A − B operation can support several branch and comparison decisions. The control unit interprets the flags according to the requested signed or unsigned condition."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Condition"),rx.table.column_header_cell("Typical test after A − B"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("A = B"),rx.table.cell("Z = 1")),
                        rx.table.row(rx.table.cell("A ≠ B"),rx.table.cell("Z = 0")),
                        rx.table.row(rx.table.cell("A < B signed"),rx.table.cell("N ⊕ V = 1")),
                        rx.table.row(rx.table.cell("A ≥ B signed"),rx.table.cell("N ⊕ V = 0")),
                        rx.table.row(rx.table.cell("A < B unsigned"),rx.table.cell("C = 0 (no-borrow convention)")),
                        rx.table.row(rx.table.cell("A ≥ B unsigned"),rx.table.cell("C = 1 (no-borrow convention)")),
                    ),width="100%")),
            _section("6","Comparison result generation",
                rx.text("Some ALUs expose comparison as a normal result operation such as SET-LESS-THAN: the output word becomes 1 when the condition is true and 0 otherwise."),
                rx.code_block("condition false → 0000...0000\ncondition true  → 0000...0001",language="textile",width="100%"),
                rx.callout("Comparison decisions can be generated from existing flags and routed through the ALU result-selection network.",icon="git-compare-arrows")),
            rx.card(rx.vstack(
                rx.badge("LESSON 07 COMPLETE",color_scheme="green"),
                rx.heading("You can now derive comparisons from subtraction and ALU flags.",size="5"),
                rx.text("Next: assemble arithmetic, logic, control, comparison and flags into a complete ALU architecture.",color="#475569"),
                rx.link(rx.button("Next · Complete ALU Architecture",color_scheme="indigo"),href="/academy/unit-8/integrated-alu-design",text_decoration="none"),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def integrated_alu_design_capstone_lesson()->rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 08 · LESSON 08 · PATH FINALE",color_scheme="indigo"),
            rx.heading("Complete ALU Architecture & Design Challenge",size="8"),
            rx.text("The Path 08 finale brings the complete arithmetic logic unit together: operand conditioning, fast arithmetic, bitwise logic, comparison generation, operation decoding, result selection and status flags.",size="4",color="#475569",line_height="1.6"),
            _section("1","Complete ALU block architecture",
                rx.text("A practical ALU is built from cooperating sub-blocks. Operands feed arithmetic, logic and comparison paths; a control decoder selects the requested operation; a final selector drives the result bus."),
                rx.code_block("                 ┌─ Arithmetic unit ─────────┐\nA,B ─ conditioning├─ Logic unit ─────────────┼─→ Result MUX ─→ F\n                 └─ Compare / SLT logic ───┘\n                         ↑\n                    ALU control decoder\n                         ↓\n                    C  V  Z  N flags",language="textile",width="100%"),
                _practice("Which block converts encoded ALU control bits into internal select signals?",AluPathState.capstone_control_answer,AluPathState.set_capstone_control_answer,AluPathState.check_capstone_control,AluPathState.capstone_control_feedback,"block")),
            _section("2","Integrated operation table",
                rx.text("A clear ALU specification defines control code, operation, result source and relevant flag behaviour."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Code"),rx.table.column_header_cell("Operation"),rx.table.column_header_cell("Result"),rx.table.column_header_cell("Key flags"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("000"),rx.table.cell("ADD"),rx.table.cell("A + B"),rx.table.cell("C,V,Z,N")),
                        rx.table.row(rx.table.cell("001"),rx.table.cell("SUB"),rx.table.cell("A − B"),rx.table.cell("C,V,Z,N")),
                        rx.table.row(rx.table.cell("010"),rx.table.cell("AND"),rx.table.cell("A AND B"),rx.table.cell("Z,N")),
                        rx.table.row(rx.table.cell("011"),rx.table.cell("OR"),rx.table.cell("A OR B"),rx.table.cell("Z,N")),
                        rx.table.row(rx.table.cell("100"),rx.table.cell("XOR"),rx.table.cell("A XOR B"),rx.table.cell("Z,N")),
                        rx.table.row(rx.table.cell("101"),rx.table.cell("SLT signed"),rx.table.cell("N ⊕ V"),rx.table.cell("Z,N by result")),
                        rx.table.row(rx.table.cell("110"),rx.table.cell("INC A"),rx.table.cell("A + 1"),rx.table.cell("C,V,Z,N")),
                        rx.table.row(rx.table.cell("111"),rx.table.cell("Reserved"),rx.table.cell("Defined safe result"),rx.table.cell("Defined")),
                    ),width="100%")),
            _section("3","Result selection and flag timing",
                rx.text("Flags must describe the selected ALU result and operation. Z and N can be derived from the final result bus. C and V originate in arithmetic logic when defined."),
                rx.code_block("Selected F → zero detector → Z\nSelected F MSB ─────────→ N\nAdder carry-out ────────→ C\nAdder overflow logic ───→ V",language="textile",width="100%"),
                _practice("Which flag must become 1 when the selected ALU result is all zeros?",AluPathState.capstone_flag_answer,AluPathState.set_capstone_flag_answer,AluPathState.check_capstone_flag,AluPathState.capstone_flag_feedback,"flag")),
            _section("4","Datapath/control separation",
                rx.text("The datapath performs transformations; the controller decides which transformation happens. Separating these responsibilities makes the ALU easier to extend, test and integrate."),
                rx.callout("Clean interface: operands A/B + ALUCtrl in, result F + flags out.",icon="waypoints")),
            _section("5","Engineering verification checklist",
                rx.code_block("✓ every legal control code selects the intended operation\n✓ ADD/SUB boundary values checked\n✓ signed overflow checked\n✓ unsigned carry / borrow convention checked\n✓ AND/OR/XOR checked bitwise\n✓ signed/unsigned comparisons checked\n✓ Z/N derived from final selected result\n✓ reserved codes deterministic",language="textile",width="100%"),
                _practice("Name one structured method for verifying all ALU operations and flags.",AluPathState.capstone_verify_answer,AluPathState.set_capstone_verify_answer,AluPathState.check_capstone_verify,AluPathState.capstone_verify_feedback,"verification method")),
            _section("6","Design challenge",
                rx.heading("Design a 4-bit educational ALU",size="4"),
                rx.text("Inputs A[3:0], B[3:0], ALUCtrl[2:0]. Output F[3:0]. Support ADD, SUB, AND, OR, XOR, signed SLT and INC; reserve one code. Generate C, V, Z and N."),
                rx.code_block("Deliverables:\n1. operation/control table\n2. block diagram\n3. arithmetic equations\n4. logic-function table\n5. comparison equations\n6. flag equations\n7. verification vectors",language="textile",width="100%")),
            _section("7","Path 08 concept map",
                rx.hstack(rx.badge("Binary arithmetic",color_scheme="blue"),rx.text("→"),rx.badge("Carry / overflow",color_scheme="red"),rx.text("→"),rx.badge("Fast adders",color_scheme="orange"),rx.text("→"),rx.badge("Datapaths",color_scheme="indigo"),rx.text("→"),rx.badge("Logic unit",color_scheme="purple"),rx.text("→"),rx.badge("ALU control",color_scheme="cyan"),rx.text("→"),rx.badge("Flags / compare",color_scheme="green"),wrap="wrap",spacing="2")),
            rx.card(rx.vstack(
                rx.badge("PATH 08 · COMPLETE",color_scheme="green"),
                rx.heading("Computer Arithmetic & ALU Design complete",size="6"),
                rx.text("You have progressed from binary arithmetic to a complete ALU architecture with control, logic, comparison and status flags.",color="#475569"),
                rx.hstack(rx.link(rx.button("Return to Academy",variant="soft"),href="/academy",text_decoration="none"),rx.link(rx.button("Open Simulator",color_scheme="indigo"),href="/",text_decoration="none"),wrap="wrap",spacing="3"),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")
