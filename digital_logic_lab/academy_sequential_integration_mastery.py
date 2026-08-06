"""BoolNexa Academy Path 05 — Lessons 9 and 10: integrated sequential design and mastery."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class SequentialMasteryState(rx.State):
    block_answer:str=""
    block_feedback:str=""
    timing_answer:str=""
    timing_feedback:str=""
    q1:str=""
    q2:str=""
    q3:str=""
    q4:str=""
    q5:str=""
    mastery_score:int=0
    mastery_feedback:str=""

    def set_block_answer(self, value: str) -> None:
        self.block_answer = value

    def set_q1(self, value: str) -> None:
        self.q1 = value

    def set_q2(self, value: str) -> None:
        self.q2 = value

    def set_q3(self, value: str) -> None:
        self.q3 = value

    def set_q4(self, value: str) -> None:
        self.q4 = value

    def set_q5(self, value: str) -> None:
        self.q5 = value

    def set_timing_answer(self, value: str) -> None:
        self.timing_answer = value

    def check_block(self):
        v=self.block_answer.strip().lower().replace(" ","")
        self.block_feedback="Correct. The state register stores the controller's present state." if v in {"stateregister","register","flipflops","flip-flops"} else "Which block physically remembers the FSM state between clock events?"

    def check_timing(self):
        v=self.timing_answer.strip().lower().replace(" ","")
        self.timing_feedback="Correct. Setup time is the required stable-data interval before the sampling edge." if v in {"setup","setuptime","tsetup"} else "This timing requirement is measured before the active clock edge."

    def grade_mastery(self):
        score=0
        if self.q1.strip().lower().replace(" ","") in {"dflipflop","dff","d"}: score+=1
        if self.q2.strip().lower().replace(" ","") in {"register","shiftregister"}: score+=1
        if self.q3.strip().lower().replace(" ","") in {"counter","binarycounter"}: score+=1
        if self.q4.strip().lower().replace(" ","") in {"moore","mooremachine"}: score+=1
        if self.q5.strip().lower().replace(" ","") in {"metastability","metastable"}: score+=1
        self.mastery_score=score
        if score==5:
            self.mastery_feedback="Mastery achieved: 5/5. Path 05 complete."
        elif score>=4:
            self.mastery_feedback=f"Strong result: {score}/5. Review the missed concept, then retry."
        else:
            self.mastery_feedback=f"Score: {score}/5. Revisit the relevant sequential-logic lessons before retrying."

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def sequential_integration_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 09",color_scheme="blue"),
        rx.heading("Integrated Sequential-System Design",size="8"),
        rx.text("Real controllers combine state storage, combinational decision logic, registers, counters and carefully timed interfaces. This lesson brings the whole sequential path together as one engineering workflow.",size="4",color="#475569",line_height="1.6"),
        sec("1","Think in datapath + control",
            rx.text("A useful architecture separates the datapath, which stores or transforms data, from the controller, which decides when operations occur."),
            rx.code_block("Inputs ─► [ DATAPATH: registers / counter / logic ] ─► Outputs\n                    ▲                 │\n                    │ control         │ status\n                    │                 ▼\n                 [ FSM CONTROLLER ]\n                        ▲\n                       CLK",language="markup"),
            rx.callout("This separation scales from classroom controllers to processors, communication interfaces and embedded hardware.",icon="info")),
        sec("2","Worked system: timed process controller",
            rx.text("Requirement: wait for START, run a process for four clock cycles, assert DONE, then wait for RESET."),
            table(("State","Counter action","Outputs"),(("IDLE","Clear","busy=0, done=0"),("RUN","Count","busy=1, done=0"),("COMPLETE","Hold","busy=0, done=1"))),
            rx.code_block("IDLE --START--> RUN --count reaches 4--> COMPLETE\n ^                                      |\n |---------------- RESET ---------------|",language="markup")),
        sec("3","Assign responsibilities",
            rx.unordered_list(
                rx.list_item("State register: remembers IDLE, RUN or COMPLETE."),
                rx.list_item("FSM next-state logic: chooses the next controller state."),
                rx.list_item("Counter register: remembers elapsed cycles."),
                rx.list_item("Comparator/terminal-count logic: detects completion."),
                rx.list_item("Output logic: generates busy, done, counter-enable and counter-clear.")
            ),
            rx.text("Which block physically stores the controller's present state?"),
            rx.hstack(rx.input(value=SequentialMasteryState.block_answer,on_change=SequentialMasteryState.set_block_answer,placeholder="Block",max_width="200px"),rx.button("Check",on_click=SequentialMasteryState.check_block)),
            rx.cond(SequentialMasteryState.block_feedback!="",rx.callout(SequentialMasteryState.block_feedback,icon="brain"),rx.box())),
        sec("4","Cycle-by-cycle reasoning",
            table(("Clock event","Before edge","Action at/after edge"),(
                ("Reset","Unknown / previous","State→IDLE, counter→0"),
                ("START edge","IDLE","State→RUN"),
                ("RUN cycle 1","RUN, count=0","count→1"),
                ("RUN cycle 4","RUN, terminal count","State→COMPLETE"),
                ("RESET edge","COMPLETE","State→IDLE, counter→0")
            )),
        ),
        sec("5","Timing still matters",
            rx.text("Even a logically correct controller must satisfy register timing. Combinational paths must settle before the receiving register's setup window, and data must remain stable through its hold window."),
            rx.code_block("Launching FF ─tCQ─► logic ─► Receiving FF\n                               ↑\n                    must satisfy setup\n                    and hold constraints",language="markup"),
            rx.text("Which timing requirement specifies that data must be stable before the active edge?"),
            rx.hstack(rx.input(value=SequentialMasteryState.timing_answer,on_change=SequentialMasteryState.set_timing_answer,placeholder="Requirement",max_width="180px"),rx.button("Check",on_click=SequentialMasteryState.check_timing)),
            rx.cond(SequentialMasteryState.timing_feedback!="",rx.callout(SequentialMasteryState.timing_feedback,icon="brain"),rx.box())),
        sec("6","Verification plan",
            rx.unordered_list(
                rx.list_item("Reset and confirm the defined initial state."),
                rx.list_item("Test START while IDLE and verify entry to RUN."),
                rx.list_item("Count exactly the required number of clock events."),
                rx.list_item("Verify DONE and BUSY never contradict the specification."),
                rx.list_item("Test RESET and unusual input persistence."),
                rx.list_item("Check unused states and recovery behaviour."),
                rx.list_item("Review clock-domain crossings and asynchronous inputs.")
            ),
            rx.callout("Verify both functional behaviour and timing assumptions. Sequential correctness is a function of logic plus time.",icon="lightbulb",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← FSM design",variant="soft"),href="/academy/unit-5/fsm-design"),rx.spacer(),rx.text("Path 05 · Lesson 9",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Mastery challenge →",variant="soft"),href="/academy/unit-5/mastery-challenge"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def sequential_mastery_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 10",color_scheme="blue"),
        rx.heading("Sequential Logic Mastery Challenge",size="8"),
        rx.text("Complete Path 05 by connecting storage, timing, registers, counters and state-machine concepts in one capstone assessment.",size="4",color="#475569",line_height="1.6"),
        sec("1","Rapid knowledge check",
            rx.text("Q1. Which flip-flop naturally stores a computed next-state bit?"),
            rx.input(value=SequentialMasteryState.q1,on_change=SequentialMasteryState.set_q1,placeholder="Answer",max_width="260px"),
            rx.text("Q2. Which structure stores a multi-bit word?"),
            rx.input(value=SequentialMasteryState.q2,on_change=SequentialMasteryState.set_q2,placeholder="Answer",max_width="260px"),
            rx.text("Q3. Which sequential block repeatedly advances through a numeric state sequence?"),
            rx.input(value=SequentialMasteryState.q3,on_change=SequentialMasteryState.set_q3,placeholder="Answer",max_width="260px"),
            rx.text("Q4. Which FSM model has outputs determined by the present state only?"),
            rx.input(value=SequentialMasteryState.q4,on_change=SequentialMasteryState.set_q4,placeholder="Answer",max_width="260px"),
            rx.text("Q5. What phenomenon can occur after a setup/hold violation?"),
            rx.input(value=SequentialMasteryState.q5,on_change=SequentialMasteryState.set_q5,placeholder="Answer",max_width="260px"),
            rx.button("Grade Path 05",on_click=SequentialMasteryState.grade_mastery,color_scheme="blue"),
            rx.cond(SequentialMasteryState.mastery_feedback!="",rx.callout(SequentialMasteryState.mastery_feedback,icon="graduation-cap"),rx.box())),
        sec("2","Capstone specification: pedestrian crossing controller",
            rx.text("Design a simplified synchronous controller with states VEHICLE_GO, VEHICLE_WAIT and PEDESTRIAN_GO. A pedestrian request starts a safe transition; after a timed pedestrian interval the controller returns to vehicle flow."),
            rx.code_block("Inputs:  request, timer_done, reset\nOutputs: vehicle_green, pedestrian_green, timer_start\n\nSafety rule:\nvehicle_green and pedestrian_green must NEVER be 1 together.",language="markup"),
            rx.callout("This is an educational synchronous controller abstraction. Real traffic-control systems require additional safety states, standards, fault handling and independent fail-safe mechanisms.",icon="triangle-alert",color_scheme="amber")),
        sec("3","Build the state plan",
            table(("State","vehicle_green","pedestrian_green","Purpose"),(("VEHICLE_GO","1","0","Normal traffic flow"),("VEHICLE_WAIT","0","0","Safety transition interval"),("PEDESTRIAN_GO","0","1","Pedestrian crossing interval"))),
            rx.code_block("VEHICLE_GO --request--> VEHICLE_WAIT\nVEHICLE_WAIT --timer_done--> PEDESTRIAN_GO\nPEDESTRIAN_GO --timer_done--> VEHICLE_GO",language="markup")),
        sec("4","Implementation architecture",
            rx.code_block("request ───────────────┐\ntimer_done ────────────┼─► next-state logic ─► state DFFs\npresent state ─────────┘                         ▲\n                                                CLK\n\npresent state ─► output decode ─► lights / timer control\n\ncounter/register ─► timer_done",language="markup"),
            rx.text("The capstone deliberately reuses nearly every Path 05 concept: D flip-flops, state registers, counters, synchronous timing and Moore-style outputs.")),
        sec("5","Verification checklist",
            rx.unordered_list(
                rx.list_item("Reset enters a safe, defined state."),
                rx.list_item("A request causes the intended state sequence."),
                rx.list_item("Both green outputs are never asserted simultaneously."),
                rx.list_item("Timer completion is sampled correctly."),
                rx.list_item("Persistent request behaviour is explicitly defined."),
                rx.list_item("Unused state encodings recover safely."),
                rx.list_item("Asynchronous external requests are synchronized before FSM use.")
            ),
            rx.callout("A successful simulation is evidence, not a substitute for a complete specification and systematic verification.",icon="info")),
        sec("6","Path 05 complete",
            rx.callout("You can now reason about digital systems that remember: latches, flip-flops, clocks, timing, registers, counters and finite-state machines.",icon="graduation-cap",color_scheme="green"),
            rx.text("The next Academy path can build on this foundation with larger digital architectures and implementation-oriented design.")),
        rx.hstack(rx.link(rx.button("← Integrated design",variant="soft"),href="/academy/unit-5/integrated-design"),rx.spacer(),rx.text("Path 05 · Lesson 10",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Begin Path 06 →",color_scheme="blue"),href="/academy/unit-6/memory-foundations"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")
