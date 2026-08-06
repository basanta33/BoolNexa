"""BoolNexa Tools Lab — exact Number System Laboratory."""

from __future__ import annotations

import reflex as rx

from .conversion_engine import ConversionError, convert_all, group_binary
from .explanation_engine import build_explanation
from .validators import validate_precision, validate_source_base
from .ui import COLORS, app_header


BASE_OPTIONS = ["Binary (2)", "Octal (8)", "Decimal (10)", "Hexadecimal (16)"]
BASE_VALUE_MAP = {
    "Binary (2)": 2,
    "Octal (8)": 8,
    "Decimal (10)": 10,
    "Hexadecimal (16)": 16,
}


class NumberSystemLabState(rx.State):
    """Interactive state for exact integer and fractional conversion."""

    source_base_label: str = "Hexadecimal (16)"
    input_value: str = "2FD34.2FF"
    precision_text: str = "32"

    binary_value: str = ""
    grouped_binary_value: str = ""
    octal_value: str = ""
    decimal_value: str = ""
    hexadecimal_value: str = ""

    error_message: str = ""
    explanation_steps: list[str] = []
    show_steps: bool = True

    def on_load(self) -> None:
        self.convert()

    def set_source_base(self, value: str) -> None:
        self.source_base_label = value
        self.convert()

    def set_input_value(self, value: str) -> None:
        self.input_value = value
        self.convert()

    def set_precision_text(self, value: str) -> None:
        self.precision_text = value

    def apply_precision(self) -> None:
        self.convert()

    def toggle_steps(self) -> None:
        self.show_steps = not self.show_steps

    def load_example(self, value: str, base_label: str) -> None:
        self.source_base_label = base_label
        self.input_value = value
        self.convert()

    def convert(self) -> None:
        try:
            source_base = validate_source_base(
                BASE_VALUE_MAP.get(self.source_base_label, 16)
            )
            precision = validate_precision(self.precision_text)
            bundle = convert_all(self.input_value, source_base, precision)
        except ConversionError as exc:
            self.error_message = str(exc)
            self.binary_value = ""
            self.grouped_binary_value = ""
            self.octal_value = ""
            self.decimal_value = ""
            self.hexadecimal_value = ""
            self.explanation_steps = []
            return

        self.error_message = ""
        self.binary_value = bundle.binary
        self.grouped_binary_value = group_binary(bundle.binary)
        self.octal_value = bundle.octal
        self.decimal_value = bundle.decimal
        self.hexadecimal_value = bundle.hexadecimal
        self.explanation_steps = build_explanation(bundle)


def _result_card(title: str, value: rx.Var | str, subtitle: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(title, color="#94a3b8", font_size="0.78rem", font_weight="700"),
            rx.spacer(),
            rx.text(subtitle, color="#64748b", font_size="0.72rem"),
            width="100%",
        ),
        rx.text(
            value,
            color="#f8fafc",
            font_family="monospace",
            font_size="1.03rem",
            font_weight="700",
            overflow_wrap="anywhere",
            margin_top="0.65rem",
            line_height="1.6",
        ),
        padding="1rem",
        background="#111827",
        border="1px solid #2b374a",
        border_radius="0.8rem",
        min_height="7rem",
    )


def _example_button(label: str, value: str, base_label: str) -> rx.Component:
    return rx.button(
        label,
        on_click=lambda: NumberSystemLabState.load_example(value, base_label),
        size="2",
        variant="soft",
        color_scheme="gray",
        cursor="pointer",
    )


def number_system_lab() -> rx.Component:
    """Render the Number System Laboratory page."""

    return rx.box(
        app_header("numbers"),
        rx.box(
            rx.vstack(
                rx.badge(
                    "TOOLS LAB • NUMBER SYSTEMS",
                    color_scheme="orange",
                    variant="soft",
                    size="2",
                ),
                rx.heading(
                    "Exact Number System Laboratory",
                    size="8",
                    color="#f8fafc",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    "Convert integers and fractional values among binary, octal, "
                    "decimal and hexadecimal—with exact arithmetic and teaching steps.",
                    color="#aab6c8",
                    max_width="54rem",
                    line_height="1.7",
                ),
                align="start",
                spacing="3",
                width="100%",
            ),
            padding="2.2rem 1.4rem 1rem",
            max_width="82rem",
            margin="0 auto",
        ),
        rx.box(
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.heading("Input", size="5", color="#f8fafc"),
                        rx.text("Source number system", color="#94a3b8", font_size="0.8rem"),
                        rx.select(
                            BASE_OPTIONS,
                            value=NumberSystemLabState.source_base_label,
                            on_change=NumberSystemLabState.set_source_base,
                            width="100%",
                        ),
                        rx.text("Value", color="#94a3b8", font_size="0.8rem"),
                        rx.input(
                            value=NumberSystemLabState.input_value,
                            on_change=NumberSystemLabState.set_input_value,
                            placeholder="Example: 2FD34.2FF",
                            size="3",
                            width="100%",
                            font_family="monospace",
                        ),
                        rx.text(
                            "Fractional output precision",
                            color="#94a3b8",
                            font_size="0.8rem",
                        ),
                        rx.hstack(
                            rx.input(
                                value=NumberSystemLabState.precision_text,
                                on_change=NumberSystemLabState.set_precision_text,
                                width="7rem",
                                type="number",
                                min_="1",
                                max_="128",
                            ),
                            rx.button(
                                "Apply",
                                on_click=NumberSystemLabState.apply_precision,
                                color_scheme="orange",
                                cursor="pointer",
                            ),
                        ),
                        rx.cond(
                            NumberSystemLabState.error_message != "",
                            rx.callout(
                                NumberSystemLabState.error_message,
                                icon="triangle-alert",
                                color_scheme="red",
                                width="100%",
                            ),
                        ),
                        rx.separator(),
                        rx.text("Try an example", color="#94a3b8", font_size="0.8rem"),
                        rx.flex(
                            _example_button("Hex fraction", "2FD34.2FF", "Hexadecimal (16)"),
                            _example_button("Binary fraction", "101101.101", "Binary (2)"),
                            _example_button("Octal fraction", "734.125", "Octal (8)"),
                            _example_button("Large integer", "FFFFFFFFFFFFFFFF", "Hexadecimal (16)"),
                            wrap="wrap",
                            gap="0.5rem",
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                    padding="1.25rem",
                    background="#172033",
                    border="1px solid #2b374a",
                    border_radius="1rem",
                    height="fit-content",
                ),
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Live conversion", size="5", color="#f8fafc"),
                            rx.spacer(),
                            rx.badge("Exact rational engine", color_scheme="green"),
                            width="100%",
                        ),
                        rx.grid(
                            _result_card(
                                "BINARY",
                                NumberSystemLabState.grouped_binary_value,
                                "base 2",
                            ),
                            _result_card(
                                "OCTAL",
                                NumberSystemLabState.octal_value,
                                "base 8",
                            ),
                            _result_card(
                                "DECIMAL",
                                NumberSystemLabState.decimal_value,
                                "base 10",
                            ),
                            _result_card(
                                "HEXADECIMAL",
                                NumberSystemLabState.hexadecimal_value,
                                "base 16",
                            ),
                            columns=rx.breakpoints(initial="1", md="2"),
                            spacing="3",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.heading("Step-by-step explanation", size="5", color="#f8fafc"),
                            rx.spacer(),
                            rx.button(
                                rx.cond(
                                    NumberSystemLabState.show_steps,
                                    "Hide steps",
                                    "Show steps",
                                ),
                                on_click=NumberSystemLabState.toggle_steps,
                                variant="soft",
                                color_scheme="orange",
                                cursor="pointer",
                            ),
                            width="100%",
                        ),
                        rx.cond(
                            NumberSystemLabState.show_steps,
                            rx.vstack(
                                rx.foreach(
                                    NumberSystemLabState.explanation_steps,
                                    lambda step, index: rx.hstack(
                                        rx.box(
                                            index + 1,
                                            min_width="1.7rem",
                                            height="1.7rem",
                                            display="flex",
                                            align_items="center",
                                            justify_content="center",
                                            border_radius="999px",
                                            background="#ff5a1f",
                                            color="white",
                                            font_size="0.75rem",
                                            font_weight="800",
                                        ),
                                        rx.text(
                                            step,
                                            color="#dbe4f0",
                                            font_family="monospace",
                                            overflow_wrap="anywhere",
                                        ),
                                        align="start",
                                        width="100%",
                                        spacing="3",
                                    ),
                                ),
                                width="100%",
                                align="start",
                                spacing="3",
                                padding="1rem",
                                background="#111827",
                                border="1px solid #2b374a",
                                border_radius="0.8rem",
                            ),
                        ),
                        spacing="4",
                        align="start",
                        width="100%",
                    ),
                    padding="1.25rem",
                    background="#172033",
                    border="1px solid #2b374a",
                    border_radius="1rem",
                ),
                columns=rx.breakpoints(initial="1", lg="320px 1fr"),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            max_width="82rem",
            margin="0 auto",
            padding="1rem 1.4rem 3rem",
        ),
        min_height="100vh",
        background="#0b1120",
        on_mount=NumberSystemLabState.on_load,
    )
