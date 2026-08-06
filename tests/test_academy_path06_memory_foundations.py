from pathlib import Path
ROOT=Path(__file__).parents[1]
APP=(ROOT/"digital_logic_lab"/"digital_logic_lab.py").read_text(encoding="utf-8")
LESSONS=(ROOT/"digital_logic_lab"/"academy_memory_foundations.py").read_text(encoding="utf-8")
PREVIOUS=(ROOT/"digital_logic_lab"/"academy_sequential_integration_mastery.py").read_text(encoding="utf-8")

def test_routes():
    assert 'route="/academy/unit-6/memory-foundations"' in APP
    assert 'route="/academy/unit-6/ram-rom"' in APP

def test_memory_foundations():
    for x in ["From flip-flops to memory arrays","Words, width and capacity","Capacity","2ⁿ distinct locations","Volatile and non-volatile memory","Memory hierarchy","check_capacity","check_address"]: assert x in LESSONS

def test_ram_rom():
    for x in ["RAM: read and write","Random access","ROM: stored lookup information","Mask ROM","PROM","EPROM","EEPROM","Flash","Read timing","Write timing","Memory versus registers"]: assert x in LESSONS

def test_precision():
    assert "does not mean the memory returns random data" in LESSONS
    assert "device-specific" in LESSONS
    assert "Synchronous memories" in LESSONS

def test_navigation():
    assert 'href="/academy/unit-6/memory-foundations"' in PREVIOUS
    assert 'href="/academy/unit-6/ram-rom"' in LESSONS
    assert 'href="/academy/unit-6/sram-dram"' in LESSONS
    assert "Path 06 · Lesson 1" in LESSONS and "Path 06 · Lesson 2" in LESSONS
