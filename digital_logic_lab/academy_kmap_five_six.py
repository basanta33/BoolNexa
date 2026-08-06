"""BoolNexa Academy Path 03 lessons 7 and 8: five- and six-variable K-maps."""

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


class KMapFiveSixState(rx.State):
    five_cells: str = ""
    five_feedback: str = ""
    five_columns: str = ""
    five_columns_feedback: str = ""
    six_cells: str = ""
    six_feedback: str = ""
    six_shape: str = ""
    six_shape_feedback: str = ""

    def set_five_cells(self, value: str) -> None:
        self.five_cells = value

    def set_five_columns(self, value: str) -> None:
        self.five_columns = value

    def set_six_cells(self, value: str) -> None:
        self.six_cells = value

    def set_six_shape(self, value: str) -> None:
        self.six_shape = value

    def check_five_cells(self):
        self.five_feedback = (
            "Correct. Five variables give 2⁵ = 32 cells."
            if self.five_cells.strip() == "32"
            else "Use 2ⁿ cells. For five variables, calculate 2⁵."
        )

    def check_five_columns(self):
        value = self.five_columns.strip().replace(" ", "")
        self.five_columns_feedback = (
            "Correct. A 4×8 layout has 8 columns."
            if value == "8"
            else "The BoolNexa five-variable map is 4 rows by 8 columns."
        )

    def check_six_cells(self):
        self.six_feedback = (
            "Correct. Six variables give 2⁶ = 64 cells."
            if self.six_cells.strip() == "64"
            else "Use 2ⁿ cells. For six variables, calculate 2⁶."
        )

    def check_six_shape(self):
        value = self.six_shape.strip().lower().replace(" ", "").replace("×", "x")
        self.six_shape_feedback = (
            "Correct. BoolNexa uses one 8×8 Gray-code map for six variables."
            if value in {"8x8", "8by8"}
            else "Six variables require 64 cells, arranged here as one 8×8 Gray-code map."
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(number, color_scheme="blue"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            align="stretch",
            spacing="3",
        ),
        **PANEL,
    )


def _table(headers, rows):
    return rx.table.root(
        rx.table.header(
            rx.table.row(*[rx.table.column_header_cell(x) for x in headers])
        ),
        rx.table.body(
            *[rx.table.row(*[rx.table.cell(x) for x in row]) for row in rows]
        ),
        width="100%",
        variant="surface",
    )


def five_variable_kmap_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 07", color_scheme="blue"),
            rx.heading("Five-Variable Karnaugh Maps", size="8"),
            rx.text(
                "Five variables produce 32 minterms. BoolNexa uses a single 4×8 Gray-code map "
                "so all minterms remain visible in one continuous learning view.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "From 16 cells to 32 cells",
                rx.text(
                    "Adding one Boolean variable doubles the number of possible input combinations. "
                    "A five-variable function therefore requires 32 K-map cells."
                ),
                rx.code_block(
                    "4 variables → 2⁴ = 16 cells\n"
                    "5 variables → 2⁵ = 32 cells",
                    language="markup",
                ),
                rx.text("How many cells are in a five-variable K-map?"),
                rx.hstack(
                    rx.input(
                        value=KMapFiveSixState.five_cells,
                        on_change=KMapFiveSixState.set_five_cells,
                        placeholder="Cells",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=KMapFiveSixState.check_five_cells),
                ),
                rx.cond(
                    KMapFiveSixState.five_feedback != "",
                    rx.callout(KMapFiveSixState.five_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "BoolNexa 4×8 layout",
                rx.text(
                    "We assign two variables to the rows and three variables to the columns. "
                    "For variables A,B,C,D,E, the rows use AB and the columns use CDE."
                ),
                _table(
                    ("AB \\ CDE", "000", "001", "011", "010", "110", "111", "101", "100"),
                    (
                        ("00", "m0", "m1", "m3", "m2", "m6", "m7", "m5", "m4"),
                        ("01", "m8", "m9", "m11", "m10", "m14", "m15", "m13", "m12"),
                        ("11", "m24", "m25", "m27", "m26", "m30", "m31", "m29", "m28"),
                        ("10", "m16", "m17", "m19", "m18", "m22", "m23", "m21", "m20"),
                    ),
                ),
                rx.text("How many columns does this five-variable layout use?"),
                rx.hstack(
                    rx.input(
                        value=KMapFiveSixState.five_columns,
                        on_change=KMapFiveSixState.set_five_columns,
                        placeholder="Columns",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=KMapFiveSixState.check_five_columns),
                ),
                rx.cond(
                    KMapFiveSixState.five_columns_feedback != "",
                    rx.callout(KMapFiveSixState.five_columns_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "3",
                "Three-bit Gray-code order",
                rx.text(
                    "The eight columns must preserve one-bit adjacency. "
                    "The reflected three-bit Gray-code order is:"
                ),
                rx.code_block(
                    "000 → 001 → 011 → 010 → 110 → 111 → 101 → 100",
                    language="markup",
                ),
                rx.callout(
                    "Do not replace this with ordinary binary order. K-map grouping depends on Gray-code adjacency.",
                    icon="info",
                ),
            ),
            _section(
                "4",
                "Reflection and folded adjacency",
                rx.text(
                    "A five-variable K-map can be understood as two reflected four-variable halves. "
                    "The boundary between 010 and 110 is a reflection boundary, and the outermost columns "
                    "100 and 000 are also adjacent through wrap-around."
                ),
                rx.code_block(
                    "C=0 half                 C=1 half\n"
                    "000  001  011  010   |   110  111  101  100\n"
                    "                   reflection\n\n"
                    "Physical neighbours in Gray order differ by one bit.\n"
                    "Outer edge: 100 ↔ 000",
                    language="markup",
                ),
            ),
            _section(
                "5",
                "Grouping on a 4×8 map",
                rx.text(
                    "All familiar grouping rules still apply: powers of two, largest valid groups, overlap when useful, "
                    "and wrap-around. A logical group may appear as coordinated pieces when the reflected map is unfolded."
                ),
                rx.callout(
                    "Always judge grouping by Boolean adjacency, not by whether the loop looks like one ordinary rectangle on paper.",
                    icon="lightbulb",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "Practice in BoolNexa",
                rx.text(
                    "Enter a five-variable expression in Boolean Lab and inspect the 4×8 map. "
                    "Check the row/column Gray codes before studying the coloured groups."
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Open Boolean Lab", color_scheme="blue"),
                        href="/tools/boolean",
                    ),
                    rx.link(
                        rx.button("Open Circuit Generator", variant="soft"),
                        href="/tools/circuit",
                    ),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← SOP, POS & don't-cares", variant="soft"),
                    href="/academy/unit-3/sop-pos-dont-cares",
                ),
                rx.spacer(),
                rx.text("Path 03 · Lesson 7", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-3/six-variable-kmaps",
                ),
                width="100%",
                padding_y="16px",
            ),
            spacing="5",
            align="stretch",
            max_width="1100px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh",
        background="#f8fafc",
    )


def six_variable_kmap_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 03 · LESSON 08", color_scheme="blue"),
            rx.heading("Six-Variable Karnaugh Maps", size="8"),
            rx.text(
                "Six variables produce 64 minterms. BoolNexa presents them as one 8×8 Gray-code map, "
                "with three variables on each axis.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Sixty-four cells",
                rx.text(
                    "A six-variable Boolean function has 2⁶ possible input combinations, so the K-map contains 64 cells."
                ),
                rx.code_block(
                    "6 variables → 2⁶ = 64 cells",
                    language="markup",
                ),
                rx.text("How many cells are required?"),
                rx.hstack(
                    rx.input(
                        value=KMapFiveSixState.six_cells,
                        on_change=KMapFiveSixState.set_six_cells,
                        placeholder="Cells",
                        max_width="160px",
                    ),
                    rx.button("Check", on_click=KMapFiveSixState.check_six_cells),
                ),
                rx.cond(
                    KMapFiveSixState.six_feedback != "",
                    rx.callout(KMapFiveSixState.six_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "2",
                "One 8×8 Gray-code map",
                rx.text(
                    "For A,B,C,D,E,F, BoolNexa places ABC on the rows and DEF on the columns. "
                    "Both axes follow the same three-bit reflected Gray-code order."
                ),
                rx.code_block(
                    "Rows ABC:     000 001 011 010 110 111 101 100\n"
                    "Columns DEF:  000 001 011 010 110 111 101 100",
                    language="markup",
                ),
                rx.text("What is the shape of the BoolNexa six-variable K-map?"),
                rx.hstack(
                    rx.input(
                        value=KMapFiveSixState.six_shape,
                        on_change=KMapFiveSixState.set_six_shape,
                        placeholder="e.g. 8x8",
                        max_width="180px",
                    ),
                    rx.button("Check", on_click=KMapFiveSixState.check_six_shape),
                ),
                rx.cond(
                    KMapFiveSixState.six_shape_feedback != "",
                    rx.callout(KMapFiveSixState.six_shape_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "3",
                "Two-dimensional reflection",
                rx.text(
                    "The 8×8 map is a reflected representation in both directions. "
                    "The vertical and horizontal fold boundaries help you see how groups relate across higher-dimensional adjacency."
                ),
                rx.code_block(
                    "          DEF Gray-code columns\n"
                    "ABC       000 001 011 010 | 110 111 101 100\n"
                    "000\n"
                    "001\n"
                    "011\n"
                    "010       ----------------+----------------\n"
                    "110\n"
                    "111\n"
                    "101\n"
                    "100\n\n"
                    "Opposite outer edges also wrap around.",
                    language="markup",
                ),
            ),
            _section(
                "4",
                "Grouping still uses powers of two",
                rx.text(
                    "Group sizes remain 1,2,4,8,16,32 or 64. "
                    "The goal is still to keep only variables that remain constant throughout the selected group."
                ),
                rx.code_block(
                    "1 cell  → 6 literals\n"
                    "2 cells → 5 literals\n"
                    "4 cells → 4 literals\n"
                    "8 cells → 3 literals\n"
                    "16 cells → 2 literals\n"
                    "32 cells → 1 literal\n"
                    "64 cells → F = 1",
                    language="markup",
                ),
            ),
            _section(
                "5",
                "Avoid a common mistake",
                rx.text(
                    "Do not treat an 8×8 K-map as an ordinary checkerboard where only obvious flat rectangles matter. "
                    "Gray-code, reflection and wrap-around determine logical adjacency."
                ),
                rx.callout(
                    "When a valid higher-variable group looks visually split, keep the logical group intact and interpret the pieces together.",
                    icon="lightbulb",
                    color_scheme="amber",
                ),
            ),
            _section(
                "6",
                "Explore a six-variable map",
                rx.text(
                    "Use Boolean Lab with a six-variable expression. First confirm that the map has 8 Gray-coded rows and 8 Gray-coded columns. "
                    "Then inspect group size, wrap-around and reflection behaviour."
                ),
                rx.link(
                    rx.button("Open Boolean Lab", color_scheme="blue"),
                    href="/tools/boolean",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Five-variable K-maps", variant="soft"),
                    href="/academy/unit-3/five-variable-kmaps",
                ),
                rx.spacer(),
                rx.text("Path 03 · Lesson 8", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-3/advanced-strategy",
                ),
                width="100%",
                padding_y="16px",
            ),
            spacing="5",
            align="stretch",
            max_width="1100px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh",
        background="#f8fafc",
    )
