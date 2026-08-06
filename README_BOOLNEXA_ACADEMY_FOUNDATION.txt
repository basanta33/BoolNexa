BoolNexa v1.1 - Academy Foundation
==================================

This replacement package adds:
- /academy route and responsive Academy dashboard
- Seven syllabus-aligned curriculum units (44 guided hours)
- Boolean algebra history featuring George Boole and Claude Shannon
- Reusable 15-section lesson template
- Nine practical/laboratory work categories
- Simulator header link to Academy
- Curriculum regression tests

Installation on Windows
-----------------------
1. Back up D:\Projects\BoolNexa.
2. Extract this ZIP directly into D:\Projects\BoolNexa.
3. Choose Replace files when prompted.
4. Run:

   D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest -q
   D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run

Manual checks
-------------
- Open http://localhost:3000/academy
- Confirm all seven unit cards appear.
- Confirm the Boolean Algebra history panel appears.
- Click Launch Simulator and confirm the simulator opens.
- From the simulator, click Academy and confirm the Academy opens.

Validated in the build workspace
--------------------------------
- Python compilation passed.
- 39 tests passed.
