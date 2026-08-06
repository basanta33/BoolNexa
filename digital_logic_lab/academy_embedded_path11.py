"""BoolNexa Academy Path 11 — Embedded Systems & Real-Time Computing."""
from __future__ import annotations

import reflex as rx

from .ui import app_header

PANEL = {
    "border": "1px solid #e2e8f0",
    "border_radius": "16px",
    "padding": "22px",
    "background": "white",
    "width": "100%",
}


class EmbeddedSystemsState(rx.State):
    embedded_answer: str = ""
    embedded_feedback: str = ""
    realtime_answer: str = ""
    realtime_feedback: str = ""
    firmware_answer: str = ""
    firmware_feedback: str = ""
    gpio_answer: str = ""
    gpio_feedback: str = ""
    pull_answer: str = ""
    pull_feedback: str = ""
    driver_answer: str = ""
    driver_feedback: str = ""
    adc_answer: str = ""
    adc_feedback: str = ""
    nyquist_answer: str = ""
    nyquist_feedback: str = ""
    reference_answer: str = ""
    reference_feedback: str = ""
    pwm_answer: str = ""
    pwm_feedback: str = ""
    duty_answer: str = ""
    duty_feedback: str = ""
    timer_answer: str = ""
    timer_feedback: str = ""
    isr_answer: str = ""
    isr_feedback: str = ""
    latency_answer: str = ""
    latency_feedback: str = ""
    priority_answer: str = ""
    priority_feedback: str = ""
    rtos_answer: str = ""
    rtos_feedback: str = ""
    deadline_answer: str = ""
    deadline_feedback: str = ""
    preemption_answer: str = ""
    preemption_feedback: str = ""
    uart_answer: str = ""
    uart_feedback: str = ""
    spi_answer: str = ""
    spi_feedback: str = ""
    i2c_answer: str = ""
    i2c_feedback: str = ""
    watchdog_answer: str = ""
    watchdog_feedback: str = ""
    brownout_answer: str = ""
    brownout_feedback: str = ""
    fault_answer: str = ""
    fault_feedback: str = ""

    def set_embedded_answer(self, value: str) -> None:
        self.embedded_answer = value

    def set_realtime_answer(self, value: str) -> None:
        self.realtime_answer = value

    def set_firmware_answer(self, value: str) -> None:
        self.firmware_answer = value

    def set_gpio_answer(self, value: str) -> None:
        self.gpio_answer = value

    def set_pull_answer(self, value: str) -> None:
        self.pull_answer = value

    def set_driver_answer(self, value: str) -> None:
        self.driver_answer = value

    def set_adc_answer(self, value: str) -> None:
        self.adc_answer = value

    def set_nyquist_answer(self, value: str) -> None:
        self.nyquist_answer = value

    def set_reference_answer(self, value: str) -> None:
        self.reference_answer = value

    def set_pwm_answer(self, value: str) -> None:
        self.pwm_answer = value

    def set_duty_answer(self, value: str) -> None:
        self.duty_answer = value

    def set_timer_answer(self, value: str) -> None:
        self.timer_answer = value

    def set_isr_answer(self, value: str) -> None:
        self.isr_answer = value

    def set_latency_answer(self, value: str) -> None:
        self.latency_answer = value

    def set_priority_answer(self, value: str) -> None:
        self.priority_answer = value

    def set_rtos_answer(self, value: str) -> None:
        self.rtos_answer = value

    def set_deadline_answer(self, value: str) -> None:
        self.deadline_answer = value

    def set_preemption_answer(self, value: str) -> None:
        self.preemption_answer = value

    def set_uart_answer(self, value: str) -> None:
        self.uart_answer = value

    def set_spi_answer(self, value: str) -> None:
        self.spi_answer = value

    def set_i2c_answer(self, value: str) -> None:
        self.i2c_answer = value

    def set_watchdog_answer(self, value: str) -> None:
        self.watchdog_answer = value

    def set_brownout_answer(self, value: str) -> None:
        self.brownout_answer = value

    def set_fault_answer(self, value: str) -> None:
        self.fault_answer = value

    def check_watchdog(self) -> None:
        value = self.watchdog_answer.strip().lower().replace(" ", "").replace("-", "")
        self.watchdog_feedback = (
            "Correct. A watchdog timer detects missing software progress and can force recovery."
            if value in {"watchdog", "watchdogtimer", "wdt"}
            else "What hardware timer can reset or recover a system when software stops making expected progress?"
        )

    def check_brownout(self) -> None:
        value = self.brownout_answer.strip().lower().replace(" ", "").replace("-", "")
        self.brownout_feedback = (
            "Correct. Brownout detection protects operation when supply voltage falls below a safe threshold."
            if value in {"brownout", "brownoutdetector", "brownoutdetection", "bod"}
            else "What protection mechanism detects supply voltage dropping below a safe operating level?"
        )

    def check_fault(self) -> None:
        value = self.fault_answer.strip().lower().replace(" ", "").replace("-", "")
        self.fault_feedback = (
            "Correct. Fault containment prevents a local failure from propagating into the rest of the system."
            if value in {"faultcontainment", "containment", "faultisolation", "isolation"}
            else "What reliability principle keeps one failing subsystem from corrupting the rest of the system?"
        )

    def check_uart(self) -> None:
        value = self.uart_answer.strip().lower().replace(" ", "").replace("-", "")
        self.uart_feedback = (
            "Correct. UART is asynchronous serial communication and normally does not require a shared clock line."
            if value in {"uart", "universalasynchronousreceivertransmitter"}
            else "Which common serial peripheral communicates asynchronously without a shared clock line?"
        )

    def check_spi(self) -> None:
        value = self.spi_answer.strip().lower().replace(" ", "").replace("-", "")
        self.spi_feedback = (
            "Correct. SPI commonly uses a serial clock plus separate controller-to-peripheral and peripheral-to-controller data paths."
            if value in {"spi", "serialperipheralinterface"}
            else "Which synchronous serial interface commonly uses SCLK plus separate data paths?"
        )

    def check_i2c(self) -> None:
        value = self.i2c_answer.strip().lower().replace(" ", "").replace("-", "").replace("²", "2")
        self.i2c_feedback = (
            "Correct. I²C uses SDA for data and SCL for clock on a shared addressed bus."
            if value in {"i2c", "iic", "interintegratedcircuit"}
            else "Which two-wire addressed bus commonly uses SDA and SCL?"
        )

    def check_rtos(self) -> None:
        value = self.rtos_answer.strip().lower().replace(" ", "").replace("-", "")
        self.rtos_feedback = (
            "Correct. RTOS means real-time operating system."
            if value in {"rtos", "realtimeoperatingsystem"}
            else "What does RTOS stand for?"
        )

    def check_deadline(self) -> None:
        value = self.deadline_answer.strip().lower().replace(" ", "").replace("-", "")
        self.deadline_feedback = (
            "Correct. A deadline is the time by which a real-time activity must complete or produce its required result."
            if value in {"deadline", "timedeadline"}
            else "What term describes the required completion time bound for a real-time activity?"
        )

    def check_preemption(self) -> None:
        value = self.preemption_answer.strip().lower().replace(" ", "").replace("-", "")
        self.preemption_feedback = (
            "Correct. Preemption lets the scheduler suspend one task so a more urgent eligible task can run."
            if value in {"preemption", "preemptive", "preempt"}
            else "What scheduling mechanism allows a running task to be suspended so another eligible task can execute?"
        )

    def check_isr(self) -> None:
        value = self.isr_answer.strip().lower().replace(" ", "").replace("-", "")
        self.isr_feedback = (
            "Correct. An ISR is the interrupt service routine executed in response to an interrupt."
            if value in {"isr", "interruptserviceroutine", "interrupthandler"}
            else "What routine runs when the processor accepts an interrupt?"
        )

    def check_latency(self) -> None:
        value = self.latency_answer.strip().lower().replace(" ", "").replace("-", "")
        self.latency_feedback = (
            "Correct. Interrupt latency is the delay from the interrupt event/request until its handler begins executing."
            if value in {"interruptlatency", "latency", "responselatency"}
            else "What term describes the delay between an interrupt request and the start of its handler?"
        )

    def check_priority(self) -> None:
        value = self.priority_answer.strip().lower().replace(" ", "").replace("-", "")
        self.priority_feedback = (
            "Correct. Interrupt priority determines which pending interrupt is serviced first and, where supported, which handler may pre-empt another."
            if value in {"priority", "interruptpriority", "prioritylevel"}
            else "What interrupt property determines precedence when multiple interrupt sources compete for CPU service?"
        )

    def check_pwm(self) -> None:
        value = self.pwm_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pwm_feedback = (
            "Correct. PWM means pulse-width modulation."
            if value in {"pwm", "pulsewidthmodulation"}
            else "What does the abbreviation PWM stand for?"
        )

    def check_duty(self) -> None:
        value = self.duty_answer.strip().lower().replace(" ", "").replace("%", "")
        self.duty_feedback = (
            "Correct. A 50% duty cycle keeps the waveform high for half of each period."
            if value in {"50", "half", "onehalf", "50percent"}
            else "If a signal is high for exactly half of every period, what is its duty cycle?"
        )

    def check_timer(self) -> None:
        value = self.timer_answer.strip().lower().replace(" ", "").replace("-", "")
        self.timer_feedback = (
            "Correct. A timer/counter advances from a clock or event source and can generate compare or overflow events."
            if value in {"timer", "counter", "timercounter", "timer/counter"}
            else "Which hardware peripheral counts clock ticks and can create compare or overflow events?"
        )

    def check_adc(self) -> None:
        value = self.adc_answer.strip().lower().replace(" ", "").replace("-", "")
        self.adc_feedback = (
            "Correct. An ADC converts an analog input level into a digital numeric code."
            if value in {"adc", "analogtodigitalconverter", "analoguetodigitalconverter"}
            else "Which converter changes an analog voltage into a digital number?"
        )

    def check_nyquist(self) -> None:
        value = self.nyquist_answer.strip().lower().replace(" ", "").replace("-", "")
        self.nyquist_feedback = (
            "Correct. A sampled system needs a sampling rate greater than twice the highest signal frequency to avoid aliasing in the ideal band-limited case."
            if value in {"twice", "2x", "2", "greaterthantwice", "morethantwice", "nyquist"}
            else "Relative to the highest signal frequency, what minimum sampling-rate relationship is required by the Nyquist criterion?"
        )

    def check_reference(self) -> None:
        value = self.reference_answer.strip().lower().replace(" ", "").replace("-", "")
        self.reference_feedback = (
            "Correct. The ADC reference defines the voltage scale used to map an input into digital codes."
            if value in {"reference", "vref", "referencevoltage", "voltagereference", "adcreference"}
            else "What voltage defines the ADC conversion scale or full-scale reference?"
        )

    def check_gpio(self) -> None:
        value = self.gpio_answer.strip().lower().replace(" ", "").replace("-", "")
        self.gpio_feedback = (
            "Correct. GPIO is the general-purpose digital input/output interface used for software-controlled pins."
            if value in {"gpio", "generalpurposeio", "generalpurposeinputoutput"}
            else "What peripheral gives software direct general-purpose control of digital input/output pins?"
        )

    def check_pull(self) -> None:
        value = self.pull_answer.strip().lower().replace(" ", "").replace("-", "")
        self.pull_feedback = (
            "Correct. A pull-up or pull-down resistor gives an otherwise undriven input a defined default logic level."
            if value in {"pullup", "pulldown", "pullresistor", "pullupresistor", "pulldownresistor"}
            else "What resistor arrangement gives a digital input a defined level when no external source drives it?"
        )

    def check_driver(self) -> None:
        value = self.driver_answer.strip().lower().replace(" ", "").replace("-", "")
        self.driver_feedback = (
            "Correct. A driver stage lets a low-power logic pin safely control a higher-current load."
            if value in {"driver", "driverstage", "transistor", "mosfet", "transistordriver"}
            else "What interface stage is used when a GPIO pin cannot safely supply the current required by a load?"
        )

    def check_embedded(self) -> None:
        value = self.embedded_answer.strip().lower().replace(" ", "").replace("-", "")
        self.embedded_feedback = (
            "Correct. An embedded system is a computer built into a larger product to perform a focused function."
            if value in {"embeddedsystem", "embeddedcomputer", "embedded"}
            else "What kind of computer is built into a larger product for a dedicated function?"
        )

    def check_realtime(self) -> None:
        value = self.realtime_answer.strip().lower().replace(" ", "").replace("-", "")
        self.realtime_feedback = (
            "Correct. A real-time requirement includes a timing deadline, not only a logically correct result."
            if value in {"deadline", "timingdeadline", "realtime", "timingconstraint"}
            else "What timing requirement says a result must be produced before a specified time limit?"
        )

    def check_firmware(self) -> None:
        value = self.firmware_answer.strip().lower().replace(" ", "").replace("-", "")
        self.firmware_feedback = (
            "Correct. Firmware is software closely tied to the embedded hardware and stored for device operation."
            if value in {"firmware", "embeddedsoftware"}
            else "What do we commonly call software stored in and closely controlling an embedded device?"
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(number, color_scheme="teal"),
                rx.heading(title, size="5"),
                align="center",
            ),
            *children,
            spacing="4",
            align="stretch",
        ),
        style=PANEL,
    )


def _practice(question, value, setter, checker, feedback, placeholder) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(question, weight="bold"),
            rx.hstack(
                rx.input(value=value, on_change=setter, placeholder=placeholder, width="100%"),
                rx.button("Check", on_click=checker, color_scheme="teal"),
                width="100%",
            ),
            rx.cond(feedback != "", rx.text(feedback, size="2", color="#0f766e")),
            spacing="2",
            align="stretch",
        ),
        padding="14px",
        border="1px solid #5eead4",
        border_radius="12px",
        background="#f0fdfa",
        width="100%",
    )


def embedded_systems_foundations_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 01", color_scheme="teal", width="100%"),
            rx.heading("Embedded Systems Foundations", size="8"),
            rx.text(
                "An embedded system combines a processor, memory, peripherals and software inside a larger product. Unlike a general-purpose computer, it is designed around a specific function, physical environment, timing requirement and resource budget.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "What makes a computer embedded",
                rx.text(
                    "An embedded computer is part of a larger device rather than being the product's general-purpose computing interface. It may control a washing machine, vehicle subsystem, medical instrument, router, sensor node or industrial controller."
                ),
                rx.code_block(
                    "larger product\n"
                    "┌────────────────────────────────────┐\n"
                    "│ sensors → embedded computer → actuators │\n"
                    "│              │                         │\n"
                    "│           firmware                     │\n"
                    "└────────────────────────────────────┘",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "What kind of computer is built into a larger product for a dedicated function?",
                    EmbeddedSystemsState.embedded_answer,
                    EmbeddedSystemsState.set_embedded_answer,
                    EmbeddedSystemsState.check_embedded,
                    EmbeddedSystemsState.embedded_feedback,
                    "computer type",
                ),
            ),
            _section(
                "2",
                "Embedded design begins with system requirements",
                rx.text(
                    "Hardware and software choices follow from requirements. A designer must know what inputs are sensed, what outputs are controlled, how quickly the system must react, how much energy it may consume and what failures are acceptable."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Requirement"),
                            rx.table.column_header_cell("Example question"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Function"), rx.table.cell("What must the product do?")),
                        rx.table.row(rx.table.cell("Timing"), rx.table.cell("How quickly must it react?")),
                        rx.table.row(rx.table.cell("Power"), rx.table.cell("Battery-powered, mains-powered or energy-limited?")),
                        rx.table.row(rx.table.cell("Memory"), rx.table.cell("How much code/data/storage is required?")),
                        rx.table.row(rx.table.cell("Reliability"), rx.table.cell("What happens if software or hardware fails?")),
                        rx.table.row(rx.table.cell("Cost"), rx.table.cell("What hardware budget is practical at product scale?")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "3",
                "Microcontrollers integrate a small computer on one chip",
                rx.text(
                    "A microcontroller commonly combines a CPU core, program memory, RAM and peripheral controllers on one integrated circuit. This reduces component count and makes it well suited to embedded control."
                ),
                rx.code_block(
                    "┌──────────── microcontroller ────────────┐\n"
                    "│ CPU │ Flash/ROM │ RAM │ GPIO │ Timers │\n"
                    "│     UART / SPI / I²C / ADC / other I/O │\n"
                    "└─────────────────────────────────────────┘",
                    language="textile",
                    width="100%",
                ),
                rx.text(
                    "Path 09 explained the CPU; Path 10 connected memory and peripherals; Path 11 now uses those blocks as a complete embedded platform."
                ),
            ),
            _section(
                "4",
                "Inputs connect software to the physical world",
                rx.text(
                    "Digital inputs may read switches or logic-level sensors. Analog-to-digital converters can measure continuously varying signals such as temperature-sensor voltage. Communication peripherals receive information from other devices."
                ),
                rx.code_block(
                    "physical quantity → sensor → electrical signal → interface/ADC → software value",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "5",
                "Outputs let software affect the physical world",
                rx.text(
                    "GPIO can drive digital control signals, timers can generate PWM, and communication interfaces can command external controllers. Higher-power loads usually require driver electronics rather than being connected directly to processor pins."
                ),
                rx.code_block(
                    "software decision → peripheral register → output signal → driver → actuator",
                    language="textile",
                    width="100%",
                ),
                rx.callout(
                    "A processor pin is a logic interface, not automatically a power source for motors, heaters or other high-current loads.",
                    icon="triangle-alert",
                    color_scheme="orange",
                ),
            ),
            _section(
                "6",
                "Firmware is the hardware-aware software layer",
                rx.text(
                    "Firmware initializes the processor, configures clocks and peripherals, responds to events, processes data and controls outputs. It is often stored in nonvolatile program memory so the device can start without loading an operating system from disk."
                ),
                _practice(
                    "What do we commonly call software stored in and closely controlling an embedded device?",
                    EmbeddedSystemsState.firmware_answer,
                    EmbeddedSystemsState.set_firmware_answer,
                    EmbeddedSystemsState.check_firmware,
                    EmbeddedSystemsState.firmware_feedback,
                    "embedded software",
                ),
            ),
            _section(
                "7",
                "Super-loop firmware is the simplest execution model",
                rx.text(
                    "A small embedded program may initialize hardware once and then repeat a main loop forever. Each iteration checks inputs, updates internal state and drives outputs."
                ),
                rx.code_block(
                    "initialize hardware\n"
                    "while true:\n"
                    "    read inputs\n"
                    "    update control logic\n"
                    "    update outputs\n"
                    "    handle background work",
                    language="textile",
                    width="100%",
                ),
                rx.text(
                    "This model is easy to understand, but long-running work in one part of the loop can delay everything else."
                ),
            ),
            _section(
                "8",
                "Interrupts make embedded systems event-responsive",
                rx.text(
                    "Timers, communication peripherals and external pins can interrupt the CPU when an event needs attention. The main program can continue background work instead of polling every source continuously."
                ),
                rx.code_block(
                    "main loop ────────────────┐\n"
                    "                          │ timer/UART/GPIO event\n"
                    "                          ↓\n"
                    "                    interrupt service\n"
                    "                          │\n"
                    "                          └────→ resume main loop",
                    language="textile",
                    width="100%",
                ),
                rx.callout(
                    "Interrupt handlers should generally do bounded, necessary work and defer larger processing when possible.",
                    icon="info",
                    color_scheme="blue",
                ),
            ),
            _section(
                "9",
                "Real-time correctness includes time",
                rx.text(
                    "A real-time system is not defined merely by being fast. Correctness can depend on producing the required result before a deadline. Missing the deadline may reduce quality or may be unacceptable, depending on the system."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Type"),
                            rx.table.column_header_cell("Meaning"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Soft real-time"), rx.table.cell("Occasional deadline misses degrade service but may be tolerated")),
                        rx.table.row(rx.table.cell("Hard real-time"), rx.table.cell("A required deadline must not be missed for correct/safe operation")),
                    ),
                    width="100%",
                ),
                _practice(
                    "What timing requirement says a result must be produced before a specified time limit?",
                    EmbeddedSystemsState.realtime_answer,
                    EmbeddedSystemsState.set_realtime_answer,
                    EmbeddedSystemsState.check_realtime,
                    EmbeddedSystemsState.realtime_feedback,
                    "time limit",
                ),
            ),
            _section(
                "10",
                "Resource constraints shape architecture",
                rx.text(
                    "Embedded systems may have limited RAM, Flash, CPU performance, energy, pins and bandwidth. Good design therefore avoids unnecessary work and selects hardware appropriate to the real task."
                ),
                rx.hstack(
                    rx.badge("CPU", color_scheme="blue"),
                    rx.text("execution budget"),
                    rx.badge("RAM", color_scheme="purple"),
                    rx.text("working data"),
                    rx.badge("Flash", color_scheme="orange"),
                    rx.text("program/storage"),
                    rx.badge("Power", color_scheme="green"),
                    rx.text("energy budget"),
                    wrap="wrap",
                    spacing="2",
                ),
            ),
            _section(
                "11",
                "Trace a simple temperature-control system",
                rx.code_block(
                    "1. timer generates a periodic sampling event\n"
                    "2. firmware starts/reads temperature sensor conversion\n"
                    "3. measured value enters RAM\n"
                    "4. control logic compares temperature with set point\n"
                    "5. timer/PWM or GPIO updates fan/heater command\n"
                    "6. watchdog confirms software continues making progress\n"
                    "7. communication interface may report status externally\n"
                    "8. loop repeats before the next required deadline",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "12",
                "Lesson checkpoint",
                rx.text(
                    "You can now define an embedded system, identify the role of a microcontroller, connect sensors and actuators to firmware, explain super-loop and interrupt-driven execution, and distinguish functional correctness from real-time timing correctness."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 01 COMPLETE", color_scheme="green"),
                    rx.heading("The complete computer is now being designed for a physical task.", size="5"),
                    rx.text(
                        "Next: learn digital and analog GPIO, pin configuration and safe hardware interfacing.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · GPIO, Pin Control & Hardware Interfacing", color_scheme="teal"),
                        href="/academy/unit-11/gpio-pin-control-hardware-interfacing",
                        text_decoration="none",
                    ),
                    spacing="3",
                    align="start",
                ),
                width="100%",
            ),
            spacing="6",
            align="stretch",
            max_width="1050px",
            width="100%",
            margin="0 auto",
            padding="32px 20px 64px",
        ),
        min_height="100vh",
        background="#f8fafc",
    )


def gpio_pin_control_hardware_interfacing_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 02", color_scheme="teal", width="100%"),
            rx.heading("GPIO, Pin Control & Hardware Interfacing", size="8"),
            rx.text(
                "General-purpose input/output (GPIO) pins are the simplest bridge between firmware and external hardware. Safe GPIO use requires more than writing 0 or 1: software must configure direction, electrical behavior, default levels and the interface between low-power logic and real-world loads.",
                size="4",
                color="#475569",
                line_height="1.6",
            ),
            _section(
                "1",
                "GPIO turns processor pins into programmable digital interfaces",
                rx.text(
                    "A GPIO peripheral lets software configure selected pins as digital inputs or outputs. The same physical package pin may also support alternate peripheral functions such as UART, SPI, PWM or timer capture."
                ),
                rx.code_block(
                    "CPU bus → GPIO registers → pin control logic → package pin\n"
                    "                         ↑\n"
                    "                    direction / value",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "What peripheral gives software direct general-purpose control of digital input/output pins?",
                    EmbeddedSystemsState.gpio_answer,
                    EmbeddedSystemsState.set_gpio_answer,
                    EmbeddedSystemsState.check_gpio,
                    EmbeddedSystemsState.gpio_feedback,
                    "digital pin peripheral",
                ),
            ),
            _section(
                "2",
                "Direction decides whether the pin senses or drives",
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Mode"),
                            rx.table.column_header_cell("Meaning"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Input"), rx.table.cell("External circuitry determines the pin level; software reads it")),
                        rx.table.row(rx.table.cell("Output"), rx.table.cell("GPIO output driver actively drives a configured logic level")),
                        rx.table.row(rx.table.cell("Alternate function"), rx.table.cell("Another peripheral controls or samples the pin")),
                    ),
                    width="100%",
                ),
                rx.callout(
                    "Avoid configuring two connected outputs to drive opposite levels. That creates electrical contention rather than a valid logic operation.",
                    icon="triangle-alert",
                    color_scheme="orange",
                ),
            ),
            _section(
                "3",
                "GPIO registers expose pin state to firmware",
                rx.text(
                    "A typical controller provides direction, output-data and input-data registers. Some devices also provide atomic set/clear registers so software can change selected bits without disturbing neighboring pins."
                ),
                rx.code_block(
                    "DIR     bit=1 → output, bit=0 → input\n"
                    "OUT     value requested on output pins\n"
                    "IN      sampled logic levels from pins\n"
                    "SET/CLR optional atomic output-bit control",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "4",
                "Inputs must not be left electrically undefined",
                rx.text(
                    "A high-impedance input draws very little current and may not settle to a predictable logic level if nothing drives it. Pull-up or pull-down resistors establish a default state."
                ),
                rx.code_block(
                    "pull-up input\n"
                    "Vcc ── resistor ──┬── GPIO input\n"
                    "                  └── switch ── GND\n\n"
                    "switch open  → input reads HIGH\n"
                    "switch closed→ input reads LOW",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "What resistor arrangement gives a digital input a defined level when no external source drives it?",
                    EmbeddedSystemsState.pull_answer,
                    EmbeddedSystemsState.set_pull_answer,
                    EmbeddedSystemsState.check_pull,
                    EmbeddedSystemsState.pull_feedback,
                    "input bias",
                ),
            ),
            _section(
                "5",
                "Mechanical switches can bounce",
                rx.text(
                    "A physical switch does not always transition cleanly once. Contacts can briefly open and close several times, causing multiple digital edges from one human press. Debouncing filters those transitions in hardware or software."
                ),
                rx.code_block(
                    "ideal press:   ____|‾‾‾‾‾‾\n"
                    "real press:    ____|‾|_|‾|_‾‾‾\n"
                    "debounced:     _________|‾‾‾‾",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "6",
                "Logic levels and voltage limits matter",
                rx.text(
                    "A digital HIGH is not an abstract 1 at the pin; it is a voltage that must fall within the receiver's valid input range. GPIO pins also have maximum voltage and current ratings."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Check"),
                            rx.table.column_header_cell("Why it matters"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Input voltage"), rx.table.cell("Too high can damage the device")),
                        rx.table.row(rx.table.cell("HIGH/LOW thresholds"), rx.table.cell("Levels must be recognized reliably")),
                        rx.table.row(rx.table.cell("Output current"), rx.table.cell("Pin driver has limited source/sink capability")),
                        rx.table.row(rx.table.cell("Total package current"), rx.table.cell("Many active pins can exceed shared limits")),
                    ),
                    width="100%",
                ),
                rx.callout(
                    "Exact electrical limits come from the microcontroller datasheet. Never infer them only from the logic value used in software.",
                    icon="info",
                    color_scheme="blue",
                ),
            ),
            _section(
                "7",
                "High-current loads need a driver stage",
                rx.text(
                    "LEDs need current limiting, while relays, motors and other loads usually require a transistor or dedicated driver. The GPIO controls the driver; the driver handles the load current."
                ),
                rx.code_block(
                    "GPIO ─→ resistor/gate drive ─→ transistor/MOSFET ─→ load\n"
                    "                                                  ↑\n"
                    "                                           external supply",
                    language="textile",
                    width="100%",
                ),
                _practice(
                    "What interface stage is used when a GPIO pin cannot safely supply the current required by a load?",
                    EmbeddedSystemsState.driver_answer,
                    EmbeddedSystemsState.set_driver_answer,
                    EmbeddedSystemsState.check_driver,
                    EmbeddedSystemsState.driver_feedback,
                    "load interface",
                ),
            ),
            _section(
                "8",
                "Inductive loads need protection",
                rx.text(
                    "Relays, solenoids and motors store energy in magnetic fields. When current is switched off, the changing field can create a large voltage. Appropriate suppression such as a flyback path protects the switching device."
                ),
                rx.code_block(
                    "supply ── coil/load ── transistor ── GND\n"
                    "          │        │\n"
                    "          └─ protection path across inductive load",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "9",
                "Pin multiplexing selects GPIO or peripheral ownership",
                rx.text(
                    "A microcontroller has limited package pins, so one pin may serve several internal peripherals. Pin-multiplexer configuration determines whether GPIO, UART, SPI, timer/PWM or another block owns the signal."
                ),
                rx.code_block(
                    "GPIO ───┐\n"
                    "UART ───┼─→ pin multiplexer ─→ physical pin\n"
                    "Timer ──┤\n"
                    "SPI ────┘",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "10",
                "Safe initialization prevents unwanted output glitches",
                rx.text(
                    "Startup order matters. Firmware should establish a safe output value and electrical configuration before enabling a pin that controls a real actuator."
                ),
                rx.code_block(
                    "safer startup example\n"
                    "1. determine required safe level\n"
                    "2. preload output-data register\n"
                    "3. configure pull/drive behavior\n"
                    "4. switch pin direction or mux to active output\n"
                    "5. enable downstream hardware if required",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "11",
                "Trace a button-controlled LED",
                rx.code_block(
                    "1. configure BUTTON pin as input with pull-up\n"
                    "2. configure LED control pin as output\n"
                    "3. preload LED output to safe OFF state\n"
                    "4. read BUTTON input\n"
                    "5. debounce the sampled state\n"
                    "6. if pressed, write LED output active\n"
                    "7. if released, write LED output inactive\n"
                    "8. repeat or respond through an interrupt",
                    language="textile",
                    width="100%",
                ),
            ),
            _section(
                "12",
                "Lesson checkpoint",
                rx.text(
                    "You can now configure GPIO direction and data, explain pull resistors and switch bounce, respect voltage/current constraints, identify when a driver stage is required, understand pin multiplexing, and plan a safe hardware startup sequence."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 02 COMPLETE", color_scheme="green"),
                    rx.heading("Firmware can now safely sense and drive external digital hardware.", size="5"),
                    rx.text(
                        "Next: learn analog sensing, ADC conversion, sampling and sensor acquisition.",
                        color="#475569",
                    ),
                    rx.button("Lesson 3 · ADC, Analog Signals & Sensor Acquisition", on_click=rx.redirect("/academy/unit-11/adc-analog-signals-sensor-acquisition")),
                    spacing="3",
                    align="start",
                ),
                width="100%",
            ),
            spacing="6",
            align="stretch",
            max_width="1050px",
            width="100%",
            margin="0 auto",
            padding="32px 20px 64px",
        ),
        min_height="100vh",
        background="#f8fafc",
    )


def adc_analog_signals_sensor_acquisition_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 03", color_scheme="teal", width="100%"),
            rx.heading("ADC, Analog Signals & Sensor Acquisition", size="8"),
            rx.text(
                "Embedded systems often need to measure physical quantities that are not naturally binary. Sensors convert temperature, light, pressure, position, sound and other phenomena into electrical signals; an analog-to-digital converter (ADC) lets firmware represent those signals as numbers.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Analog signals vary continuously over a range",
                rx.text("A digital input classifies a voltage as a logic state, while an analog input measures where a signal lies within an allowed range. Real sensors may produce a voltage directly or require conditioning before conversion."),
                rx.code_block(
                    "physical quantity → sensor → analog voltage → ADC → digital code → firmware\n\n"
                    "temperature       electrical signal          number",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which converter changes an analog voltage into a digital number?",
                    EmbeddedSystemsState.adc_answer, EmbeddedSystemsState.set_adc_answer,
                    EmbeddedSystemsState.check_adc, EmbeddedSystemsState.adc_feedback, "converter",
                ),
            ),
            _section(
                "2", "An ADC quantises voltage into discrete codes",
                rx.text("An N-bit ADC has 2^N possible output codes. Increasing resolution provides more code levels across the same input range, reducing the ideal quantisation step size."),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Resolution"),
                        rx.table.column_header_cell("Ideal code levels"),
                        rx.table.column_header_cell("Example"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("8-bit"), rx.table.cell("256"), rx.table.cell("codes 0–255")),
                        rx.table.row(rx.table.cell("10-bit"), rx.table.cell("1024"), rx.table.cell("codes 0–1023")),
                        rx.table.row(rx.table.cell("12-bit"), rx.table.cell("4096"), rx.table.cell("codes 0–4095")),
                        rx.table.row(rx.table.cell("16-bit"), rx.table.cell("65536"), rx.table.cell("codes 0–65535")),
                    ), width="100%",
                ),
            ),
            _section(
                "3", "The reference voltage defines the conversion scale",
                rx.text("The ADC reference voltage establishes the scale against which the input is measured. For a simple unipolar ideal ADC, the input range commonly extends from ground toward the reference/full-scale limit."),
                rx.code_block(
                    "ideal relationship:\n"
                    "code ≈ (Vin / Vref) × full-scale code\n\n"
                    "Example idea: same Vin + smaller valid Vref → larger code",
                    language="textile", width="100%",
                ),
                _practice(
                    "What voltage defines the ADC conversion scale or full-scale reference?",
                    EmbeddedSystemsState.reference_answer, EmbeddedSystemsState.set_reference_answer,
                    EmbeddedSystemsState.check_reference, EmbeddedSystemsState.reference_feedback, "voltage scale",
                ),
            ),
            _section(
                "4", "Sampling turns a time-varying signal into measurements",
                rx.text("An ADC observes the input at discrete instants. The sampling rate states how many conversions are taken each second. A sample-and-hold circuit may briefly capture the input so it remains sufficiently stable during conversion."),
                rx.code_block(
                    "analog waveform:   ~~~~~~~ continuous ~~~~~~~\n"
                    "sample instants:   |  |  |  |  |  |  |  |\n"
                    "digital samples:   42 47 55 51 44 39 41 48",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Sampling too slowly causes aliasing",
                rx.text("If the sampling rate is too low, different analog frequencies can produce indistinguishable sampled data. For an ideally band-limited signal, the Nyquist criterion requires a sampling frequency greater than twice the highest frequency that must be represented."),
                rx.callout(
                    "Real acquisition systems normally use an analog anti-alias filter before the ADC so unwanted frequency content above the intended measurement band is attenuated.",
                    icon="info", color_scheme="blue",
                ),
                _practice(
                    "Relative to the highest signal frequency, what minimum sampling-rate relationship is required by the Nyquist criterion?",
                    EmbeddedSystemsState.nyquist_answer, EmbeddedSystemsState.set_nyquist_answer,
                    EmbeddedSystemsState.check_nyquist, EmbeddedSystemsState.nyquist_feedback, "sampling relationship",
                ),
            ),
            _section(
                "6", "Sensor conditioning prepares the signal for the ADC",
                rx.text("A sensor output may be too small, too noisy, offset from the required range or too high in impedance. Conditioning circuits can amplify, attenuate, level-shift, buffer and filter the signal."),
                rx.code_block(
                    "sensor → protection → amplifier/buffer → low-pass filter → ADC\n"
                    "           safe range      usable scale        anti-alias",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Source impedance and acquisition time affect accuracy",
                rx.text("Many microcontroller ADCs charge an internal sampling capacitor from the external source. If the source impedance is too high or the acquisition interval too short, that capacitor may not settle close enough to the true input voltage."),
                rx.callout(
                    "ADC input-drive requirements are device-specific. Use the microcontroller datasheet when selecting source impedance, acquisition time and any buffer amplifier.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "8", "Noise and grounding can move measured codes",
                rx.text("Power-supply noise, digital switching, poor grounding, long sensor wiring and electromagnetic interference can disturb analog measurements. Layout, decoupling, filtering and sensible separation of noisy and sensitive paths improve acquisition quality."),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Problem"),
                        rx.table.column_header_cell("Typical design response"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("High-frequency noise"), rx.table.cell("Analog low-pass filtering")),
                        rx.table.row(rx.table.cell("Supply/reference noise"), rx.table.cell("Decoupling and stable reference design")),
                        rx.table.row(rx.table.cell("Long/noisy wiring"), rx.table.cell("Shielding, differential sensing or filtering where appropriate")),
                        rx.table.row(rx.table.cell("Random sample variation"), rx.table.cell("Averaging/oversampling when bandwidth permits")),
                    ), width="100%",
                ),
            ),
            _section(
                "9", "Calibration converts ADC codes into useful units",
                rx.text("Firmware usually needs engineering units rather than raw codes. A conversion model can apply scale and offset, while calibration compares measurements with known references to estimate and correct systematic error."),
                rx.code_block(
                    "raw ADC code → voltage estimate → sensor transfer function → engineering unit\n"
                    "     2480     →     2.00 V      →       model       →     25 °C",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "ADC acquisition can be polled, interrupted or DMA-driven",
                rx.text("Slow occasional measurements may be started and read by firmware directly. Periodic sampling can use a timer trigger plus an interrupt. High-rate streams can use DMA to move conversion results into a memory buffer with little CPU work."),
                rx.code_block(
                    "timer → ADC trigger → conversion → DMA → sample buffer\n"
                    "                                      ↓\n"
                    "                              firmware processes block",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace a complete temperature-sensor acquisition",
                rx.code_block(
                    "1. determine sensor output range and bandwidth\n"
                    "2. verify ADC input and reference-voltage limits\n"
                    "3. condition/filter the analog signal if required\n"
                    "4. choose resolution and sampling rate\n"
                    "5. configure ADC channel and acquisition timing\n"
                    "6. trigger conversions from software or a timer\n"
                    "7. collect samples by polling, interrupt or DMA\n"
                    "8. convert codes to voltage\n"
                    "9. apply sensor calibration/transfer function\n"
                    "10. validate readings against known conditions",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text("You can now distinguish analog and digital sensing, explain ADC resolution and reference voltage, reason about sampling and aliasing, identify signal-conditioning needs, and trace a sensor measurement from the physical world into calibrated firmware data."),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 03 COMPLETE", color_scheme="green"),
                    rx.heading("The embedded system can now acquire real-world analog measurements.", size="5"),
                    rx.text("Next: learn PWM, timers and waveform generation for controlling power and timing external hardware.", color="#475569"),
                    rx.button("Lesson 4 · PWM, Timers & Waveform Generation", on_click=rx.redirect("/academy/unit-11/pwm-timers-waveform-generation")),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def pwm_timers_waveform_generation_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 04", color_scheme="teal", width="100%"),
            rx.heading("PWM, Timers & Waveform Generation", size="8"),
            rx.text(
                "Embedded systems frequently need precise timing without forcing the CPU to toggle pins in software. Hardware timers count clock events, while output-compare and PWM hardware transform those counts into periodic events and waveforms for motors, LEDs, audio, power conversion and communication timing.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A hardware timer counts from a time base",
                rx.text("A timer/counter receives a clock or external event source and advances a numeric count. Prescalers can divide a fast peripheral clock so the counter advances more slowly, extending the measurable interval."),
                rx.code_block(
                    "peripheral clock → prescaler → timer/counter → compare/overflow event\n"
                    "   48 MHz           ÷48          1 MHz count       precise timing",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which hardware peripheral counts clock ticks and can create compare or overflow events?",
                    EmbeddedSystemsState.timer_answer, EmbeddedSystemsState.set_timer_answer,
                    EmbeddedSystemsState.check_timer, EmbeddedSystemsState.timer_feedback, "timing peripheral",
                ),
            ),
            _section(
                "2", "Period and frequency describe repeating waveforms",
                rx.text("Frequency tells how many cycles occur each second. Period is the duration of one cycle, so frequency and period are reciprocals."),
                rx.code_block(
                    "frequency f = 1 / T\n"
                    "period    T = 1 / f\n\n"
                    "1 kHz → T = 1 ms\n"
                    "100 Hz → T = 10 ms",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Compare registers schedule events at exact counts",
                rx.text("A timer can compare its current count with a programmed value. A match may set a status flag, request an interrupt, reset the counter or change an output pin entirely in hardware."),
                rx.code_block(
                    "count:   0 1 2 3 4 5 6 7 0 1 2 ...\n"
                    "compare:       ^       ^\n"
                    "event:         X       X",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "4", "PWM encodes control in pulse width",
                rx.text("Pulse-width modulation repeats a digital pulse at a chosen frequency while varying how long the output remains active during each period. Loads that respond to average energy can therefore be controlled efficiently with a switching signal."),
                rx.code_block(
                    "25%:  ┌─┐   ┌─┐   ┌─┐\n"
                    "      │ │___│ │___│ │___\n\n"
                    "50%:  ┌──┐  ┌──┐  ┌──┐\n"
                    "      │  │__│  │__│  │__\n\n"
                    "75%:  ┌───┐ ┌───┐ ┌───┐\n"
                    "      │   |_|   |_|   |_",
                    language="textile", width="100%",
                ),
                _practice(
                    "What does PWM stand for?",
                    EmbeddedSystemsState.pwm_answer, EmbeddedSystemsState.set_pwm_answer,
                    EmbeddedSystemsState.check_pwm, EmbeddedSystemsState.pwm_feedback, "abbreviation",
                ),
            ),
            _section(
                "5", "Duty cycle is the active fraction of a period",
                rx.text("Duty cycle is commonly expressed as a percentage: active time divided by total period, multiplied by 100. Polarity matters: an active-low output reverses the electrical interpretation of high and low."),
                rx.code_block(
                    "duty cycle = Ton / Tperiod × 100%\n\n"
                    "Ton = 0.5 ms, period = 1 ms → duty = 50%",
                    language="textile", width="100%",
                ),
                _practice(
                    "If a signal is high for exactly half of every period, what is its duty cycle?",
                    EmbeddedSystemsState.duty_answer, EmbeddedSystemsState.set_duty_answer,
                    EmbeddedSystemsState.check_duty, EmbeddedSystemsState.duty_feedback, "percentage",
                ),
            ),
            _section(
                "6", "Timer resolution limits waveform choices",
                rx.text("The timer clock and counter width determine which periods and duty steps can be represented. A higher PWM frequency leaves fewer timer counts per period unless the timer clock is also increased."),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Design choice"),
                        rx.table.column_header_cell("Effect"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Faster timer clock"), rx.table.cell("Finer timing resolution")),
                        rx.table.row(rx.table.cell("Larger prescaler"), rx.table.cell("Longer range, coarser timing")),
                        rx.table.row(rx.table.cell("Higher PWM frequency"), rx.table.cell("Shorter period and often fewer duty steps")),
                        rx.table.row(rx.table.cell("Wider counter"), rx.table.cell("Larger count range")),
                    ), width="100%",
                ),
            ),
            _section(
                "7", "PWM can control LEDs and motor drivers",
                rx.text("PWM is often used for LED brightness and motor power commands, but a microcontroller pin normally supplies only a logic-level control signal. Power loads require suitable transistor, MOSFET or driver circuitry."),
                rx.callout(
                    "Do not connect motors, high-current LEDs or other power loads directly to a GPIO pin. Respect current, voltage, flyback and thermal requirements.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "8", "Hardware PWM reduces timing jitter",
                rx.text("Software-generated pulses can shift when interrupts or other tasks delay execution. A hardware timer continues counting independently, producing edges with much more deterministic timing."),
                rx.code_block(
                    "software toggling: CPU → delay → GPIO → delay → GPIO\n"
                    "hardware PWM:      timer peripheral ─────────→ output pin\n"
                    "                    CPU configures once",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Input capture measures external timing",
                rx.text("Timer peripherals can also timestamp an external edge by copying the current counter value into a capture register. Consecutive captures can measure pulse width, frequency, period or event spacing."),
                rx.code_block(
                    "external edge ───────┐       ┌───────\n"
                    "                     ↓       ↓\n"
                    "timer count       capture A capture B\n"
                    "period counts = capture B - capture A",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "Timers can trigger other peripherals",
                rx.text("A timer event does not always need CPU intervention. Many microcontrollers can route timer triggers directly to ADCs, DACs, DMA engines or other peripherals, producing accurately timed acquisition and output pipelines."),
                rx.code_block(
                    "timer compare → ADC sample → DMA buffer\n"
                    "timer update  → DAC value → analog waveform\n"
                    "timer PWM     → output pin → driver/load",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Trace a PWM configuration",
                rx.code_block(
                    "1. choose required PWM frequency\n"
                    "2. identify peripheral timer clock\n"
                    "3. choose prescaler and period/top count\n"
                    "4. choose duty/compare count\n"
                    "5. configure output polarity\n"
                    "6. route timer channel to the required pin\n"
                    "7. enable timer/PWM output\n"
                    "8. update duty safely while running\n"
                    "9. verify frequency and duty with measurement equipment",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text("You can now explain timer counting, prescaling, compare events, period and frequency, PWM duty cycle, resolution trade-offs, hardware waveform generation, input capture and peripheral triggering."),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 04 COMPLETE", color_scheme="green"),
                    rx.heading("You can now generate and measure precisely timed embedded signals.", size="5"),
                    rx.text("Next: learn embedded interrupts, priorities, latency and interrupt-service routines.", color="#475569"),
                    rx.link(
                        rx.button("Next · Interrupts, Priorities & ISR Design", color_scheme="teal"),
                        href="/academy/unit-11/interrupts-priorities-isr-design",
                        text_decoration="none",
                    ),
                    spacing="3", align="start",
                ), width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )


def interrupts_priorities_isr_design_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 05", color_scheme="teal", width="100%"),
            rx.heading("Interrupts, Priorities & ISR Design", size="8"),
            rx.text("Embedded systems must respond to asynchronous events without wasting CPU time polling every device. Interrupts provide that event-driven path, but reliable real-time behaviour depends on priorities, bounded latency and carefully designed interrupt service routines.", size="4", color="#475569", line_height="1.6"),
            _section("1","An interrupt redirects execution to an event handler",
                rx.text("A peripheral or external source raises an interrupt request. If the request is enabled and accepted, the processor preserves enough execution context, identifies the handler and begins the interrupt service routine (ISR)."),
                rx.code_block("main code → interrupt request → save/establish context → ISR → restore context → resume", language="textile", width="100%"),
                _practice("What routine runs when the processor accepts an interrupt?", EmbeddedSystemsState.isr_answer, EmbeddedSystemsState.set_isr_answer, EmbeddedSystemsState.check_isr, EmbeddedSystemsState.isr_feedback, "handler name")),
            _section("2","Interrupt sources can be internal or external",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Source"),rx.table.column_header_cell("Example event"))),rx.table.body(
                    rx.table.row(rx.table.cell("Timer"),rx.table.cell("Compare match or overflow")),
                    rx.table.row(rx.table.cell("GPIO"),rx.table.cell("External edge or level")),
                    rx.table.row(rx.table.cell("UART/SPI/I²C"),rx.table.cell("Receive, transmit or error condition")),
                    rx.table.row(rx.table.cell("ADC"),rx.table.cell("Conversion complete")),
                    rx.table.row(rx.table.cell("DMA"),rx.table.cell("Transfer complete/error")),
                    rx.table.row(rx.table.cell("System"),rx.table.cell("Fault, watchdog or software-generated event"))),width="100%")),
            _section("3","The interrupt controller manages pending work",
                rx.text("An interrupt controller collects requests, applies enable/mask settings and priority rules, then presents an eligible interrupt to the CPU."),
                rx.code_block("devices → pending bits → mask/enable → priority selection → CPU\n                         ↑\n                    software policy",language="textile",width="100%")),
            _section("4","Priority decides precedence",
                rx.text("When several interrupts are pending, priority determines which eligible source is serviced first. On systems that support nested interrupts, a sufficiently high-priority request may pre-empt a lower-priority ISR."),
                _practice("What interrupt property determines precedence when multiple interrupt sources compete for CPU service?", EmbeddedSystemsState.priority_answer, EmbeddedSystemsState.set_priority_answer, EmbeddedSystemsState.check_priority, EmbeddedSystemsState.priority_feedback, "precedence property"),
                rx.callout("Priority numbering is architecture-specific: on some controllers a smaller numeric value means higher priority. Check the device documentation.",icon="info",color_scheme="blue")),
            _section("5","Interrupt latency is a real-time quantity",
                rx.text("Interrupt latency is the elapsed time from an interrupt becoming serviceable until the corresponding handler begins. Current instruction completion, masking, higher-priority work and context handling can all contribute."),
                rx.code_block("event/request ────────┬──────── ISR begins\n                      └ latency ─┘",language="textile",width="100%"),
                _practice("What term describes the delay between an interrupt request and the start of its handler?", EmbeddedSystemsState.latency_answer, EmbeddedSystemsState.set_latency_answer, EmbeddedSystemsState.check_latency, EmbeddedSystemsState.latency_feedback, "response delay")),
            _section("6","ISR execution time also affects responsiveness",
                rx.text("Latency gets the CPU into the ISR; execution time determines how long that ISR occupies the processor. Long handlers delay lower-priority work and may increase worst-case response time."),
                rx.code_block("response time ≈ interrupt latency + required ISR execution\n\nshort bounded ISR → predictable system\nlong/blocking ISR → delayed events and timing risk",language="textile",width="100%")),
            _section("7","Keep interrupt handlers bounded and non-blocking",
                rx.text("A good ISR normally acknowledges the hardware event, captures minimal time-critical data, updates small shared state and defers expensive processing to normal execution context."),
                rx.code_block("ISR:\n  acknowledge/clear source\n  capture essential data\n  signal deferred work\n  return\n\nmain/task:\n  perform larger processing",language="textile",width="100%"),
                rx.callout("Avoid indefinite loops, long delays and operations that can block waiting for another event inside an ISR.",icon="triangle-alert",color_scheme="orange")),
            _section("8","Shared data creates concurrency hazards",
                rx.text("An ISR can interrupt ordinary code while both access the same data. Atomic operations, short critical sections, queues or architecture-appropriate synchronization protect shared state."),
                rx.code_block("main context ── reads/updates shared state\n                    ↑\n                 possible pre-emption\n                    ↓\nISR context  ── reads/updates shared state",language="textile",width="100%"),
                rx.text("The exact synchronization method depends on the processor, compiler, operating environment and data being protected.")),
            _section("9","Interrupt flags must be handled correctly",
                rx.text("Many peripherals retain a status or pending flag until software acknowledges it using the device-defined mechanism. If the source is not cleared correctly, the CPU may immediately enter the ISR again."),
                rx.code_block("event → status flag set → IRQ → ISR\n                              │\n                              └→ acknowledge/clear according to peripheral rules",language="textile",width="100%")),
            _section("10","Critical sections trade protection for latency",
                rx.text("Temporarily masking interrupts can protect a very small operation, but excessive masking increases latency. Real-time design therefore keeps critical sections as short as practical."),
                rx.code_block("disable/mask relevant IRQs\n  tiny critical update\nrestore previous IRQ state",language="textile",width="100%")),
            _section("11","Trace a UART receive interrupt",
                rx.code_block("1. UART receives a byte and sets RX-ready status\n2. interrupt controller marks UART request pending\n3. CPU completes/pauses current work according to architecture\n4. CPU vectors to UART ISR\n5. ISR reads received byte/status\n6. ISR stores byte in a software buffer\n7. ISR acknowledges required interrupt condition\n8. ISR signals that data is available\n9. ISR returns\n10. normal code parses/processes buffered data",language="textile",width="100%")),
            _section("12","Lesson checkpoint",
                rx.text("You can now explain interrupt entry and return, identify common interrupt sources, reason about pending/enabled states and priority, define interrupt latency, design short bounded ISRs, and recognize shared-data and interrupt-flag hazards.")),
            rx.card(rx.vstack(
                rx.badge("LESSON 05 COMPLETE",color_scheme="green"),
                rx.heading("Your embedded system can now respond predictably to asynchronous events.",size="5"),
                rx.text("Next: learn real-time scheduling, tasks and deterministic timing.",color="#475569"),
                rx.link(
                    rx.button("Next · Real-Time Scheduling, Tasks & Determinism", color_scheme="teal"),
                    href="/academy/unit-11/real-time-scheduling-tasks-determinism",
                    text_decoration="none",
                ),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def real_time_scheduling_tasks_determinism_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 06", color_scheme="teal", width="100%"),
            rx.heading("Real-Time Scheduling, Tasks & Determinism", size="8"),
            rx.text("Real-time computing is about producing a correct result within a required time bound. An RTOS helps structure concurrent embedded work into tasks, but deterministic behaviour still depends on scheduling policy, priorities, execution-time bounds and disciplined synchronization.", size="4", color="#475569", line_height="1.6"),
            _section("1","Real-time correctness includes timing",
                rx.text("A general-purpose system may be judged mainly by throughput or average response. A real-time system also has timing requirements: a result delivered too late may be incorrect for the application."),
                rx.code_block("functional correctness + timing correctness = real-time correctness",language="textile",width="100%"),
                _practice("What term describes the required completion time bound for a real-time activity?",EmbeddedSystemsState.deadline_answer,EmbeddedSystemsState.set_deadline_answer,EmbeddedSystemsState.check_deadline,EmbeddedSystemsState.deadline_feedback,"time bound")),
            _section("2","Hard and soft real-time requirements differ",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Class"),rx.table.column_header_cell("Meaning"))),rx.table.body(
                    rx.table.row(rx.table.cell("Hard real-time"),rx.table.cell("Missing a required deadline is unacceptable for the specified system requirement")),
                    rx.table.row(rx.table.cell("Firm real-time"),rx.table.cell("A late result has little or no value, though occasional misses may be tolerated by the application")),
                    rx.table.row(rx.table.cell("Soft real-time"),rx.table.cell("Late results reduce quality but may still be useful"))),width="100%")),
            _section("3","An RTOS organizes concurrent embedded work",
                rx.text("A real-time operating system commonly provides task scheduling, timing services, queues, semaphores, mutexes and other primitives designed for embedded concurrency."),
                rx.code_block("application tasks\n      ↓\nRTOS scheduler + timing + synchronization\n      ↓\nCPU + interrupts + peripherals",language="textile",width="100%"),
                _practice("What does RTOS stand for?",EmbeddedSystemsState.rtos_answer,EmbeddedSystemsState.set_rtos_answer,EmbeddedSystemsState.check_rtos,EmbeddedSystemsState.rtos_feedback,"operating system")),
            _section("4","Tasks move between execution states",
                rx.text("A task may be ready to run, currently running, or blocked while waiting for time, data or a synchronization event. The scheduler selects among eligible ready tasks."),
                rx.code_block("             event/data/time\nBLOCKED ─────────────────────→ READY\n                                 │\n                                 │ scheduler dispatch\n                                 ↓\n                              RUNNING\n                                 │\n                     wait/yield/pre-emption",language="textile",width="100%")),
            _section("5","Pre-emptive scheduling improves urgent response",
                rx.text("In a priority-based pre-emptive scheduler, a newly ready higher-priority task can interrupt the execution of a lower-priority task. This improves responsiveness but increases concurrency and shared-state complexity."),
                _practice("What scheduling mechanism allows a running task to be suspended so another eligible task can execute?",EmbeddedSystemsState.preemption_answer,EmbeddedSystemsState.set_preemption_answer,EmbeddedSystemsState.check_preemption,EmbeddedSystemsState.preemption_feedback,"scheduler mechanism")),
            _section("6","Periodic tasks have timing parameters",
                rx.text("A periodic real-time task can be described by quantities such as period, relative deadline and worst-case execution time (WCET). These parameters help engineers reason about whether all required work can finish on time."),
                rx.code_block("C = worst-case execution time\nT = period\nD = relative deadline\n\njob release ── C units of CPU work ── must complete by deadline",language="textile",width="100%")),
            _section("7","CPU utilization alone is not the whole proof",
                rx.text("If tasks demand more processor time than exists, deadlines cannot all be met. But utilization below 100% does not by itself prove every deadline under every scheduling policy; schedulability analysis depends on task model and scheduler."),
                rx.callout("Use the schedulability analysis appropriate to the actual RTOS policy, task periods/deadlines, blocking times and platform overheads.",icon="info",color_scheme="blue")),
            _section("8","Blocking and priority inversion threaten timing",
                rx.text("A high-priority task can be forced to wait for a resource held by a lower-priority task. If an intermediate-priority task then prevents the lower-priority owner from running, priority inversion can extend the blocking interval."),
                rx.code_block("HIGH: waits for mutex ─────────────┐\nLOW:  owns mutex, needs CPU to release it\nMID:  can pre-empt LOW → inversion grows",language="textile",width="100%"),
                rx.text("RTOS mechanisms such as priority inheritance can bound or reduce this effect when used correctly.")),
            _section("9","Queues separate producers and consumers",
                rx.text("Message queues let one context produce data while another consumes it. They are often safer and easier to reason about than uncontrolled shared global state."),
                rx.code_block("ISR / producer task → queue → processing task\n                       │\n                 bounded buffer",language="textile",width="100%")),
            _section("10","Determinism means bounded, explainable timing",
                rx.text("Deterministic software avoids unbounded waits and uncontrolled execution paths in time-critical code. Engineers care about worst-case behaviour, not only average speed."),
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Risk"),rx.table.column_header_cell("Real-time response"))),rx.table.body(
                    rx.table.row(rx.table.cell("Unbounded loop"),rx.table.cell("Bound iterations or move outside critical path")),
                    rx.table.row(rx.table.cell("Blocking I/O"),rx.table.cell("Use asynchronous/bounded mechanisms")),
                    rx.table.row(rx.table.cell("Long critical section"),rx.table.cell("Shorten protected region")),
                    rx.table.row(rx.table.cell("Dynamic contention"),rx.table.cell("Analyze and bound resource blocking"))),width="100%")),
            _section("11","Trace a periodic control task",
                rx.code_block("1. hardware timer establishes control period\n2. RTOS releases/wakes control task\n3. scheduler dispatches it at configured priority\n4. task reads latest sensor data\n5. task computes control output\n6. task updates actuator command\n7. task completes before deadline\n8. task blocks until next release\n9. lower-priority background work uses remaining CPU time\n10. timing measurements verify worst-case margin",language="textile",width="100%")),
            _section("12","Lesson checkpoint",
                rx.text("You can now distinguish real-time from merely fast execution, explain hard/firm/soft timing requirements, describe RTOS task states and pre-emption, reason about period/deadline/WCET, recognize priority inversion, and design bounded task communication.")),
            rx.card(rx.vstack(
                rx.badge("LESSON 06 COMPLETE",color_scheme="green"),
                rx.heading("You can now structure embedded work around explicit timing guarantees.",size="5"),
                rx.text("Next: learn embedded communication interfaces and peripheral buses.",color="#475569"),
                rx.link(
                    rx.button("Next · UART, SPI, I²C & Peripheral Communication", color_scheme="teal"),
                    href="/academy/unit-11/uart-spi-i2c-peripheral-communication",
                    text_decoration="none",
                ),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def uart_spi_i2c_peripheral_communication_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 07", color_scheme="teal", width="100%"),
            rx.heading("UART, SPI, I²C & Peripheral Communication", size="8"),
            rx.text("Microcontrollers rarely work alone. Serial peripheral interfaces connect processors to sensors, displays, converters, radios, memories and other controllers. Choosing and configuring a bus requires understanding timing, wiring, addressing, framing and electrical constraints.", size="4", color="#475569", line_height="1.6"),
            _section("1","Serial links move information over a small number of wires",
                rx.text("Instead of dedicating one wire to every data bit, serial interfaces transmit bits over time. This reduces pin count and wiring but requires both endpoints to agree on the protocol."),
                rx.code_block("parallel: D7 D6 D5 D4 D3 D2 D1 D0 → many data wires\nserial:   data bits → one/few data wires over time",language="textile",width="100%")),
            _section("2","UART is asynchronous serial communication",
                rx.text("A UART transmitter and receiver agree on parameters such as baud rate, data bits, parity and stop bits. Because there is no shared clock line, each side uses its own clock and relies on framing to recover byte timing."),
                rx.code_block("idle  start  D0 D1 D2 D3 D4 D5 D6 D7  stop\n  1      0    ←──── data bits ────→      1",language="textile",width="100%"),
                _practice("Which common serial peripheral communicates asynchronously without a shared clock line?",EmbeddedSystemsState.uart_answer,EmbeddedSystemsState.set_uart_answer,EmbeddedSystemsState.check_uart,EmbeddedSystemsState.uart_feedback,"serial interface")),
            _section("3","UART is naturally point-to-point at the logic level",
                rx.text("A basic logic-level UART connection normally uses TX from one device to RX of the other, plus a common reference. Physical-layer standards and transceivers can extend UART-style data over longer or more robust links."),
                rx.callout("Never assume connector voltage levels are compatible. Logic-level UART, RS-232 and RS-485 use different electrical signalling arrangements.",icon="triangle-alert",color_scheme="orange")),
            _section("4","SPI is synchronous and typically full-duplex",
                rx.text("SPI commonly uses a controller-generated serial clock (SCLK), a controller-to-peripheral data line, a peripheral-to-controller data line and one chip-select signal per selected peripheral."),
                rx.code_block("controller SCLK ─────────→ peripheral(s)\ncontroller MOSI ─────────→ peripheral\ncontroller MISO ←───────── peripheral\ncontroller CS   ─────────→ selected peripheral",language="textile",width="100%"),
                _practice("Which synchronous serial interface commonly uses SCLK plus separate data paths?",EmbeddedSystemsState.spi_answer,EmbeddedSystemsState.set_spi_answer,EmbeddedSystemsState.check_spi,EmbeddedSystemsState.spi_feedback,"synchronous interface")),
            _section("5","SPI mode defines clock polarity and phase",
                rx.text("SPI devices must agree on when the clock idles and on which clock edge data changes or is sampled. These properties are commonly described by CPOL and CPHA."),
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Parameter"),rx.table.column_header_cell("Purpose"))),rx.table.body(
                    rx.table.row(rx.table.cell("CPOL"),rx.table.cell("Clock idle polarity")),
                    rx.table.row(rx.table.cell("CPHA"),rx.table.cell("Clock phase / sampling relationship")),
                    rx.table.row(rx.table.cell("Bit order"),rx.table.cell("Whether MSB or LSB is transferred first")),
                    rx.table.row(rx.table.cell("Clock rate"),rx.table.cell("Transfer timing speed"))),width="100%")),
            _section("6","I²C shares two open-drain-style signal lines",
                rx.text("I²C uses serial data (SDA) and serial clock (SCL). Devices generally pull these lines low and external pull-up resistors return them high, allowing multiple devices to share the bus."),
                rx.code_block("VDD      VDD\n |        |\nRp       Rp\n |        |\nSDA ─────┼──── devices\nSCL ─────┼──── devices",language="textile",width="100%"),
                _practice("Which two-wire addressed bus commonly uses SDA and SCL?",EmbeddedSystemsState.i2c_answer,EmbeddedSystemsState.set_i2c_answer,EmbeddedSystemsState.check_i2c,EmbeddedSystemsState.i2c_feedback,"two-wire bus")),
            _section("7","I²C transfers include addressing and acknowledgement",
                rx.text("A controller starts a transaction, sends an address and transfer direction, then exchanges data bytes. Receivers acknowledge bytes according to the protocol, and the controller eventually issues a stop or repeated-start sequence."),
                rx.code_block("START → address + R/W → ACK → data → ACK → ... → STOP",language="textile",width="100%")),
            _section("8","Pull-ups and bus capacitance shape I²C timing",
                rx.text("Because the bus rises through pull-up resistance and capacitance, resistor choice, wiring length, device capacitance and target bus speed affect rise time."),
                rx.callout("Use the device and I²C timing specifications to choose pull-ups. A value that works on a short low-capacitance prototype may not suit a larger bus.",icon="info",color_scheme="blue")),
            _section("9","Choose an interface from system requirements",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Interface"),rx.table.column_header_cell("Useful characteristics"))),rx.table.body(
                    rx.table.row(rx.table.cell("UART"),rx.table.cell("Simple asynchronous point-to-point byte stream")),
                    rx.table.row(rx.table.cell("SPI"),rx.table.cell("Clocked, often high-throughput, simple framing, extra select wiring")),
                    rx.table.row(rx.table.cell("I²C"),rx.table.cell("Two shared signal wires with addressed peripherals"))),width="100%"),
                rx.text("The best choice also depends on device support, distance, throughput, latency, pin budget, electrical environment and software complexity.")),
            _section("10","Interrupts and DMA reduce communication overhead",
                rx.text("Polling is simple for occasional transfers. Interrupt-driven drivers let firmware work while bytes arrive or depart. DMA can move blocks between a peripheral and memory with little CPU involvement."),
                rx.code_block("polling: CPU ↔ peripheral each step\ninterrupt: peripheral → IRQ → service buffer\nDMA: peripheral ↔ memory buffer; CPU handles blocks/events",language="textile",width="100%")),
            _section("11","Trace an I²C sensor register read",
                rx.code_block("1. configure SDA/SCL pins and I²C timing\n2. START\n3. send sensor write address → ACK\n4. send target register address → ACK\n5. repeated START\n6. send sensor read address → ACK\n7. receive data byte(s)\n8. ACK intermediate bytes / NACK final byte as required\n9. STOP\n10. convert received register data into engineering units",language="textile",width="100%")),
            _section("12","Lesson checkpoint",
                rx.text("You can now distinguish asynchronous UART from synchronous SPI, explain SPI clock modes, describe I²C addressing and pull-ups, compare interface trade-offs, and choose polling, interrupts or DMA for peripheral transfers.")),
            rx.card(rx.vstack(
                rx.badge("LESSON 07 COMPLETE",color_scheme="green"),
                rx.heading("You can now connect embedded processors to common digital peripherals.",size="5"),
                rx.text("Next: integrate the complete embedded system through firmware architecture, reliability and debugging.",color="#475569"),
                rx.link(
                    rx.button("Next · Embedded System Integration, Reliability & Debugging", color_scheme="teal"),
                    href="/academy/unit-11/embedded-system-integration-reliability-debugging",
                    text_decoration="none",
                ),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def embedded_system_integration_reliability_debugging_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 11 · LESSON 08", color_scheme="teal", width="100%"),
            rx.heading("Embedded System Integration, Reliability & Debugging", size="8"),
            rx.text(
                "A working embedded product is more than a collection of individually correct peripherals. Integration must make hardware, firmware, timing, power, communication and fault handling cooperate reliably under real operating conditions.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Integration connects the complete signal-and-software path",
                rx.text(
                    "A complete embedded system connects physical inputs to sensing hardware, software decisions and physical outputs. Every boundary introduces assumptions about timing, voltage, data representation and failure behaviour."
                ),
                rx.code_block(
                    "sensor → conditioning/ADC → firmware/RTOS → control logic → GPIO/PWM/driver → actuator\n"
                    "                    ↕\n"
                    "             UART / SPI / I²C / storage / diagnostics",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "2", "Startup sequencing establishes a known safe state",
                rx.text(
                    "On reset, firmware should bring clocks, memory, GPIO, peripherals and external hardware into a deliberate state. Outputs that control actuators should not briefly enter unsafe values while initialization is incomplete."
                ),
                rx.code_block(
                    "reset\n"
                    " ↓\n"
                    "safe clocks/power assumptions\n"
                    " ↓\n"
                    "initialize memory + variables\n"
                    " ↓\n"
                    "configure safe GPIO defaults\n"
                    " ↓\n"
                    "initialize peripherals\n"
                    " ↓\n"
                    "self-check / communications\n"
                    " ↓\n"
                    "enable active control",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Watchdogs detect missing software progress",
                rx.text(
                    "A watchdog timer must be serviced within a defined interval. Correct software refreshes it only after required work has progressed. If execution hangs or misses the expected health path, the watchdog can reset or escalate the fault."
                ),
                _practice(
                    "What hardware timer can reset or recover a system when software stops making expected progress?",
                    EmbeddedSystemsState.watchdog_answer,
                    EmbeddedSystemsState.set_watchdog_answer,
                    EmbeddedSystemsState.check_watchdog,
                    EmbeddedSystemsState.watchdog_feedback,
                    "recovery timer",
                ),
                rx.callout(
                    "Refreshing the watchdog unconditionally from a timer interrupt can hide a dead main task. The refresh point should represent real system health.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "4", "Brownout detection protects low-voltage operation",
                rx.text(
                    "Processors and memories can behave unpredictably below their guaranteed supply range. Brownout detection monitors supply voltage and can hold the system in reset or trigger recovery before unsafe execution occurs."
                ),
                _practice(
                    "What protection mechanism detects supply voltage dropping below a safe operating level?",
                    EmbeddedSystemsState.brownout_answer,
                    EmbeddedSystemsState.set_brownout_answer,
                    EmbeddedSystemsState.check_brownout,
                    EmbeddedSystemsState.brownout_feedback,
                    "supply protection",
                ),
            ),
            _section(
                "5", "Fault containment limits propagation",
                rx.text(
                    "A robust design assumes that components can fail. Fault containment isolates bad data, stuck communications, invalid sensor values or failed subsystems so one local problem does not immediately corrupt the complete product."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Fault"),
                        rx.table.column_header_cell("Containment example"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Sensor out of range"), rx.table.cell("Reject/flag reading; enter fallback mode")),
                        rx.table.row(rx.table.cell("Communication timeout"), rx.table.cell("Retry, isolate device, use last-safe value")),
                        rx.table.row(rx.table.cell("Actuator feedback mismatch"), rx.table.cell("Disable command and raise fault")),
                        rx.table.row(rx.table.cell("Task failure"), rx.table.cell("Watchdog or supervisory recovery")),
                    ), width="100%",
                ),
                _practice(
                    "What reliability principle keeps one failing subsystem from corrupting the rest of the system?",
                    EmbeddedSystemsState.fault_answer,
                    EmbeddedSystemsState.set_fault_answer,
                    EmbeddedSystemsState.check_fault,
                    EmbeddedSystemsState.fault_feedback,
                    "reliability principle",
                ),
            ),
            _section(
                "6", "Timeouts convert indefinite waiting into bounded behaviour",
                rx.text(
                    "Real systems cannot assume every peripheral responds forever. A timeout gives communication, synchronization and state-machine waits an upper bound so software can detect failure and choose a recovery path."
                ),
                rx.code_block(
                    "request device\n"
                    "start timeout\n"
                    "wait for completion\n"
                    " ├─ success before timeout → continue\n"
                    " └─ timeout → fault/retry/fallback",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Assertions and diagnostics expose impossible states",
                rx.text(
                    "Development builds can use assertions to catch violated assumptions early. Production firmware can retain lightweight error counters, reset causes, fault codes and event logs for field diagnosis."
                ),
                rx.code_block(
                    "if impossible_condition:\n"
                    "    record fault context\n"
                    "    enter defined safe/recovery path\n\n"
                    "diagnostics: reset cause + error counter + timestamp + state",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "Debugging starts by observing the right layer",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Tool"),
                        rx.table.column_header_cell("Best used for"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Debugger/JTAG/SWD"), rx.table.cell("CPU state, memory, breakpoints, registers")),
                        rx.table.row(rx.table.cell("Logic analyzer"), rx.table.cell("Digital timing and UART/SPI/I²C transactions")),
                        rx.table.row(rx.table.cell("Oscilloscope"), rx.table.cell("Voltage shape, noise, rise time, analog/PWM behaviour")),
                        rx.table.row(rx.table.cell("Serial logs"), rx.table.cell("Runtime events, state transitions, fault messages")),
                        rx.table.row(rx.table.cell("Trace/profiling"), rx.table.cell("Timing, task execution and latency")),
                    ), width="100%",
                ),
                rx.callout(
                    "A debugger can change timing. Time-sensitive faults should also be investigated with non-intrusive traces, timestamps or external measurement tools.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "9", "Reproduce faults before changing code",
                rx.text(
                    "Reliable debugging starts with a repeatable failure condition. Record hardware revision, firmware version, input conditions, timing, power state and communication sequence before modifying the system."
                ),
                rx.code_block(
                    "observe → reproduce → isolate → measure → form hypothesis → test one change → verify",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "Integration testing crosses subsystem boundaries",
                rx.text(
                    "Unit tests check small pieces; integration tests exercise real interactions between drivers, tasks, peripherals and hardware. Boundary conditions such as startup, timeout, overflow, communication loss and power interruption deserve explicit tests."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Test layer"),
                        rx.table.column_header_cell("Question"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Unit"), rx.table.cell("Does this function/module behave correctly?")),
                        rx.table.row(rx.table.cell("Driver"), rx.table.cell("Does the peripheral interface work under normal/error cases?")),
                        rx.table.row(rx.table.cell("Integration"), rx.table.cell("Do multiple subsystems cooperate correctly?")),
                        rx.table.row(rx.table.cell("System"), rx.table.cell("Does the complete product meet functional and timing requirements?")),
                    ), width="100%",
                ),
            ),
            _section(
                "11", "Trace an integrated fault-and-recovery scenario",
                rx.code_block(
                    "1. periodic control task reads sensor via I²C\n"
                    "2. sensor stops responding\n"
                    "3. driver timeout expires instead of blocking forever\n"
                    "4. software increments communication-fault counter\n"
                    "5. control logic substitutes a defined safe fallback value\n"
                    "6. actuator command moves to safe operating mode\n"
                    "7. diagnostic event is recorded\n"
                    "8. retry policy attempts sensor recovery\n"
                    "9. repeated failure escalates to subsystem reset or watchdog recovery\n"
                    "10. startup self-check verifies safe re-entry",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Path 11 integration checkpoint",
                rx.text(
                    "You can now connect GPIO, ADC, PWM, interrupts, RTOS scheduling and serial buses into a complete embedded architecture, then add watchdogs, brownout protection, timeouts, diagnostics, fault containment and structured debugging."
                ),
                rx.code_block(
                    "physical world\n"
                    "   ↓\n"
                    "GPIO / ADC / communication\n"
                    "   ↓\n"
                    "interrupts + RTOS tasks + timing\n"
                    "   ↓\n"
                    "control logic\n"
                    "   ↓\n"
                    "PWM / GPIO / peripheral outputs\n"
                    "   ↓\n"
                    "actuators\n\n"
                    "surrounding all layers: watchdogs • timeouts • diagnostics • safe states • tests",
                    language="textile", width="100%",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("PATH 11 COMPLETE", color_scheme="green"),
                    rx.heading("Embedded Systems & Real-Time Computing is complete.", size="5"),
                    rx.text(
                        "You can now design, interface, schedule, communicate, diagnose and harden a complete embedded system.",
                        color="#475569",
                    ),
                    spacing="3", align="start",
                ),
                width="100%",
            ),
            spacing="6", align="stretch", max_width="1050px", width="100%",
            margin="0 auto", padding="32px 20px 64px",
        ),
        min_height="100vh", background="#f8fafc",
    )
