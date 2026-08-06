BoolNexa Shared Design System — Sprint 1

Copy the folder:
  ui
into:
  D:\Projects\BoolNexa\digital_logic_lab\ui

Replace:
  D:\Projects\BoolNexa\digital_logic_lab\boolean_lab.py
  D:\Projects\BoolNexa\digital_logic_lab\number_system_lab.py

No change is required to digital_logic_lab.py in this sprint.

Test:
  D:\Projects\BoolNexa\.venv\Scripts\python.exe -m pytest tests -q

Run:
  D:\Projects\BoolNexa\.venv\Scripts\python.exe -m reflex run

Review:
  http://localhost:3000/tools/boolean
  http://localhost:3000/tools/number-systems

Main changes:
- professional light engineering palette
- shared sticky navigation
- compact truth table
- sticky table headers
- scrollable table capped at 430px
- smaller cells and metric cards
- highlighted output column
- reusable theme and UI components
