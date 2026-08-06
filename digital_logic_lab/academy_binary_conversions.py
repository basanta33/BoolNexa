"""BoolNexa Academy Path 01 conversion lessons."""

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


class BinaryConversionState(rx.State):
    decimal_value: str = "45"
    binary_answer: str = ""
    binary_feedback: str = ""
    binary_quiz: str = ""
    binary_quiz_feedback: str = ""

    binary_value: str = "101101"
    decimal_answer: str = ""
    decimal_feedback: str = ""
    decimal_quiz: str = ""
    decimal_quiz_feedback: str = ""

    def set_binary_answer(self, value: str) -> None:
        self.binary_answer = value

    def set_binary_quiz(self, value: str) -> None:
        self.binary_quiz = value

    def set_binary_value(self, value: str) -> None:
        self.binary_value = value

    def set_decimal_answer(self, value: str) -> None:
        self.decimal_answer = value

    def set_decimal_quiz(self, value: str) -> None:
        self.decimal_quiz = value

    def set_decimal_value(self, value: str) -> None:
        self.decimal_value = value

    def check_decimal_to_binary(self):
        try:
            value = int(self.decimal_value)
            if not 0 <= value <= 255:
                self.binary_feedback = "Use a whole number from 0 to 255."
                return
            expected = format(value, "b")
            cleaned = self.binary_answer.strip().replace(" ", "")
            self.binary_feedback = (
                f"Correct. {value}₁₀ = {expected}₂."
                if cleaned == expected
                else f"Not yet. Repeated division by 2 gives {expected}₂."
            )
        except ValueError:
            self.binary_feedback = "Enter a valid decimal whole number."

    def check_decimal_binary_quiz(self):
        cleaned = self.binary_quiz.strip().replace(" ", "")
        self.binary_quiz_feedback = (
            "Correct. 26₁₀ = 11010₂."
            if cleaned == "11010"
            else "Try again. Divide 26 repeatedly by 2 and read the remainders upward."
        )

    def check_binary_to_decimal(self):
        cleaned = self.binary_value.strip().replace(" ", "")
        if not cleaned or any(ch not in "01" for ch in cleaned):
            self.decimal_feedback = "Enter a binary number using only 0 and 1."
            return
        expected = int(cleaned, 2)
        self.decimal_feedback = (
            f"Correct. {cleaned}₂ = {expected}₁₀."
            if self.decimal_answer.strip() == str(expected)
            else f"Not yet. Add the active powers of two: the answer is {expected}."
        )

    def check_binary_decimal_quiz(self):
        self.decimal_quiz_feedback = (
            "Correct. 110101₂ = 53₁₀."
            if self.decimal_quiz.strip() == "53"
            else "Try again: 32 + 16 + 4 + 1 = ?"
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


def _weights_visual(bits: str) -> rx.Component:
    weights = [2 ** power for power in range(len(bits) - 1, -1, -1)]
    return rx.hstack(
        *[
            rx.box(
                rx.vstack(
                    rx.text(bit, size="5", weight="bold"),
                    rx.text(str(weight), size="2", color="#64748b"),
                    spacing="1",
                    align="center",
                ),
                border="1px solid #cbd5e1",
                border_radius="10px",
                padding="10px 14px",
                min_width="58px",
            )
            for bit, weight in zip(bits, weights)
        ],
        wrap="wrap",
        spacing="2",
    )


def decimal_to_binary_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 03", color_scheme="blue"),
            rx.heading("Decimal to Binary", size="8"),
            rx.text(
                "Convert decimal whole numbers to binary using repeated division by 2 "
                "and positional weights.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Learning objectives",
                rx.text("By the end of this lesson you should be able to:"),
                rx.unordered_list(
                    rx.list_item("explain why division by 2 produces binary digits;"),
                    rx.list_item("convert decimal integers to binary;"),
                    rx.list_item("check a result using powers of two."),
                ),
            ),
            _section(
                "2", "Method: repeated division by 2",
                rx.text(
                    "Divide the decimal number by 2. Record each remainder. Continue "
                    "with the quotient until it reaches zero. Read the remainders from "
                    "bottom to top."
                ),
                rx.code_block(
                    "45 ÷ 2 = 22 remainder 1\n"
                    "22 ÷ 2 = 11 remainder 0\n"
                    "11 ÷ 2 =  5 remainder 1\n"
                    " 5 ÷ 2 =  2 remainder 1\n"
                    " 2 ÷ 2 =  1 remainder 0\n"
                    " 1 ÷ 2 =  0 remainder 1\n\n"
                    "Read upward → 101101₂",
                    language="markup",
                ),
                rx.callout("Therefore 45₁₀ = 101101₂.", icon="circle-check", color_scheme="green"),
            ),
            _section(
                "3", "Check with positional weights",
                _weights_visual("101101"),
                rx.text("32 + 8 + 4 + 1 = 45", weight="bold"),
            ),
            _section(
                "4", "Interactive practice",
                rx.text("Choose a decimal value from 0 to 255 and convert it yourself."),
                rx.hstack(
                    rx.input(
                        value=BinaryConversionState.decimal_value,
                        on_change=BinaryConversionState.set_decimal_value,
                        placeholder="Decimal value",
                        max_width="180px",
                    ),
                    rx.input(
                        value=BinaryConversionState.binary_answer,
                        on_change=BinaryConversionState.set_binary_answer,
                        placeholder="Your binary answer",
                        max_width="240px",
                    ),
                    rx.button("Check", on_click=BinaryConversionState.check_decimal_to_binary),
                    wrap="wrap",
                ),
                rx.cond(
                    BinaryConversionState.binary_feedback != "",
                    rx.callout(BinaryConversionState.binary_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Quick check",
                rx.text("Convert 26₁₀ to binary."),
                rx.hstack(
                    rx.input(
                        value=BinaryConversionState.binary_quiz,
                        on_change=BinaryConversionState.set_binary_quiz,
                        placeholder="Binary answer",
                        max_width="220px",
                    ),
                    rx.button("Submit", on_click=BinaryConversionState.check_decimal_binary_quiz),
                ),
                rx.cond(
                    BinaryConversionState.binary_quiz_feedback != "",
                    rx.callout(BinaryConversionState.binary_quiz_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "Practice in BoolNexa",
                rx.text(
                    "Open the real Number System Laboratory and verify several decimal-to-binary conversions."
                ),
                rx.link(
                    rx.button("Open Number System Laboratory", color_scheme="blue"),
                    href="/tools/number-systems",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Binary place value", variant="soft"), href="/academy/unit-1/binary-place-value"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 3 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-1/binary-to-decimal"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def binary_to_decimal_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 04", color_scheme="blue"),
            rx.heading("Binary to Decimal", size="8"),
            rx.text(
                "Translate a binary number into decimal by adding the positional "
                "weights of every bit that is 1.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Learning objectives",
                rx.unordered_list(
                    rx.list_item("identify the weight of each binary position;"),
                    rx.list_item("expand a binary number as powers of two;"),
                    rx.list_item("convert binary integers to decimal accurately."),
                ),
            ),
            _section(
                "2", "Worked example: 101101₂",
                _weights_visual("101101"),
                rx.code_block(
                    "101101₂\n"
                    "= 1×2⁵ + 0×2⁴ + 1×2³ + 1×2² + 0×2¹ + 1×2⁰\n"
                    "= 32 + 0 + 8 + 4 + 0 + 1\n"
                    "= 45₁₀",
                    language="markup",
                ),
            ),
            _section(
                "3", "Why the method works",
                rx.text(
                    "Binary is a positional number system. Moving one place to the "
                    "left doubles the place value: 1, 2, 4, 8, 16, 32, 64, ..."
                ),
                rx.callout(
                    "Only positions containing 1 contribute to the decimal total.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "4", "Interactive practice",
                rx.hstack(
                    rx.input(
                        value=BinaryConversionState.binary_value,
                        on_change=BinaryConversionState.set_binary_value,
                        placeholder="Binary value",
                        max_width="220px",
                    ),
                    rx.input(
                        value=BinaryConversionState.decimal_answer,
                        on_change=BinaryConversionState.set_decimal_answer,
                        placeholder="Decimal answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=BinaryConversionState.check_binary_to_decimal),
                    wrap="wrap",
                ),
                rx.cond(
                    BinaryConversionState.decimal_feedback != "",
                    rx.callout(BinaryConversionState.decimal_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Quick check",
                rx.text("What is 110101₂ in decimal?"),
                rx.hstack(
                    rx.input(
                        value=BinaryConversionState.decimal_quiz,
                        on_change=BinaryConversionState.set_decimal_quiz,
                        placeholder="Decimal answer",
                        max_width="220px",
                    ),
                    rx.button("Submit", on_click=BinaryConversionState.check_binary_decimal_quiz),
                ),
                rx.cond(
                    BinaryConversionState.decimal_quiz_feedback != "",
                    rx.callout(BinaryConversionState.decimal_quiz_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "Use the real laboratory",
                rx.text(
                    "Verify your conversions in Number Systems, then try values with more bits."
                ),
                rx.link(
                    rx.button("Open Number System Laboratory", color_scheme="blue"),
                    href="/tools/number-systems",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Decimal to binary", variant="soft"), href="/academy/unit-1/decimal-to-binary"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 4 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-1/octal-and-hexadecimal"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
