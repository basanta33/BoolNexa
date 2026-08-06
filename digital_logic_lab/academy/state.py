"""Shared state for Academy navigation and learner progress."""
from __future__ import annotations
import reflex as rx
from .models import TOTAL_LESSONS

class AcademyState(rx.State):
    selected_path: int = 1
    completed_lessons: list[str] = []
    xp: int = 0
    streak_days: int = 1

    def select_path(self, number: int) -> None:
        self.selected_path = max(1, min(7, int(number)))

    def complete_lesson(self, lesson_id: str, xp_award: int = 20) -> None:
        lesson_id = lesson_id.strip()
        if lesson_id and lesson_id not in self.completed_lessons:
            self.completed_lessons = [*self.completed_lessons, lesson_id]
            self.xp += max(0, int(xp_award))

    @rx.var
    def completed_count(self) -> int:
        return len(self.completed_lessons)

    @rx.var
    def progress_percent(self) -> int:
        return round((self.completed_count / TOTAL_LESSONS) * 100) if TOTAL_LESSONS else 0
