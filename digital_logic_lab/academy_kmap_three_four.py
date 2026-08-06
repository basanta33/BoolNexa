"""BoolNexa Academy Path 03 lessons 3 and 4: three- and four-variable K-maps."""

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


class KMapThreeFourState(rx.State):
    three_cells: str = ""
    three_feedback: str = ""
    pair_answer: str = ""
    pair_feedback: str = ""
    four_cells: str = ""
    four_feedback: str = ""
    corner_answer: str = ""
    corner_feedback: str = ""

    def set_corner_answer(self, value: str) -> None:
        self.corner_answer = value

    def set_four_cells(self, value: str) -> None:
        self.four_cells = value

    def set_pair_answer(self, value: str) -> None:
        self.pair_answer = value

    def set_three_cells(self, value: str) -> None:
        self.three_cells = value

    def check_three_cells(self):
        self.three_feedback = (
            "Correct. Three variables give 2³ = 8 cells."
            if self.three_cells.strip() == "8"
            else "Use 2ⁿ cells. For n=3, calculate 2³."
        )

    def check_pair(self):
        value = self.pair_answer.strip().upper().replace(" ", "")
        self.pair_feedback = (
            "Correct. In A'B'C' + A'B'C, only C changes, leaving A'B'."
            if value in {"A'B'", "A̅B̅"}
            else "Compare the two minterms. C changes; A and B remain 0."
        )

    def check_four_cells(self):
        self.four_feedback = (
            "Correct. Four variables give 2⁴ = 16 cells."
            if self.four_cells.strip() == "16"
            else "Use 2ⁿ cells. Four variables require 2⁴ cells."
        )

    def check_corner(self):
        value = self.corner_answer.strip().lower().replace(" ", "")
        self.corner_feedback = (
            "Correct. All four corners are adjacent through horizontal and vertical wrap-around."
            if value in {"yes", "y", "true"}
            else "Remember that the left/right edges and top/bottom edges wrap around."
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


def three_variable_kmap_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 03", color_scheme="blue"),
            rx.heading("Three-Variable Karnaugh Maps", size="8"),
            rx.text(
                "Extend the K-map to eight cells. The key new idea is Gray-code ordering across two variables "
                "while preserving one-variable adjacency.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Eight cells",
                rx.text("A three-variable function has 2³ = 8 possible input combinations."),
                _table(
                    ("A \\ BC", "00", "01", "11", "10"),
                    (
                        ("0", "m0", "m1", "m3", "m2"),
                        ("1", "m4", "m5", "m7", "m6"),
                    ),
                ),
                rx.text("Notice the column order: 00, 01, 11, 10 — not ordinary binary order."),
                rx.text("How many cells does a three-variable K-map contain?"),
                rx.hstack(
                    rx.input(value=KMapThreeFourState.three_cells,
                             on_change=KMapThreeFourState.set_three_cells,
                             placeholder="Cells", max_width="160px"),
                    rx.button("Check", on_click=KMapThreeFourState.check_three_cells),
                ),
                rx.cond(KMapThreeFourState.three_feedback != "",
                        rx.callout(KMapThreeFourState.three_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "Map minterms correctly",
                rx.text(
                    "For F(A,B,C)=Σm(0,1,2,3), place 1s in m0, m1, m2 and m3. "
                    "These occupy the complete A=0 row even though the displayed column order is Gray coded."
                ),
                rx.code_block(
                    "        BC\n"
                    "        00  01  11  10\n"
                    "A = 0 | 1 | 1 | 1 | 1 |\n"
                    "A = 1 | 0 | 0 | 0 | 0 |\n\n"
                    "One group of 4 → A'",
                    language="markup",
                ),
            ),
            _section(
                "3", "Pairs remove one variable",
                rx.text("Consider two adjacent minterms: A'B'C' and A'B'C."),
                rx.code_block("A'B'C' + A'B'C = A'B'(C' + C) = A'B'", language="markup"),
                rx.text("What is the simplified term?"),
                rx.hstack(
                    rx.input(value=KMapThreeFourState.pair_answer,
                             on_change=KMapThreeFourState.set_pair_answer,
                             placeholder="Term", max_width="180px"),
                    rx.button("Check", on_click=KMapThreeFourState.check_pair),
                ),
                rx.cond(KMapThreeFourState.pair_feedback != "",
                        rx.callout(KMapThreeFourState.pair_feedback, icon="calculator"), rx.box()),
            ),
            _section(
                "4", "Groups of four",
                rx.text(
                    "A four-cell group in a three-variable K-map eliminates two variables. "
                    "For the complete A=0 row, B and C both change while A remains 0, producing A'."
                ),
                rx.callout(
                    "Prefer a group of four over two separate pairs whenever the larger group covers the same required 1s.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "5", "Wrap-around remains important",
                rx.text(
                    "The first and last Gray-code columns, 00 and 10, are adjacent because they differ only in B. "
                    "This allows groups to cross the left and right boundaries."
                ),
                rx.code_block("00 ↔ 10  ✓ one-bit difference\n00 ↔ 11  ✗ two-bit difference", language="markup"),
            ),
            _section(
                "6", "Practice with the real tool",
                rx.text(
                    "Enter a three-variable expression in Boolean Lab, compare its truth table with the K-map, "
                    "then identify the largest valid groups before looking at BoolNexa's simplified result."
                ),
                rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
            ),
            rx.hstack(
                rx.link(rx.button("← Two-variable K-maps", variant="soft"),
                        href="/academy/unit-3/two-variable-kmaps"),
                rx.spacer(), rx.text("Path 03 · Lesson 3", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-3/four-variable-kmaps"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def four_variable_kmap_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 04", color_scheme="blue"),
            rx.heading("Four-Variable Karnaugh Maps", size="8"),
            rx.text(
                "A four-variable K-map contains 16 cells arranged as a 4×4 Gray-code grid. "
                "It introduces powerful edge and corner groupings that may not look adjacent at first.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "The 4×4 map",
                _table(
                    ("AB \\ CD", "00", "01", "11", "10"),
                    (
                        ("00", "m0", "m1", "m3", "m2"),
                        ("01", "m4", "m5", "m7", "m6"),
                        ("11", "m12", "m13", "m15", "m14"),
                        ("10", "m8", "m9", "m11", "m10"),
                    ),
                ),
                rx.text(
                    "Both rows and columns use Gray-code order 00, 01, 11, 10. "
                    "This keeps every horizontal and vertical neighbour one bit apart."
                ),
                rx.text("How many cells are in a four-variable K-map?"),
                rx.hstack(
                    rx.input(value=KMapThreeFourState.four_cells,
                             on_change=KMapThreeFourState.set_four_cells,
                             placeholder="Cells", max_width="160px"),
                    rx.button("Check", on_click=KMapThreeFourState.check_four_cells),
                ),
                rx.cond(KMapThreeFourState.four_feedback != "",
                        rx.callout(KMapThreeFourState.four_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "2", "Largest groups first",
                rx.text(
                    "Possible group sizes are 1, 2, 4, 8 or 16 cells. "
                    "Larger groups eliminate more variables and normally produce simpler terms."
                ),
                rx.code_block(
                    "1 cell  → 4 variables remain\n"
                    "2 cells → 3 variables remain\n"
                    "4 cells → 2 variables remain\n"
                    "8 cells → 1 variable remains\n"
                    "16 cells → F = 1",
                    language="markup",
                ),
            ),
            _section(
                "3", "Edges wrap around",
                rx.text(
                    "The left edge touches the right edge, and the top edge touches the bottom edge. "
                    "Therefore groups may span opposite boundaries."
                ),
                rx.callout(
                    "Do not treat the K-map as a flat ordinary table. Logically, its opposite edges are neighbours.",
                    icon="info",
                ),
            ),
            _section(
                "4", "The four corners form a group",
                rx.text(
                    "Because both dimensions wrap around, the four corner cells are mutually connected as a valid 2×2 group."
                ),
                rx.code_block(
                    "● | . | . | ●\n"
                    "--+---+---+--\n"
                    ". | . | . | .\n"
                    ". | . | . | .\n"
                    "--+---+---+--\n"
                    "● | . | . | ●\n\n"
                    "The four ● cells form one valid group of 4.",
                    language="markup",
                ),
                rx.text("Can all four corners form one valid K-map group? Type yes or no."),
                rx.hstack(
                    rx.input(value=KMapThreeFourState.corner_answer,
                             on_change=KMapThreeFourState.set_corner_answer,
                             placeholder="yes / no", max_width="180px"),
                    rx.button("Check", on_click=KMapThreeFourState.check_corner),
                ),
                rx.cond(KMapThreeFourState.corner_feedback != "",
                        rx.callout(KMapThreeFourState.corner_feedback, icon="brain"), rx.box()),
            ),
            _section(
                "5", "Overlap when it helps",
                rx.text(
                    "A 1 may belong to more than one group. Overlap is useful when it lets you create larger groups "
                    "or cover isolated required cells with fewer literals."
                ),
                rx.callout(
                    "The goal is not to minimise the number of drawn loops alone; the goal is a correct, simple Boolean expression.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "6", "Analyse in BoolNexa",
                rx.text(
                    "Use a four-variable expression in Boolean Lab. Before accepting the simplified result, "
                    "identify Gray-code positions, edge adjacency, largest groups and any useful overlap yourself."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", color_scheme="blue"), href="/tools/boolean"),
                    rx.link(rx.button("Open Circuit Generator", variant="soft"), href="/tools/circuit"),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Three-variable K-maps", variant="soft"),
                        href="/academy/unit-3/three-variable-kmaps"),
                rx.spacer(), rx.text("Path 03 · Lesson 4", size="2", color="#64748b"), rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-3/prime-implicants"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
