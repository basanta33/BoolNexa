"""BoolNexa Boolean Laboratory — compact textbook-style truth tables."""

from __future__ import annotations

import reflex as rx
from typing import TypedDict
from .boolean_engine import (
    BooleanExpressionError,
    classify_expression,
    generate_truth_table,
)
from .boolean_simplifier import simplify_expression
from .kmap_engine import build_kmap
from .kmap_renderer import group_color, serialize_kmap
from .simplification_steps import SimplificationStep


def _clean_expression_input(value: str) -> str:
    """Uppercase and restrict the student's Boolean-expression input."""
    value = value.replace("’", "'").replace("′", "'")
    return "".join(
        ch.upper()
        for ch in value
        if ch.isalpha() or ch in "'+&() "
    )


def _parse_sigma_m_numbers(value: str) -> list[int]:
    """Parse comma-separated Σm numbers, allowing only unique values 0..63."""
    raw = value.strip()
    if not raw:
        raise ValueError("Enter at least one minterm number.")

    parts = [part.strip() for part in raw.split(",")]
    if any(not part or not part.isdigit() for part in parts):
        raise ValueError(
            "Use only minterm numbers separated by commas, for example 0,2,4,6."
        )

    minterms = [int(part) for part in parts]
    if any(number >= 64 for number in minterms):
        raise ValueError("Minterm numbers must be between 0 and 63.")
    if len(set(minterms)) != len(minterms):
        raise ValueError("Do not repeat a minterm number.")
    return minterms


def _sigma_m_to_expression(value: str, variable_count: int) -> str:
    """Convert Σm values to canonical SOP for an explicit 2..6 variable map."""
    minterms = _parse_sigma_m_numbers(value)
    if variable_count < 2 or variable_count > 6:
        raise ValueError("Choose between 2 and 6 variables.")

    maximum = (1 << variable_count) - 1
    invalid = [number for number in minterms if number > maximum]
    if invalid:
        raise ValueError(
            f"For {variable_count} variables, minterms must be between 0 and {maximum}."
        )

    variables = "ABCDEF"[:variable_count]
    terms: list[str] = []
    for number in sorted(minterms):
        bits = format(number, f"0{variable_count}b")
        terms.append(
            "".join(
                variable if bit == "1" else variable + "'"
                for variable, bit in zip(variables, bits)
            )
        )
    return " + ".join(terms)
from .ui import (
    COLORS,
    app_header,
    metric_card,
    page_intro,
    panel,
    primary_button,
    secondary_button,
)
class KMapOutlineView(TypedDict):
    group: str
    color: str
    inset: str
    top_offset: str
    right_offset: str
    bottom_offset: str
    left_offset: str
    top: str
    right: str
    bottom: str
    left: str
    wrap_horizontal: str
    wrap_vertical: str


class KMapCellView(TypedDict):
    value: str
    minterm: str
    groups: str
    outlines: list[KMapOutlineView]


class KMapSegmentView(TypedDict):
    group: str
    color: str
    left: str
    top: str
    width: str
    height: str
    border_top: str
    border_right: str
    border_bottom: str
    border_left: str
    radius_top_left: str
    radius_top_right: str
    radius_bottom_right: str
    radius_bottom_left: str
    open_left: str
    open_right: str
    open_top: str
    open_bottom: str


class KMapFacetView(TypedDict):
    index: int
    code: str
    rows: list[list[KMapCellView]]
    segments: list[KMapSegmentView]


class KMapGroupView(TypedDict):
    number: str
    term: str
    minterms: str
    size: str
    essential: str
    color: str

class BooleanLabState(rx.State):
    """State for expression analysis and compact truth-table presentation."""

    expression: str = "A(B+C')"
    minterm_numbers: str = ""
    minterm_variable_count: str = "3"
    minterm_input_error: str = ""
    input_source: str = "expression"
    show_intermediate: bool = False

    normalized_expression: str = ""
    variables: list[str] = []
    intermediate_headers: list[str] = []
    rows: list[dict[str, str]] = []

    minterm_text: str = ""
    maxterm_text: str = ""
    canonical_sop: str = ""
    canonical_pos: str = ""
    classification: str = ""
    error_message: str = ""

    simplified_expression: str = ""
    simplifier_steps: list[dict[str, str]] = []
    simplifier_error: str = ""
    simplifier_summary: str = ""

    kmap_error: str = ""
    kmap_row_variables: str = ""
    kmap_column_variables: str = ""
    kmap_facet_variables: str = ""
    kmap_variables_label: str = ""
    kmap_function_label: str = ""
    kmap_row_codes: list[str] = []
    kmap_column_codes: list[str] = []
    kmap_facets: list[KMapFacetView] = []
    kmap_groups: list[KMapGroupView] = []
    kmap_simplified: str = ""

    def on_load(self) -> None:
        self.reduce_function()

    def _clear_kmap_result(self) -> None:
        """Clear rendered K-map data when the source function changes."""
        self.kmap_error = ""
        self.kmap_row_variables = ""
        self.kmap_column_variables = ""
        self.kmap_facet_variables = ""
        self.kmap_variables_label = ""
        self.kmap_function_label = ""
        self.kmap_row_codes = []
        self.kmap_column_codes = []
        self.kmap_facets = []
        self.kmap_groups = []
        self.kmap_simplified = ""

    def set_expression(self, value: str) -> None:
        """Expression mode: uppercase valid symbols and invalidate old K-map output."""
        self.expression = _clean_expression_input(value)
        self.input_source = "expression"
        self._clear_kmap_result()

    def set_minterm_variable_count(self, value: str) -> None:
        """Set the explicit variable width used by canonical Σm input."""
        if value not in {"2", "3", "4", "5", "6"}:
            self.minterm_input_error = "Choose between 2 and 6 variables."
            return
        self.minterm_variable_count = value
        self.minterm_input_error = ""

        # Revalidate an already-entered list against the new width.
        if self.minterm_numbers.strip():
            try:
                _sigma_m_to_expression(
                    self.minterm_numbers,
                    int(self.minterm_variable_count),
                )
            except ValueError as exc:
                self.minterm_input_error = str(exc)

    def set_minterm_numbers(self, value: str) -> None:
        """Accept digits/commas/spaces and enforce the selected variable range."""
        cleaned = "".join(ch for ch in value if ch.isdigit() or ch in ", ")
        complete_tokens = [
            token.strip() for token in cleaned.split(",") if token.strip()
        ]
        maximum = (1 << int(self.minterm_variable_count)) - 1
        if any(
            token.isdigit() and int(token) > maximum
            for token in complete_tokens
        ):
            self.minterm_input_error = (
                f"For {self.minterm_variable_count} variables, "
                f"minterms must be between 0 and {maximum}."
            )
            return

        self.minterm_numbers = cleaned
        self.minterm_input_error = ""

    def _apply_source_expression(self, source_expression: str) -> None:
        """Populate truth table, simplification and K-map from an explicit source.

        This deliberately does not read or write the visible Expression field,
        so Σm mode cannot conflict with a stale expression typed above it.
        """
        try:
            table = generate_truth_table(
                source_expression,
                include_intermediate=self.show_intermediate,
                max_variables=8,
            )
        except BooleanExpressionError as exc:
            self.error_message = str(exc)
            self.simplifier_error = str(exc)
            self.kmap_error = str(exc)
            self.normalized_expression = ""
            self.variables = []
            self.intermediate_headers = []
            self.rows = []
            self.minterm_text = ""
            self.maxterm_text = ""
            self.canonical_sop = ""
            self.canonical_pos = ""
            self.classification = ""
            self._clear_kmap_result()
            return

        self.error_message = ""
        self.normalized_expression = table.normalized_expression
        self.variables = table.variables
        self.intermediate_headers = table.intermediate_headers
        self.rows = table.rows
        self.minterm_text = (
            "Σm(" + ", ".join(str(number) for number in table.minterms) + ")"
            if table.minterms
            else "Σm(∅)"
        )
        self.maxterm_text = (
            "ΠM(" + ", ".join(str(number) for number in table.maxterms) + ")"
            if table.maxterms
            else "ΠM(∅)"
        )
        self.canonical_sop = table.canonical_sop
        self.canonical_pos = table.canonical_pos
        self.classification = classify_expression(table)

        try:
            simplified = simplify_expression(source_expression)
        except BooleanExpressionError as exc:
            self.simplifier_error = str(exc)
            self.simplified_expression = ""
            self.simplifier_steps = []
            self.simplifier_summary = ""
        else:
            self.simplifier_error = ""
            self.simplified_expression = simplified.simplified
            self.simplifier_steps = [
                {
                    "number": str(step.number),
                    "before": step.before,
                    "after": step.after,
                    "law": step.law_name,
                    "formula": step.formula,
                    "explanation": step.explanation,
                }
                for step in simplified.steps
            ]
            self.simplifier_summary = (
                f"{simplified.literal_count_before} → {simplified.literal_count_after} literals; "
                f"{simplified.term_count_before} → {simplified.term_count_after} terms"
            )

        try:
            result = build_kmap(source_expression)
        except BooleanExpressionError as exc:
            self.kmap_error = str(exc)
            self._clear_kmap_result()
            return

        self.kmap_error = ""
        self.kmap_row_variables = "".join(result.row_variables)
        self.kmap_column_variables = "".join(result.column_variables)
        self.kmap_facet_variables = "".join(result.facet_variables)
        self.kmap_variables_label = "".join(result.variables)
        self.kmap_function_label = "F(" + ",".join(result.variables) + ")"
        self.kmap_row_codes = result.row_codes
        self.kmap_column_codes = result.column_codes
        self.kmap_facets = serialize_kmap(result)
        self.kmap_groups = [
            {
                "number": str(group.index),
                "term": group.term,
                "minterms": ", ".join(f"m{number}" for number in group.minterms),
                "size": str(group.size),
                "essential": "Essential" if group.essential else "Prime",
                "color": group_color(group.index),
            }
            for group in result.groups
        ]
        self.kmap_simplified = result.simplified_expression

    def generate_from_minterms(self) -> None:
        """Σm mode converts minterms to canonical SOP and displays it in Expression."""
        try:
            source_expression = _sigma_m_to_expression(
                self.minterm_numbers,
                int(self.minterm_variable_count),
            )
        except ValueError as exc:
            self.minterm_input_error = str(exc)
            return

        self.minterm_input_error = ""
        self.input_source = "minterms"

        # Show the expanded canonical SOP in the main Expression box so the
        # student can see exactly what the entered minterms represent.
        self.expression = source_expression

        # Then run truth table, simplification and K-map from that same source.
        self._apply_source_expression(source_expression)

    def set_show_intermediate(self, value: bool) -> None:
        """Refresh the visible truth table so evaluation columns appear/disappear."""
        self.show_intermediate = value
        self._apply_source_expression(self.expression)

    def load_example(self, value: str) -> None:
        self.expression = value
        self.minterm_input_error = ""
        self.reduce_function()

    def reduce_function(self) -> None:
        """Expression mode: run the complete workflow from the visible expression."""
        self.input_source = "expression"
        self._apply_source_expression(self.expression)

    def generate(self) -> None:
        try:
            table = generate_truth_table(
                self.expression,
                include_intermediate=self.show_intermediate,
                max_variables=8,
            )
        except BooleanExpressionError as exc:
            self.error_message = str(exc)
            self.normalized_expression = ""
            self.variables = []
            self.intermediate_headers = []
            self.rows = []
            self.minterm_text = ""
            self.maxterm_text = ""
            self.canonical_sop = ""
            self.canonical_pos = ""
            self.classification = ""
            return

        self.error_message = ""
        self.normalized_expression = table.normalized_expression
        self.variables = table.variables
        self.intermediate_headers = table.intermediate_headers
        self.rows = table.rows
        self.minterm_text = (
            "Σm(" + ", ".join(str(value) for value in table.minterms) + ")"
            if table.minterms
            else "Σm(∅)"
        )
        self.maxterm_text = (
            "ΠM(" + ", ".join(str(value) for value in table.maxterms) + ")"
            if table.maxterms
            else "ΠM(∅)"
        )
        self.canonical_sop = table.canonical_sop
        self.canonical_pos = table.canonical_pos
        self.classification = classify_expression(table)



    def simplify(self) -> None:
        try:
            result = simplify_expression(self.expression)
        except BooleanExpressionError as exc:
            self.simplifier_error = str(exc)
            self.simplified_expression = ""
            self.simplifier_steps = []
            self.simplifier_summary = ""
            return

        self.simplifier_error = ""
        self.simplified_expression = result.simplified
        self.simplifier_steps = [
            {
                "number": str(step.number),
                "before": step.before,
                "after": step.after,
                "law": step.law_name,
                "formula": step.formula,
                "explanation": step.explanation,
            }
            for step in result.steps
        ]
        self.simplifier_summary = (
            f"{result.literal_count_before} → {result.literal_count_after} literals; "
            f"{result.term_count_before} → {result.term_count_after} terms"
        )


    def generate_kmap(self) -> None:
        try:
            result = build_kmap(self.expression)
        except BooleanExpressionError as exc:
            self.kmap_error = str(exc)
            self.kmap_row_variables = ""
            self.kmap_column_variables = ""
            self.kmap_facet_variables = ""
            self.kmap_variables_label = ""
            self.kmap_function_label = ""
            self.kmap_row_codes = []
            self.kmap_column_codes = []
            self.kmap_facets = []
            self.kmap_groups = []
            self.kmap_simplified = ""
            return

        self.kmap_error = ""
        self.kmap_row_variables = "".join(result.row_variables)
        self.kmap_column_variables = "".join(result.column_variables)
        self.kmap_facet_variables = "".join(result.facet_variables)
        self.kmap_variables_label = "".join(result.variables)
        self.kmap_function_label = "F(" + ",".join(result.variables) + ")"
        self.kmap_row_codes = result.row_codes
        self.kmap_column_codes = result.column_codes
        self.kmap_facets = serialize_kmap(result)
        self.kmap_groups = [
            {
                "number": str(group.index),
                "term": group.term,
                "minterms": ", ".join(f"m{value}" for value in group.minterms),
                "size": str(group.size),
                "essential": "Essential" if group.essential else "Prime",
                "color": group_color(group.index),
            }
            for group in result.groups
        ]
        self.kmap_simplified = result.simplified_expression

def _group_heading(
    label: str,
    span,
    *,
    background: str,
) -> rx.Component:
    return rx.table.column_header_cell(
        label,
        col_span=span,
        background=background,
        color=COLORS["text"],
        font_size="0.74rem",
        font_weight="900",
        letter_spacing="0.045em",
        text_align="center",
        padding="0.48rem 0.55rem",
        border_bottom=f"1px solid {COLORS['border_strong']}",
        white_space="nowrap",
    )


def _column_heading(
    label,
    *,
    output: bool = False,
    intermediate: bool = False,
) -> rx.Component:
    return rx.table.column_header_cell(
        label,
        background=(
            COLORS["primary_soft"]
            if output
            else COLORS["surface_soft"]
            if intermediate
            else COLORS["table_header"]
        ),
        color=COLORS["text"],
        font_family="monospace",
        font_size="0.76rem",
        font_weight="850",
        text_align="center",
        padding="0.42rem 0.55rem",
        min_width="150px" if output else "105px" if intermediate else "52px",
        max_width="210px" if output else "150px" if intermediate else "58px",
        white_space="nowrap",
    )


def _data_cell(
    value,
    *,
    output: bool = False,
    intermediate: bool = False,
    row_index=None,
) -> rx.Component:
    regular_background = rx.cond(
        row_index % 2 == 0,
        COLORS["table_even"],
        COLORS["table_odd"],
    )

    return rx.table.cell(
        value,
        font_family="monospace",
        font_size="0.77rem",
        font_weight="850" if output else "650",
        color=(
            rx.cond(
                value == "1",
                COLORS["success"],
                COLORS["danger"],
            )
            if output
            else COLORS["text"]
        ),
        background=(
            rx.cond(
                value == "1",
                COLORS["success_soft"],
                COLORS["danger_soft"],
            )
            if output
            else regular_background
        ),
        text_align="center",
        padding="0.34rem 0.5rem",
        min_width="150px" if output else "105px" if intermediate else "52px",
        max_width="210px" if output else "150px" if intermediate else "58px",
        white_space="nowrap",
    )


def _compact_truth_table() -> rx.Component:
    """Render grouped INPUTS / EVALUATION / OUTPUT headings."""

    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _group_heading(
                        "INPUTS",
                        BooleanLabState.variables.length(),
                        background="#DDE8F8",
                    ),
                    rx.cond(
                        BooleanLabState.show_intermediate
                        & (BooleanLabState.intermediate_headers.length() > 0),
                        _group_heading(
                            "EVALUATION",
                            BooleanLabState.intermediate_headers.length(),
                            background="#E9EDF5",
                        ),
                    ),
                    _group_heading(
                        "OUTPUT",
                        1,
                        background="#DDE8F8",
                    ),
                ),
                rx.table.row(
                    rx.foreach(
                        BooleanLabState.variables,
                        lambda variable: _column_heading(variable),
                    ),
                    rx.cond(
                        BooleanLabState.show_intermediate,
                        rx.foreach(
                            BooleanLabState.intermediate_headers,
                            lambda header: _column_heading(
                                header,
                                intermediate=True,
                            ),
                        ),
                    ),
                    _column_heading(
                        "F = " + BooleanLabState.normalized_expression,
                        output=True,
                    ),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    BooleanLabState.rows,
                    lambda row, row_index: rx.table.row(
                        rx.foreach(
                            BooleanLabState.variables,
                            lambda variable: _data_cell(
                                row[variable],
                                row_index=row_index,
                            ),
                        ),
                        rx.cond(
                            BooleanLabState.show_intermediate,
                            rx.foreach(
                                BooleanLabState.intermediate_headers,
                                lambda header: _data_cell(
                                    row[header],
                                    intermediate=True,
                                    row_index=row_index,
                                ),
                            ),
                        ),
                        _data_cell(
                            row["F"],
                            output=True,
                            row_index=row_index,
                        ),
                    )
                )
            ),
            variant="surface",
            size="1",
            width="auto",
            table_layout="auto",
        ),
        width="fit-content",
        max_width="100%",
        max_height="410px",
        overflow="auto",
        margin="0 auto",
        border=f"1px solid {COLORS['border']}",
        border_radius="11px",
        background=COLORS["surface"],
    )



def _mano_kmap_facet(facet: KMapFacetView) -> rx.Component:
    return rx.box(
        rx.cond(
            BooleanLabState.kmap_facet_variables != "",
            rx.vstack(
                rx.text(
                    BooleanLabState.kmap_facet_variables,
                    font_weight="850",
                    color=COLORS["text"],
                ),
                rx.text(
                    facet["code"],
                    font_family="monospace",
                    color=COLORS["text"],
                ),
                spacing="1",
                align="center",
                margin_bottom="0.55rem",
                   ),
                ),
                rx.hstack(
            rx.box(
                width="0",
                min_width="0",
            ),
            rx.vstack(
                rx.hstack(
                    rx.box(width="3.1rem", min_width="3.1rem"),
                    rx.foreach(
                        BooleanLabState.kmap_column_codes,
                        lambda code: rx.box(
                            code,
                            width="4.9rem",
                            text_align="center",
                            font_weight="850",
                            font_family="monospace",
                            color="#111827",
                        ),
                    ),
                    spacing="0",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.foreach(
                            BooleanLabState.kmap_row_codes,
                            lambda code: rx.box(
                                code,
                                width="3.1rem",
                                height="4.4rem",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                font_weight="850",
                                font_family="monospace",
                                color="#111827",
                            ),
                        ),
                        spacing="0",
                    ),
                    rx.box(
                        rx.text(
                            BooleanLabState.kmap_function_label,
                            position="absolute",
                            top="-4.35rem",
                            left="-3.15rem",
                            font_weight="900",
                            font_size="1.05rem",
                            color="#111827",
                            white_space="nowrap",
                        ),
                        rx.text(
                            BooleanLabState.kmap_row_variables,
                            position="absolute",
                            top="-1.55rem",
                            left="-2.55rem",
                            font_weight="900",
                            color="#111827",
                        ),
                        rx.text(
                            BooleanLabState.kmap_column_variables,
                            position="absolute",
                            top="-2.55rem",
                            left="-0.25rem",
                            font_weight="900",
                            color="#111827",
                        ),
                        rx.box(
                            position="absolute",
                            top="-2.25rem",
                            left="-2.25rem",
                            width="3.182rem",
                            border_top="4px solid #111827",
                            transform="rotate(45deg)",
                            transform_origin="left center",
                        ),
                        # Reflection-map fold guides for higher-variable K-maps.
                        # 5 variables: one vertical mirror axis between columns 4 and 5.
                        # 6 variables: vertical + horizontal mirror axes, forming 4 quadrants.
                        rx.cond(
                            BooleanLabState.kmap_column_codes.length() == 8,
                            rx.box(
                                position="absolute",
                                left="calc(19.6rem - 2px)",
                                top="0",
                                height="100%",
                                border_left="4px double #94A3B8",
                                pointer_events="none",
                                z_index="2",
                            ),
                        ),
                        rx.cond(
                            (BooleanLabState.kmap_column_codes.length() == 8)
                            & (BooleanLabState.kmap_row_codes.length() == 8),
                            rx.box(
                                position="absolute",
                                left="0",
                                top="calc(17.6rem - 2px)",
                                width="100%",
                                border_top="4px double #94A3B8",
                                pointer_events="none",
                                z_index="2",
                            ),
                        ),
                        rx.vstack(
                            rx.foreach(
                                facet["rows"],
                                lambda row: rx.hstack(
                                    rx.foreach(
                                        row,
                                        lambda cell: rx.box(
                                            rx.text(
                                                cell["minterm"],
                                                position="absolute",
                                                top="0.2rem",
                                                left="0.3rem",
                                                color="#64748B",
                                                font_size="0.62rem",
                                                font_family="monospace",
                                            ),
                                            rx.text(
                                                cell["value"],
                                                font_size="1.15rem",
                                                font_weight="900",
                                                color=COLORS["text"],
                                            ),
                                            width="4.9rem",
                                            height="4.4rem",
                                            display="flex",
                                            align_items="center",
                                            justify_content="center",
                                            position="relative",
                                            background="#FFFFFF",
                                            border="3px solid #111827",
                                        ),
                                    ),
                                    spacing="0",
                                ),
                            ),
                            spacing="0",
                        ),
                        rx.foreach(
                            facet["segments"],
                            lambda segment: rx.box(
                                position="absolute",
                                left=segment["left"],
                                top=segment["top"],
                                width=segment["width"],
                                height=segment["height"],
                                border_top=segment["border_top"],
                                border_right=segment["border_right"],
                                border_bottom=segment["border_bottom"],
                                border_left=segment["border_left"],
                                border_top_left_radius=segment["radius_top_left"],
                                border_top_right_radius=segment["radius_top_right"],
                                border_bottom_right_radius=segment["radius_bottom_right"],
                                border_bottom_left_radius=segment["radius_bottom_left"],
                                pointer_events="none",
                                z_index="6",
                            ),
                        ),
                        position="relative",
                        width="fit-content",
                        overflow="visible",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="0",
                align="start",
            ),
            spacing="0",
            align="start",
        ),
        padding="4rem 1.2rem 1rem 3.2rem",
        background="#FFFFFF",
        border=f"1px solid {COLORS['border']}",
        border_radius="10px",
        width="fit-content",
        min_width="fit-content",
    )


def _kmap_panel() -> rx.Component:
    return panel(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "FUNCTION REDUCTION · KARNAUGH MAP",
                        color=COLORS["primary"],
                        font_size="0.7rem",
                        font_weight="900",
                        letter_spacing="0.06em",
                    ),
                    rx.heading(
                        "K-map plot & grouping",
                        size="4",
                        color=COLORS["text"],
                    ),
                    rx.text(
                        "Mano-style Gray-code map. Each selected group has a different outline; cells are never colour-filled.",
                        color=COLORS["text_muted"],
                        font_size="0.74rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.badge(
                    "Reduced: F = " + BooleanLabState.kmap_simplified,
                    background=COLORS["success_soft"],
                    color=COLORS["success"],
                ),
                width="100%",
                align="center",
            ),
            rx.cond(
                BooleanLabState.kmap_error != "",
                rx.callout(
                    BooleanLabState.kmap_error,
                    icon="triangle-alert",
                    color_scheme="red",
                    width="100%",
                ),
                rx.vstack(
                    rx.flex(
                        rx.foreach(
                            BooleanLabState.kmap_facets,
                            _mano_kmap_facet,
                        ),
                        wrap="wrap",
                        gap="1.2rem",
                        justify="center",
                        width="100%",
                        overflow_x="auto",
                    ),
                    rx.cond(
                        BooleanLabState.kmap_groups.length() > 0,
                        rx.box(
                            rx.text(
                                "Group combinations",
                                color=COLORS["text"],
                                font_weight="850",
                                margin_bottom="0.65rem",
                            ),
                            rx.flex(
                                rx.foreach(
                                    BooleanLabState.kmap_groups,
                                    lambda group: rx.box(
                                        rx.hstack(
                                            rx.badge(
                                                "G" + group["number"],
                                                background="#FFFFFF",
                                                color=group["color"],
                                                border="1px solid " + group["color"],
                                            ),
                                            rx.text(
                                                group["term"],
                                                font_family="monospace",
                                                font_weight="850",
                                                color=group["color"],
                                            ),
                                            rx.badge(
                                                group["essential"],
                                                background=COLORS["success_soft"],
                                                color=COLORS["success"],
                                            ),
                                            spacing="2",
                                            align="center",
                                        ),
                                        rx.text(
                                            group["minterms"] + "  →  " + group["term"] + " · " + group["size"] + " cells",
                                            color=COLORS["text_muted"],
                                            font_size="0.72rem",
                                            margin_top="0.35rem",
                                        ),
                                        padding="0.75rem",
                                        border="2px solid " + group["color"],
                                        border_radius="9px",
                                        background="#FFFFFF",
                                    ),
                                ),
                                wrap="wrap",
                                gap="0.65rem",
                            ),
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                    align="stretch",
                ),
            ),
            spacing="3",
            width="100%",
            align="stretch",
        )
    )

def boolean_lab() -> rx.Component:
    """Render the Boolean Laboratory page."""

    return rx.box(
        app_header("boolean"),
        rx.box(
            rx.vstack(
                page_intro(
                    "TOOLS LAB · BOOLEAN ENGINE",
                    "Boolean Expression & Truth Table Laboratory",
                    "Generate a compact textbook-style truth table with clearly "
                    "separated input variables and final output.",
                ),
                rx.grid(
                    panel(
                        rx.vstack(
                            rx.heading(
                                "Expression",
                                size="4",
                                color=COLORS["text"],
                            ),
                            rx.text(
                                "Expression input",
                                color=COLORS["text_muted"],
                                font_size="0.72rem",
                            ),
                            rx.input(
                                value=BooleanLabState.expression,
                                on_change=BooleanLabState.set_expression,
                                placeholder="Example: A(B+C')",
                                width="100%",
                                font_family="monospace",
                                background=COLORS["surface_soft"],
                                border=f"1px solid {COLORS['border_strong']}",
                            ),
                            rx.box(
                                rx.text(
                                    "Or enter canonical minterms",
                                    color=COLORS["text_muted"],
                                    font_size="0.75rem",
                                    font_weight="800",
                                    margin_bottom="0.45rem",
                                ),
                                rx.hstack(
                                    rx.hstack(
                                        rx.text(
                                            "Variables",
                                            font_size="0.72rem",
                                            font_weight="800",
                                            color=COLORS["text"],
                                        ),
                                        rx.select(
                                            ["2", "3", "4", "5", "6"],
                                            value=BooleanLabState.minterm_variable_count,
                                            on_change=BooleanLabState.set_minterm_variable_count,
                                            width="5.2rem",
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            "Σm(",
                                            font_family="monospace",
                                            font_weight="900",
                                            font_size="1rem",
                                            color=COLORS["text"],
                                        ),
                                        rx.input(
                                            value=BooleanLabState.minterm_numbers,
                                            on_change=BooleanLabState.set_minterm_numbers,
                                            placeholder="3,5,6,7",
                                            width="12rem",
                                            font_family="monospace",
                                        ),
                                        rx.text(
                                            ")",
                                            font_family="monospace",
                                            font_weight="900",
                                            font_size="1rem",
                                            color=COLORS["text"],
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    secondary_button(
                                        "Use Σm input",
                                        BooleanLabState.generate_from_minterms,
                                    ),
                                    wrap="wrap",
                                    spacing="2",
                                    align="center",
                                ),
                                rx.text(
                                    "Choose 2–6 variables, then type only minterm numbers and commas. The valid range updates with the selected variable count.",
                                    color=COLORS["text_muted"],
                                    font_size="0.68rem",
                                    margin_top="0.35rem",
                                ),
                                rx.cond(
                                    BooleanLabState.minterm_input_error != "",
                                    rx.callout(
                                        BooleanLabState.minterm_input_error,
                                        icon="triangle-alert",
                                        color_scheme="red",
                                        width="100%",
                                        margin_top="0.5rem",
                                    ),
                                ),
                                width="100%",
                                padding="0.7rem",
                                border=f"1px solid {COLORS['border']}",
                                border_radius="10px",
                                background=COLORS["surface_soft"],
                            ),
                            primary_button(
                                "Generate truth table",
                                BooleanLabState.reduce_function,
                            ),
                            secondary_button(
                                "Reduce function + K-map",
                                BooleanLabState.reduce_function,
                            ),
                            rx.hstack(
                                rx.switch(
                                    checked=BooleanLabState.show_intermediate,
                                    on_change=BooleanLabState.set_show_intermediate,
                                    color_scheme="indigo",
                                ),
                                rx.vstack(
                                    rx.text(
                                        "Show evaluation steps",
                                        color=COLORS["text"],
                                        font_size="0.84rem",
                                        font_weight="700",
                                    ),
                                    rx.text(
                                        "Off by default for a standard truth table.",
                                        color=COLORS["text_muted"],
                                        font_size="0.7rem",
                                    ),
                                    spacing="0",
                                    align="start",
                                ),
                                align="center",
                            ),
                            rx.cond(
                                BooleanLabState.error_message != "",
                                rx.callout(
                                    BooleanLabState.error_message,
                                    icon="triangle-alert",
                                    color_scheme="red",
                                    width="100%",
                                ),
                            ),
                            rx.separator(),
                            rx.text(
                                "Examples",
                                color=COLORS["text_muted"],
                                font_size="0.75rem",
                                font_weight="800",
                            ),
                            rx.flex(
                                secondary_button(
                                    "A(B+C')",
                                    lambda: BooleanLabState.load_example("A(B+C')"),
                                ),
                                secondary_button(
                                    "AB + AB'",
                                    lambda: BooleanLabState.load_example("AB + AB'"),
                                ),
                                secondary_button(
                                    "AB + BC + CA",
                                    lambda: BooleanLabState.load_example("AB + BC + CA"),
                                ),
                                secondary_button(
                                    "A ⊕ B",
                                    lambda: BooleanLabState.load_example("A ⊕ B"),
                                ),
                                wrap="wrap",
                                gap="0.45rem",
                            ),
                            rx.separator(),
                            rx.text(
                                "NOT: ' ! ~    AND: adjacency . * &    "
                                "OR: + |    XOR: ^ ⊕",
                                color=COLORS["text_muted"],
                                font_family="monospace",
                                font_size="0.7rem",
                                line_height="1.6",
                            ),
                            align="start",
                            spacing="3",
                            width="100%",
                        )
                    ),
                    rx.vstack(
                        rx.grid(
                            metric_card(
                                "NORMALIZED",
                                BooleanLabState.normalized_expression,
                                compact=True,
                            ),
                            metric_card(
                                "VARIABLES",
                                BooleanLabState.variables.to_string(),
                                compact=True,
                            ),
                            metric_card(
                                "CLASSIFICATION",
                                BooleanLabState.classification,
                                compact=True,
                            ),
                            metric_card(
                                "MINTERMS",
                                BooleanLabState.minterm_text,
                                compact=True,
                            ),
                            columns=rx.breakpoints(
                                initial="1",
                                sm="2",
                                xl="4",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        panel(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Truth table",
                                        size="4",
                                        color=COLORS["text"],
                                    ),
                                    rx.spacer(),
                                    rx.badge(
                                        BooleanLabState.rows.length().to_string()
                                        + " rows",
                                        background=COLORS["success_soft"],
                                        color=COLORS["success"],
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                rx.text(
                                    "Input columns stay narrow; the output column "
                                    "shows the complete function.",
                                    color=COLORS["text_muted"],
                                    font_size="0.75rem",
                                ),
                                _compact_truth_table(),
                                spacing="3",
                                width="100%",
                                align="stretch",
                            )
                        ),
                        panel(
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            "BOOLEAN SIMPLIFIER",
                                            color=COLORS["primary"],
                                            font_size="0.7rem",
                                            font_weight="900",
                                            letter_spacing="0.06em",
                                        ),
                                        rx.heading(
                                            "Step-by-step minimum SOP",
                                            size="4",
                                            color=COLORS["text"],
                                        ),
                                        spacing="1",
                                        align="start",
                                    ),
                                    rx.spacer(),
                                    rx.badge(
                                        BooleanLabState.simplifier_summary,
                                        background=COLORS["primary_soft"],
                                        color=COLORS["primary"],
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                rx.cond(
                                    BooleanLabState.simplifier_error != "",
                                    rx.callout(
                                        BooleanLabState.simplifier_error,
                                        icon="triangle-alert",
                                        color_scheme="red",
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        metric_card(
                                            "SIMPLIFIED RESULT",
                                            BooleanLabState.simplified_expression,
                                            compact=False,
                                        ),
                                        rx.foreach(
                                            BooleanLabState.simplifier_steps,
                                            lambda step: rx.box(
                                                rx.hstack(
                                                    rx.box(
                                                        step["number"],
                                                        width="1.7rem",
                                                        height="1.7rem",
                                                        display="flex",
                                                        align_items="center",
                                                        justify_content="center",
                                                        border_radius="999px",
                                                        background=COLORS["primary"],
                                                        color="white",
                                                        font_weight="900",
                                                        font_size="0.72rem",
                                                    ),
                                                    rx.vstack(
                                                        rx.hstack(
                                                            rx.text(
                                                                step["law"],
                                                                color=COLORS["text"],
                                                                font_weight="850",
                                                            ),
                                                            rx.badge(
                                                                step["formula"],
                                                                background=COLORS["surface_soft"],
                                                                color=COLORS["text_muted"],
                                                            ),
                                                            spacing="2",
                                                            align="center",
                                                        ),
                                                        rx.text(
                                                            step["before"] + "  →  " + step["after"],
                                                            color=COLORS["primary"],
                                                            font_family="monospace",
                                                            font_weight="750",
                                                            overflow_wrap="anywhere",
                                                        ),
                                                        rx.text(
                                                            step["explanation"],
                                                            color=COLORS["text_muted"],
                                                            font_size="0.78rem",
                                                            line_height="1.55",
                                                        ),
                                                        spacing="1",
                                                        align="start",
                                                        width="100%",
                                                    ),
                                                    spacing="3",
                                                    align="start",
                                                    width="100%",
                                                ),
                                                padding="0.85rem",
                                                border=f"1px solid {COLORS['border']}",
                                                border_radius="11px",
                                                background=COLORS["surface_soft"],
                                                width="100%",
                                            ),
                                        ),
                                        width="100%",
                                        spacing="3",
                                        align="stretch",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                                align="stretch",
                            )
                        ),
                        _kmap_panel(),
                        panel(
                            rx.vstack(
                                rx.heading(
                                    "Canonical forms",
                                    size="4",
                                    color=COLORS["text"],
                                ),
                                rx.grid(
                                    metric_card(
                                        "CANONICAL SOP",
                                        BooleanLabState.canonical_sop,
                                        compact=True,
                                    ),
                                    metric_card(
                                        "CANONICAL POS",
                                        BooleanLabState.canonical_pos,
                                        compact=True,
                                    ),
                                    columns=rx.breakpoints(initial="1", lg="2"),
                                    spacing="3",
                                    width="100%",
                                ),
                                spacing="3",
                                width="100%",
                                align="stretch",
                            )
                        ),
                        width="100%",
                        spacing="4",
                        align="stretch",
                    ),
                    columns=rx.breakpoints(initial="1", lg="290px 1fr"),
                    spacing="4",
                    width="100%",
                    align_items="start",
                ),
                spacing="5",
                width="100%",
                align="stretch",
            ),
            max_width="82rem",
            margin="0 auto",
            padding="2rem 1.25rem 3rem",
        ),
        min_height="100vh",
        background=COLORS["page"],
        on_mount=BooleanLabState.on_load,
    )
