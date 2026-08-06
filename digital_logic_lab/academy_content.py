"""Curriculum data for BoolNexa Academy."""
from __future__ import annotations
from typing import Final

ACADEMY_UNITS: Final[tuple[dict[str, object], ...]] = (
    {"number": 1, "title": "Binary Systems", "hours": 5, "lessons": 10, "summary": "Digital systems, binary place value, base conversion, arithmetic, signed numbers, digital codes, storage and binary mastery."},
    {"number": 2, "title": "Boolean Algebra and Logic Gates", "hours": 5, "lessons": 10, "summary": "Logic states, gates, Boolean expressions and laws, truth tables, circuit translation and universal-gate implementation, with historical context from George Boole and Claude Shannon."},
    {"number": 3, "title": "Karnaugh Maps and Logic Simplification", "hours": 5, "lessons": 10, "summary": "Two- through six-variable K-maps, prime implicants, SOP/POS, don't-cares, advanced grouping strategy and simplification mastery."},
    {"number": 4, "title": "Combinational Logic", "hours": 5, "lessons": 10, "summary": "Combinational design foundations, adders, subtractors, comparators, multiplexers, demultiplexers, decoders, encoders and integrated design."},
    {"number": 5, "title": "Sequential Logic and FSMs", "hours": 8, "lessons": 10, "summary": "Sequential foundations, latches, flip-flops, clock timing, registers, counters, finite-state machines and integrated sequential design."},
    {"number": 6, "title": "Digital Memory Systems", "hours": 10, "lessons": 10, "summary": "Memory foundations, RAM and ROM, SRAM and DRAM, organisation, cache, virtual memory, reliability and memory-system performance."},
    {"number": 7, "title": "Registers and Counters", "hours": 6, "lessons": 7, "summary": "Registers, shift registers, ripple and synchronous counters, programmable counting, timing sequences and integrated control."},
    {"number": 8, "title": "Computer Arithmetic and ALU Design", "hours": 7, "lessons": 8, "summary": "Binary arithmetic hardware, carry and overflow, fast adders, datapaths, logic functions, ALU control, status flags and integrated ALU design."},
    {"number": 9, "title": "Processor Architecture and CPU Datapath", "hours": 7, "lessons": 8, "summary": "CPU architecture, instruction execution, register transfer, instruction formats, datapaths, control, branching and integrated processor design."},
    {"number": 10, "title": "Computer Organisation and System Integration", "hours": 8, "lessons": 8, "summary": "System interconnects, I/O organisation, memory-mapped peripherals, interrupts, buses, DMA and complete computer-system integration."},
    {"number": 11, "title": "Embedded Systems and Real-Time Computing", "hours": 8, "lessons": 8, "summary": "Embedded-system architecture, microcontrollers, GPIO, sensing, firmware execution, real-time timing, reliability and integrated physical-system control."},
    {"number": 12, "title": "HDL, FPGA and Digital System Design", "hours": 8, "lessons": 8, "summary": "Hardware description languages, FPGA architecture, synthesis, simulation, timing, state machines and complete programmable digital-system implementation."},
)

LABS: Final[tuple[str, ...]] = (
    "Familiarisation with logic gates",
    "Combinational circuits",
    "Code converters",
    "Design with multiplexers",
    "Adders and subtractors",
    "Flip-flops",
    "Sequential circuits",
    "Counters",
    "Clock pulse generator",
)

LESSON_SECTIONS: Final[tuple[str, ...]] = (
    "Learning objectives", "Historical background", "Originator and contributors",
    "Theory", "Mathematical representation", "Truth table", "Logic symbol",
    "Timing behaviour", "Hardware implementation", "Interactive simulation",
    "Real-world applications", "Quiz", "Challenge", "Summary", "References",
)
