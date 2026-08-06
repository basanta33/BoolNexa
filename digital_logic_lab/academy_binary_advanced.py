"""BoolNexa Academy Path 01 advanced binary-system lessons."""

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


class BinaryAdvancedState(rx.State):
    hex_answer: str = ""
    hex_feedback: str = ""
    octal_answer: str = ""
    octal_feedback: str = ""

    add_answer: str = ""
    add_feedback: str = ""
    subtract_answer: str = ""
    subtract_feedback: str = ""

    def set_add_answer(self, value: str) -> None:
        self.add_answer = value

    def set_hex_answer(self, value: str) -> None:
        self.hex_answer = value

    def set_octal_answer(self, value: str) -> None:
        self.octal_answer = value

    def set_subtract_answer(self, value: str) -> None:
        self.subtract_answer = value

    def check_hex(self):
        cleaned = self.hex_answer.strip().upper().replace(" ", "")
        self.hex_feedback = (
            "Correct. 11101101₂ = ED₁₆."
            if cleaned == "ED"
            else "Try again. Group from the right: 1110 1101 → E D."
        )

    def check_octal(self):
        cleaned = self.octal_answer.strip().replace(" ", "")
        self.octal_feedback = (
            "Correct. 101110₂ = 56₈."
            if cleaned == "56"
            else "Try again. Group in threes: 101 110 → 5 6."
        )

    def check_addition(self):
        cleaned = self.add_answer.strip().replace(" ", "")
        self.add_feedback = (
            "Correct. 1011₂ + 0110₂ = 10001₂."
            if cleaned == "10001"
            else "Not yet. Add from the right and carry whenever a column totals 2 or 3."
        )

    def check_subtraction(self):
        cleaned = self.subtract_answer.strip().replace(" ", "")
        self.subtract_feedback = (
            "Correct. 11010₂ − 00111₂ = 10011₂."
            if cleaned == "10011"
            else "Try again. Borrow 1 from the next binary place when 0 − 1 occurs."
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


def _digit_group(bits: str, label: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(bits, font_family="monospace", size="5", weight="bold"),
            rx.text(label, size="2", color="#64748b"),
            spacing="1",
            align="center",
        ),
        padding="12px 18px",
        border="1px solid #cbd5e1",
        border_radius="12px",
        min_width="95px",
    )


def octal_hex_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 05", color_scheme="blue"),
            rx.heading("Octal & Hexadecimal", size="8"),
            rx.text(
                "Learn why engineers use octal and hexadecimal as compact shorthand "
                "for long binary patterns.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Why use octal and hexadecimal?",
                rx.text(
                    "Binary is ideal for digital hardware but long binary strings are "
                    "hard to read. Octal compresses every 3 binary bits into one digit. "
                    "Hexadecimal compresses every 4 binary bits into one digit."
                ),
                rx.hstack(
                    _digit_group("101", "octal digit 5"),
                    _digit_group("1101", "hex digit D"),
                    wrap="wrap",
                ),
            ),
            _section(
                "2",
                "Binary ↔ Octal",
                rx.text("Group binary digits in sets of three from the right."),
                rx.code_block(
                    "101110₂\n"
                    "101 110\n"
                    " 5   6\n\n"
                    "101110₂ = 56₈",
                    language="markup",
                ),
                rx.text(
                    "If the leftmost group has fewer than 3 bits, pad it with leading zeros."
                ),
            ),
            _section(
                "3",
                "Binary ↔ Hexadecimal",
                rx.text(
                    "Group binary digits in sets of four. Hexadecimal digits after 9 "
                    "continue as A, B, C, D, E and F."
                ),
                rx.code_block(
                    "11101101₂\n"
                    "1110 1101\n"
                    "  E    D\n\n"
                    "11101101₂ = ED₁₆",
                    language="markup",
                ),
                rx.callout(
                    "A=10, B=11, C=12, D=13, E=14, F=15",
                    icon="info",
                ),
            ),
            _section(
                "4",
                "Quick practice: hexadecimal",
                rx.text("Convert 11101101₂ to hexadecimal."),
                rx.hstack(
                    rx.input(
                        value=BinaryAdvancedState.hex_answer,
                        on_change=BinaryAdvancedState.set_hex_answer,
                        placeholder="Hex answer",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=BinaryAdvancedState.check_hex),
                ),
                rx.cond(
                    BinaryAdvancedState.hex_feedback != "",
                    rx.callout(BinaryAdvancedState.hex_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Quick practice: octal",
                rx.text("Convert 101110₂ to octal."),
                rx.hstack(
                    rx.input(
                        value=BinaryAdvancedState.octal_answer,
                        on_change=BinaryAdvancedState.set_octal_answer,
                        placeholder="Octal answer",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=BinaryAdvancedState.check_octal),
                ),
                rx.cond(
                    BinaryAdvancedState.octal_feedback != "",
                    rx.callout(BinaryAdvancedState.octal_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6",
                "Practice in BoolNexa",
                rx.text(
                    "Use the Number System Laboratory to convert several binary, octal "
                    "and hexadecimal values and compare its worked steps."
                ),
                rx.link(
                    rx.button("Open Number System Laboratory", color_scheme="blue"),
                    href="/tools/number-systems",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Binary to decimal", variant="soft"),
                    href="/academy/unit-1/binary-to-decimal",
                ),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 5 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-1/binary-arithmetic",
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


def binary_arithmetic_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 06", color_scheme="blue"),
            rx.heading("Binary Arithmetic", size="8"),
            rx.text(
                "Apply the same column-by-column ideas used in decimal arithmetic, "
                "but with only the digits 0 and 1.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "Binary addition rules",
                rx.code_block(
                    "0 + 0 = 0\n"
                    "0 + 1 = 1\n"
                    "1 + 0 = 1\n"
                    "1 + 1 = 10  (sum 0, carry 1)\n"
                    "1 + 1 + 1 = 11  (sum 1, carry 1)",
                    language="markup",
                ),
            ),
            _section(
                "2",
                "Worked addition",
                rx.code_block(
                    "   1011\n"
                    " + 0110\n"
                    " ------\n"
                    "  10001\n\n"
                    "11₁₀ + 6₁₀ = 17₁₀",
                    language="markup",
                ),
                rx.callout(
                    "A carry occurs whenever a column total is 2 or 3.",
                    icon="lightbulb",
                    color_scheme="amber",
                ),
            ),
            _section(
                "3",
                "Binary subtraction and borrowing",
                rx.text(
                    "When a column contains 0 − 1, borrow from the next position to the left. "
                    "In binary, borrowing 1 gives 10₂ in the current column."
                ),
                rx.code_block(
                    "   11010\n"
                    " - 00111\n"
                    " -------\n"
                    "   10011\n\n"
                    "26₁₀ − 7₁₀ = 19₁₀",
                    language="markup",
                ),
            ),
            _section(
                "4",
                "Practice addition",
                rx.text("Calculate 1011₂ + 0110₂."),
                rx.hstack(
                    rx.input(
                        value=BinaryAdvancedState.add_answer,
                        on_change=BinaryAdvancedState.set_add_answer,
                        placeholder="Binary result",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=BinaryAdvancedState.check_addition),
                ),
                rx.cond(
                    BinaryAdvancedState.add_feedback != "",
                    rx.callout(BinaryAdvancedState.add_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Practice subtraction",
                rx.text("Calculate 11010₂ − 00111₂."),
                rx.hstack(
                    rx.input(
                        value=BinaryAdvancedState.subtract_answer,
                        on_change=BinaryAdvancedState.set_subtract_answer,
                        placeholder="Binary result",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=BinaryAdvancedState.check_subtraction),
                ),
                rx.cond(
                    BinaryAdvancedState.subtract_feedback != "",
                    rx.callout(BinaryAdvancedState.subtract_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "6",
                "Connect arithmetic to digital circuits",
                rx.text(
                    "Binary addition is implemented by half adders and full adders. "
                    "After practising the arithmetic, open the Simulator and explore "
                    "the adder components in MSI/LSI."
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Open Simulator", color_scheme="blue"),
                        href="/",
                    ),
                    rx.link(
                        rx.button("Open Number Systems", variant="soft"),
                        href="/tools/number-systems",
                    ),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Octal & hexadecimal", variant="soft"),
                    href="/academy/unit-1/octal-and-hexadecimal",
                ),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 6 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-1/signed-binary",
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
