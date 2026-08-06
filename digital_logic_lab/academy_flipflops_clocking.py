"""BoolNexa Academy Path 05 — Lessons 3 and 4: flip-flops and clock timing."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class FlipFlopClockState(rx.State):
    d_answer:str=""
    d_feedback:str=""
    jk_answer:str=""
    jk_feedback:str=""
    t_answer:str=""
    t_feedback:str=""
    timing_answer:str=""
    timing_feedback:str=""

    def set_d_answer(self, value: str) -> None:
        self.d_answer = value

    def set_jk_answer(self, value: str) -> None:
        self.jk_answer = value

    def set_t_answer(self, value: str) -> None:
        self.t_answer = value

    def set_timing_answer(self, value: str) -> None:
        self.timing_answer = value

    def check_d(self):
        self.d_feedback="Correct. A positive-edge D flip-flop captures D=1 at the rising edge, so Q becomes 1." if self.d_answer.strip()=="1" else "Look only at D at the active rising edge."

    def check_jk(self):
        v=self.jk_answer.strip().lower().replace(" ","")
        self.jk_feedback="Correct. J=K=1 toggles the JK flip-flop." if v in {"toggle","toggles","q'","invert","inverts"} else "The JK flip-flop removes the SR invalid case by assigning J=K=1 a useful action."

    def check_t(self):
        v=self.t_answer.strip().lower().replace(" ","")
        self.t_feedback="Correct. With T=1, the T flip-flop toggles on each active clock edge." if v in {"toggle","toggles","invert","inverts","q'"} else "T stands for toggle."

    def check_timing(self):
        v=self.timing_answer.strip().lower().replace(" ","")
        self.timing_feedback="Correct. Violating setup or hold requirements can drive a flip-flop into metastability." if v in {"metastability","metastable"} else "What temporary indeterminate behaviour can occur when timing requirements are violated?"

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def flipflops_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 03",color_scheme="blue"),
        rx.heading("D, JK & T Flip-Flops",size="8"),
        rx.text("Flip-flops are edge-triggered storage elements. They update state around a specified clock transition, making them central to synchronous digital systems.",size="4",color="#475569",line_height="1.6"),
        sec("1","Edge-triggered D flip-flop",
            table(("D at active edge","Q(next)"),(("0","0"),("1","1"))),
            rx.code_block("Q(next) = D  (sampled at the active clock edge)",language="markup"),
            rx.text("For a positive-edge D flip-flop, D=1 just before a valid rising edge. What is Q after the edge?"),
            rx.hstack(rx.input(value=FlipFlopClockState.d_answer,on_change=FlipFlopClockState.set_d_answer,placeholder="Q",max_width="120px"),rx.button("Check",on_click=FlipFlopClockState.check_d)),
            rx.cond(FlipFlopClockState.d_feedback!="",rx.callout(FlipFlopClockState.d_feedback,icon="brain"),rx.box())),
        sec("2","JK flip-flop",
            table(("J","K","Q(next)","Action"),(("0","0","Q","Hold"),("0","1","0","Reset"),("1","0","1","Set"),("1","1","Q'","Toggle"))),
            rx.code_block("Q(next) = JQ' + K'Q",language="markup"),
            rx.text("What happens when J=1 and K=1?"),
            rx.hstack(rx.input(value=FlipFlopClockState.jk_answer,on_change=FlipFlopClockState.set_jk_answer,placeholder="Action",max_width="180px"),rx.button("Check",on_click=FlipFlopClockState.check_jk)),
            rx.cond(FlipFlopClockState.jk_feedback!="",rx.callout(FlipFlopClockState.jk_feedback,icon="brain"),rx.box())),
        sec("3","T flip-flop",
            table(("T","Q(next)","Action"),(("0","Q","Hold"),("1","Q'","Toggle"))),
            rx.code_block("Q(next) = T ⊕ Q",language="markup"),
            rx.text("What does a T flip-flop do at each active edge when T=1?"),
            rx.hstack(rx.input(value=FlipFlopClockState.t_answer,on_change=FlipFlopClockState.set_t_answer,placeholder="Action",max_width="180px"),rx.button("Check",on_click=FlipFlopClockState.check_t)),
            rx.cond(FlipFlopClockState.t_feedback!="",rx.callout(FlipFlopClockState.t_feedback,icon="brain"),rx.box())),
        sec("4","Characteristic versus excitation thinking",
            rx.text("A characteristic table tells what next state results from given inputs. An excitation table asks the reverse question: what inputs are required to achieve a desired state transition?"),
            table(("Desired transition","D","T","JK example"),(("0→0","0","0","J=0,K=X"),("0→1","1","1","J=1,K=X"),("1→0","0","1","J=X,K=1"),("1→1","1","0","J=X,K=0")))),
        sec("5","Asynchronous preset and clear",
            rx.text("Many physical flip-flops include preset/set and clear/reset controls that can override normal clocked operation."),
            rx.callout("Asynchronous control polarity varies by device. Always inspect the symbol bubbles and datasheet; do not assume active-high behaviour.",icon="info")),
        sec("6","Choosing a flip-flop",
            rx.unordered_list(rx.list_item("D: natural choice for registers and storing a computed next-state bit."),rx.list_item("T: convenient for toggling and counters."),rx.list_item("JK: flexible Set/Reset/Hold/Toggle behaviour and useful for learning state design."))),
        rx.hstack(rx.link(rx.button("← Latches",variant="soft"),href="/academy/unit-5/latches"),rx.spacer(),rx.text("Path 05 · Lesson 3",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/clock-timing"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def clock_timing_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 04",color_scheme="blue"),
        rx.heading("Clocking, Setup/Hold Time & Metastability",size="8"),
        rx.text("Correct logic equations are not enough for sequential hardware. Data must also arrive and remain stable within timing windows around the active clock edge.",size="4",color="#475569",line_height="1.6"),
        sec("1","Clock vocabulary",
            table(("Term","Meaning"),(("Period T","Time between equivalent clock edges"),("Frequency f","Cycles per second; f=1/T"),("Duty cycle","Fraction of a period the clock is high"),("Rising edge","0→1 transition"),("Falling edge","1→0 transition"))),
            rx.code_block("f = 1/T\nExample: T = 10 ns → f = 100 MHz",language="markup")),
        sec("2","Setup time",
            rx.text("Setup time tsetup is the minimum interval for which the data input must already be stable before the active clock edge."),
            rx.code_block("D stable ─────────────┐\n                     │ setup window\n───────────────[ tsetup ]─↑ CLK edge",language="markup")),
        sec("3","Hold time",
            rx.text("Hold time thold is the minimum interval for which data must remain stable after the active clock edge."),
            rx.code_block("CLK edge ↑─[ thold ]────────\n             │\nD must remain stable here",language="markup"),
            rx.callout("Setup is before the sampling edge; hold is after it.",icon="lightbulb",color_scheme="amber")),
        sec("4","Clock-to-Q and synchronous timing",
            rx.text("After an active edge, a flip-flop output does not change instantaneously. Clock-to-Q delay tCQ describes this response delay. Combinational logic then consumes additional propagation time before the next register."),
            rx.code_block("Register A ─tCQ─► combinational logic ─► Register B\n     ↑                                      ↑\n   clock                                  next clock",language="markup"),
            rx.text("A simplified setup constraint is:"),
            rx.code_block("Tclock ≥ tCQ(max) + tlogic(max) + tsetup\n(plus clock-skew/uncertainty terms in real designs)",language="markup")),
        sec("5","Metastability",
            rx.text("If a flip-flop's setup or hold requirement is violated, its internal state may temporarily take unusually long to resolve to a valid logic level. This is metastability."),
            rx.text("What phenomenon can result from violating setup or hold timing?"),
            rx.hstack(rx.input(value=FlipFlopClockState.timing_answer,on_change=FlipFlopClockState.set_timing_answer,placeholder="Answer",max_width="200px"),rx.button("Check",on_click=FlipFlopClockState.check_timing)),
            rx.cond(FlipFlopClockState.timing_feedback!="",rx.callout(FlipFlopClockState.timing_feedback,icon="brain"),rx.box()),
            rx.callout("Metastability cannot be eliminated absolutely; good synchronous design reduces its probability and prevents unsafe propagation.",icon="info")),
        sec("6","Asynchronous inputs and synchronizers",
            rx.text("Signals arriving from unrelated clock domains or external devices can change near a sampling edge. A common single-bit CDC technique is a chain of flip-flops in the receiving clock domain, allowing extra resolution time."),
            rx.code_block("async input ─► DFF1 ─► DFF2 ─► synchronized signal\n                 ↑       ↑\n              receiving clock",language="markup"),
            rx.callout("A simple two-flip-flop synchronizer is appropriate for many single-bit level signals, but multi-bit buses, pulses and high-throughput clock-domain crossings require other CDC techniques.",icon="triangle-alert",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← Flip-flops",variant="soft"),href="/academy/unit-5/flip-flops"),rx.spacer(),rx.text("Path 05 · Lesson 4",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/registers"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")
