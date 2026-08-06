"""BoolNexa Academy Path 10 — Computer Organisation & System Integration."""
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


class SystemIntegrationState(rx.State):
    interface_answer: str = ""
    interface_feedback: str = ""
    address_answer: str = ""
    address_feedback: str = ""
    handshake_answer: str = ""
    handshake_feedback: str = ""
    mappedio_answer: str = ""
    mappedio_feedback: str = ""
    status_answer: str = ""
    status_feedback: str = ""
    polling_answer: str = ""
    polling_feedback: str = ""
    interrupt_answer: str = ""
    interrupt_feedback: str = ""
    vector_answer: str = ""
    vector_feedback: str = ""
    context_answer: str = ""
    context_feedback: str = ""
    bus_answer: str = ""
    bus_feedback: str = ""
    arbitration_answer: str = ""
    arbitration_feedback: str = ""
    dma_answer: str = ""
    dma_feedback: str = ""
    burst_answer: str = ""
    burst_feedback: str = ""
    coherence_answer: str = ""
    coherence_feedback: str = ""
    timer_answer: str = ""
    timer_feedback: str = ""
    prescaler_answer: str = ""
    prescaler_feedback: str = ""
    watchdog_answer: str = ""
    watchdog_feedback: str = ""
    serial_answer: str = ""
    serial_feedback: str = ""
    uart_answer: str = ""
    uart_feedback: str = ""
    spi_answer: str = ""
    spi_feedback: str = ""
    block_answer: str = ""
    block_feedback: str = ""
    sector_answer: str = ""
    sector_feedback: str = ""
    queue_answer: str = ""
    queue_feedback: str = ""

    def set_interface_answer(self, value: str) -> None:
        self.interface_answer = value

    def set_address_answer(self, value: str) -> None:
        self.address_answer = value

    def set_handshake_answer(self, value: str) -> None:
        self.handshake_answer = value

    def set_mappedio_answer(self, value: str) -> None:
        self.mappedio_answer = value

    def set_status_answer(self, value: str) -> None:
        self.status_answer = value

    def set_polling_answer(self, value: str) -> None:
        self.polling_answer = value

    def set_interrupt_answer(self, value: str) -> None:
        self.interrupt_answer = value

    def set_vector_answer(self, value: str) -> None:
        self.vector_answer = value

    def set_context_answer(self, value: str) -> None:
        self.context_answer = value

    def set_bus_answer(self, value: str) -> None:
        self.bus_answer = value

    def set_arbitration_answer(self, value: str) -> None:
        self.arbitration_answer = value

    def set_dma_answer(self, value: str) -> None:
        self.dma_answer = value

    def set_burst_answer(self, value: str) -> None:
        self.burst_answer = value

    def set_coherence_answer(self, value: str) -> None:
        self.coherence_answer = value

    def set_timer_answer(self, value: str) -> None:
        self.timer_answer = value

    def set_prescaler_answer(self, value: str) -> None:
        self.prescaler_answer = value

    def set_watchdog_answer(self, value: str) -> None:
        self.watchdog_answer = value

    def set_serial_answer(self, value: str) -> None:
        self.serial_answer = value

    def set_uart_answer(self, value: str) -> None:
        self.uart_answer = value

    def set_spi_answer(self, value: str) -> None:
        self.spi_answer = value

    def set_block_answer(self, value: str) -> None:
        self.block_answer = value

    def set_sector_answer(self, value: str) -> None:
        self.sector_answer = value

    def set_queue_answer(self, value: str) -> None:
        self.queue_answer = value

    def check_interface(self) -> None:
        value = self.interface_answer.strip().lower().replace(" ", "").replace("-", "")
        self.interface_feedback = (
            "Correct. An interface connects blocks with agreed data, address and control behaviour."
            if value in {"interface", "iointerface", "businterface"}
            else "What hardware boundary connects two system blocks using defined signals and rules?"
        )

    def check_address(self) -> None:
        value = self.address_answer.strip().lower().replace(" ", "").replace("-", "")
        self.address_feedback = (
            "Correct. Address decoding selects the one target whose assigned address range matches the CPU address."
            if value in {"addressdecoder", "addressdecoding", "decoder", "decode"}
            else "What logic determines which memory or peripheral responds to a CPU address?"
        )

    def check_handshake(self) -> None:
        value = self.handshake_answer.strip().lower().replace(" ", "").replace("-", "")
        self.handshake_feedback = (
            "Correct. Handshaking coordinates transfers when blocks cannot assume identical response timing."
            if value in {"handshake", "handshaking"}
            else "What technique uses request/ready or valid/acknowledge signals to coordinate a transfer?"
        )

    def check_mappedio(self) -> None:
        value = self.mappedio_answer.strip().lower().replace(" ", "").replace("-", "")
        self.mappedio_feedback = (
            "Correct. Memory-mapped I/O places peripheral registers in the processor's normal address space."
            if value in {"memorymappedio", "memorymapped", "mmio"}
            else "What I/O organisation lets normal load/store instructions access device registers by address?"
        )

    def check_status(self) -> None:
        value = self.status_answer.strip().lower().replace(" ", "").replace("-", "")
        self.status_feedback = (
            "Correct. A status register reports device state such as ready, busy, error or data-available."
            if value in {"statusregister", "status", "stateregister"}
            else "Which device register tells software whether a peripheral is ready, busy or has data available?"
        )

    def check_polling(self) -> None:
        value = self.polling_answer.strip().lower().replace(" ", "").replace("-", "")
        self.polling_feedback = (
            "Correct. Polling repeatedly reads device status until the required condition becomes true."
            if value in {"polling", "poll"}
            else "What software technique repeatedly checks a peripheral status register until the device is ready?"
        )

    def check_bus(self) -> None:
        value = self.bus_answer.strip().lower().replace(" ", "").replace("-", "")
        self.bus_feedback = (
            "Correct. A bus is a shared communication path used by system components."
            if value in {"bus", "systembus", "sharedbus"}
            else "What shared communication path carries information between system components?"
        )

    def check_arbitration(self) -> None:
        value = self.arbitration_answer.strip().lower().replace(" ", "").replace("-", "")
        self.arbitration_feedback = (
            "Correct. Arbitration selects which requesting master receives ownership of a shared bus."
            if value in {"arbitration", "busarbitration", "arbiter"}
            else "What process decides which requester may control a shared bus?"
        )

    def check_dma(self) -> None:
        value = self.dma_answer.strip().lower().replace(" ", "").replace("-", "")
        self.dma_feedback = (
            "Correct. DMA lets a controller move data between memory and a peripheral with much less CPU involvement per transfer."
            if value in {"dma", "directmemoryaccess"}
            else "What mechanism lets a controller transfer data directly between memory and a device without the CPU copying every item?"
        )

    def check_burst(self) -> None:
        value = self.burst_answer.strip().lower().replace(" ", "").replace("-", "")
        self.burst_feedback = (
            "Correct. A burst transfer moves several data items after one arbitration/setup phase."
            if value in {"burst", "bursttransfer", "blocktransfer"}
            else "What transfer style moves several consecutive data items after one setup/arbitration phase?"
        )

    def check_coherence(self) -> None:
        value = self.coherence_answer.strip().lower().replace(" ", "").replace("-", "")
        self.coherence_feedback = (
            "Correct. Cache coherence/maintenance is needed so CPU caches and DMA-visible memory do not disagree about the latest data."
            if value in {"coherence", "cachecoherence", "cachemaintenance", "cachecoherency"}
            else "What issue must be managed when DMA accesses memory that may also be cached by the CPU?"
        )

    def check_block(self) -> None:
        value = self.block_answer.strip().lower().replace(" ", "").replace("-", "")
        self.block_feedback = ("Correct. A block device transfers addressed chunks of persistent data." if value in {"blockdevice","blockstorage","blockio","block"} else "What storage abstraction reads and writes addressed chunks rather than individual characters?")

    def check_sector(self) -> None:
        value = self.sector_answer.strip().lower().replace(" ", "").replace("-", "")
        self.sector_feedback = ("Correct. A logical block/sector address identifies a particular block presented by the device." if value in {"sector","sectoraddress","logicalblock","logicalblockaddress","lba"} else "What address identifies a particular logical block on a storage device?")

    def check_queue(self) -> None:
        value = self.queue_answer.strip().lower().replace(" ", "").replace("-", "")
        self.queue_feedback = ("Correct. A request/command queue holds pending storage operations." if value in {"queue","requestqueue","commandqueue","ioqueue"} else "What structure holds multiple pending storage requests so they can be scheduled efficiently?")

    def check_serial(self) -> None:
        value = self.serial_answer.strip().lower().replace(" ", "").replace("-", "")
        self.serial_feedback = ("Correct. Serial communication transfers a word as an ordered sequence of bits over time." if value in {"serial","serialcommunication","serialinterface"} else "What communication style sends the bits of a word sequentially rather than on many parallel data lines?")

    def check_uart(self) -> None:
        value = self.uart_answer.strip().lower().replace(" ", "").replace("-", "")
        self.uart_feedback = ("Correct. A UART commonly frames asynchronous data with start and stop bits." if value in {"uart","universalasynchronousreceivertransmitter"} else "Which common asynchronous serial peripheral uses TX/RX and start/stop framing?")

    def check_spi(self) -> None:
        value = self.spi_answer.strip().lower().replace(" ", "").replace("-", "")
        self.spi_feedback = ("Correct. SPI uses an explicit serial clock and separate data paths for synchronous full-duplex transfers." if value in {"spi","serialperipheralinterface"} else "Which synchronous serial interface commonly uses SCLK, MOSI, MISO and chip-select?")

    def check_timer(self) -> None:
        value = self.timer_answer.strip().lower().replace(" ", "").replace("-", "")
        self.timer_feedback = (
            "Correct. A hardware timer/counter advances from a clock or event source and can signal when a programmed condition occurs."
            if value in {"timer", "counter", "hardwaretimer", "timercounter"}
            else "What hardware block counts clock ticks or external events to measure or schedule time?"
        )

    def check_prescaler(self) -> None:
        value = self.prescaler_answer.strip().lower().replace(" ", "").replace("-", "")
        self.prescaler_feedback = (
            "Correct. A prescaler divides the incoming clock so the counter advances more slowly."
            if value in {"prescaler", "clockdivider", "divider"}
            else "What timer component divides the source clock before it reaches the counter?"
        )

    def check_watchdog(self) -> None:
        value = self.watchdog_answer.strip().lower().replace(" ", "").replace("-", "")
        self.watchdog_feedback = (
            "Correct. A watchdog timer detects failure to make expected progress and can request recovery."
            if value in {"watchdog", "watchdogtimer", "wdt"}
            else "What timer is periodically serviced by healthy software and triggers recovery if servicing stops?"
        )

    def check_interrupt(self) -> None:
        value = self.interrupt_answer.strip().lower().replace(" ", "").replace("-", "")
        self.interrupt_feedback = (
            "Correct. An interrupt lets a device request CPU attention asynchronously instead of being polled continuously."
            if value in {"interrupt", "irq", "interruptrequest"}
            else "What mechanism lets a peripheral request CPU attention when service is needed?"
        )

    def check_vector(self) -> None:
        value = self.vector_answer.strip().lower().replace(" ", "").replace("-", "")
        self.vector_feedback = (
            "Correct. An interrupt vector identifies or leads the processor to the appropriate interrupt service routine."
            if value in {"interruptvector", "vector", "vectoraddress"}
            else "What value or table entry directs the CPU toward the correct interrupt service routine?"
        )

    def check_context(self) -> None:
        value = self.context_answer.strip().lower().replace(" ", "").replace("-", "")
        self.context_feedback = (
            "Correct. Saving context preserves the interrupted program state so execution can resume correctly."
            if value in {"context", "contextsave", "savecontext", "contextsaving"}
            else "What must be preserved before an ISR changes processor state needed by the interrupted program?"
        )


def _section(number: str, title: str, *children) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(rx.badge(number, color_scheme="teal"), rx.heading(title, size="5"), align="center"),
            *children,
            spacing="4", align="stretch",
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
            spacing="2", align="stretch",
        ),
        padding="14px", border="1px solid #5eead4", border_radius="12px",
        background="#f0fdfa", width="100%",
    )


def system_interconnect_foundations_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 01", color_scheme="teal", width="100%"),
            rx.heading("System Interconnect & CPU–Memory/I/O Foundations", size="8"),
            rx.text(
                "A processor becomes a useful computer only when it can exchange information reliably with memory and external devices. This lesson builds the system-level view: buses carry information, address decoding selects a target, and control timing makes every transfer unambiguous.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "From CPU datapath to complete computer system",
                rx.text("Path 09 focused inside the processor. Path 10 moves outward and connects the CPU to memory, timers, displays, sensors, storage and other peripherals through explicit interfaces."),
                rx.code_block(
                    "                 ┌──────── CPU ────────┐\n"
                    "                 │ address / data / ctl│\n"
                    "                 └─────────┬───────────┘\n"
                    "                           BUS\n"
                    "             ┌──────────────┼──────────────┐\n"
                    "          Memory          Timer          I/O device",
                    language="textile", width="100%",
                ),
                _practice(
                    "What hardware boundary connects two system blocks using defined signals and transfer rules?",
                    SystemIntegrationState.interface_answer,
                    SystemIntegrationState.set_interface_answer,
                    SystemIntegrationState.check_interface,
                    SystemIntegrationState.interface_feedback,
                    "hardware boundary",
                ),
            ),
            _section(
                "2", "Three kinds of information travel through an interconnect",
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Signal group"), rx.table.column_header_cell("Purpose"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Address"), rx.table.cell("Identifies the memory location or peripheral/register being accessed")),
                        rx.table.row(rx.table.cell("Data"), rx.table.cell("Carries the value being read or written")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("Defines direction, validity, enable, ready/wait and transfer timing")),
                    ), width="100%",
                ),
                rx.callout("A bus is not only a bundle of data wires. A usable transaction needs enough addressing and control information to tell every participant what the data means.", icon="info", color_scheme="blue"),
            ),
            _section(
                "3", "Address decoding selects exactly one target",
                rx.text("Every mapped component owns an address or range. Decoder logic examines high-order address bits and generates a chip-select or enable for the matching target. Non-selected devices must ignore the transaction."),
                rx.code_block(
                    "CPU address ──→ address decoder\n"
                    "                  ├─ 0x0000–0x7FFF → RAM select\n"
                    "                  ├─ 0x8000–0x80FF → timer select\n"
                    "                  └─ 0x8100–0x81FF → GPIO select",
                    language="textile", width="100%",
                ),
                _practice(
                    "What logic determines which memory or peripheral responds to a CPU address?",
                    SystemIntegrationState.address_answer,
                    SystemIntegrationState.set_address_answer,
                    SystemIntegrationState.check_address,
                    SystemIntegrationState.address_feedback,
                    "selection logic",
                ),
            ),
            _section(
                "4", "A read transaction has a direction and an owner",
                rx.code_block(
                    "1. CPU places target ADDRESS\n"
                    "2. CPU asserts READ / valid control\n"
                    "3. selected target obtains the requested value\n"
                    "4. target drives DATA back toward CPU\n"
                    "5. transfer completes; controls are released",
                    language="textile", width="100%",
                ),
                rx.text("Only the selected responder should drive a shared read-data path. This is the system-level version of the bus-contention rule learned for CPU register transfers."),
            ),
            _section(
                "5", "A write transaction reverses the data direction",
                rx.code_block(
                    "1. CPU places target ADDRESS\n"
                    "2. CPU places write DATA\n"
                    "3. CPU asserts WRITE / valid control\n"
                    "4. selected target captures the value\n"
                    "5. transfer completes",
                    language="textile", width="100%",
                ),
                rx.text("The address still selects the destination, but the processor is now the data source. Write-enable timing must prevent accidental modification of an unselected device."),
            ),
            _section(
                "6", "Memory-mapped I/O gives devices addresses",
                rx.text("In a memory-mapped system, peripheral registers occupy part of the processor's address space. Ordinary load and store operations can therefore communicate with device registers."),
                rx.table.root(
                    rx.table.header(rx.table.row(rx.table.column_header_cell("Example address"), rx.table.column_header_cell("Meaning"))),
                    rx.table.body(
                        rx.table.row(rx.table.cell("0x8000"), rx.table.cell("Timer control register")),
                        rx.table.row(rx.table.cell("0x8004"), rx.table.cell("Timer count register")),
                        rx.table.row(rx.table.cell("0x8100"), rx.table.cell("GPIO output register")),
                        rx.table.row(rx.table.cell("0x8104"), rx.table.cell("GPIO input register")),
                    ), width="100%",
                ),
                rx.callout("Addresses shown here are teaching examples, not a specification for a particular commercial processor.", icon="book-open", color_scheme="gray"),
            ),
            _section(
                "7", "Fast and slow components need timing coordination",
                rx.text("A CPU may issue a request faster than a peripheral can answer. A fixed timing assumption works only when the responder always meets that timing. Otherwise the interface needs a way to indicate completion."),
                rx.code_block(
                    "master:  request + address/data ──────────────┐\n"
                    "slave :                     ready/ack ──────┘\n"
                    "transfer completes only when the agreed condition is satisfied",
                    language="textile", width="100%",
                ),
                _practice(
                    "What technique uses request/ready or valid/acknowledge signals to coordinate a transfer?",
                    SystemIntegrationState.handshake_answer,
                    SystemIntegrationState.set_handshake_answer,
                    SystemIntegrationState.check_handshake,
                    SystemIntegrationState.handshake_feedback,
                    "coordination technique",
                ),
            ),
            _section(
                "8", "Interconnect correctness rules",
                rx.text("A robust transaction answers four questions: Who is selected? Who may drive the data? When is the value valid? When is the transfer complete? Address decoding, direction controls and timing rules answer these questions."),
                rx.hstack(
                    rx.badge("Select", color_scheme="orange"), rx.text("→ one intended target"),
                    rx.badge("Direction", color_scheme="blue"), rx.text("→ one legal data source"),
                    rx.badge("Timing", color_scheme="purple"), rx.text("→ sample only when valid"),
                    wrap="wrap", spacing="2",
                ),
            ),
            _section(
                "9", "Trace one complete peripheral write",
                rx.code_block(
                    "Instruction: STORE R2, [0x8100]\n"
                    "R2 = 0x00000005\n\n"
                    "CPU address = 0x8100  → decoder selects GPIO\n"
                    "CPU data    = 0x00000005\n"
                    "CPU control = WRITE\n"
                    "GPIO captures 0x00000005 when the transfer completes\n"
                    "Result: output register now contains 0x00000005",
                    language="textile", width="100%",
                ),
                rx.text("The CPU instruction, datapath, address decoder, bus and peripheral interface all participate in one system-level operation."),
            ),
            _section(
                "10", "Lesson checkpoint",
                rx.text("You can now explain how a CPU reaches memory and I/O through address, data and control signals; how decoding selects a target; and why transaction timing matters."),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 01 COMPLETE", color_scheme="green"),
                    rx.heading("The processor is now connected to the outside system.", size="5"),
                    rx.text("Next: compare dedicated I/O organisation with memory-mapped I/O and examine device registers in more detail.", color="#475569"),
                    rx.link(
                        rx.button("Next · I/O Organisation & Memory-Mapped I/O", color_scheme="teal"),
                        href="/academy/unit-10/io-organisation-memory-mapped-io",
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


def io_organisation_memory_mapped_io_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 02", color_scheme="teal", width="100%"),
            rx.heading("I/O Organisation & Memory-Mapped I/O", size="8"),
            rx.text(
                "Input/output organisation defines how software sees peripherals and how device registers connect to the processor. The central idea is simple: a peripheral exposes controlled registers, and the CPU reads or writes those registers using a well-defined addressing scheme.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A peripheral is controlled through registers",
                rx.text(
                    "A peripheral interface hides device-specific electrical details behind a small set of software-visible registers. Typical interfaces provide a data register plus control and status registers."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Register"),
                            rx.table.column_header_cell("Typical role"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Data"), rx.table.cell("Carries input data or output data")),
                        rx.table.row(rx.table.cell("Status"), rx.table.cell("Reports ready, busy, error, interrupt or data-available state")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("Enables modes, starts operations, clears conditions or configures the device")),
                    ),
                    width="100%",
                ),
                rx.callout(
                    "The exact register set depends on the device. The CPU does not need to know the internal circuit details if the register interface is well defined.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "2", "Two classic ways to organise processor I/O",
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Organisation"),
                            rx.table.column_header_cell("Addressing model"),
                            rx.table.column_header_cell("Software access"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.table.cell("Memory-mapped I/O"),
                            rx.table.cell("Memory and peripherals share one address space"),
                            rx.table.cell("Normal load/store instructions"),
                        ),
                        rx.table.row(
                            rx.table.cell("Isolated / port-mapped I/O"),
                            rx.table.cell("I/O has a separate port space"),
                            rx.table.cell("Dedicated I/O instructions or cycles"),
                        ),
                    ),
                    width="100%",
                ),
                _practice(
                    "What I/O organisation lets normal load/store instructions access peripheral registers by address?",
                    SystemIntegrationState.mappedio_answer,
                    SystemIntegrationState.set_mappedio_answer,
                    SystemIntegrationState.check_mappedio,
                    SystemIntegrationState.mappedio_feedback,
                    "I/O organisation",
                ),
            ),
            _section(
                "3", "Memory-mapped I/O treats device registers like addressed locations",
                rx.text(
                    "In memory-mapped I/O (MMIO), a peripheral register occupies an address just like a memory location. Address decoding decides whether a transaction reaches RAM, ROM or a peripheral."
                ),
                rx.code_block(
                    "Example address map\n"
                    "0x0000_0000 – 0x0000_FFFF   RAM\n"
                    "0x4000_0000                 UART_DATA\n"
                    "0x4000_0004                 UART_STATUS\n"
                    "0x4000_0008                 UART_CONTROL\n"
                    "0x4000_1000                 GPIO_DATA\n"
                    "0x4000_1004                 GPIO_DIRECTION",
                    language="textile", width="100%",
                ),
                rx.text(
                    "These are teaching addresses. Real processors define their own memory maps in hardware documentation."
                ),
            ),
            _section(
                "4", "Address decoding routes each access to the correct device",
                rx.code_block(
                    "CPU address/data/control\n"
                    "          │\n"
                    "          ▼\n"
                    "    system decoder\n"
                    "     ├── RAM select\n"
                    "     ├── UART select\n"
                    "     └── GPIO select\n\n"
                    "selected peripheral may then decode low address bits\n"
                    "to choose DATA, STATUS or CONTROL register",
                    language="textile", width="100%",
                ),
                rx.text(
                    "System-level decoding chooses the device; local decoding inside the peripheral interface chooses one register within that device."
                ),
            ),
            _section(
                "5", "Status registers let software observe device state",
                rx.text(
                    "A status register is normally read by software and contains individual flag bits. For example, a serial receiver may expose RX_READY, TX_READY and ERROR bits."
                ),
                rx.code_block(
                    "UART_STATUS\n"
                    "bit 0  RX_READY   = 1 when received data can be read\n"
                    "bit 1  TX_READY   = 1 when transmitter can accept another byte\n"
                    "bit 2  ERROR      = 1 when the interface detected a transfer error",
                    language="textile", width="100%",
                ),
                _practice(
                    "Which device register tells software whether a peripheral is ready, busy or has data available?",
                    SystemIntegrationState.status_answer,
                    SystemIntegrationState.set_status_answer,
                    SystemIntegrationState.check_status,
                    SystemIntegrationState.status_feedback,
                    "device register",
                ),
            ),
            _section(
                "6", "Control registers let software command the peripheral",
                rx.text(
                    "Control registers are written by software. Their bits may enable the peripheral, choose operating modes, start a conversion, select interrupt behavior or reset an internal condition."
                ),
                rx.code_block(
                    "GPIO_DIRECTION = 0x0000000F\n"
                    "binary: ...0000 1111\n"
                    "meaning in this teaching example:\n"
                    "pins 0–3 configured as outputs\n"
                    "remaining pins configured as inputs",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Register bits are hardware contracts. Software must preserve reserved bits and obey the access rules defined by the device.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "7", "Polling is the simplest way to wait for a device",
                rx.text(
                    "Software can repeatedly read a status bit until the device becomes ready. This is called polling. It is easy to understand but may waste processor time if the device is slow."
                ),
                rx.code_block(
                    "repeat:\n"
                    "    status ← READ UART_STATUS\n"
                    "until TX_READY = 1\n"
                    "WRITE UART_DATA ← next_byte",
                    language="textile", width="100%",
                ),
                _practice(
                    "What software technique repeatedly checks a peripheral status register until the device is ready?",
                    SystemIntegrationState.polling_answer,
                    SystemIntegrationState.set_polling_answer,
                    SystemIntegrationState.check_polling,
                    SystemIntegrationState.polling_feedback,
                    "waiting technique",
                ),
            ),
            _section(
                "8", "Read-only, write-only and read/write behavior matter",
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Access type"),
                            rx.table.column_header_cell("Example"),
                            rx.table.column_header_cell("Important rule"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Read-only"), rx.table.cell("status"), rx.table.cell("writes may be ignored or invalid")),
                        rx.table.row(rx.table.cell("Write-only"), rx.table.cell("command/FIFO input"), rx.table.cell("read value may be meaningless")),
                        rx.table.row(rx.table.cell("Read/write"), rx.table.cell("configuration"), rx.table.cell("software can inspect and update stored control bits")),
                    ),
                    width="100%",
                ),
                rx.text(
                    "The address alone is not enough: the interface also considers whether the current bus transaction is a read or a write."
                ),
            ),
            _section(
                "9", "Trace a complete MMIO output operation",
                rx.code_block(
                    "Goal: write value 0x55 to UART_DATA at 0x4000_0000\n\n"
                    "1. CPU executes STORE using address 0x4000_0000\n"
                    "2. system decoder selects UART\n"
                    "3. UART local decoder selects DATA register\n"
                    "4. CPU drives write data 0x55\n"
                    "5. write control becomes valid\n"
                    "6. UART captures 0x55 and begins transmission\n"
                    "7. UART may clear TX_READY until it can accept another byte",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "10", "Why MMIO fits naturally with the CPU datapath",
                rx.text(
                    "Path 09 already gave the CPU load and store operations. MMIO reuses that machinery: the ALU forms an address, the bus carries it, decoding selects the target, and the peripheral register participates in the transaction instead of ordinary RAM."
                ),
                rx.hstack(
                    rx.badge("LOAD", color_scheme="blue"), rx.text("→ read memory or mapped device register"),
                    rx.badge("STORE", color_scheme="orange"), rx.text("→ write memory or mapped device register"),
                    wrap="wrap", spacing="2",
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.text(
                    "You can now distinguish memory-mapped and isolated I/O, explain data/status/control registers, trace address decoding to a device register, and describe polling."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 02 COMPLETE", color_scheme="green"),
                    rx.heading("Software-visible peripheral organisation is now connected to the hardware bus.", size="5"),
                    rx.text(
                        "Next: learn why interrupts let devices request CPU attention without constant polling.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Interrupts & Interrupt-Driven I/O", color_scheme="teal"),
                        href="/academy/unit-10/interrupts-interrupt-driven-io",
                        text_decoration="none",
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


def interrupts_interrupt_driven_io_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 03", color_scheme="teal", width="100%"),
            rx.heading("Interrupts & Interrupt-Driven I/O", size="8"),
            rx.text(
                "Polling makes the CPU repeatedly ask whether a device needs service. Interrupt-driven I/O reverses that relationship: a peripheral raises a request when an event occurs, allowing the processor to do useful work between device events.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Why interrupts exist",
                rx.text(
                    "Peripherals often operate much more slowly than the CPU and events may occur unpredictably. Constant polling can waste instruction cycles. An interrupt gives hardware a controlled way to attract processor attention only when service is required."
                ),
                rx.code_block(
                    "POLLING\nCPU: check? check? check? check? ready! service\n\n"
                    "INTERRUPT-DRIVEN\nCPU: useful work ────────────────┐\n"
                    "device:                  IRQ ────┘ → service",
                    language="textile", width="100%",
                ),
                _practice(
                    "What mechanism lets a peripheral request CPU attention when service is needed?",
                    SystemIntegrationState.interrupt_answer,
                    SystemIntegrationState.set_interrupt_answer,
                    SystemIntegrationState.check_interrupt,
                    SystemIntegrationState.interrupt_feedback,
                    "hardware request",
                ),
            ),
            _section(
                "2", "An interrupt is a controlled change in program flow",
                rx.text(
                    "When an enabled interrupt is accepted, the CPU temporarily suspends the current instruction stream, records enough state to return later, and transfers control to an interrupt service routine (ISR)."
                ),
                rx.code_block(
                    "normal program\n"
                    "     │\n"
                    "     ├── instruction\n"
                    "     ├── instruction       peripheral raises IRQ\n"
                    "     │                           │\n"
                    "     └──── CPU accepts interrupt┘\n"
                    "                 ↓\n"
                    "           save return state\n"
                    "                 ↓\n"
                    "          execute ISR\n"
                    "                 ↓\n"
                    "       return from interrupt\n"
                    "                 ↓\n"
                    "        resume normal program",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "3", "Interrupt enable and masking control whether requests are accepted",
                rx.text(
                    "A request may be pending without being immediately serviced. Global interrupt enable, per-device enable bits and priority/mask logic determine whether the CPU accepts a request at a particular time."
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Control"),
                            rx.table.column_header_cell("Purpose"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Global enable"), rx.table.cell("Allows or blocks maskable interrupts at CPU level")),
                        rx.table.row(rx.table.cell("Device enable"), rx.table.cell("Allows a particular peripheral to generate an interrupt")),
                        rx.table.row(rx.table.cell("Mask"), rx.table.cell("Temporarily prevents selected interrupt sources from being accepted")),
                        rx.table.row(rx.table.cell("Pending flag"), rx.table.cell("Records that an interrupt condition is waiting for service")),
                    ),
                    width="100%",
                ),
            ),
            _section(
                "4", "Interrupt vectors identify the correct service routine",
                rx.text(
                    "A system with several interrupt sources needs a way to choose the correct ISR. In a vectored design, an interrupt number, vector address or vector-table entry leads the processor to the appropriate handler."
                ),
                rx.code_block(
                    "interrupt source → vector / interrupt ID → vector table → ISR address\n\n"
                    "example teaching table:\n"
                    "vector 0 → timer ISR\n"
                    "vector 1 → UART receive ISR\n"
                    "vector 2 → GPIO ISR",
                    language="textile", width="100%",
                ),
                _practice(
                    "What value or table entry directs the CPU toward the correct interrupt service routine?",
                    SystemIntegrationState.vector_answer,
                    SystemIntegrationState.set_vector_answer,
                    SystemIntegrationState.check_vector,
                    SystemIntegrationState.vector_feedback,
                    "interrupt routing value",
                ),
            ),
            _section(
                "5", "The CPU must preserve the interrupted program",
                rx.text(
                    "The ISR may use registers and change condition flags. The processor and/or software therefore preserve the state required to resume the interrupted code correctly. This preserved state is commonly called context."
                ),
                rx.code_block(
                    "before ISR: PC = return point, registers contain program state\n"
                    "enter ISR : preserve required context\n"
                    "ISR       : may use registers and flags\n"
                    "exit ISR  : restore required context\n"
                    "resume    : continue as though service happened between instructions",
                    language="textile", width="100%",
                ),
                _practice(
                    "What must be preserved before an ISR changes processor state needed by the interrupted program?",
                    SystemIntegrationState.context_answer,
                    SystemIntegrationState.set_context_answer,
                    SystemIntegrationState.check_context,
                    SystemIntegrationState.context_feedback,
                    "saved program state",
                ),
            ),
            _section(
                "6", "A good ISR handles the cause, not just the request",
                rx.text(
                    "The handler normally determines why the device interrupted, transfers or processes the necessary data, clears or acknowledges the interrupt condition when required, and then returns."
                ),
                rx.code_block(
                    "UART receive ISR\n"
                    "1. read status / identify receive event\n"
                    "2. read received byte from UART_DATA\n"
                    "3. store byte in software buffer\n"
                    "4. clear/acknowledge condition if required\n"
                    "5. return from interrupt",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "Exact acknowledgement behavior is device-specific. Some flags clear when a register is read; others require an explicit write.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "7", "Polling and interrupts trade simplicity for responsiveness",
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Method"),
                            rx.table.column_header_cell("Strength"),
                            rx.table.column_header_cell("Cost / limitation"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Polling"), rx.table.cell("Simple, predictable software flow"), rx.table.cell("CPU time spent repeatedly checking status")),
                        rx.table.row(rx.table.cell("Interrupt-driven"), rx.table.cell("CPU works on other tasks until service is requested"), rx.table.cell("Needs interrupt hardware, context handling and careful ISR design")),
                    ),
                    width="100%",
                ),
                rx.text(
                    "Neither method is universally best. Very simple or timing-critical loops may poll; event-driven systems often benefit from interrupts."
                ),
            ),
            _section(
                "8", "Priority resolves simultaneous interrupt requests",
                rx.text(
                    "If multiple devices request service together, priority logic determines which request is accepted first. Some systems use fixed priorities; others provide programmable priority levels."
                ),
                rx.code_block(
                    "pending: TIMER, UART, GPIO\n"
                    "priority: UART > TIMER > GPIO\n"
                    "CPU services UART first\n"
                    "other pending requests remain until eligible",
                    language="textile", width="100%",
                ),
                rx.text(
                    "Priority is distinct from masking: priority chooses among eligible requests, while masking can make a request temporarily ineligible."
                ),
            ),
            _section(
                "9", "Interrupt latency measures response delay",
                rx.text(
                    "Interrupt latency is the time from a service-requiring event/request to the point where the corresponding ISR begins useful handling. It can include instruction completion, arbitration, context entry and other implementation delays."
                ),
                rx.callout(
                    "Low latency matters for time-sensitive devices, but correctness also requires bounded ISR work so other events are not blocked for too long.",
                    icon="clock", color_scheme="purple",
                ),
            ),
            _section(
                "10", "Trace one complete interrupt-driven input",
                rx.code_block(
                    "1. CPU executes normal program\n"
                    "2. UART receives a byte and sets RX_READY\n"
                    "3. enabled UART asserts interrupt request\n"
                    "4. CPU accepts request at a valid boundary\n"
                    "5. return state / required context is preserved\n"
                    "6. vector selects UART receive ISR\n"
                    "7. ISR reads UART_DATA and stores the byte\n"
                    "8. interrupt condition is cleared/acknowledged\n"
                    "9. context is restored\n"
                    "10. return-from-interrupt resumes the normal program",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.text(
                    "You can now explain why interrupts reduce polling, trace interrupt entry and return, describe masks and pending flags, explain vectors and context, and compare polling with interrupt-driven I/O."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 03 COMPLETE", color_scheme="green"),
                    rx.heading("Peripherals can now request CPU attention efficiently.", size="5"),
                    rx.text(
                        "Next: examine shared buses, arbitration and the protocols that coordinate multiple system components.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · System Buses, Arbitration & Protocols", color_scheme="teal"),
                        href="/academy/unit-10/system-buses-arbitration-protocols",
                        text_decoration="none",
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


def system_buses_arbitration_protocols_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 04", color_scheme="teal", width="100%"),
            rx.heading("System Buses, Arbitration & Protocols", size="8"),
            rx.text(
                "A system bus lets processors, memories and I/O controllers exchange addresses, data and control information. When several capable initiators share that path, arbitration and protocol rules keep every transfer ordered and unambiguous.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A bus is a shared communication path",
                rx.text("Instead of providing a dedicated connection between every pair of components, a bus allows multiple blocks to use a common set of signals under defined ownership and timing rules."),
                rx.code_block(
                    "                 ┌──────── CPU ────────┐\n"
                    "                 │ address / data / ctl│\n"
                    "                 └─────────┬───────────┘\n"
                    "                           BUS\n"
                    "                 ┌──────────┼──────────┐\n"
                    "              Memory      DMA/I/O     Timer",
                    language="textile", width="100%",
                ),
                _practice(
                    "What shared communication path carries information between system components?",
                    SystemIntegrationState.bus_answer,
                    SystemIntegrationState.set_bus_answer,
                    SystemIntegrationState.check_bus,
                    SystemIntegrationState.bus_feedback,
                    "shared path",
                ),
            ),
            _section(
                "2", "Address, data and control signals have different jobs",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Signal group"),
                        rx.table.column_header_cell("Purpose"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Address"), rx.table.cell("Identifies the target location or device register")),
                        rx.table.row(rx.table.cell("Data"), rx.table.cell("Carries the value being transferred")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("Describes direction, validity, acknowledgement and timing")),
                    ), width="100%",
                ),
                rx.text("These logical groups may use separate physical wires or may be multiplexed onto the same pins at different times."),
            ),
            _section(
                "3", "Bus masters initiate; targets respond",
                rx.text("A bus master (initiator) begins a transaction by selecting a target and specifying an operation. The addressed target responds with data, acceptance or completion information."),
                rx.code_block(
                    "MASTER                         TARGET\n"
                    "  │ -- address + READ ----------> │\n"
                    "  │ <--------- data ------------- │\n"
                    "  │ <------- complete/ready ----- │",
                    language="textile", width="100%",
                ),
                rx.callout("A CPU is commonly a bus master, but DMA engines and other controllers may also initiate transfers.", icon="info", color_scheme="blue"),
            ),
            _section(
                "4", "Shared buses require ownership",
                rx.text("Two masters must not drive incompatible values onto the same shared signals simultaneously. Ownership rules ensure that only the granted master controls master-driven bus signals during its transaction."),
                rx.code_block(
                    "CPU request ──┐\n"
                    "DMA request ──┼──> ARBITER ──> one grant\n"
                    "GPU request ──┘\n\n"
                    "grant → selected master owns the bus for the permitted transfer",
                    language="textile", width="100%",
                ),
                _practice(
                    "What process decides which requester may control a shared bus?",
                    SystemIntegrationState.arbitration_answer,
                    SystemIntegrationState.set_arbitration_answer,
                    SystemIntegrationState.check_arbitration,
                    SystemIntegrationState.arbitration_feedback,
                    "ownership decision",
                ),
            ),
            _section(
                "5", "Arbitration policies balance latency and fairness",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Policy"),
                        rx.table.column_header_cell("Idea"),
                        rx.table.column_header_cell("Trade-off"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Fixed priority"), rx.table.cell("Highest-priority requester wins"), rx.table.cell("Fast and simple; low priority may wait too long")),
                        rx.table.row(rx.table.cell("Round-robin"), rx.table.cell("Priority rotates among requesters"), rx.table.cell("Improves fairness")),
                        rx.table.row(rx.table.cell("Time-sliced"), rx.table.cell("Ownership opportunities are scheduled"), rx.table.cell("Predictable sharing; may waste unused slots")),
                    ), width="100%",
                ),
            ),
            _section(
                "6", "A protocol defines a legal transaction",
                rx.text("The bus protocol specifies when address and control become valid, when data is transferred, how a target reports completion, and what happens if a target is slow or unavailable."),
                rx.code_block(
                    "READ transaction\n"
                    "1. master obtains ownership\n"
                    "2. master presents address + READ\n"
                    "3. target decodes address\n"
                    "4. target presents read data\n"
                    "5. target signals ready/complete\n"
                    "6. master samples data and ends transfer",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Synchronous buses use a shared timing reference",
                rx.text("In a synchronous bus, participants interpret transaction phases relative to a common clock. This makes timing relationships explicit in clock cycles."),
                rx.code_block(
                    "clock : _/‾\\_/‾\\_/‾\\_/‾\\_\n"
                    "addr  : ----[ VALID ]-------\n"
                    "read  : ----[   1   ]-------\n"
                    "data  : --------[ DATA ]----\n"
                    "ready : -----------[1]------",
                    language="textile", width="100%",
                ),
                rx.text("A slow target may require wait states or a ready signal so the transaction can take additional cycles."),
            ),
            _section(
                "8", "Asynchronous buses coordinate with handshakes",
                rx.text("An asynchronous bus does not require every transfer phase to be tied to one shared clock. Request/valid and acknowledge/ready relationships coordinate progress."),
                rx.code_block(
                    "master: address/data valid ────────┐\n"
                    "                                     │\n"
                    "target:                 acknowledge ─┘\n"
                    "master: observe acknowledgement → finish transfer",
                    language="textile", width="100%",
                ),
                rx.text("Handshake timing allows components with different response speeds to communicate, though the protocol and interface logic must manage the timing safely."),
            ),
            _section(
                "9", "Latency and bandwidth describe different performance limits",
                rx.text("Latency is the delay to complete an individual transaction. Bandwidth is the amount of useful information transferable per unit time. Arbitration delay, wait states, protocol overhead and bus width all influence observed performance."),
                rx.callout("A bus can have high peak bandwidth yet still give an individual requester noticeable latency when many masters compete for ownership.", icon="clock", color_scheme="purple"),
            ),
            _section(
                "10", "Trace arbitration and one complete transfer",
                rx.code_block(
                    "1. CPU and DMA both request the shared bus\n"
                    "2. arbiter grants DMA according to current policy\n"
                    "3. DMA becomes bus master\n"
                    "4. DMA presents target address and READ control\n"
                    "5. addressed memory decodes the request\n"
                    "6. memory returns data and asserts ready\n"
                    "7. DMA captures data\n"
                    "8. DMA ends the transaction and releases ownership\n"
                    "9. arbiter can grant the waiting CPU request",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "11", "Lesson checkpoint",
                rx.text("You can now identify bus signal groups, distinguish masters from targets, explain why arbitration is required, compare arbitration policies, trace a transaction, and contrast synchronous timing with asynchronous handshaking."),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 04 COMPLETE", color_scheme="green"),
                    rx.heading("Shared communication is now coordinated by ownership and protocol.", size="5"),
                    rx.text("Next: connect system transfers to DMA and higher-throughput data movement.", color="#475569"),
                    rx.link(
                        rx.button("Next · DMA & High-Throughput Data Movement", color_scheme="teal"),
                        href="/academy/unit-10/dma-high-throughput-data-movement",
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


def dma_high_throughput_data_movement_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 05", color_scheme="teal", width="100%"),
            rx.heading("DMA & High-Throughput Data Movement", size="8"),
            rx.text(
                "Programmed I/O makes the CPU move each item itself. Direct Memory Access (DMA) adds a transfer engine that can become a bus master and move blocks of data between memory and peripherals with much less processor work per byte or word.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "Why DMA is useful",
                rx.text(
                    "For a large transfer, repeatedly loading from a device register and storing to memory consumes CPU instructions and bus transactions. DMA lets software configure a transfer once, then allows hardware to perform the repetitive movement."
                ),
                rx.code_block(
                    "PROGRAMMED I/O\n"
                    "CPU: read device → write memory → read device → write memory → ...\n\n"
                    "DMA\n"
                    "CPU: configure DMA ───────────────┐\n"
                    "DMA:                 transfer block directly\n"
                    "CPU: useful work ────────────────┘",
                    language="textile", width="100%",
                ),
                _practice(
                    "What mechanism lets a controller transfer data directly between memory and a device without the CPU copying every item?",
                    SystemIntegrationState.dma_answer,
                    SystemIntegrationState.set_dma_answer,
                    SystemIntegrationState.check_dma,
                    SystemIntegrationState.dma_feedback,
                    "transfer mechanism",
                ),
            ),
            _section(
                "2", "A DMA engine needs transfer descriptors",
                rx.text(
                    "Before starting, software gives the DMA controller enough information to identify the source, destination, direction and amount of data. Real controllers may also include width, stride, burst size and interrupt options."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Field"),
                        rx.table.column_header_cell("Purpose"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Source address"), rx.table.cell("Where data comes from")),
                        rx.table.row(rx.table.cell("Destination address"), rx.table.cell("Where data goes")),
                        rx.table.row(rx.table.cell("Transfer count"), rx.table.cell("How many bytes/words/items to move")),
                        rx.table.row(rx.table.cell("Control"), rx.table.cell("Direction, width, increment rules, enable and completion behavior")),
                    ), width="100%",
                ),
            ),
            _section(
                "3", "DMA becomes a bus master",
                rx.text(
                    "The DMA controller cannot move memory data merely by observing the bus. It must obtain permission to initiate transactions. The arbitration concepts from Lesson 4 therefore apply directly."
                ),
                rx.code_block(
                    "CPU request ──┐\n"
                    "DMA request ──┼──> bus arbiter ──> grant\n"
                    "other master ─┘\n\n"
                    "when DMA is granted:\n"
                    "DMA issues addresses + read/write controls + data transfers",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "DMA reduces CPU copying work, but it does not make the interconnect free. DMA traffic still consumes memory and bus bandwidth.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "4", "Peripheral-to-memory DMA",
                rx.text(
                    "For an input stream, the peripheral supplies data and the DMA engine writes it into memory. The source may be a fixed device-data register while the destination address increments through a buffer."
                ),
                rx.code_block(
                    "device DATA register  ──→ DMA ──→ RAM buffer\n"
                    "fixed source address          destination increments\n\n"
                    "sample sequence:\n"
                    "RAM[0x2000] ← item0\n"
                    "RAM[0x2004] ← item1\n"
                    "RAM[0x2008] ← item2",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Memory-to-peripheral DMA",
                rx.text(
                    "For output, DMA reads a memory buffer and writes successive items to the peripheral. The memory source increments while the device register address may remain fixed."
                ),
                rx.code_block(
                    "RAM buffer ──→ DMA ──→ device DATA register\n"
                    "source increments          fixed destination address",
                    language="textile", width="100%",
                ),
                rx.text(
                    "This pattern is common for transmit buffers, display data, storage interfaces and other stream-oriented devices."
                ),
            ),
            _section(
                "6", "Burst transfers improve bus efficiency",
                rx.text(
                    "A bus transaction has overhead: arbitration, addressing and control setup. A burst keeps ownership long enough to transfer several related data items, reducing setup overhead per item."
                ),
                rx.code_block(
                    "single transfers:\n"
                    "[arb+addr+DATA] [arb+addr+DATA] [arb+addr+DATA]\n\n"
                    "burst:\n"
                    "[arb+addr+ DATA0 DATA1 DATA2 DATA3 ]",
                    language="textile", width="100%",
                ),
                _practice(
                    "What transfer style moves several consecutive data items after one setup/arbitration phase?",
                    SystemIntegrationState.burst_answer,
                    SystemIntegrationState.set_burst_answer,
                    SystemIntegrationState.check_burst,
                    SystemIntegrationState.burst_feedback,
                    "transfer style",
                ),
            ),
            _section(
                "7", "DMA completion is often reported by interrupt",
                rx.text(
                    "The CPU should not have to poll every transferred item. A common design is: configure DMA, enable it, perform other work, and receive an interrupt when the block completes or an error occurs."
                ),
                rx.code_block(
                    "CPU: program descriptor → start DMA → continue other work\n"
                    "DMA: transfer ... transfer ... transfer ... done\n"
                    "DMA: set completion status + interrupt CPU\n"
                    "ISR: check result, release/process buffer, schedule next transfer",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "Buffers decouple producer and consumer timing",
                rx.text(
                    "A memory buffer absorbs timing differences between a peripheral stream and software processing. Double buffering or ring buffers can let DMA fill one region while software processes another."
                ),
                rx.code_block(
                    "device → DMA → [ Buffer A ] → software processing\n"
                    "              [ Buffer B ]\n\n"
                    "cycle 1: DMA fills A, CPU processes B\n"
                    "cycle 2: DMA fills B, CPU processes A",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "9", "Caches create a visibility problem",
                rx.text(
                    "DMA commonly reads or writes main memory while the CPU may hold cached copies of the same addresses. Without a coherent design or explicit cache-maintenance rules, the CPU and DMA controller can observe different versions of the data."
                ),
                rx.code_block(
                    "CPU cache:     buffer = OLD value\n"
                    "main memory:   buffer = NEW value written by DMA\n\n"
                    "CPU must not keep using stale cached data",
                    language="textile", width="100%",
                ),
                _practice(
                    "What issue must be managed when DMA accesses memory that may also be cached by the CPU?",
                    SystemIntegrationState.coherence_answer,
                    SystemIntegrationState.set_coherence_answer,
                    SystemIntegrationState.check_coherence,
                    SystemIntegrationState.coherence_feedback,
                    "memory consistency issue",
                ),
                rx.callout(
                    "Specific cache-maintenance instructions and coherency guarantees depend on the processor and system architecture.",
                    icon="triangle-alert", color_scheme="orange",
                ),
            ),
            _section(
                "10", "High throughput still requires balanced resources",
                rx.text(
                    "DMA performance can be limited by the peripheral, interconnect, memory controller, bus arbitration, transfer width or software buffer management. The slowest relevant resource limits sustained throughput."
                ),
                rx.hstack(
                    rx.badge("Peripheral", color_scheme="blue"),
                    rx.text("→ produces/consumes data"),
                    rx.badge("Bus", color_scheme="orange"),
                    rx.text("→ carries transactions"),
                    rx.badge("Memory", color_scheme="purple"),
                    rx.text("→ stores the block"),
                    wrap="wrap", spacing="2",
                ),
            ),
            _section(
                "11", "Trace a complete DMA receive operation",
                rx.code_block(
                    "1. software allocates RAM buffer at 0x2000\n"
                    "2. CPU configures DMA: source=UART_DATA, destination=0x2000, count=256\n"
                    "3. CPU enables UART/DMA request and starts channel\n"
                    "4. incoming data makes peripheral request DMA service\n"
                    "5. DMA requests and receives bus ownership as needed\n"
                    "6. DMA reads UART_DATA and writes successive RAM locations\n"
                    "7. count reaches zero\n"
                    "8. DMA marks completion and optionally interrupts CPU\n"
                    "9. software verifies status and processes the completed buffer",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now explain why DMA reduces CPU transfer overhead, describe DMA descriptors, connect DMA to bus arbitration, trace both transfer directions, explain bursts and buffering, and identify the CPU-cache visibility issue."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 05 COMPLETE", color_scheme="green"),
                    rx.heading("High-volume data can now move through the system without CPU copying every item.", size="5"),
                    rx.text(
                        "Next: study timers, counters and system timing as programmable hardware resources.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Timers, Counters & System Timing", color_scheme="teal"),
                        href="/academy/unit-10/timers-counters-system-timing",
                        text_decoration="none",
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


def timers_counters_system_timing_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 06", color_scheme="teal", width="100%"),
            rx.heading("Timers, Counters & System Timing", size="8"),
            rx.text(
                "Digital systems need hardware that can measure elapsed time, count events, schedule periodic work and detect missing progress. Timers and counters provide those functions by advancing state from a clock or external event source.",
                size="4", color="#475569", line_height="1.6",
            ),
            _section(
                "1", "A timer is a counter with a time base",
                rx.text(
                    "A binary counter changes value on selected input events. When those events come from a known clock, the count represents elapsed time. Control registers determine whether the counter runs, its direction, and what happens at programmed values."
                ),
                rx.code_block(
                    "source clock ──→ timer/counter ──→ current count\n"
                    "                         │\n"
                    "                         └── compare/overflow event",
                    language="textile", width="100%",
                ),
                _practice(
                    "What hardware block counts clock ticks or external events to measure or schedule time?",
                    SystemIntegrationState.timer_answer,
                    SystemIntegrationState.set_timer_answer,
                    SystemIntegrationState.check_timer,
                    SystemIntegrationState.timer_feedback,
                    "timing block",
                ),
            ),
            _section(
                "2", "Timer registers make timing programmable",
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Register"),
                        rx.table.column_header_cell("Typical role"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("COUNT"), rx.table.cell("Current timer/counter value")),
                        rx.table.row(rx.table.cell("COMPARE"), rx.table.cell("Value that generates a match event")),
                        rx.table.row(rx.table.cell("CONTROL"), rx.table.cell("Enable, mode, clock source, prescale and interrupt options")),
                        rx.table.row(rx.table.cell("STATUS"), rx.table.cell("Overflow, match, capture or other event flags")),
                    ), width="100%",
                ),
                rx.text("These registers can be exposed through the memory-mapped I/O model introduced earlier in Path 10."),
            ),
            _section(
                "3", "Prescalers extend the useful timing range",
                rx.text(
                    "A fast processor clock may make a small counter overflow too quickly. A prescaler divides the source frequency so the timer receives a slower tick."
                ),
                rx.code_block(
                    "48 MHz source ──÷48──→ 1 MHz timer tick\n"
                    "                       1 tick = 1 microsecond\n\n"
                    "counter value 1000 → about 1 millisecond elapsed",
                    language="textile", width="100%",
                ),
                _practice(
                    "What timer component divides the source clock before it reaches the counter?",
                    SystemIntegrationState.prescaler_answer,
                    SystemIntegrationState.set_prescaler_answer,
                    SystemIntegrationState.check_prescaler,
                    SystemIntegrationState.prescaler_feedback,
                    "clock divider",
                ),
            ),
            _section(
                "4", "Overflow and compare-match create events",
                rx.text(
                    "Overflow occurs when a finite-width counter wraps beyond its maximum value. Compare-match hardware instead checks whether COUNT equals a programmed COMPARE value. Either event can set a status flag or request an interrupt."
                ),
                rx.code_block(
                    "COUNT:   ... 247 248 249 250 ...\n"
                    "COMPARE:             250\n"
                    "event:                 ↑ match\n\n"
                    "8-bit overflow: 254 → 255 → 0",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "5", "Periodic timers schedule repeated work",
                rx.text(
                    "A timer can automatically reload or reset after a compare event. This creates a regular sequence of events without software manually rebuilding the delay after every period."
                ),
                rx.code_block(
                    "time ─────────────────────────────────────→\n"
                    "tick event:    ↑        ↑        ↑        ↑\n"
                    "               T        2T       3T       4T\n\n"
                    "each event may set a flag or request an interrupt",
                    language="textile", width="100%",
                ),
                rx.callout(
                    "The timer provides the periodic event; software execution may begin slightly later because interrupt latency and higher-priority work can delay service.",
                    icon="info", color_scheme="blue",
                ),
            ),
            _section(
                "6", "Input capture timestamps external events",
                rx.text(
                    "Capture hardware copies the current counter value into a capture register when an external edge occurs. Software can subtract captured timestamps to measure periods, pulse widths or event spacing."
                ),
                rx.code_block(
                    "free-running counter:  ... 1200 1201 1202 ... 1840 ...\n"
                    "external edge:                 ↑           ↑\n"
                    "capture register:            1202        1840\n\n"
                    "measured interval = 1840 - 1202 = 638 timer ticks",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "7", "Output compare can control hardware precisely",
                rx.text(
                    "On a compare match, hardware may toggle, set or clear an output pin without waiting for software. This supports accurate waveform generation and is a foundation for pulse-width modulation."
                ),
                rx.code_block(
                    "counter ──compare──→ output action\n"
                    "                       │\n"
                    "                       └── toggle/set/clear pin",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "8", "PWM encodes control in pulse width",
                rx.text(
                    "Pulse-width modulation repeats a fixed period while changing how long the output stays active. The duty cycle is the active fraction of each period."
                ),
                rx.code_block(
                    "25% duty:  ‾‾____  ‾‾____  ‾‾____\n"
                    "50% duty:  ‾‾‾___  ‾‾‾___  ‾‾‾___\n"
                    "75% duty:  ‾‾‾‾__  ‾‾‾‾__  ‾‾‾‾__\n\n"
                    "duty cycle = active time / period × 100%",
                    language="textile", width="100%",
                ),
                rx.text("Hardware PWM is commonly used for motor control, LED brightness, power conversion and other regularly timed outputs."),
            ),
            _section(
                "9", "Watchdog timers detect missing progress",
                rx.text(
                    "A watchdog is configured with a timeout and periodically serviced by correctly progressing software. If servicing stops because the system hangs or becomes trapped, the watchdog expires and can trigger an interrupt or reset."
                ),
                rx.code_block(
                    "healthy:  service ── service ── service ── service\n"
                    "fault:    service ── service ─────────────── TIMEOUT → recovery",
                    language="textile", width="100%",
                ),
                _practice(
                    "What timer is periodically serviced by healthy software and triggers recovery if servicing stops?",
                    SystemIntegrationState.watchdog_answer,
                    SystemIntegrationState.set_watchdog_answer,
                    SystemIntegrationState.check_watchdog,
                    SystemIntegrationState.watchdog_feedback,
                    "recovery timer",
                ),
            ),
            _section(
                "10", "Clock domains and timer sources matter",
                rx.text(
                    "A timer may run from the CPU clock, a divided peripheral clock, a low-frequency oscillator or an external signal. The chosen source determines resolution, range, power behavior and whether the timer can continue when parts of the processor are idle."
                ),
                rx.table.root(
                    rx.table.header(rx.table.row(
                        rx.table.column_header_cell("Source"),
                        rx.table.column_header_cell("Useful property"),
                    )),
                    rx.table.body(
                        rx.table.row(rx.table.cell("Fast peripheral clock"), rx.table.cell("Fine timing resolution")),
                        rx.table.row(rx.table.cell("Prescaled clock"), rx.table.cell("Longer measurable intervals")),
                        rx.table.row(rx.table.cell("Low-power clock"), rx.table.cell("Timing while major blocks sleep")),
                        rx.table.row(rx.table.cell("External event"), rx.table.cell("Counts real-world pulses rather than elapsed clock time")),
                    ), width="100%",
                ),
            ),
            _section(
                "11", "Trace a periodic interrupt timer",
                rx.code_block(
                    "1. software selects timer clock and prescaler\n"
                    "2. software programs COMPARE for the desired interval\n"
                    "3. software enables compare interrupt and starts timer\n"
                    "4. COUNT advances on each timer tick\n"
                    "5. COUNT reaches COMPARE\n"
                    "6. timer sets match status and requests interrupt\n"
                    "7. interrupt controller delivers the request to CPU\n"
                    "8. ISR performs/schedules the periodic task and clears the event\n"
                    "9. auto-reload/reset begins the next period",
                    language="textile", width="100%",
                ),
            ),
            _section(
                "12", "Lesson checkpoint",
                rx.text(
                    "You can now explain timer/counter operation, prescaling, overflow and compare events, periodic interrupts, input capture, output compare, PWM, watchdog recovery and the importance of selecting an appropriate clock source."
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.badge("LESSON 06 COMPLETE", color_scheme="green"),
                    rx.heading("System timing is now represented by programmable hardware rather than software delay loops.", size="5"),
                    rx.text(
                        "Next: connect the processor to serial and parallel peripheral interfaces.",
                        color="#475569",
                    ),
                    rx.link(
                        rx.button("Next · Peripheral Interfaces & Serial Communication", color_scheme="teal"),
                        href="/academy/unit-10/peripheral-interfaces-serial-communication",
                        text_decoration="none",
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


def peripheral_interfaces_serial_communication_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 07", color_scheme="teal", width="100%"),
            rx.heading("Peripheral Interfaces & Serial Communication", size="8"),
            rx.text("Processors rarely connect directly to every sensor, display, converter or storage device. Peripheral controllers translate CPU-visible registers and bus transactions into electrical protocols that external devices understand.", size="4", color="#475569", line_height="1.6"),
            _section("1", "Peripheral controllers bridge two worlds",
                rx.text("On the CPU side, a controller exposes memory-mapped data, status and control registers. On the device side, it generates protocol-specific signals, timing and framing."),
                rx.code_block("CPU/system bus ──→ peripheral registers ──→ protocol engine ──→ external device\n                    data/status/control       timing + framing", language="textile", width="100%")),
            _section("2", "Parallel and serial interfaces trade pins for timing",
                rx.text("A parallel interface can transfer several bits at once using several data lines. A serial interface sends bits sequentially, greatly reducing pin count and often simplifying cabling."),
                rx.code_block("parallel 8-bit:  D7 D6 D5 D4 D3 D2 D1 D0  → word together\n\nserial:          line → b7 → b6 → b5 → b4 → b3 → b2 → b1 → b0", language="textile", width="100%"),
                _practice("What communication style sends the bits of a word sequentially rather than on many parallel data lines?", SystemIntegrationState.serial_answer, SystemIntegrationState.set_serial_answer, SystemIntegrationState.check_serial, SystemIntegrationState.serial_feedback, "communication style")),
            _section("3", "Serial links need framing and timing rules",
                rx.text("Both ends must agree how bits are ordered and when they are valid. A protocol defines bit rate or clocking, frame boundaries, direction, addressing and error detection."),
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Protocol concern"),rx.table.column_header_cell("Question it answers"))),rx.table.body(
                    rx.table.row(rx.table.cell("Timing"),rx.table.cell("When is each bit sampled?")),
                    rx.table.row(rx.table.cell("Framing"),rx.table.cell("Where does a transfer begin and end?")),
                    rx.table.row(rx.table.cell("Direction"),rx.table.cell("Who may transmit and when?")),
                    rx.table.row(rx.table.cell("Addressing"),rx.table.cell("Which device is the target?")),
                    rx.table.row(rx.table.cell("Integrity"),rx.table.cell("How can transmission errors be detected?"))),width="100%")),
            _section("4", "UART provides asynchronous point-to-point serial I/O",
                rx.text("A Universal Asynchronous Receiver/Transmitter does not send a separate clock line. Transmitter and receiver instead agree on a baud rate. Each character is framed so the receiver can synchronize to its beginning."),
                rx.code_block("idle   start   data bits                  stop   idle\n 1  ────0──── d0 d1 d2 d3 d4 d5 d6 d7 ───1──── 1\n\nTX of one device ─────────→ RX of the other\nRX of one device ←───────── TX of the other",language="textile",width="100%"),
                _practice("Which common asynchronous serial peripheral uses TX/RX and start/stop framing?",SystemIntegrationState.uart_answer,SystemIntegrationState.set_uart_answer,SystemIntegrationState.check_uart,SystemIntegrationState.uart_feedback,"serial peripheral")),
            _section("5", "UART status separates CPU speed from line speed",
                rx.text("Transmit and receive buffers allow software and the serial line to operate at different moments. Status flags report conditions such as transmit space, received data and framing or overrun errors."),
                rx.code_block("CPU write → TX register/FIFO → serializer → TX pin\nCPU read  ← RX register/FIFO ← deserializer ← RX pin\n                 ↑\n            status / IRQ",language="textile",width="100%"),
                rx.callout("Polling can inspect UART status repeatedly, while interrupt-driven I/O lets the controller request service only when useful work is available.",icon="info",color_scheme="blue")),
            _section("6", "SPI is synchronous and clocked by a controller",
                rx.text("The Serial Peripheral Interface uses an explicit clock. A controller selects a target and shifts data in and out on each clock cycle. Separate transmit and receive data paths make full-duplex exchange possible."),
                rx.code_block("controller                     peripheral\nSCLK  ─────────────────────────→ clock\nMOSI  ─────────────────────────→ data in\nMISO  ←───────────────────────── data out\nCS    ─────────────────────────→ select",language="textile",width="100%"),
                _practice("Which synchronous serial interface commonly uses SCLK, MOSI, MISO and chip-select?",SystemIntegrationState.spi_answer,SystemIntegrationState.set_spi_answer,SystemIntegrationState.check_spi,SystemIntegrationState.spi_feedback,"interface")),
            _section("7", "Chip-select lets one SPI controller reach several targets",
                rx.text("Clock and data signals may be shared, while separate chip-select lines identify the active peripheral. Only the selected target should respond to the current transaction."),
                rx.code_block("                 ┌── CS0 → device A\nSPI controller ──┼── CS1 → device B\n   SCLK/MOSI/MISO└── CS2 → device C",language="textile",width="100%")),
            _section("8", "I²C shares clock and data among addressed devices",
                rx.text("Inter-Integrated Circuit (I²C) commonly uses two shared lines: SCL for clock and SDA for bidirectional data. Devices are selected by addresses carried within the transaction rather than by a dedicated select wire per device."),
                rx.code_block("controller ── SCL ─────────┬──── device 0x20\n           ── SDA ─────────┼──── device 0x48\n                            └──── device 0x68\n\nSTART → address + R/W → acknowledge → data ... → STOP",language="textile",width="100%")),
            _section("9", "Protocol choice depends on system requirements",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Interface"),rx.table.column_header_cell("Typical strength"),rx.table.column_header_cell("Typical trade-off"))),rx.table.body(
                    rx.table.row(rx.table.cell("UART"),rx.table.cell("Simple asynchronous point-to-point link"),rx.table.cell("Both ends must agree on timing")),
                    rx.table.row(rx.table.cell("SPI"),rx.table.cell("Fast synchronous transfers and full duplex"),rx.table.cell("More wires and often one select per target")),
                    rx.table.row(rx.table.cell("I²C"),rx.table.cell("Many addressed devices on two shared signal lines"),rx.table.cell("More structured shared-bus protocol")),
                    rx.table.row(rx.table.cell("Parallel"),rx.table.cell("Several bits transferred simultaneously"),rx.table.cell("Consumes more pins and routing resources"))),width="100%")),
            _section("10", "Interrupts and DMA scale peripheral data movement",
                rx.text("A low-rate device may be handled by polling. Interrupts reduce wasted CPU checking. For sustained streams, DMA can move blocks between peripheral FIFOs and memory while the CPU performs other work."),
                rx.code_block("low activity:       CPU polling → peripheral\nevent driven:       peripheral → IRQ → CPU service\nhigh throughput:    peripheral ⇄ DMA ⇄ memory\n                                  └→ completion IRQ",language="textile",width="100%")),
            _section("11", "Trace a UART receive operation",
                rx.code_block("1. remote transmitter sends start bit and framed data\n2. UART receiver samples incoming RX bits at configured timing\n3. UART reconstructs the character and checks framing\n4. character enters receive register/FIFO\n5. RX-ready status becomes active\n6. controller may request an interrupt\n7. CPU/ISR reads the memory-mapped UART data register\n8. software consumes or buffers the received character",language="textile",width="100%")),
            _section("12", "Lesson checkpoint",
                rx.text("You can now distinguish parallel and serial transfer, explain framing and synchronization, trace UART operation, identify SPI signals, describe I²C addressing, and connect peripheral interfaces to polling, interrupts and DMA.")),
            rx.card(rx.vstack(
                rx.badge("LESSON 07 COMPLETE",color_scheme="green"),
                rx.heading("CPU-visible registers are now connected to real peripheral communication protocols.",size="5"),
                rx.text("Next: study storage interfaces, block devices and persistent data movement.",color="#475569"),
                rx.link(
                        rx.button("Next · Storage Systems & Block I/O", color_scheme="teal"),
                        href="/academy/unit-10/storage-systems-block-io",
                        text_decoration="none",
                    ),
                spacing="3",align="start"),width="100%"),
            spacing="6",align="stretch",max_width="1050px",width="100%",margin="0 auto",padding="32px 20px 64px"),
        min_height="100vh",background="#f8fafc")


def storage_systems_block_io_lesson() -> rx.Component:
    return rx.box(
        app_header(),
        rx.vstack(
            rx.badge("PATH 10 · LESSON 08", color_scheme="teal", width="100%"),
            rx.heading("Storage Systems & Block I/O", size="8"),
            rx.text("Persistent storage completes the system-level journey. Block storage presents addressable chunks of data that move through controllers, queues, DMA and memory before software can use them.", size="4", color="#475569", line_height="1.6"),
            _section("1", "Storage devices preserve data beyond normal execution",
                rx.text("Main memory is fast working storage but is commonly volatile. Persistent storage retains information beyond normal execution. A storage controller bridges the system interconnect to the underlying medium."),
                rx.code_block("CPU / memory\n    │\nsystem interconnect\n    │\nstorage controller ──→ persistent medium", language="textile", width="100%")),
            _section("2", "Block I/O moves addressed chunks",
                rx.text("A block device presents data as numbered blocks. Software requests one or more blocks by address; the controller moves the corresponding data between storage and memory."),
                rx.code_block("logical blocks\n[0] [1] [2] [3] [4] ... [N]\n\nREAD block 3 → return block contents\nWRITE block 4 → store supplied block data", language="textile", width="100%"),
                _practice("What storage abstraction reads and writes addressed chunks rather than individual characters?", SystemIntegrationState.block_answer, SystemIntegrationState.set_block_answer, SystemIntegrationState.check_block, SystemIntegrationState.block_feedback, "storage abstraction")),
            _section("3", "Logical block addressing hides physical details",
                rx.text("Software normally works with logical block numbers rather than exact physical media locations. The controller translates the logical request into device-specific operations."),
                rx.code_block("software request: LBA 1200\n        ↓\nstorage controller translation\n        ↓\nphysical medium operation", language="textile", width="100%"),
                _practice("What address identifies a particular logical block on a storage device?", SystemIntegrationState.sector_answer, SystemIntegrationState.set_sector_answer, SystemIntegrationState.check_sector, SystemIntegrationState.sector_feedback, "block address")),
            _section("4", "Storage controllers expose commands, status and data movement",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Controller element"), rx.table.column_header_cell("Purpose"))), rx.table.body(
                    rx.table.row(rx.table.cell("Command"), rx.table.cell("Read, write, flush or another requested operation")),
                    rx.table.row(rx.table.cell("Address"), rx.table.cell("Logical block or command-specific location")),
                    rx.table.row(rx.table.cell("Length"), rx.table.cell("Number of blocks or bytes")),
                    rx.table.row(rx.table.cell("Status"), rx.table.cell("Busy, complete, error and device state")),
                    rx.table.row(rx.table.cell("Data pointer / descriptor"), rx.table.cell("Identifies the memory buffer"))), width="100%")),
            _section("5", "DMA is a natural partner for block storage",
                rx.text("Storage requests often involve far more data than a CPU should copy register-by-register. DMA moves a block directly between the device interface and RAM."),
                rx.code_block("READ : storage → controller → DMA/interconnect → RAM\nWRITE: RAM → DMA/interconnect → controller → storage", language="textile", width="100%"),
                rx.callout("The CPU creates and manages the request, while DMA handles repetitive data movement.", icon="info", color_scheme="blue")),
            _section("6", "Queues allow multiple storage requests",
                rx.text("A storage interface may accept several commands before earlier ones finish. Queues hold pending work and allow requests to be scheduled efficiently."),
                rx.code_block("request queue\n┌─────────────┐\n│ READ  LBA 8 │\n│ WRITE LBA 2 │\n│ READ LBA 90 │\n└──────┬──────┘\n       ↓\n controller / device", language="textile", width="100%"),
                _practice("What structure holds multiple pending storage requests so they can be scheduled efficiently?", SystemIntegrationState.queue_answer, SystemIntegrationState.set_queue_answer, SystemIntegrationState.check_queue, SystemIntegrationState.queue_feedback, "pending-request structure")),
            _section("7", "Completion needs a clear notification path",
                rx.text("A request may complete much later than it was issued. Interrupts commonly let the storage controller notify the CPU when a command finishes or fails."),
                rx.code_block("CPU submits request → continues other work\ncontroller/device executes operation\ncontroller sets completion status + IRQ\nISR/driver examines status and releases completed buffer", language="textile", width="100%")),
            _section("8", "Caching improves apparent storage performance",
                rx.text("Systems buffer recently used storage data in memory. Reads may be satisfied from a cache, and writes may be accumulated before reaching the physical medium."),
                rx.code_block("CPU\n │\nmemory/page cache\n │   cache hit → return quickly\n └── cache miss / dirty writeback → storage controller", language="textile", width="100%"),
                rx.callout("Cached data in volatile memory is not necessarily persistent until the system guarantees it has reached the required storage layer.", icon="triangle-alert", color_scheme="orange")),
            _section("9", "Flush and ordering protect persistence semantics",
                rx.text("A flush or barrier-style operation can require earlier writes to reach a defined persistence point before later work is considered safe."),
                rx.code_block("write A → write B → FLUSH → acknowledge\n                         ↑\n        earlier required writes reach persistence point", language="textile", width="100%")),
            _section("10", "Different storage media have different costs",
                rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Characteristic"), rx.table.column_header_cell("System consequence"))), rx.table.body(
                    rx.table.row(rx.table.cell("Long access latency"), rx.table.cell("Queues and caching become important")),
                    rx.table.row(rx.table.cell("High sequential bandwidth"), rx.table.cell("Large block and DMA transfers are efficient")),
                    rx.table.row(rx.table.cell("Write constraints"), rx.table.cell("Controller may buffer, reorder or translate writes")),
                    rx.table.row(rx.table.cell("Finite endurance"), rx.table.cell("Some technologies require wear-management strategies"))), width="100%")),
            _section("11", "Trace a complete block read",
                rx.code_block("1. software allocates a RAM buffer\n2. software creates READ request for LBA 1200, length 4 blocks\n3. driver/controller queues the command\n4. controller/device obtains requested persistent data\n5. DMA transfers the blocks into RAM\n6. controller records completion status\n7. controller interrupts CPU\n8. ISR/driver validates completion\n9. software consumes the buffer", language="textile", width="100%")),
            _section("12", "Path 10 integration checkpoint",
                rx.text("You can now follow data from CPU instructions through memory-mapped registers, interrupts, buses, DMA, timers and serial interfaces to persistent block storage."),
                rx.code_block("CPU\n ├─ MMIO → peripheral registers\n ├─ IRQ  ← event-driven devices\n ├─ bus arbitration / protocol\n ├─ DMA ⇄ RAM ⇄ high-volume peripherals\n ├─ timers → scheduled events\n ├─ UART / SPI / I²C → external devices\n └─ block I/O → persistent storage", language="textile", width="100%")),
            rx.card(rx.vstack(
                rx.badge("PATH 10 COMPLETE", color_scheme="green"),
                rx.heading("Computer Organisation & System Integration is complete.", size="5"),
                rx.text("CPU, memory, buses, DMA, interrupts, timers, peripheral protocols and storage now form one complete system-level picture.", color="#475569"),
                spacing="3", align="start"), width="100%"),
            spacing="6", align="stretch", max_width="1050px", width="100%", margin="0 auto", padding="32px 20px 64px"),
        min_height="100vh", background="#f8fafc")
