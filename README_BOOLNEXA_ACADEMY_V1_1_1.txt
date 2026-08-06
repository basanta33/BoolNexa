BoolNexa Academy v1.1.1 - Interactive Lesson Engine
====================================================

This release turns the Academy foundation into a working simulation-led learning experience.

Added
-----
1. Structured Unit 1 lesson catalogue.
2. Dedicated lesson route:
   /academy/unit-1/why-computers-use-binary
3. First complete interactive lesson.
4. Four-bit live switch simulator.
5. Binary, weighted and decimal value displays.
6. Automatic target-value challenge.
7. Immediate knowledge-check feedback.
8. Direct connection from lesson to the main circuit simulator.
9. Pure binary helper functions and regression tests.

Installation
------------
Extract this ZIP directly over D:\Projects\BoolNexa and replace files.

Validation
----------
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest -q
D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run

Open
----
http://localhost:3000/academy
http://localhost:3000/academy/unit-1/why-computers-use-binary
