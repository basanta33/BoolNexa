"""BoolNexa Academy Path 05 — Lessons 5 and 6: registers, shift registers and counters."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class RegisterCounterState(rx.State):
    register_bits:str=""
    register_feedback:str=""
    shift_answer:str=""
    shift_feedback:str=""
    counter_mod:str=""
    counter_feedback:str=""
    divide_answer:str=""
    divide_feedback:str=""

    def set_counter_mod(self, value: str) -> None:
        self.counter_mod = value

    def set_divide_answer(self, value: str) -> None:
        self.divide_answer = value

    def set_register_bits(self, value: str) -> None:
        self.register_bits = value

    def set_shift_answer(self, value: str) -> None:
        self.shift_answer = value

    def check_register_bits(self):
        self.register_feedback="Correct. A 4-bit register normally uses four one-bit storage elements." if self.register_bits.strip()=="4" else "Each stored bit needs one flip-flop."

    def check_shift(self):
        v=self.shift_answer.strip().replace(" ","")
        self.shift_feedback="Correct. After a right shift with serial-in 0, 1011 becomes 0101." if v=="0101" else "Move every stored bit one position to the right and insert 0 at the left."

    def check_counter_mod(self):
        self.counter_feedback="Correct. A 3-bit binary counter has 2³ = 8 distinct states, so it is modulo-8." if self.counter_mod.strip()=="8" else "An n-bit binary counter has 2ⁿ states."

    def check_divide(self):
        v=self.divide_answer.strip().replace(" ","").lower()
        self.divide_feedback="Correct. A toggling flip-flop changes state once per input edge, producing half the input frequency." if v in {"2","f/2","divideby2","÷2"} else "A T flip-flop with T=1 needs two input clock periods for one full output cycle."

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def registers_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 05",color_scheme="blue"),
        rx.heading("Registers & Shift Registers",size="8"),
        rx.text("A register groups flip-flops to store a multi-bit word. Shift registers add controlled movement of stored bits, enabling serial/parallel conversion, delay and sequence generation.",size="4",color="#475569",line_height="1.6"),
        sec("1","Parallel registers",
            rx.text("A four-bit register can use four D flip-flops sharing a common clock. On the active edge, all four bits are sampled together."),
            rx.code_block("D3 ─► DFF ─► Q3\nD2 ─► DFF ─► Q2\nD1 ─► DFF ─► Q1\nD0 ─► DFF ─► Q0\n       ▲ shared clock",language="markup"),
            rx.text("How many one-bit flip-flops are normally required to store four bits?"),
            rx.hstack(rx.input(value=RegisterCounterState.register_bits,on_change=RegisterCounterState.set_register_bits,placeholder="Number",max_width="140px"),rx.button("Check",on_click=RegisterCounterState.check_register_bits)),
            rx.cond(RegisterCounterState.register_feedback!="",rx.callout(RegisterCounterState.register_feedback,icon="brain"),rx.box())),
        sec("2","Shift-register families",
            table(("Type","Input","Output","Typical idea"),(("SISO","Serial","Serial","Bit delay"),("SIPO","Serial","Parallel","Serial-to-parallel conversion"),("PISO","Parallel","Serial","Parallel-to-serial conversion"),("PIPO","Parallel","Parallel","Ordinary register"))),
            rx.callout("The labels describe how data enters and leaves; actual devices may support several modes in one universal shift register.",icon="info")),
        sec("3","Right shifting",
            rx.text("During a right shift, each bit moves toward the least-significant position while a new serial bit enters the most-significant stage."),
            rx.code_block("Before:  Q3 Q2 Q1 Q0 = 1 0 1 1\nSerial-in = 0\nAfter:               0 1 0 1",language="markup"),
            rx.text("What does 1011 become after one right shift with serial-in 0?"),
            rx.hstack(rx.input(value=RegisterCounterState.shift_answer,on_change=RegisterCounterState.set_shift_answer,placeholder="4 bits",max_width="160px"),rx.button("Check",on_click=RegisterCounterState.check_shift)),
            rx.cond(RegisterCounterState.shift_feedback!="",rx.callout(RegisterCounterState.shift_feedback,icon="brain"),rx.box())),
        sec("4","Universal shift register",
            rx.text("A universal shift register can commonly hold, shift left, shift right and parallel-load. Multiplexers before each D flip-flop select which next-state source is used."),
            table(("Mode","Operation"),(("00","Hold"),("01","Shift right"),("10","Shift left"),("11","Parallel load"))),
            rx.callout("Mode encodings vary by device; always verify the actual design or datasheet.",icon="info")),
        sec("5","Applications",
            rx.unordered_list(rx.list_item("Temporary multi-bit storage."),rx.list_item("Serial/parallel data conversion."),rx.list_item("Digital delay lines."),rx.list_item("Sequence and pattern generation."),rx.list_item("Data movement inside processors and communication hardware."))),
        sec("6","Design insight",
            rx.text("A register is not a new primitive—it is a structured collection of flip-flops. Shift behaviour comes from carefully choosing each flip-flop's next-state input."),
            rx.code_block("next Q3 ← serial input\nnext Q2 ← Q3\nnext Q1 ← Q2\nnext Q0 ← Q1",language="markup")),
        rx.hstack(rx.link(rx.button("← Clock timing",variant="soft"),href="/academy/unit-5/clock-timing"),rx.spacer(),rx.text("Path 05 · Lesson 5",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/counters"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def counters_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 06",color_scheme="blue"),
        rx.heading("Binary Counters",size="8"),
        rx.text("Counters move through a defined sequence of states in response to clock events. They are used for event counting, timing, frequency division, addressing and control sequencing.",size="4",color="#475569",line_height="1.6"),
        sec("1","A 3-bit up-counter",
            table(("Clock count","Q2 Q1 Q0","Decimal"),(("0","000","0"),("1","001","1"),("2","010","2"),("3","011","3"),("4","100","4"),("5","101","5"),("6","110","6"),("7","111","7"),("8","000","0 again"))),
            rx.text("How many distinct states does a full 3-bit binary counter have?"),
            rx.hstack(rx.input(value=RegisterCounterState.counter_mod,on_change=RegisterCounterState.set_counter_mod,placeholder="States",max_width="140px"),rx.button("Check",on_click=RegisterCounterState.check_counter_mod)),
            rx.cond(RegisterCounterState.counter_feedback!="",rx.callout(RegisterCounterState.counter_feedback,icon="calculator"),rx.box())),
        sec("2","Modulo-N counters",
            rx.text("The modulus is the number of distinct states in the repeating sequence. A full n-bit binary counter is modulo-2ⁿ, but counters can be designed with shorter sequences."),
            rx.code_block("3-bit binary counter → MOD-8\nDecade counter          → MOD-10\nCustom 0,1,2,3,4,0...   → MOD-5",language="markup")),
        sec("3","Asynchronous (ripple) counters",
            rx.text("In a ripple counter, the external clock drives the first flip-flop and later stages are clocked from earlier stage outputs. State changes therefore ripple through the chain."),
            rx.callout("Because propagation delays accumulate, intermediate output patterns can briefly appear during transitions. Ripple counters are simple but are not ideal for high-speed synchronous systems.",icon="triangle-alert",color_scheme="amber")),
        sec("4","Synchronous counters",
            rx.text("In a synchronous counter, all flip-flops receive the same clock. Combinational next-state logic determines which stages toggle at that edge."),
            rx.code_block("Common CLK ─► FF0\n           ├► FF1\n           ├► FF2\n           └► FF3\n\nAll state bits update from the same clock event.",language="markup"),
            table(("Feature","Ripple","Synchronous"),(("Clocking","Stage-to-stage","Common clock"),("Delay","Accumulates through stages","Next-state logic + FF timing"),("Speed","Lower for large chains","Better suited to higher speed")))),
        sec("5","Counters as frequency dividers",
            rx.text("A flip-flop that toggles on every active edge produces an output whose full cycle takes two input clock periods. Cascaded binary-counter bits divide frequency by powers of two."),
            rx.code_block("Q0 = fCLK / 2\nQ1 = fCLK / 4\nQ2 = fCLK / 8",language="markup"),
            rx.text("A T flip-flop has T=1 continuously. By what factor does its Q output divide the input clock frequency?"),
            rx.hstack(rx.input(value=RegisterCounterState.divide_answer,on_change=RegisterCounterState.set_divide_answer,placeholder="Factor",max_width="150px"),rx.button("Check",on_click=RegisterCounterState.check_divide)),
            rx.cond(RegisterCounterState.divide_feedback!="",rx.callout(RegisterCounterState.divide_feedback,icon="brain"),rx.box())),
        sec("6","Up, down and programmable counting",
            rx.text("Counters may count upward, downward, load a starting value, enable/disable counting, or reset to a defined state. These controls turn a basic counter into a reusable subsystem."),
            rx.callout("Counter outputs are state variables. In later lessons, the same state-transition thinking will lead directly to finite-state machines.",icon="lightbulb",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← Registers",variant="soft"),href="/academy/unit-5/registers"),rx.spacer(),rx.text("Path 05 · Lesson 6",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/fsm"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")
