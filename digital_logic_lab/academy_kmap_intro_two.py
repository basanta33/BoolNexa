"""BoolNexa Academy Path 03 lessons 1 and 2: Karnaugh maps."""

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


class KMapIntroState(rx.State):
    cells_answer: str = ""
    cells_feedback: str = ""
    adjacency_answer: str = ""
    adjacency_feedback: str = ""
    group_answer: str = ""
    group_feedback: str = ""
    simplify_answer: str = ""
    simplify_feedback: str = ""

    def set_adjacency_answer(self, value: str) -> None:
        self.adjacency_answer = value

    def set_cells_answer(self, value: str) -> None:
        self.cells_answer = value

    def set_group_answer(self, value: str) -> None:
        self.group_answer = value

    def set_simplify_answer(self, value: str) -> None:
        self.simplify_answer = value

    def check_cells(self):
        self.cells_feedback = (
            "Correct. Two variables produce 2² = 4 K-map cells."
            if self.cells_answer.strip() == "4"
            else "Use 2ⁿ cells for n variables."
        )

    def check_adjacency(self):
        value = self.adjacency_answer.strip().lower().replace(" ", "")
        self.adjacency_feedback = (
            "Correct. Adjacent K-map cells differ in exactly one variable."
            if value in {"1", "one", "onevariable"}
            else "Neighbouring K-map cells differ by one variable."
        )

    def check_group(self):
        self.group_feedback = (
            "Correct. A pair contains two adjacent cells."
            if self.group_answer.strip() == "2"
            else "Valid group sizes are powers of two: 1, 2, 4, 8, ..."
        )

    def check_simplify(self):
        value = self.simplify_answer.strip().upper().replace(" ", "")
        self.simplify_feedback = (
            "Correct. A'B' + A'B = A'."
            if value in {"A'", "¬A", "A̅"}
            else "B changes across the pair, so B disappears; A remains 0."
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


def kmap_intro_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 01", color_scheme="blue"),
            rx.heading("Introduction to Karnaugh Maps", size="8"),
            rx.text(
                "Karnaugh maps turn truth-table information into a visual simplification method. "
                "They help students recognise neighbouring minterms and remove variables that do not affect the result.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Why simplify logic?",
                rx.text(
                    "Equivalent Boolean expressions can require different numbers of gates. "
                    "Simplification can reduce hardware, wiring and logic depth without changing the function."
                ),
                rx.code_block("Before: F = A'B' + A'B\nAfter:  F = A'\n\nBoth have the same truth table.",
                              language="markup"),
            ),
            _section(
                "2", "What is a K-map?",
                rx.text(
                    "A K-map has one cell for every input combination. Horizontal and vertical neighbours "
                    "are arranged so exactly one variable changes."
                ),
                rx.code_block("2 variables → 4 cells\n3 variables → 8 cells\n4 variables → 16 cells",
                              language="markup"),
                rx.text("How many cells are required for a two-variable K-map?"),
                rx.hstack(
                    rx.input(value=KMapIntroState.cells_answer, on_change=KMapIntroState.set_cells_answer,
                             placeholder="Cells", max_width="160px"),
                    rx.button("Check", on_click=KMapIntroState.check_cells),
                ),
                rx.cond(KMapIntroState.cells_feedback != "",
                        rx.callout(KMapIntroState.cells_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "3", "Gray-code adjacency",
                rx.text(
                    "K-maps use Gray-code ordering. For example, larger maps use 00, 01, 11, 10 "
                    "so neighbouring positions change by only one bit."
                ),
                rx.code_block("Gray-code order: 00 → 01 → 11 → 10", language="markup"),
                rx.text("How many variables change between adjacent K-map cells?"),
                rx.hstack(
                    rx.input(value=KMapIntroState.adjacency_answer,
                             on_change=KMapIntroState.set_adjacency_answer,
                             placeholder="Number", max_width="160px"),
                    rx.button("Check", on_click=KMapIntroState.check_adjacency),
                ),
                rx.cond(KMapIntroState.adjacency_feedback != "",
                        rx.callout(KMapIntroState.adjacency_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "4", "Grouping rules",
                rx.unordered_list(
                    rx.list_item("For SOP simplification, group cells containing 1."),
                    rx.list_item("Groups are rectangular and contain 1, 2, 4, 8, ... cells."),
                    rx.list_item("Make groups as large as possible."),
                    rx.list_item("Every required 1 must be covered."),
                    rx.list_item("Groups may overlap when useful."),
                    rx.list_item("Opposite edges are adjacent because a K-map wraps around."),
                ),
                rx.callout(
                    "Diagonal cells are not adjacent. Adjacency is horizontal or vertical, including wrap-around.",
                    icon="info",
                ),
            ),
            _section(
                "5", "Why grouping simplifies",
                rx.text(
                    "A variable that changes inside a valid group disappears from the simplified term. "
                    "Only variables that stay constant remain."
                ),
                rx.code_block("A'B' + A'B\n= A'(B' + B)\n= A'(1)\n= A'", language="markup"),
            ),
            _section(
                "6", "Learn by using BoolNexa",
                rx.text(
                    "Open Boolean Lab, enter A'B' + A'B, generate the truth table and inspect its K-map. "
                    "Compare the visual group with the simplified expression A'."
                ),
                rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
            ),
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(), rx.text("Path 03 · Lesson 1", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-3/two-variable-kmaps"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def two_variable_kmap_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 02", color_scheme="blue"),
            rx.heading("Two-Variable Karnaugh Maps", size="8"),
            rx.text(
                "Start with the smallest complete K-map. Map four truth-table rows into four cells "
                "and learn how an adjacent pair removes one changing variable.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The four cells",
                _table(("A \\ B", "0", "1"), (("0", "A'B'", "A'B"), ("1", "AB'", "AB"))),
                rx.text("Each cell is one minterm. Horizontal or vertical neighbours differ in one variable."),
            ),
            _section(
                "2", "Truth table → K-map",
                rx.text("Example: F is 1 for inputs 00 and 01."),
                _table(("A","B","F"),
                       (("0","0","1"),("0","1","1"),("1","0","0"),("1","1","0"))),
                rx.code_block(
                    "        B\n"
                    "        0   1\n"
                    "A = 0 | 1 | 1 |\n"
                    "A = 1 | 0 | 0 |\n\n"
                    "The two 1s form one horizontal pair.",
                    language="markup",
                ),
            ),
            _section(
                "3", "Pair → simplified term",
                rx.text(
                    "Inside the pair, B changes while A stays 0. "
                    "B disappears and the constant condition A=0 becomes A'."
                ),
                rx.code_block("A'B' + A'B = A'", language="markup"),
                rx.text("Simplify A'B' + A'B."),
                rx.hstack(
                    rx.input(value=KMapIntroState.simplify_answer,
                             on_change=KMapIntroState.set_simplify_answer,
                             placeholder="Simplified term", max_width="200px"),
                    rx.button("Check", on_click=KMapIntroState.check_simplify),
                ),
                rx.cond(KMapIntroState.simplify_feedback != "",
                        rx.callout(KMapIntroState.simplify_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "Valid group sizes",
                rx.code_block("1 cell  ✓\n2 cells ✓\n3 cells ✗\n4 cells ✓", language="markup"),
                rx.text("How many cells are in a valid K-map pair?"),
                rx.hstack(
                    rx.input(value=KMapIntroState.group_answer, on_change=KMapIntroState.set_group_answer,
                             placeholder="Cells", max_width="160px"),
                    rx.button("Check", on_click=KMapIntroState.check_group),
                ),
                rx.cond(KMapIntroState.group_feedback != "",
                        rx.callout(KMapIntroState.group_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Grouping all four cells",
                rx.text(
                    "If all four cells are 1, both A and B change within the group. "
                    "No variable remains, so the function simplifies to constant 1."
                ),
                rx.code_block("F = A'B' + A'B + AB' + AB\nF = 1", language="markup"),
            ),
            _section(
                "6", "Verify and build",
                rx.text(
                    "Use Boolean Lab to confirm the K-map and simplified expression, then use Circuit Generator "
                    "to compare the original and simplified logic implementations."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← K-map introduction", variant="soft"), href="/academy/unit-3/kmap-introduction"),
                rx.spacer(), rx.text("Path 03 · Lesson 2", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-3/three-variable-kmaps"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
