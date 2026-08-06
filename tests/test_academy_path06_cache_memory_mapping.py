from pathlib import Path

ROOT = Path(__file__).parents[1]
APP = (ROOT / "digital_logic_lab" / "digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS = (ROOT / "digital_logic_lab" / "academy_memory_foundations.py").read_text(encoding="utf-8")


def test_path06_lessons_5_6_routes_registered():
    assert 'route="/academy/unit-6/cache-memory"' in APP
    assert 'route="/academy/unit-6/cache-mapping"' in APP
    assert "cache_memory_lesson" in APP
    assert "cache_mapping_lesson" in APP


def test_cache_memory_core_content():
    for text in [
        "Cache Memory & Locality",
        "Why a cache helps",
        "Temporal locality",
        "Spatial locality",
        "Cache lines and block transfers",
        "Cache hit",
        "Cache miss",
        "AMAT = hit time + (miss rate × miss penalty)",
        "check_cache_locality",
        "check_cache_hit",
        "check_cache_line",
    ]:
        assert text in LESSONS


def test_cache_mapping_core_content():
    for text in [
        "Cache Mapping, Hits & Misses",
        "Direct-mapped cache",
        "memory block number mod number of cache lines",
        "Why the tag is necessary",
        "Set associative",
        "Fully associative",
        "Compulsory (cold)",
        "Capacity",
        "Conflict",
        "Write-through",
        "Write-back",
        "check_direct_map",
        "check_tag",
        "check_miss",
    ]:
        assert text in LESSONS


def test_cache_math_and_precision_language():
    assert "13 mod 8 = 5" in LESSONS
    assert "AMAT = 1 + (0.05 × 40) = 3 ns" in LESSONS
    assert "architecture-specific" in LESSONS
    assert "processor documentation" in LESSONS
    assert "Do not assume fixed bit positions" in LESSONS


def test_path06_lessons_1_to_6_navigation_chain():
    for href in [
        '/academy/unit-6/ram-rom',
        '/academy/unit-6/sram-dram',
        '/academy/unit-6/memory-organisation',
        '/academy/unit-6/cache-memory',
        '/academy/unit-6/cache-mapping',
    ]:
        assert f'href="{href}"' in LESSONS
    for number in range(1, 7):
        assert f"Path 06 · Lesson {number}" in LESSONS


def test_lesson_4_now_advances_to_lesson_5():
    lesson4 = LESSONS.split("def memory_organisation_lesson():", 1)[1].split("def cache_memory_lesson():", 1)[0]
    assert 'href="/academy/unit-6/cache-memory"' in lesson4
    assert "Next lesson →" in lesson4


def test_lesson_5_advances_to_lesson_6():
    lesson5 = LESSONS.split("def cache_memory_lesson():", 1)[1].split("def cache_mapping_lesson():", 1)[0]
    assert 'href="/academy/unit-6/cache-mapping"' in lesson5
    assert "Next lesson →" in lesson5
