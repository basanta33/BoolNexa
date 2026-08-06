"""BoolNexa Academy Path 01 lessons 9 and 10."""

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


class BinaryStorageMasteryState(rx.State):
    byte_answer: str = ""
    byte_feedback: str = ""
    storage_answer: str = ""
    storage_feedback: str = ""
    mastery_binary: str = ""
    mastery_hex: str = ""
    mastery_twos: str = ""
    mastery_score: str = ""

    def set_byte_answer(self, value: str) -> None:
        self.byte_answer = value

    def set_mastery_binary(self, value: str) -> None:
        self.mastery_binary = value

    def set_mastery_hex(self, value: str) -> None:
        self.mastery_hex = value

    def set_mastery_twos(self, value: str) -> None:
        self.mastery_twos = value

    def set_storage_answer(self, value: str) -> None:
        self.storage_answer = value

    def check_byte(self):
        value = self.byte_answer.strip()
        self.byte_feedback = (
            "Correct. One byte contains 8 bits."
            if value == "8"
            else "Try again. A byte is a standard group of eight binary digits."
        )

    def check_storage(self):
        value = self.storage_answer.strip().replace(" ", "")
        self.storage_feedback = (
            "Correct. 4 KiB = 4 × 1024 = 4096 bytes."
            if value == "4096"
            else "Use 1 KiB = 1024 bytes, then multiply by 4."
        )

    def check_mastery(self):
        score = 0
        if self.mastery_binary.strip().replace(" ", "") == "101010":
            score += 1
        if self.mastery_hex.strip().upper().replace(" ", "") == "3F":
            score += 1
        if self.mastery_twos.strip().replace(" ", "") == "11111011":
            score += 1
        if score == 3:
            self.mastery_score = "3/3 — Excellent. Path 01 mastery check complete."
        elif score == 2:
            self.mastery_score = "2/3 — Good work. Review the one answer that needs correction."
        else:
            self.mastery_score = f"{score}/3 — Review the worked lessons and try again."


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


def binary_storage_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 09", color_scheme="blue"),
            rx.heading("Bits, Bytes, Storage & Registers", size="8"),
            rx.text(
                "Connect binary numbers to the way digital systems group, store and move information.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "From bits to bytes",
                rx.text(
                    "A bit is one binary digit. Eight bits form one byte. Larger data quantities "
                    "are built from bytes."
                ),
                rx.code_block(
                    "1 bit   = one 0 or 1\n"
                    "1 nibble = 4 bits\n"
                    "1 byte  = 8 bits\n"
                    "1 KiB   = 1024 bytes\n"
                    "1 MiB   = 1024 KiB\n"
                    "1 GiB   = 1024 MiB",
                    language="markup",
                ),
                rx.callout(
                    "A byte has 256 possible bit patterns because 2⁸ = 256.",
                    icon="info",
                ),
            ),
            _section(
                "2", "Words and registers",
                rx.text(
                    "Processors commonly operate on fixed groups of bits called words. "
                    "Registers are small, fast storage locations inside digital systems that hold "
                    "binary data temporarily."
                ),
                rx.code_block(
                    "8-bit register:   10110100\n"
                    "16-bit register:  0000000010110100\n"
                    "32-bit word:      00000000 00000000 00000000 10110100",
                    language="markup",
                ),
            ),
            _section(
                "3", "Why bit width matters",
                rx.text(
                    "The number of available bits controls how many patterns can be represented. "
                    "An unsigned n-bit quantity has 2ⁿ possible patterns."
                ),
                rx.code_block(
                    "4 bits  → 2⁴  = 16 patterns  → 0 to 15 unsigned\n"
                    "8 bits  → 2⁸  = 256 patterns → 0 to 255 unsigned\n"
                    "16 bits → 2¹⁶ = 65,536 patterns",
                    language="markup",
                ),
            ),
            _section(
                "4", "Quick check: byte size",
                rx.text("How many bits are in one byte?"),
                rx.hstack(
                    rx.input(
                        value=BinaryStorageMasteryState.byte_answer,
                        on_change=BinaryStorageMasteryState.set_byte_answer,
                        placeholder="Number of bits",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=BinaryStorageMasteryState.check_byte),
                ),
                rx.cond(
                    BinaryStorageMasteryState.byte_feedback != "",
                    rx.callout(BinaryStorageMasteryState.byte_feedback, icon="brain"),
                    rx.box(),
                ),
            ),
            _section(
                "5", "Storage calculation",
                rx.text("How many bytes are in 4 KiB?"),
                rx.hstack(
                    rx.input(
                        value=BinaryStorageMasteryState.storage_answer,
                        on_change=BinaryStorageMasteryState.set_storage_answer,
                        placeholder="Bytes",
                        max_width="200px",
                    ),
                    rx.button("Check", on_click=BinaryStorageMasteryState.check_storage),
                ),
                rx.cond(
                    BinaryStorageMasteryState.storage_feedback != "",
                    rx.callout(BinaryStorageMasteryState.storage_feedback, icon="calculator"),
                    rx.box(),
                ),
            ),
            _section(
                "6", "See storage elements in hardware",
                rx.text(
                    "Registers are built from sequential logic. Open the Simulator and inspect "
                    "flip-flops and register/counter components before the final Path 01 review."
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
                rx.link(rx.button("← Digital codes", variant="soft"), href="/academy/unit-1/digital-codes"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 9 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Final challenge →", variant="soft"), href="/academy/unit-1/mastery-challenge"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )


def binary_mastery_lesson() -> rx.Component:
    return rx.box(
        app_header("academy"),
        rx.vstack(
            rx.badge("PATH 01 · LESSON 10", color_scheme="green"),
            rx.heading("Binary Systems Mastery Challenge", size="8"),
            rx.text(
                "Review the complete Binary Systems path and prove that you can move confidently "
                "between decimal, binary, hexadecimal and signed representations.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "What you have learned",
                rx.grid(
                    rx.callout("Binary place value and powers of two", icon="circle-check"),
                    rx.callout("Decimal ↔ binary conversion", icon="circle-check"),
                    rx.callout("Octal and hexadecimal grouping", icon="circle-check"),
                    rx.callout("Binary addition and subtraction", icon="circle-check"),
                    rx.callout("Signed binary and two's complement", icon="circle-check"),
                    rx.callout("BCD, Gray code, bits, bytes and storage", icon="circle-check"),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3",
                ),
            ),
            _section(
                "2", "Mastery challenge",
                rx.text("Answer all three without using the laboratory first."),
                rx.vstack(
                    rx.text("A. Convert 42₁₀ to binary."),
                    rx.input(
                        value=BinaryStorageMasteryState.mastery_binary,
                        on_change=BinaryStorageMasteryState.set_mastery_binary,
                        placeholder="Binary answer",
                        max_width="260px",
                    ),
                    rx.text("B. Convert 111111₂ to hexadecimal."),
                    rx.input(
                        value=BinaryStorageMasteryState.mastery_hex,
                        on_change=BinaryStorageMasteryState.set_mastery_hex,
                        placeholder="Hex answer",
                        max_width="260px",
                    ),
                    rx.text("C. Write −5 as 8-bit two's complement."),
                    rx.input(
                        value=BinaryStorageMasteryState.mastery_twos,
                        on_change=BinaryStorageMasteryState.set_mastery_twos,
                        placeholder="8-bit answer",
                        max_width="260px",
                    ),
                    rx.button("Check mastery score", on_click=BinaryStorageMasteryState.check_mastery),
                    rx.cond(
                        BinaryStorageMasteryState.mastery_score != "",
                        rx.callout(BinaryStorageMasteryState.mastery_score, icon="trophy"),
                        rx.box(),
                    ),
                    align="start",
                    spacing="3",
                ),
            ),
            _section(
                "3", "Verify with the real laboratory",
                rx.text(
                    "After answering from memory, use Number Systems to verify the conversions. "
                    "Learning is stronger when the tool confirms reasoning rather than replacing it."
                ),
                rx.link(
                    rx.button("Verify in Number System Laboratory", color_scheme="blue"),
                    href="/tools/number-systems",
                    align_self="flex-start",
                ),
            ),
            _section(
                "4", "Bridge to Path 02",
                rx.text(
                    "Binary values become useful when logic gates make decisions about them. "
                    "The next path introduces Boolean algebra, AND/OR/NOT gates, truth tables and "
                    "the connection between expressions and real circuits."
                ),
                rx.hstack(
                    rx.link(rx.button("Open Boolean Lab", variant="soft"), href="/tools/boolean"),
                    rx.link(rx.button("Explore Simulator", variant="soft"), href="/"),
                    wrap="wrap",
                ),
            ),
            _section(
                "5", "Path 01 complete",
                rx.callout(
                    "You have reached the end of Binary Systems. Continue to Boolean Algebra & Logic Gates.",
                    icon="graduation-cap",
                    color_scheme="green",
                ),
                rx.link(
                    rx.button("Begin Path 02 →", size="3", color_scheme="blue"),
                    href="/academy",
                    align_self="flex-start",
                ),
            ),
            rx.hstack(
                rx.link(rx.button("← Bits & storage", variant="soft"), href="/academy/unit-1/binary-storage"),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 10 of 10", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(rx.button("Academy home", variant="soft"), href="/academy"),
                width="100%", padding_y="16px",
            ),
            spacing="5", align="stretch", max_width="1100px", width="100%",
            margin="0 auto", padding=rx.breakpoints(initial="20px", md="36px"),
        ),
        min_height="100vh", background="#f8fafc",
    )
