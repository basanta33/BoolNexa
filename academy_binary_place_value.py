"""BoolNexa Academy — Unit 1, Lesson 2: Binary Place Value Explorer."""
from __future__ import annotations

import reflex as rx


class BinaryPlaceValueState(rx.State):
    """Interactive state for binary place-value practice."""

    bit_7: int = 0
    bit_6: int = 0
    bit_5: int = 0
    bit_4: int = 0
    bit_3: int = 0
    bit_2: int = 0
    bit_1: int = 0
    bit_0: int = 0

    target_value: int = 37
    prediction: str = ""
    prediction_checked: bool = False
    hint_level: int = 0

    quiz_answer: str = ""
    quiz_submitted: bool = False
    lesson_complete: bool = False

    stored_xp: str = rx.LocalStorage("0", name="boolnexa_academy_xp", sync=True)
    stored_completed_lessons: str = rx.LocalStorage(
        "", name="boolnexa_completed_lessons", sync=True
    )

    def _toggle(self, name: str) -> None:
        setattr(self, name, 0 if getattr(self, name) else 1)
        self.prediction_checked = False

    def toggle_bit_7(self) -> None:
        self._toggle("bit_7")

    def toggle_bit_6(self) -> None:
        self._toggle("bit_6")

    def toggle_bit_5(self) -> None:
        self._toggle("bit_5")

    def toggle_bit_4(self) -> None:
        self._toggle("bit_4")

    def toggle_bit_3(self) -> None:
        self._toggle("bit_3")

    def toggle_bit_2(self) -> None:
        self._toggle("bit_2")

    def toggle_bit_1(self) -> None:
        self._toggle("bit_1")

    def toggle_bit_0(self) -> None:
        self._toggle("bit_0")

    def reset_bits(self) -> None:
        self.bit_7 = self.bit_6 = self.bit_5 = self.bit_4 = 0
        self.bit_3 = self.bit_2 = self.bit_1 = self.bit_0 = 0
        self.prediction = ""
        self.prediction_checked = False
        self.hint_level = 0

    def set_prediction(self, value: str) -> None:
        self.prediction = value
        self.prediction_checked = False

    def check_prediction(self) -> None:
        self.prediction_checked = True

    def request_hint(self) -> None:
        if self.hint_level < 3:
            self.hint_level += 1

    def set_quiz_answer(self, value: str) -> None:
        self.quiz_answer = value
        self.quiz_submitted = False

    def submit_quiz(self) -> None:
        self.quiz_submitted = True

    def complete_lesson(self) -> None:
        if not self.can_complete:
            return
        lesson_id = "unit-1-lesson-2"
        if lesson_id not in self.stored_completed_lessons:
            try:
                current_xp = int(self.stored_xp or "0")
            except ValueError:
                current_xp = 0
            self.stored_xp = str(current_xp + 60)
            separator = "," if self.stored_completed_lessons else ""
            self.stored_completed_lessons = (
                f"{self.stored_completed_lessons}{separator}{lesson_id}"
            )
        self.lesson_complete = True

    @rx.var
    def decimal_value(self) -> int:
        return (
            self.bit_7 * 128
            + self.bit_6 * 64
            + self.bit_5 * 32
            + self.bit_4 * 16
            + self.bit_3 * 8
            + self.bit_2 * 4
            + self.bit_1 * 2
            + self.bit_0
        )

    @rx.var
    def binary_text(self) -> str:
        return (
            f"{self.bit_7}{self.bit_6}{self.bit_5}{self.bit_4}"
            f"{self.bit_3}{self.bit_2}{self.bit_1}{self.bit_0}"
        )

    @rx.var
    def expanded_form(self) -> str:
        return (
            f"({self.bit_7}×128)+({self.bit_6}×64)+({self.bit_5}×32)+"
            f"({self.bit_4}×16)+({self.bit_3}×8)+({self.bit_2}×4)+"
            f"({self.bit_1}×2)+({self.bit_0}×1)"
        )

    @rx.var
    def prediction_correct(self) -> bool:
        return self.prediction.strip() == str(self.decimal_value)

    @rx.var
    def challenge_complete(self) -> bool:
        return self.decimal_value == self.target_value

    @rx.var
    def quiz_correct(self) -> bool:
        return self.quiz_answer == "32"

    @rx.var
    def can_complete(self) -> bool:
        return self.challenge_complete and self.quiz_submitted and self.quiz_correct

    @rx.var
    def progress_percent(self) -> int:
        progress = 20
        if self.prediction_checked:
            progress += 20
        if self.challenge_complete:
            progress += 30
        if self.quiz_submitted and self.quiz_correct:
            progress += 30
        return min(progress, 100)


def _bit_card(label: str, weight: int, value: rx.Var, handler) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(label, size="1", color="#64748b", weight="bold"),
            rx.button(
                value.to_string(),
                on_click=handler,
                size="3",
                width="64px",
                height="64px",
                color_scheme="blue",
                variant="solid",
            ),
            rx.text(f"Weight {weight}", size="1", color="#64748b"),
            spacing="2",
            align="center",
        ),
        min_width="125px",
    )


def _section(number: str, title: str, *children: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(number, radius="full", color_scheme="blue"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            spacing="4",
            align="stretch",
        ),
        width="100%",
    )


def _progress_panel() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Unit 1 progress", size="4"),
                rx.spacer(),
                rx.badge("+60 XP", color_scheme="amber"),
                width="100%",
            ),
            rx.progress(
                value=BinaryPlaceValueState.progress_percent,
                width="100%",
                color_scheme="blue",
            ),
            rx.hstack(
                rx.text("Lesson 2 of 7", size="2", color="#64748b"),
                rx.spacer(),
                rx.text(BinaryPlaceValueState.progress_percent, "%", size="2"),
                width="100%",
            ),
            rx.text("✓ Lesson 1 · Why computers use binary", size="2"),
            rx.text("▶ Lesson 2 · Binary place value", size="2", weight="bold"),
            rx.text("○ Lesson 3 · Decimal to binary", size="2", color="#64748b"),
            spacing="3",
            align="stretch",
        ),
        width="100%",
    )


def binary_place_value_lesson() -> rx.Component:
    """Render Unit 1 Lesson 2."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.link(rx.button("← Academy", variant="soft"), href="/academy"),
                rx.spacer(),
                rx.link(rx.button("Open Simulator", color_scheme="blue"), href="/"),
                width="100%",
            ),
            _progress_panel(),
            rx.vstack(
                rx.badge("UNIT 01 · LESSON 02", color_scheme="blue"),
                rx.heading("Binary Place Value Explorer", size="8"),
                rx.text(
                    "Build eight-bit numbers, predict their decimal values and learn how "
                    "each position represents a power of two.",
                    size="4",
                    color="#475569",
                    max_width="900px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.badge("25 minutes", color_scheme="gray"),
                    rx.badge("Beginner", color_scheme="green"),
                    rx.badge("Interactive", color_scheme="amber"),
                    wrap="wrap",
                ),
                align="start",
                spacing="3",
            ),
            _section(
                "1",
                "Mission",
                rx.text(
                    "Explore the eight place values 128, 64, 32, 16, 8, 4, 2 and 1. "
                    "Then build decimal 37 using the smallest correct combination of active bits.",
                    line_height="1.7",
                ),
                rx.callout(
                    "A bit contributes its place value only when it is 1.",
                    icon="info",
                    color_scheme="blue",
                ),
            ),
            _section(
                "2",
                "Explore the powers of two",
                rx.flex(
                    _bit_card("Bit 7", 128, BinaryPlaceValueState.bit_7, BinaryPlaceValueState.toggle_bit_7),
                    _bit_card("Bit 6", 64, BinaryPlaceValueState.bit_6, BinaryPlaceValueState.toggle_bit_6),
                    _bit_card("Bit 5", 32, BinaryPlaceValueState.bit_5, BinaryPlaceValueState.toggle_bit_5),
                    _bit_card("Bit 4", 16, BinaryPlaceValueState.bit_4, BinaryPlaceValueState.toggle_bit_4),
                    _bit_card("Bit 3", 8, BinaryPlaceValueState.bit_3, BinaryPlaceValueState.toggle_bit_3),
                    _bit_card("Bit 2", 4, BinaryPlaceValueState.bit_2, BinaryPlaceValueState.toggle_bit_2),
                    _bit_card("Bit 1", 2, BinaryPlaceValueState.bit_1, BinaryPlaceValueState.toggle_bit_1),
                    _bit_card("Bit 0", 1, BinaryPlaceValueState.bit_0, BinaryPlaceValueState.toggle_bit_0),
                    gap="3",
                    wrap="wrap",
                    justify="center",
                    width="100%",
                ),
                rx.grid(
                    rx.card(
                        rx.vstack(
                            rx.text("Binary word", color="#64748b"),
                            rx.heading(BinaryPlaceValueState.binary_text, size="7"),
                        )
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Decimal value", color="#64748b"),
                            rx.heading(BinaryPlaceValueState.decimal_value, size="7"),
                        )
                    ),
                    columns=rx.breakpoints(initial="1", sm="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.callout(
                    BinaryPlaceValueState.expanded_form,
                    icon="calculator",
                    width="100%",
                ),
                rx.button(
                    "Reset bits",
                    on_click=BinaryPlaceValueState.reset_bits,
                    variant="soft",
                    align_self="flex-start",
                ),
            ),
            _section(
                "3",
                "Predict before checking",
                rx.text(
                    "Choose any pattern, calculate its decimal value yourself, then enter your prediction.",
                    color="#475569",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Predicted decimal value",
                        value=BinaryPlaceValueState.prediction,
                        on_change=BinaryPlaceValueState.set_prediction,
                        input_mode="numeric",
                        max_width="280px",
                    ),
                    rx.button(
                        "Check prediction",
                        on_click=BinaryPlaceValueState.check_prediction,
                        color_scheme="violet",
                    ),
                    wrap="wrap",
                ),
                rx.cond(
                    BinaryPlaceValueState.prediction_checked,
                    rx.cond(
                        BinaryPlaceValueState.prediction_correct,
                        rx.callout(
                            "Correct. You added the active place values accurately.",
                            icon="circle-check",
                            color_scheme="green",
                        ),
                        rx.callout(
                            "Try again. Add only the place values whose bits are 1.",
                            icon="circle-alert",
                            color_scheme="red",
                        ),
                    ),
                    rx.box(),
                ),
            ),
            _section(
                "4",
                "Build challenge: create decimal 37",
                rx.text(
                    "Use the place-value switches to make decimal 37.",
                    color="#475569",
                ),
                rx.cond(
                    BinaryPlaceValueState.challenge_complete,
                    rx.callout(
                        "Challenge passed: 00100101₂ = 37₁₀.",
                        icon="circle-check",
                        color_scheme="green",
                        width="100%",
                    ),
                    rx.callout(
                        "Target not reached. Keep adjusting the active place values.",
                        icon="target",
                        color_scheme="amber",
                        width="100%",
                    ),
                ),
                rx.button(
                    "Need a hint?",
                    on_click=BinaryPlaceValueState.request_hint,
                    variant="soft",
                    color_scheme="amber",
                    align_self="flex-start",
                ),
                rx.cond(
                    BinaryPlaceValueState.hint_level >= 1,
                    rx.callout(
                        "Hint 1: Start with the largest power of two that does not exceed 37.",
                        icon="lightbulb",
                        color_scheme="amber",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    BinaryPlaceValueState.hint_level >= 2,
                    rx.callout(
                        "Hint 2: After selecting 32, the remaining value is 5.",
                        icon="lightbulb",
                        color_scheme="amber",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    BinaryPlaceValueState.hint_level >= 3,
                    rx.callout(
                        "Hint 3: Use 32 + 4 + 1.",
                        icon="lightbulb",
                        color_scheme="amber",
                    ),
                    rx.box(),
                ),
            ),
            _section(
                "5",
                "Knowledge check",
                rx.text("In an eight-bit number, what is the place value of bit 5?"),
                rx.radio(
                    ["16", "32", "64"],
                    value=BinaryPlaceValueState.quiz_answer,
                    on_change=BinaryPlaceValueState.set_quiz_answer,
                    direction="column",
                ),
                rx.button(
                    "Submit answer",
                    on_click=BinaryPlaceValueState.submit_quiz,
                    color_scheme="blue",
                    align_self="flex-start",
                ),
                rx.cond(
                    BinaryPlaceValueState.quiz_submitted,
                    rx.cond(
                        BinaryPlaceValueState.quiz_correct,
                        rx.callout(
                            "Correct. Bit 5 represents 2⁵ = 32.",
                            icon="circle-check",
                            color_scheme="green",
                        ),
                        rx.callout(
                            "Review the place values: bit 0 is 1, so bit 5 is 32.",
                            icon="circle-alert",
                            color_scheme="red",
                        ),
                    ),
                    rx.box(),
                ),
            ),
            _section(
                "6",
                "Complete lesson",
                rx.cond(
                    BinaryPlaceValueState.can_complete,
                    rx.callout(
                        "All required activities are complete. Claim your XP.",
                        icon="trophy",
                        color_scheme="green",
                    ),
                    rx.callout(
                        "Build decimal 37 and answer the knowledge check correctly.",
                        icon="list-checks",
                        color_scheme="blue",
                    ),
                ),
                rx.button(
                    "Complete lesson · +60 XP",
                    on_click=BinaryPlaceValueState.complete_lesson,
                    disabled=~BinaryPlaceValueState.can_complete,
                    color_scheme="green",
                    size="3",
                    align_self="flex-start",
                ),
                rx.cond(
                    BinaryPlaceValueState.lesson_complete,
                    rx.callout(
                        "Lesson complete. Your progress is saved in this browser.",
                        icon="circle-check",
                        color_scheme="green",
                    ),
                    rx.box(),
                ),
            ),
            rx.hstack(
                rx.link(
                    rx.button("← Previous lesson", variant="soft"),
                    href="/academy/unit-1/why-computers-use-binary",
                ),
                rx.spacer(),
                rx.text("Unit 1 · Lesson 2 of 7", size="2", color="#64748b"),
                rx.spacer(),
                rx.link(
                    rx.button("Next lesson →", variant="soft"),
                    href="/academy/unit-1/decimal-to-binary",
                ),
                width="100%",
                padding_y="16px",
            ),
            spacing="6",
            align="stretch",
            max_width="1180px",
            width="100%",
            margin="0 auto",
            padding=rx.breakpoints(initial="20px", md="36px", xl="48px"),
        ),
        min_height="100vh",
        background="#ffffff",
    )
