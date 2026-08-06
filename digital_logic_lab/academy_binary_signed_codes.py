"""BoolNexa Academy Path 01 lessons 7 and 8."""

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


class SignedCodesState(rx.State):
    twos_answer: str = ""
    twos_feedback: str = ""
    range_answer: str = ""
    range_feedback: str = ""
    bcd_answer: str = ""
    bcd_feedback: str = ""
    gray_answer: str = ""
    gray_feedback: str = ""

    def set_bcd_answer(self, value: str) -> None:
        self.bcd_answer = value

    def set_gray_answer(self, value: str) -> None:
        self.gray_answer = value

    def set_range_answer(self, value: str) -> None:
        self.range_answer = value

    def set_twos_answer(self, value: str) -> None:
        self.twos_answer = value

    def check_twos(self):
        value = self.twos_answer.strip().replace(" ", "")
        self.twos_feedback = (
            "Correct. +13 = 00001101, invert → 11110010, add 1 → 11110011."
            if value == "11110011"
            else "Try again: write +13 in 8 bits, invert every bit, then add 1."
        )

    def check_range(self):
        value = self.range_answer.strip().replace(" ", "").replace("−", "-")
        self.range_feedback = (
            "Correct. An 8-bit two's-complement number represents −128 to +127."
            if value in {"-128to127", "-128..127", "-128,127"}
            else "Remember: n-bit two's complement ranges from −2^(n−1) to 2^(n−1)−1."
        )

    def check_bcd(self):
        value = self.bcd_answer.strip().replace(" ", "")
        self.bcd_feedback = (
            "Correct. Decimal 59 is encoded digit-by-digit: 5 → 0101 and 9 → 1001."
            if value == "01011001"
            else "BCD encodes each decimal digit separately. Encode 5, then encode 9."
        )

    def check_gray(self):
        value = self.gray_answer.strip().replace(" ", "")
        self.gray_feedback = (
            "Correct. 1011₂ converts to Gray code 1110."
            if value == "1110"
            else "Keep the MSB. Each next Gray bit is the XOR of adjacent binary bits."
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


def signed_binary_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 07", color_scheme="blue"),
            rx.heading("Signed Binary & Complements", size="8"),
            rx.text(
                "Learn how digital systems represent positive and negative integers, "
                "and why two's complement is the standard representation for signed arithmetic.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Unsigned versus signed binary",
                rx.text(
                    "With 8 unsigned bits, all 256 patterns represent 0 to 255. "
                    "With 8-bit two's complement, the same 256 patterns represent −128 to +127."
                ),
                rx.code_block(
                    "Unsigned 8-bit:       00000000 → 0      ... 11111111 → 255\n"
                    "Two's complement:     00000000 → 0      ... 01111111 → +127\n"
                    "                      10000000 → −128   ... 11111111 → −1",
                    language="markup",
                ),
            ),
            _section(
                "2", "One's complement and two's complement",
                rx.text(
                    "One's complement flips every bit. Two's complement flips every bit "
                    "and then adds 1. Two's complement avoids separate +0 and −0 representations."
                ),
                rx.code_block(
                    "+13 in 8 bits       00001101\n"
                    "invert bits          11110010   ← one's complement\n"
                    "add 1                11110011   ← two's complement = −13",
                    language="markup",
                ),
                rx.callout(
                    "To recover the magnitude of a negative two's-complement value, invert the bits and add 1.",
                    icon="lightbulb", color_scheme="amber",
                ),
            ),
            _section(
                "3", "Range of an n-bit signed number",
                rx.text("For n-bit two's complement:"),
                rx.code_block("minimum = −2^(n−1)\nmaximum = 2^(n−1) − 1", language="markup"),
                rx.text("Example: 8 bits → −128 to +127; 16 bits → −32768 to +32767."),
            ),
            _section(
                "4", "Practice: represent −13",
                rx.text("Write −13 as an 8-bit two's-complement number."),
                rx.hstack(
                    rx.input(
                        value=SignedCodesState.twos_answer,
                        on_change=SignedCodesState.set_twos_answer,
                        placeholder="8-bit answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=SignedCodesState.check_twos),
                ),
                rx.cond(
                    SignedCodesState.twos_feedback != "",
                    rx.callout(SignedCodesState.twos_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Quick check",
                rx.text("What decimal range can an 8-bit two's-complement number represent?"),
                rx.hstack(
                    rx.input(
                        value=SignedCodesState.range_answer,
                        on_change=SignedCodesState.set_range_answer,
                        placeholder="-128 to 127",
                        max_width="220px",
                    ),
                    rx.button("Submit", on_click=SignedCodesState.check_range),
                ),
                rx.cond(
                    SignedCodesState.range_feedback != "",
                    rx.callout(SignedCodesState.range_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "Practise with BoolNexa",
                rx.text(
                    "Use Number Systems to inspect binary representations and reinforce "
                    "the relationship between decimal values and fixed-width bit patterns."
                ),
                rx.link(
                    rx.button("Open Number System Laboratory", color_scheme="blue"),
                    href="/tools/number-systems",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Binary arithmetic", variant="soft"), href="/academy/unit-1/binary-arithmetic"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 7 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-1/digital-codes"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def digital_codes_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 08", color_scheme="blue"),
            rx.heading("Digital Codes", size="8"),
            rx.text(
                "Binary patterns can represent much more than ordinary numbers. "
                "Explore BCD, Gray code and character encoding.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Binary-Coded Decimal (BCD)",
                rx.text(
                    "BCD represents each decimal digit separately using four bits. "
                    "It is useful where decimal digits must be preserved directly."
                ),
                rx.code_block(
                    "Decimal 59\n"
                    "5 → 0101\n"
                    "9 → 1001\n"
                    "BCD(59) = 0101 1001\n\n"
                    "Notice: ordinary binary 59 = 00111011, which is different.",
                    language="markup",
                ),
            ),
            _section(
                "2", "Gray code",
                rx.text(
                    "Adjacent Gray-code values differ by only one bit. This reduces ambiguity "
                    "during transitions and is useful in encoders and position sensing."
                ),
                rx.code_block(
                    "Decimal   Binary   Gray\n"
                    "0         000      000\n"
                    "1         001      001\n"
                    "2         010      011\n"
                    "3         011      010\n"
                    "4         100      110",
                    language="markup",
                ),
                rx.callout(
                    "Binary → Gray: keep the MSB; each following Gray bit is XOR of two adjacent binary bits.",
                    icon="info",
                ),
            ),
            _section(
                "3", "Character codes",
                rx.text(
                    "Computers also map bit patterns to characters. ASCII historically uses "
                    "numeric codes for letters, digits and symbols; modern systems commonly use Unicode "
                    "to represent writing systems from around the world."
                ),
                rx.code_block(
                    "ASCII decimal 65 → 'A'\n"
                    "ASCII decimal 97 → 'a'\n"
                    "ASCII decimal 48 → '0'",
                    language="markup",
                ),
            ),
            _section(
                "4", "Practice: BCD",
                rx.text("Write decimal 59 in 8-bit BCD (four bits per decimal digit)."),
                rx.hstack(
                    rx.input(
                        value=SignedCodesState.bcd_answer,
                        on_change=SignedCodesState.set_bcd_answer,
                        placeholder="BCD answer",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=SignedCodesState.check_bcd),
                ),
                rx.cond(
                    SignedCodesState.bcd_feedback != "",
                    rx.callout(SignedCodesState.bcd_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Practice: Binary to Gray",
                rx.text("Convert binary 1011₂ to Gray code."),
                rx.hstack(
                    rx.input(
                        value=SignedCodesState.gray_answer,
                        on_change=SignedCodesState.set_gray_answer,
                        placeholder="Gray code",
                        max_width="220px",
                    ),
                    rx.button("Check", on_click=SignedCodesState.check_gray),
                ),
                rx.cond(
                    SignedCodesState.gray_feedback != "",
                    rx.callout(SignedCodesState.gray_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "Connect codes to digital hardware",
                rx.text(
                    "Codes become especially useful when you study encoders, decoders and display logic. "
                    "Open the Simulator to explore these MSI/LSI components."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                    rx.link(
                        rx.button("Open Number Systems", variant="soft"),
                        href="/tools/number-systems",
                    ),
                    wrap="wrap",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Signed binary", variant="soft"), href="/academy/unit-1/signed-binary"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 8 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Next lesson →", variant="soft"), href="/academy/unit-1/binary-storage"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
