"""Typed Academy domain models and immutable registries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..academy_content import ACADEMY_UNITS


@dataclass(frozen=True, slots=True)
class LearningPath:
    number: int
    title: str
    hours: int
    lessons: int
    summary: str
    artwork: str
    practice_href: str
    practice_label: str


@dataclass(frozen=True, slots=True)
class LabPreview:
    title: str
    description: str
    icon: str
    href: str
    action: str
    tool: str
    status: str = "live"


ARTWORK: Final[dict[int, str]] = {
    1: "/academy/binary-systems.svg",
    2: "/academy/boolean-gates.svg",
    3: "/academy/kmap.svg",
    4: "/academy/combinational.svg",
    5: "/academy/msi-lsi.svg",
    6: "/academy/sequential.svg",
    7: "/academy/registers-counters.svg",
    8: "/academy/combinational.svg",
    9: "/academy/combinational.svg",
    10: "/academy/msi-lsi.svg",
    11: "/academy/sequential.svg",
    12: "/academy/msi-lsi.svg",
}

PATH_PRACTICE: Final[dict[int, tuple[str, str]]] = {
    1: ("/tools/number-systems", "Practice number systems"),
    2: ("/academy/unit-2/logic-states-and-gates", "Begin Path 02"),
    3: ("/tools/boolean", "Solve with Boolean Lab"),
    4: ("/tools/circuit", "Open Circuit Generator"),
    5: ("/", "Open MSI/LSI Simulator"),
    6: ("/", "Open Sequential Simulator"),
    7: ("/", "Open Registers & Counters"),
    8: ("/academy/unit-8/binary-arithmetic-hardware", "Begin ALU design"),
    9: ("/academy/unit-9/cpu-architecture-foundations", "Begin CPU architecture"),
    10: ("/academy/unit-10/system-interconnect-foundations", "Begin system integration"),
    11: ("/academy/unit-11/embedded-systems-foundations", "Begin embedded systems"),
    12: ("/academy/unit-12/hdl-fpga-foundations", "Begin HDL & FPGA"),
}

LEARNING_PATHS: Final[tuple[LearningPath, ...]] = tuple(
    LearningPath(
        int(unit["number"]),
        str(unit["title"]),
        int(unit["hours"]),
        int(unit["lessons"]),
        str(unit["summary"]),
        ARTWORK[int(unit["number"])],
        PATH_PRACTICE[int(unit["number"])][0],
        PATH_PRACTICE[int(unit["number"])][1],
    )
    for unit in ACADEMY_UNITS
)

LAB_PREVIEWS: Final[tuple[LabPreview, ...]] = (
    LabPreview(
        "Familiarisation with logic gates",
        "Place logic gates, switches and indicators on the live canvas and verify each truth table.",
        "circuit-board",
        "/",
        "Open gate simulator",
        "Simulator",
    ),
    LabPreview(
        "Boolean functions and K-maps",
        "Enter expressions or minterms, generate the truth table, simplify the function and inspect its K-map groups.",
        "table-properties",
        "/tools/boolean",
        "Open Boolean Lab",
        "Boolean Lab",
    ),
    LabPreview(
        "Number-system conversions",
        "Practice binary, octal, decimal and hexadecimal conversion with exact worked steps.",
        "binary",
        "/tools/number-systems",
        "Open Number Systems",
        "Number Systems",
    ),
    LabPreview(
        "Combinational circuit design",
        "Convert a Boolean function into an automatically laid-out gate circuit and inspect the realization.",
        "workflow",
        "/tools/circuit",
        "Open Circuit Generator",
        "Circuit Generator",
    ),
    LabPreview(
        "MSI/LSI design",
        "Build experiments with adders, subtractors, multiplexers, decoders, encoders and other MSI/LSI blocks.",
        "boxes",
        "/",
        "Open MSI/LSI simulator",
        "Simulator",
    ),
    LabPreview(
        "Flip-flops and sequential circuits",
        "Use clocks and flip-flops to observe state, triggering and sequential behaviour on the live simulator.",
        "timer-reset",
        "/",
        "Open sequential simulator",
        "Simulator",
    ),
    LabPreview(
        "Registers and counters",
        "Construct register and counter experiments using the simulator's sequential building blocks.",
        "list-ordered",
        "/",
        "Open counter simulator",
        "Simulator",
    ),
)

TOTAL_LESSONS: Final[int] = sum(path.lessons for path in LEARNING_PATHS)
