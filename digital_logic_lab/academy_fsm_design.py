"""BoolNexa Academy Path 05 — Lessons 7 and 8: FSM foundations and practical FSM design."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class FSMState(rx.State):
    state_count:str=""
    state_count_feedback:str=""
    moore_answer:str=""
    moore_feedback:str=""
    next_answer:str=""
    next_feedback:str=""
    bits_answer:str=""
    bits_feedback:str=""

    def set_bits_answer(self, value: str) -> None:
        self.bits_answer = value

    def set_moore_answer(self, value: str) -> None:
        self.moore_answer = value

    def set_next_answer(self, value: str) -> None:
        self.next_answer = value

    def set_state_count(self, value: str) -> None:
        self.state_count = value

    def check_state_count(self):
        self.state_count_feedback="Correct. IDLE, WAIT and ACTIVE are three distinct states." if self.state_count.strip()=="3" else "Count the named operating conditions."

    def check_moore(self):
        v=self.moore_answer.strip().lower().replace(" ","")
        self.moore_feedback="Correct. In a Moore machine, outputs depend on the current state." if v in {"state","currentstate","presentstate"} else "Moore outputs are attached to states rather than directly to transitions."

    def check_next(self):
        v=self.next_answer.strip().upper().replace(" ","")
        self.next_feedback="Correct. In IDLE with START=1, the specification moves to RUN." if v=="RUN" else "Follow the transition labelled START=1 from IDLE."

    def check_bits(self):
        self.bits_feedback="Correct. Three states require at least two state bits because 2² = 4 ≥ 3." if self.bits_answer.strip()=="2" else "Find the smallest n for which 2ⁿ is at least 3."

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def fsm_foundations_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 07",color_scheme="blue"),
        rx.heading("Finite-State Machines",size="8"),
        rx.text("A finite-state machine (FSM) models sequential behaviour using a finite set of states, input-controlled transitions and outputs. FSMs turn timing and memory into an organised design method.",size="4",color="#475569",line_height="1.6"),
        sec("1","What is a state?",
            rx.text("A state is a meaningful summary of the history that matters to future behaviour. The machine does not need to remember every past input—only enough information to decide what happens next."),
            rx.code_block("Inputs + Present State → Next-State Logic → Next State\n              │\n              └──────────────► Output Logic",language="markup"),
            rx.text("A controller has states IDLE, WAIT and ACTIVE. How many states does it have?"),
            rx.hstack(rx.input(value=FSMState.state_count,on_change=FSMState.set_state_count,placeholder="Number",max_width="140px"),rx.button("Check",on_click=FSMState.check_state_count)),
            rx.cond(FSMState.state_count_feedback!="",rx.callout(FSMState.state_count_feedback,icon="brain"),rx.box())),
        sec("2","State diagrams",
            rx.text("A state diagram represents states as nodes and transitions as directed arrows. Transition labels describe the input condition that causes movement to another state."),
            rx.code_block("[IDLE] -- START=1 --> [RUN]\n   ^                    |\n   |                    | DONE=1\n   +---------------- [DONE]\n          RESET=1",language="markup"),
            rx.callout("Every transition condition should be unambiguous. For each relevant state/input combination, the next state must be defined.",icon="info")),
        sec("3","State tables",
            table(("Present state","Input","Next state"),(("IDLE","START=0","IDLE"),("IDLE","START=1","RUN"),("RUN","DONE=0","RUN"),("RUN","DONE=1","DONE"),("DONE","RESET=0","DONE"),("DONE","RESET=1","IDLE"))),
            rx.text("If the present state is IDLE and START=1, what is the next state?"),
            rx.hstack(rx.input(value=FSMState.next_answer,on_change=FSMState.set_next_answer,placeholder="State",max_width="160px"),rx.button("Check",on_click=FSMState.check_next)),
            rx.cond(FSMState.next_feedback!="",rx.callout(FSMState.next_feedback,icon="brain"),rx.box())),
        sec("4","Moore versus Mealy machines",
            table(("Model","Output depends on","Typical implication"),(("Moore","Present state","Outputs usually change with state updates"),("Mealy","Present state + current inputs","Can respond immediately to input changes"))),
            rx.text("In a Moore machine, what primarily determines the output?"),
            rx.hstack(rx.input(value=FSMState.moore_answer,on_change=FSMState.set_moore_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=FSMState.check_moore)),
            rx.cond(FSMState.moore_feedback!="",rx.callout(FSMState.moore_feedback,icon="brain"),rx.box())),
        sec("5","Outputs on states and transitions",
            rx.text("Moore diagrams commonly place outputs inside states. Mealy diagrams commonly label transitions as input/output."),
            rx.code_block("Moore: [GREEN / go=1]\n\nMealy: [WAIT] -- request=1 / grant=1 --> [WAIT]",language="markup"),
            rx.callout("Neither model is universally better. Choose the form that gives clear, safe and verifiable behaviour for the system.",icon="lightbulb",color_scheme="amber")),
        sec("6","FSM hardware structure",
            rx.text("A synchronous FSM is typically built from a state register plus combinational next-state and output logic."),
            rx.code_block("              ┌───────────────────┐\nInputs ──────►│ Next-state logic  │──► D inputs\nState bits ──►│                   │\n              └───────────────────┘\n                         │\n                    ┌────▼────┐\nCLK ───────────────►│ State   │\n                    │ register│\n                    └────┬────┘\n                         └────► state bits / output logic",language="markup")),
        rx.hstack(rx.link(rx.button("← Counters",variant="soft"),href="/academy/unit-5/counters"),rx.spacer(),rx.text("Path 05 · Lesson 7",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/fsm-design"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def fsm_design_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 05 · LESSON 08",color_scheme="blue"),
        rx.heading("Practical FSM Design",size="8"),
        rx.text("Designing an FSM means converting a behavioural requirement into states, transitions, encodings, equations and verified hardware. This workflow is used in controllers throughout digital systems.",size="4",color="#475569",line_height="1.6"),
        sec("1","The FSM design workflow",
            rx.code_block("1. Read the specification\n2. Identify inputs and outputs\n3. Choose meaningful states\n4. Draw the state diagram\n5. Build the state/output table\n6. Assign binary state codes\n7. Derive next-state/output logic\n8. Implement and verify",language="markup"),
            rx.callout("Do not choose state encodings before understanding the required behaviour. Good state definitions come from the specification.",icon="info")),
        sec("2","Worked example: simple controller",
            rx.text("Specification: remain IDLE until START=1; then RUN until DONE=1; enter COMPLETE; remain there until RESET=1."),
            table(("State","Meaning","Output busy"),(("IDLE","Waiting","0"),("RUN","Operation active","1"),("COMPLETE","Finished; waiting for reset","0"))),
            rx.code_block("IDLE --START=1--> RUN --DONE=1--> COMPLETE\n ^                                   |\n |------------- RESET=1 -------------|",language="markup")),
        sec("3","State encoding",
            rx.text("With binary encoding, N states require at least ceil(log₂N) state bits. Three states therefore need at least two bits."),
            table(("State","Example code"),(("IDLE","00"),("RUN","01"),("COMPLETE","10"),("Unused","11"))),
            rx.text("What is the minimum number of binary state bits needed for three states?"),
            rx.hstack(rx.input(value=FSMState.bits_answer,on_change=FSMState.set_bits_answer,placeholder="Bits",max_width="140px"),rx.button("Check",on_click=FSMState.check_bits)),
            rx.cond(FSMState.bits_feedback!="",rx.callout(FSMState.bits_feedback,icon="calculator"),rx.box()),
            rx.callout("Unused encodings should be considered deliberately. Robust controllers often define a recovery path to a safe state.",icon="triangle-alert",color_scheme="amber")),
        sec("4","Binary, one-hot and other encodings",
            table(("Encoding","State bits","Trade-off"),(("Binary","≈ ceil(log₂N)","Few flip-flops; potentially more decode logic"),("One-hot","One bit per state","More flip-flops; often simple state decoding"),("Custom","Depends","May optimise timing, power or safety"))),
            rx.text("Synthesis tools can often choose or optimise state encodings automatically, but understanding the trade-offs remains important.")),
        sec("5","Avoid incomplete behaviour",
            rx.unordered_list(rx.list_item("Define what happens for every relevant input condition."),rx.list_item("Define reset behaviour and initial state."),rx.list_item("Consider unused state encodings."),rx.list_item("Avoid unintended combinational feedback."),rx.list_item("For outputs controlling hardware, consider glitches and timing.")),
            rx.callout("A diagram that looks sensible is not enough. Convert it to a table and systematically verify every state/input case.",icon="info")),
        sec("6","Verification challenge",
            rx.text("For the three-state controller, verify these sequences on paper before implementation:"),
            rx.code_block("RESET → IDLE\nSTART=1 → RUN\nDONE=0 → remain RUN\nDONE=1 → COMPLETE\nRESET=0 → remain COMPLETE\nRESET=1 → IDLE",language="markup"),
            rx.text("Then ask: What happens if START remains high? What happens if DONE is already high when RUN begins? The written specification must decide such cases."),
            rx.callout("Professional FSM design is specification-driven. Ambiguity should be resolved in the requirements rather than guessed in the circuit.",icon="lightbulb",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← FSM foundations",variant="soft"),href="/academy/unit-5/fsm"),rx.spacer(),rx.text("Path 05 · Lesson 8",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-5/integrated-design"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")
