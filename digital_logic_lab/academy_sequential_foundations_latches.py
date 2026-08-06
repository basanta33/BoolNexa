"""BoolNexa Academy Path 05 — Lessons 1 and 2."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class SequentialFoundationsState(rx.State):
    state_answer:str=""
    state_feedback:str=""
    sr_answer:str=""
    sr_feedback:str=""
    d_answer:str=""
    d_feedback:str=""

    def set_d_answer(self, value: str) -> None:
        self.d_answer = value

    def set_sr_answer(self, value: str) -> None:
        self.sr_answer = value

    def set_state_answer(self, value: str) -> None:
        self.state_answer = value

    def check_state(self):
        v=self.state_answer.strip().lower().replace(" ","")
        self.state_feedback="Correct. Sequential logic depends on current inputs and stored state." if v in {"state","storedstate","memory","previousstate"} else "Think about information retained from the past."

    def check_sr(self):
        self.sr_feedback="Correct. S=1, R=0 sets Q=1." if self.sr_answer.strip()=="1" else "S means Set; with R inactive, Q becomes 1."

    def check_d(self):
        self.d_feedback="Correct. While Enable=1, Q follows D." if self.d_answer.strip()=="0" else "An enabled D latch is transparent, so Q follows D."

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def sequential_foundations_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 01",color_scheme="blue"),
        rx.heading("Sequential Logic, State & Time",size="8"),
        rx.text("Sequential circuits add memory to digital logic. Their outputs can depend on current inputs and on information stored from earlier events.",size="4",color="#475569",line_height="1.6"),
        sec("1","Combinational versus sequential",
            table(("Feature","Combinational","Sequential"),(("Depends on","Current inputs","Current inputs + stored state"),("Memory","No","Yes"),("Examples","Adder, MUX","Register, counter, FSM"))),
            rx.text("Besides current inputs, what does sequential logic depend on?"),
            rx.hstack(rx.input(value=SequentialFoundationsState.state_answer,on_change=SequentialFoundationsState.set_state_answer,placeholder="Answer",max_width="220px"),rx.button("Check",on_click=SequentialFoundationsState.check_state)),
            rx.cond(SequentialFoundationsState.state_feedback!="",rx.callout(SequentialFoundationsState.state_feedback,icon="brain"),rx.box())),
        sec("2","Present state and next state",
            rx.text("Present state is what the circuit remembers now. Inputs and next-state logic determine what should be stored next."),
            rx.code_block("Present state + inputs → next-state logic → Next state → storage → Present state",language="markup")),
        sec("3","Feedback creates storage",
            rx.text("Cross-coupled logic can feed outputs back toward inputs, allowing a stable state to persist after the initiating signal is removed."),
            rx.callout("Feedback makes timing and valid input conditions important.",icon="info")),
        sec("4","Latches and flip-flops",
            table(("Element","Control","Key behaviour"),(("Latch","Enable level","Level-sensitive"),("Flip-flop","Clock edge","Edge-triggered"))),
            rx.text("The level-sensitive versus edge-triggered distinction is fundamental.")),
        sec("5","Why clocks matter",
            rx.text("A clock provides repeated timing references so synchronous storage elements update in an organised way."),
            rx.code_block("time ─────────────────────►\nCLK  __|‾‾|__|‾‾|__|‾‾|__\n        ↑      ↑      ↑\n      clock events",language="markup")),
        sec("6","Where state is used",
            rx.unordered_list(rx.list_item("Registers store words."),rx.list_item("Counters track events."),rx.list_item("Finite-state machines control sequences."),rx.list_item("Processors coordinate operations over time."))),
        rx.hstack(rx.link(rx.button("← Academy",variant="soft"),href="/academy"),rx.spacer(),rx.text("Path 05 · Lesson 1",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/latches"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def latches_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 02",color_scheme="blue"),
        rx.heading("SR Latches & D Latches",size="8"),
        rx.text("Latches are level-sensitive one-bit storage elements. The SR latch exposes feedback directly; the D latch provides a safer single-data-input interface.",size="4",color="#475569",line_height="1.6"),
        sec("1","Active-high NOR SR latch",
            table(("S","R","Q(next)","Meaning"),(("0","0","Q(previous)","Hold"),("1","0","1","Set"),("0","1","0","Reset"),("1","1","Invalid","Forbidden"))),
            rx.callout("This is the active-high NOR SR latch. NAND SR latches use active-low inputs and different conventions.",icon="info")),
        sec("2","Set and reset",
            rx.text("For S=1 and R=0, what does Q become?"),
            rx.hstack(rx.input(value=SequentialFoundationsState.sr_answer,on_change=SequentialFoundationsState.set_sr_answer,placeholder="Q",max_width="120px"),rx.button("Check",on_click=SequentialFoundationsState.check_sr)),
            rx.cond(SequentialFoundationsState.sr_feedback!="",rx.callout(SequentialFoundationsState.sr_feedback,icon="brain"),rx.box())),
        sec("3","The forbidden SR condition",
            rx.text("For a basic NOR SR latch, S=R=1 forces both outputs low and breaks the intended complementary Q/Q' relationship. Releasing both inputs can make the resulting state depend on relative gate delays."),
            rx.callout("Treat S=R=1 as an invalid operating condition for this basic latch.",icon="triangle-alert",color_scheme="amber")),
        sec("4","D latch",
            table(("Enable E","D","Q(next)"),(("0","X","Q(previous)"),("1","0","0"),("1","1","1"))),
            rx.text("The D latch uses one data input so normal operation cannot request Set and Reset simultaneously.")),
        sec("5","Transparency",
            rx.text("A level-sensitive D latch is transparent while its enable is active. During that interval, changes at D can propagate to Q."),
            rx.text("If E=1 and D changes to 0, what should Q follow?"),
            rx.hstack(rx.input(value=SequentialFoundationsState.d_answer,on_change=SequentialFoundationsState.set_d_answer,placeholder="Q",max_width="120px"),rx.button("Check",on_click=SequentialFoundationsState.check_d)),
            rx.cond(SequentialFoundationsState.d_feedback!="",rx.callout(SequentialFoundationsState.d_feedback,icon="brain"),rx.box())),
        sec("6","From latch to flip-flop",
            rx.text("Many synchronous systems need storage to update near a defined clock edge rather than throughout an active level. Edge-triggered flip-flops solve that problem."),
            rx.code_block("Latch: level-sensitive ─────\nFlip-flop: edge-triggered ↑",language="markup")),
        rx.hstack(rx.link(rx.button("← Sequential foundations",variant="soft"),href="/academy/unit-5/sequential-foundations"),rx.spacer(),rx.text("Path 05 · Lesson 2",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/flip-flops"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")
