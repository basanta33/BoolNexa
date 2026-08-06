from pathlib import Path
ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_mux_demux.py").read_text(encoding="utf-8")
PREVIOUS = (ROOT / "digital_logic_lab" / "academy_subtractors_comparators.py").read_text(encoding="utf-8")

def test_lessons_five_and_six_are_registered():
    assert 'route="/academy/unit-4/multiplexers"' in APP
    assert 'route="/academy/unit-4/demultiplexers"' in APP

def test_mux_lesson_is_complete():
    assert "Y = S'I0 + SI1" in LESSONS
    assert "4-to-1 multiplexer" in LESSONS
    assert "2ⁿ data inputs" in LESSONS
    assert "MUX as a Boolean-function generator" in LESSONS
    assert "I0=0, I1=1, I2=1, I3=0" in LESSONS
    assert "check_mux_select" in LESSONS
    assert "check_mux_output" in LESSONS

def test_demux_lesson_is_complete():
    assert "Y0 = DS'" in LESSONS
    assert "The 1-to-4 DEMUX" in LESSONS
    assert "Y2 = D S1  S0'" in LESSONS
    assert "MUX versus DEMUX" in LESSONS
    assert "decoder" in LESSONS.lower()
    assert "check_demux_selects" in LESSONS
    assert "check_demux_output" in LESSONS

def test_navigation_and_tools():
    assert 'href="/academy/unit-4/multiplexers"' in PREVIOUS
    assert 'href="/academy/unit-4/demultiplexers"' in LESSONS
    assert LESSONS.count('href="/tools/boolean"') >= 2
    assert LESSONS.count('href="/tools/circuit"') >= 2
    assert "Path 04 · Lesson 5" in LESSONS
    assert "Path 04 · Lesson 6" in LESSONS
