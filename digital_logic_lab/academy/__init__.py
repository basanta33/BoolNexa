"""Public API for BoolNexa Academy v2.

UI symbols are loaded lazily so curriculum tooling can run without importing
Reflex and its frontend stack.
"""
from .models import LAB_PREVIEWS, LEARNING_PATHS, TOTAL_LESSONS, LabPreview, LearningPath

__all__ = ["academy", "AcademyState", "LearningPath", "LabPreview", "LEARNING_PATHS", "LAB_PREVIEWS", "TOTAL_LESSONS"]

def __getattr__(name: str):
    if name == "academy":
        from .pages.home import academy
        return academy
    if name == "AcademyState":
        from .state import AcademyState
        return AcademyState
    raise AttributeError(name)
