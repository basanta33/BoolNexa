"""BoolNexa Academy Path 06 — Lessons 1–8: memory foundations, RAM/ROM, SRAM/DRAM, organisation and cache memory."""
from __future__ import annotations
import reflex as rx
from .ui import app_header

PANEL={"border":"1px solid #e2e8f0","border_radius":"16px","padding":"22px","background":"white","width":"100%"}

class MemoryFoundationState(rx.State):
    capacity_answer:str=""
    capacity_feedback:str=""
    volatile_answer:str=""
    volatile_feedback:str=""
    address_answer:str=""
    address_feedback:str=""
    rom_answer:str=""
    rom_feedback:str=""
    sram_cell_answer:str=""
    sram_cell_feedback:str=""
    dram_refresh_answer:str=""
    dram_refresh_feedback:str=""
    density_answer:str=""
    density_feedback:str=""
    organisation_answer:str=""
    organisation_feedback:str=""
    expansion_answer:str=""
    expansion_feedback:str=""
    chip_select_answer:str=""
    chip_select_feedback:str=""
    cache_locality_answer:str=""
    cache_locality_feedback:str=""
    cache_hit_answer:str=""
    cache_hit_feedback:str=""
    cache_line_answer:str=""
    cache_line_feedback:str=""
    direct_map_answer:str=""
    direct_map_feedback:str=""
    tag_answer:str=""
    tag_feedback:str=""
    miss_answer:str=""
    miss_feedback:str=""
    page_answer:str=""
    page_feedback:str=""
    tlb_answer:str=""
    tlb_feedback:str=""
    page_fault_answer:str=""
    page_fault_feedback:str=""
    parity_answer:str=""
    parity_feedback:str=""
    ecc_answer:str=""
    ecc_feedback:str=""
    secded_answer:str=""
    secded_feedback:str=""
    hierarchy_answer:str=""
    hierarchy_feedback:str=""
    bandwidth_answer:str=""
    bandwidth_feedback:str=""
    final_answer:str=""
    final_feedback:str=""

    def set_address_answer(self, value: str) -> None:
        self.address_answer = value

    def set_bandwidth_answer(self, value: str) -> None:
        self.bandwidth_answer = value

    def set_cache_hit_answer(self, value: str) -> None:
        self.cache_hit_answer = value

    def set_cache_line_answer(self, value: str) -> None:
        self.cache_line_answer = value

    def set_cache_locality_answer(self, value: str) -> None:
        self.cache_locality_answer = value

    def set_capacity_answer(self, value: str) -> None:
        self.capacity_answer = value

    def set_chip_select_answer(self, value: str) -> None:
        self.chip_select_answer = value

    def set_density_answer(self, value: str) -> None:
        self.density_answer = value

    def set_direct_map_answer(self, value: str) -> None:
        self.direct_map_answer = value

    def set_dram_refresh_answer(self, value: str) -> None:
        self.dram_refresh_answer = value

    def set_ecc_answer(self, value: str) -> None:
        self.ecc_answer = value

    def set_expansion_answer(self, value: str) -> None:
        self.expansion_answer = value

    def set_final_answer(self, value: str) -> None:
        self.final_answer = value

    def set_hierarchy_answer(self, value: str) -> None:
        self.hierarchy_answer = value

    def set_miss_answer(self, value: str) -> None:
        self.miss_answer = value

    def set_organisation_answer(self, value: str) -> None:
        self.organisation_answer = value

    def set_page_answer(self, value: str) -> None:
        self.page_answer = value

    def set_page_fault_answer(self, value: str) -> None:
        self.page_fault_answer = value

    def set_parity_answer(self, value: str) -> None:
        self.parity_answer = value

    def set_rom_answer(self, value: str) -> None:
        self.rom_answer = value

    def set_secded_answer(self, value: str) -> None:
        self.secded_answer = value

    def set_sram_cell_answer(self, value: str) -> None:
        self.sram_cell_answer = value

    def set_tag_answer(self, value: str) -> None:
        self.tag_answer = value

    def set_tlb_answer(self, value: str) -> None:
        self.tlb_answer = value

    def set_volatile_answer(self, value: str) -> None:
        self.volatile_answer = value

    def check_capacity(self):
        v=self.capacity_answer.strip().lower().replace(" ","")
        self.capacity_feedback="Correct. 8 words × 4 bits = 32 bits of storage." if v in {"32","32bits","32bit"} else "Multiply the number of addressable words by the number of bits in each word."

    def check_volatile(self):
        v=self.volatile_answer.strip().lower().replace(" ","")
        self.volatile_feedback="Correct. RAM is normally volatile: its stored data is lost when power is removed." if v in {"ram","randomaccessmemory"} else "Which common read/write memory normally requires power to retain data?"

    def check_address(self):
        self.address_feedback="Correct. Four address bits select 2⁴ = 16 locations." if self.address_answer.strip()=="16" else "n address bits can distinguish 2ⁿ locations."

    def check_rom(self):
        v=self.rom_answer.strip().lower().replace(" ","")
        self.rom_feedback="Correct. ROM is suited to data or lookup contents intended to remain available without ordinary runtime writes." if v in {"rom","readonlymemory","read-onlymemory"} else "Think of memory normally read during operation rather than freely rewritten."

    def check_sram_cell(self):
        v=self.sram_cell_answer.strip().lower().replace(" ","").replace("-","")
        self.sram_cell_feedback=(
            "Correct. SRAM stores each bit in a bistable latch-like cell and does not need periodic refresh while power is maintained."
            if v in {"sram","staticram","staticrandomaccessmemory"}
            else "Which RAM technology uses a bistable cell rather than a charge-storage capacitor?"
        )

    def check_dram_refresh(self):
        v=self.dram_refresh_answer.strip().lower().replace(" ","").replace("-","")
        self.dram_refresh_feedback=(
            "Correct. DRAM cells store charge that leaks away, so stored rows must be refreshed periodically while the memory is powered."
            if v in {"refresh","periodicrefresh","memoryrefresh","dramrefresh"}
            else "Think about what must happen because charge in a DRAM cell gradually leaks."
        )

    def check_density(self):
        v=self.density_answer.strip().lower().replace(" ","").replace("-","")
        self.density_feedback=(
            "Correct. DRAM generally provides higher storage density and lower cost per bit, which is why it is widely used for large main-memory arrays."
            if v in {"dram","dynamicram","dynamicrandomaccessmemory"}
            else "Which technology normally uses the smaller one-transistor/one-capacitor style cell?"
        )

    def check_organisation(self):
        v=self.organisation_answer.strip().lower().replace(" ","")
        self.organisation_feedback=(
            "Correct. A 1K × 8 memory contains 1024 addressable words, with 8 bits in each word, for 8192 bits total."
            if v in {"8192","8192bits","8192bit","8kbits","8kbit"}
            else "Multiply 1024 addressable words by 8 bits per word."
        )

    def check_expansion(self):
        v=self.expansion_answer.strip().lower().replace(" ","")
        self.expansion_feedback=(
            "Correct. Two 1K × 8 devices can be placed in parallel on the same addresses to form a 1K × 16 memory."
            if v in {"2","two","2chips","2devices"}
            else "Width expansion keeps the same number of addresses and adds data bits in parallel."
        )

    def check_chip_select(self):
        v=self.chip_select_answer.strip().lower().replace(" ","").replace("-","")
        self.chip_select_feedback=(
            "Correct. A chip-select (or equivalent enable) signal ensures that only the intended memory device responds to a given address range."
            if v in {"chipselect","cs","chipenable","ce","enable"}
            else "Which control signal enables one memory device while leaving others inactive?"
        )

    def check_cache_locality(self):
        v=self.cache_locality_answer.strip().lower().replace(" ","").replace("-","")
        self.cache_locality_feedback=(
            "Correct. Temporal locality means recently used data or instructions are likely to be used again soon."
            if v in {"temporal","temporallocality"}
            else "Which form of locality describes reusing something that was accessed recently?"
        )

    def check_cache_hit(self):
        v=self.cache_hit_answer.strip().lower().replace(" ","").replace("-","")
        self.cache_hit_feedback=(
            "Correct. A cache hit means the requested block is already present in the cache and can be supplied from that level."
            if v in {"hit","cachehit"}
            else "What is the term for finding the requested block in the cache?"
        )

    def check_cache_line(self):
        v=self.cache_line_answer.strip().lower().replace(" ","").replace("-","")
        self.cache_line_feedback=(
            "Correct. A cache line (cache block) is the unit of data transferred and stored as one cache entry."
            if v in {"cacheline","line","cacheblock","block"}
            else "What do we call the fixed-size block stored in one cache entry?"
        )

    def check_direct_map(self):
        v=self.direct_map_answer.strip().lower().replace(" ","")
        self.direct_map_feedback=(
            "Correct. With 8 cache lines, memory block 13 maps to line 5 because 13 mod 8 = 5."
            if v in {"5","line5","cacheline5"}
            else "For a direct-mapped cache, compute memory-block number mod number of cache lines."
        )

    def check_tag(self):
        v=self.tag_answer.strip().lower().replace(" ","").replace("-","")
        self.tag_feedback=(
            "Correct. The tag distinguishes different memory blocks that map to the same cache line or set."
            if v in {"tag","cachetag"}
            else "Which address field identifies which candidate memory block is currently stored?"
        )

    def check_miss(self):
        v=self.miss_answer.strip().lower().replace(" ","").replace("-","")
        self.miss_feedback=(
            "Correct. A compulsory miss occurs when a block is referenced for the first time and has not yet been brought into the cache."
            if v in {"compulsory","compulsorymiss","cold","coldmiss"}
            else "Which miss type is associated with the first reference to a block?"
        )


    def check_page(self):
        v=self.page_answer.strip().lower().replace(" ","").replace("-","")
        self.page_feedback=("Correct. A page is a fixed-size block of virtual address space; a corresponding physical block is commonly called a frame."
            if v in {"page","virtualpage"} else "What is the fixed-size block of virtual address space called?")

    def check_tlb(self):
        v=self.tlb_answer.strip().lower().replace(" ","").replace("-","")
        self.tlb_feedback=("Correct. A TLB caches recently used address-translation information so many translations avoid a full page-table walk."
            if v in {"tlb","translationlookasidebuffer"} else "Which small translation cache stores recently used virtual-to-physical mappings?")

    def check_page_fault(self):
        v=self.page_fault_answer.strip().lower().replace(" ","").replace("-","")
        self.page_fault_feedback=("Correct. A page fault transfers control to the operating system when the required translation/page is not presently usable as requested."
            if v in {"pagefault","fault"} else "What event occurs when the processor cannot complete the requested virtual-memory access with the current mapping/state?")

    def check_parity(self):
        v=self.parity_answer.strip().lower().replace(" ","").replace("-","")
        self.parity_feedback=("Correct. A single parity bit can detect any odd number of bit flips in the protected group, but parity alone does not identify which bit changed."
            if v in {"detect","detection","errordetection","detecterror"} else "Does simple parity primarily detect or correct errors?")

    def check_ecc(self):
        v=self.ecc_answer.strip().lower().replace(" ","").replace("-","")
        self.ecc_feedback=("Correct. ECC stores redundant check information so the receiver can form a syndrome and, for supported error patterns, locate/correct errors."
            if v in {"syndrome","errorsyndrome"} else "What is the check result commonly called that helps identify an ECC error pattern?")

    def check_secded(self):
        v=self.secded_answer.strip().lower().replace(" ","").replace("-","")
        self.secded_feedback=("Correct. SECDED means single-error correction and double-error detection for the codeword model it is designed to protect."
            if v in {"secded","singleerrorcorrectiondoubleerrordetection"} else "Enter the common acronym for single-error correction, double-error detection.")


    def check_hierarchy(self):
        v=self.hierarchy_answer.strip().lower().replace(" ","")
        self.hierarchy_feedback=("Correct. Registers are normally the smallest and closest storage to the executing core." if v in {"register","registers"} else "Which storage level is normally closest to the executing CPU core?")

    def check_bandwidth(self):
        v=self.bandwidth_answer.strip().lower().replace(" ","")
        self.bandwidth_feedback=("Correct. Bandwidth describes the amount of data that can be transferred per unit time." if v in {"bandwidth","memorybandwidth"} else "What term describes how much data can be transferred per unit time?")

    def check_final(self):
        v=self.final_answer.strip().lower().replace(" ","").replace("-","")
        self.final_feedback=("Correct. Locality helps a hierarchy keep recently or nearby needed information in faster levels." if v in {"locality","localityofreference"} else "What principle explains why keeping recently or nearby used data in faster memory often works well?")

def sec(n,title,*items):
    return rx.box(rx.vstack(rx.hstack(rx.badge(n,color_scheme="blue"),rx.heading(title,size="5"),align="center"),*items,align="stretch",spacing="3"),**PANEL)

def table(headers,rows):
    return rx.table.root(rx.table.header(rx.table.row(*[rx.table.column_header_cell(x) for x in headers])),rx.table.body(*[rx.table.row(*[rx.table.cell(x) for x in r]) for r in rows]),width="100%",variant="surface")

def memory_foundations_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 01",color_scheme="purple"),
        rx.heading("Digital Memory Foundations",size="8"),
        rx.text("Digital systems need more than individual flip-flops. Memory organises many stored bits into addressable locations so processors, controllers and embedded systems can retain instructions, data and configuration.",size="4",color="#475569",line_height="1.6"),
        sec("1","From flip-flops to memory arrays",
            rx.text("A flip-flop stores one bit. A register stores a small word. A memory array stores many words and uses an address to select the location being accessed."),
            rx.code_block("Address ─► [ address decoder ] ─► selected word\n                                  │\nData in ───────────────────────► [ MEMORY ARRAY ] ─► Data out\n                                  ▲\n                             read/write control",language="markup")),
        sec("2","Words, width and capacity",
            table(("Term","Meaning"),(("Bit","One binary digit"),("Word","A group of bits accessed together"),("Word width","Bits per word"),("Depth","Number of addressable words"),("Capacity","Depth × word width"))),
            rx.text("A memory contains 8 words, each 4 bits wide. What is its total capacity in bits?"),
            rx.hstack(rx.input(value=MemoryFoundationState.capacity_answer,on_change=MemoryFoundationState.set_capacity_answer,placeholder="Capacity",max_width="160px"),rx.button("Check",on_click=MemoryFoundationState.check_capacity)),
            rx.cond(MemoryFoundationState.capacity_feedback!="",rx.callout(MemoryFoundationState.capacity_feedback,icon="calculator"),rx.box())),
        sec("3","Addressing",
            rx.text("With n binary address bits, up to 2ⁿ distinct locations can be selected."),
            rx.code_block("A3 A2 A1 A0 → 4 address bits → 16 possible addresses\n0000 → location 0\n...\n1111 → location 15",language="markup"),
            rx.text("How many locations can four address bits select?"),
            rx.hstack(rx.input(value=MemoryFoundationState.address_answer,on_change=MemoryFoundationState.set_address_answer,placeholder="Locations",max_width="160px"),rx.button("Check",on_click=MemoryFoundationState.check_address)),
            rx.cond(MemoryFoundationState.address_feedback!="",rx.callout(MemoryFoundationState.address_feedback,icon="brain"),rx.box())),
        sec("4","Volatile and non-volatile memory",
            table(("Class","Power removed","Examples / idea"),(("Volatile","Data normally lost","SRAM, DRAM"),("Non-volatile","Data retained","ROM, Flash, EEPROM"))),
            rx.text("Which common general-purpose read/write memory class is normally volatile?"),
            rx.hstack(rx.input(value=MemoryFoundationState.volatile_answer,on_change=MemoryFoundationState.set_volatile_answer,placeholder="Answer",max_width="180px"),rx.button("Check",on_click=MemoryFoundationState.check_volatile)),
            rx.cond(MemoryFoundationState.volatile_feedback!="",rx.callout(MemoryFoundationState.volatile_feedback,icon="brain"),rx.box())),
        sec("5","Memory hierarchy",
            rx.text("Real computers use several memory levels because no single technology simultaneously provides maximum speed, capacity, low cost and persistence."),
            rx.code_block("Fast / small / expensive per bit\n        Registers\n           ↓\n          Cache\n           ↓\n       Main memory\n           ↓\n   Persistent storage\nLarge / slower / cheaper per bit",language="markup"),
            rx.callout("This is a conceptual hierarchy. Exact technologies, sizes and latency relationships depend on the system.",icon="info")),
        sec("6","Memory is a system interface",
            rx.text("When analysing memory, always identify address width, data width, read/write controls, timing behaviour and what happens when no location is enabled."),
            rx.unordered_list(rx.list_item("How is a location selected?"),rx.list_item("When is a write accepted?"),rx.list_item("When does read data become valid?"),rx.list_item("Is the memory synchronous or asynchronous?"),rx.list_item("Does data survive loss of power?"))),
        rx.hstack(rx.link(rx.button("← Academy",variant="soft"),href="/academy"),rx.spacer(),rx.text("Path 06 · Lesson 1",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/ram-rom"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def ram_rom_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 02",color_scheme="purple"),
        rx.heading("RAM, ROM & Memory Operations",size="8"),
        rx.text("RAM and ROM represent different ways of using addressable storage. Understanding read and write operations is the foundation for later work with SRAM, DRAM, caches and processor memory systems.",size="4",color="#475569",line_height="1.6"),
        sec("1","RAM: read and write",
            rx.text("Random-access memory allows locations to be accessed by address without stepping through earlier locations. Typical RAM supports both reading and writing."),
            rx.code_block("WRITE:\nAddress + Data in + Write Enable → selected location updated\n\nREAD:\nAddress + Read control → selected location → Data out",language="markup"),
            rx.callout("“Random access” means direct address-based access; it does not mean the memory returns random data.",icon="lightbulb",color_scheme="amber")),
        sec("2","ROM: stored lookup information",
            rx.text("Read-only memory is used when stored contents are intended primarily for reading during normal operation. ROM-like structures can implement fixed tables, constants, microcode or lookup functions."),
            rx.text("Which memory type is naturally suited to a fixed lookup table that should not be freely rewritten during normal operation?"),
            rx.hstack(rx.input(value=MemoryFoundationState.rom_answer,on_change=MemoryFoundationState.set_rom_answer,placeholder="Memory type",max_width="180px"),rx.button("Check",on_click=MemoryFoundationState.check_rom)),
            rx.cond(MemoryFoundationState.rom_feedback!="",rx.callout(MemoryFoundationState.rom_feedback,icon="brain"),rx.box())),
        sec("3","ROM families",
            table(("Type","Programming idea"),(("Mask ROM","Programmed during manufacture"),("PROM","User programmable once"),("EPROM","Erasable with ultraviolet light and reprogrammable"),("EEPROM","Electrically erasable/reprogrammable"),("Flash","Electrically erased/programmed in larger blocks; widely used non-volatile storage"))),
            rx.callout("Modern usage often groups several non-volatile technologies under broad ROM-like roles, but their physical programming and erase behaviour differs.",icon="info")),
        sec("4","Read timing",
            rx.text("Memory outputs are not necessarily valid immediately after an address changes. Access time describes the delay before valid read data is available."),
            rx.code_block("Address changes ─────────────┐\n                              ├─ access time ─► valid Data out\nRead enabled ─────────────────┘",language="markup"),
            rx.text("Synchronous memories may instead define behaviour relative to clock edges, sometimes with one or more cycles of latency.")),
        sec("5","Write timing",
            rx.text("A write requires the intended address, input data and control signals to satisfy the memory's timing requirements. In synchronous RAM, a write is commonly accepted on a specified clock edge when write-enable is asserted."),
            rx.code_block("Before active edge: address/data/control become valid\n                       ↓\nCLK ──────────────────↑─────────────────\n                       │ write captured\nAfter edge: obey required hold behaviour",language="markup"),
            rx.callout("Exact setup, hold, enable polarity and read-during-write behaviour are device-specific. Consult the memory specification or HDL primitive documentation.",icon="triangle-alert",color_scheme="amber")),
        sec("6","Memory versus registers",
            table(("Feature","Register bank","Memory array"),(("Typical size","Small","Potentially large"),("Selection","Explicit control / register address","Address decoder / memory interface"),("Use","Immediate datapath state","Bulk instructions/data"),("Implementation","Flip-flops commonly","Technology-dependent cells/arrays"))),
            rx.text("The distinction is architectural as well as physical: both store bits, but they are organised and accessed differently.")),
        rx.hstack(rx.link(rx.button("← Memory foundations",variant="soft"),href="/academy/unit-6/memory-foundations"),rx.spacer(),rx.text("Path 06 · Lesson 2",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/sram-dram"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")


def sram_dram_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 03",color_scheme="purple"),
        rx.heading("SRAM vs DRAM",size="8"),
        rx.text("SRAM and DRAM are both volatile random-access memories, but they store a bit in different physical ways. That difference affects refresh, density, cost, latency and the roles each technology commonly fills in a computer system.",size="4",color="#475569",line_height="1.6"),
        sec("1","Two ways to hold a volatile bit",
            table(("Property","SRAM","DRAM"),(
                ("Storage principle","Bistable latch-like cell","Charge stored in a capacitor-like cell"),
                ("Refresh while powered","No periodic refresh required","Periodic refresh required"),
                ("Typical cell complexity","More transistors per bit","Fewer active devices per bit"),
                ("Density / cost per bit","Generally lower density / higher cost","Generally higher density / lower cost"),
                ("Common role","Caches, small fast memories","Large main-memory arrays")
            )),
            rx.callout("Both SRAM and DRAM are normally volatile: removing power loses the stored information. 'Static' does not mean non-volatile.",icon="triangle-alert",color_scheme="amber")),
        sec("2","Inside an SRAM cell",
            rx.text("An SRAM bit is held by a bistable circuit. As long as power remains valid and the cell is not deliberately written, its logical state can persist without a periodic refresh operation."),
            rx.code_block("        cross-coupled storage\n      ┌───────────────────┐\nBL ───┤ access ─ [state] ├─── BL̅\n      └───────────────────┘\n              ▲\n          word line",language="markup"),
            rx.text("Which RAM technology uses a bistable latch-like storage cell?"),
            rx.hstack(rx.input(value=MemoryFoundationState.sram_cell_answer,on_change=MemoryFoundationState.set_sram_cell_answer,placeholder="Memory type",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_sram_cell)),
            rx.cond(MemoryFoundationState.sram_cell_feedback!="",rx.callout(MemoryFoundationState.sram_cell_feedback,icon="brain"),rx.box())),
        sec("3","Inside a DRAM cell",
            rx.text("A simplified DRAM cell stores information as charge associated with a tiny capacitor and an access transistor. Because that charge leaks with time, the memory controller must restore stored information through refresh operations."),
            rx.code_block("bit line\n   │\n [access transistor] ◄── word line\n   │\n [storage capacitor]\n   │\n reference",language="markup"),
            rx.text("What maintenance operation is required because stored DRAM charge leaks?"),
            rx.hstack(rx.input(value=MemoryFoundationState.dram_refresh_answer,on_change=MemoryFoundationState.set_dram_refresh_answer,placeholder="Operation",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_dram_refresh)),
            rx.cond(MemoryFoundationState.dram_refresh_feedback!="",rx.callout(MemoryFoundationState.dram_refresh_feedback,icon="brain"),rx.box())),
        sec("4","Why DRAM reads are different",
            rx.text("A DRAM read senses a very small stored charge through a bit line and sense amplifier. In common DRAM architectures the sensing process is effectively destructive to the original cell charge, so the sensed value is restored as part of the access process."),
            rx.code_block("row activate → cell shares charge with bit line\n             → sense amplifier resolves 0 or 1\n             → value is restored into the cell",language="markup"),
            rx.callout("Modern DRAM devices hide much of this analogue detail behind commands, banks, rows, columns and timing rules. Exact command sequences and timings are device-specific.",icon="info")),
        sec("5","Speed, density and system role",
            rx.text("SRAM avoids refresh and is designed for very fast access, but its larger cell consumes more silicon area per stored bit. DRAM uses a much denser cell, making large capacities economical, but requires refresh and more elaborate access management."),
            table(("Design goal","Often favours"),(
                ("Very low latency, modest capacity","SRAM"),
                ("Large capacity at lower cost per bit","DRAM"),
                ("On-chip processor cache","SRAM"),
                ("System main memory","DRAM")
            )),
            rx.text("Which technology generally offers higher storage density?"),
            rx.hstack(rx.input(value=MemoryFoundationState.density_answer,on_change=MemoryFoundationState.set_density_answer,placeholder="SRAM or DRAM",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_density)),
            rx.cond(MemoryFoundationState.density_feedback!="",rx.callout(MemoryFoundationState.density_feedback,icon="brain"),rx.box())),
        sec("6","Do not reduce the comparison to one number",
            rx.unordered_list(
                rx.list_item("Latency depends on the exact SRAM/DRAM device, interface, clocking and access pattern."),
                rx.list_item("Power includes active, standby and refresh-related components."),
                rx.list_item("Embedded memories can use specialised implementations that do not match a desktop-memory example."),
                rx.list_item("Caches also depend on tags, replacement policy and hierarchy—not only the storage cell.")),
            rx.callout("Use SRAM-versus-DRAM as a technology trade-off model, then consult the actual memory specification for implementation numbers.",icon="lightbulb",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← RAM & ROM",variant="soft"),href="/academy/unit-6/ram-rom"),rx.spacer(),rx.text("Path 06 · Lesson 3",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/memory-organisation"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")


def memory_organisation_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 04",color_scheme="purple"),
        rx.heading("Memory Addressing, Organisation & Expansion",size="8"),
        rx.text("A memory specification tells you how many words exist, how wide each word is and how the system selects them. Once those ideas are clear, multiple memory devices can be combined to increase word width, address depth or both.",size="4",color="#475569",line_height="1.6"),
        sec("1","Read memory notation correctly",
            rx.text("Memory is often written as depth × width. For example, 1K × 8 means 1024 addressable words with 8 data bits in each word."),
            rx.code_block("1K × 8\n│    └─ 8 data bits per selected word\n└────── 1024 addressable words\n\nTotal capacity = 1024 × 8 = 8192 bits",language="markup"),
            rx.text("What is the total capacity of a 1K × 8 memory in bits?"),
            rx.hstack(rx.input(value=MemoryFoundationState.organisation_answer,on_change=MemoryFoundationState.set_organisation_answer,placeholder="Capacity",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_organisation)),
            rx.cond(MemoryFoundationState.organisation_feedback!="",rx.callout(MemoryFoundationState.organisation_feedback,icon="calculator"),rx.box())),
        sec("2","Address lines determine depth",
            rx.text("If every binary address code is used, n address inputs identify 2ⁿ locations. A 1K-deep memory therefore needs 10 address bits because 2¹⁰ = 1024."),
            table(("Address bits","Maximum distinct addresses"),(("4","16"),("8","256"),("10","1024 (1K)"),("12","4096 (4K)"),("16","65,536 (64K)"))),
            rx.callout("K in conventional memory organisation is commonly used as 1024 (= 2¹⁰) locations. Product marketing for storage capacity can use different decimal/binary conventions, so read the specification carefully.",icon="info")),
        sec("3","Width expansion: more bits per word",
            rx.text("To make a wider word, memory devices can share the same address and control signals while each device contributes a different slice of the data bus."),
            rx.code_block("Goal: 1K × 16 from 1K × 8 devices\n\nA[9:0] ─────────┬────────► chip 0: 1K × 8 ─► D[7:0]\n                └────────► chip 1: 1K × 8 ─► D[15:8]\nCS / control ───┴────────► both chips\n\nDepth stays 1K; width becomes 16 bits.",language="markup"),
            rx.text("How many 1K × 8 devices are required to build 1K × 16?"),
            rx.hstack(rx.input(value=MemoryFoundationState.expansion_answer,on_change=MemoryFoundationState.set_expansion_answer,placeholder="Devices",max_width="170px"),rx.button("Check",on_click=MemoryFoundationState.check_expansion)),
            rx.cond(MemoryFoundationState.expansion_feedback!="",rx.callout(MemoryFoundationState.expansion_feedback,icon="brain"),rx.box())),
        sec("4","Depth expansion: more addresses",
            rx.text("To increase depth, lower-order address bits can go to every memory device while higher-order address bits are decoded to enable only one device or bank for a particular address range."),
            rx.code_block("Goal: 2K × 8 from two 1K × 8 devices\n\nA[9:0] ─────────────► address inputs of both chips\nA10 ─► select logic ─► CS0 / CS1\n\nA10=0 → lower 1K addresses → chip 0\nA10=1 → upper 1K addresses → chip 1",language="markup"),
            rx.text("Which signal normally ensures that only the intended memory device responds?"),
            rx.hstack(rx.input(value=MemoryFoundationState.chip_select_answer,on_change=MemoryFoundationState.set_chip_select_answer,placeholder="Signal",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_chip_select)),
            rx.cond(MemoryFoundationState.chip_select_feedback!="",rx.callout(MemoryFoundationState.chip_select_feedback,icon="brain"),rx.box())),
        sec("5","Address maps and decoding",
            rx.text("A system address map assigns non-overlapping address ranges to memories and peripherals. Decode logic examines selected address bits and generates enable signals for the appropriate target."),
            table(("Example range","Selected target"),(("0x0000–0x03FF","Memory bank 0 (1K locations)"),("0x0400–0x07FF","Memory bank 1 (1K locations)"),("Other ranges","Other memory/peripherals or unmapped"))),
            rx.callout("The hexadecimal ranges above are an educational example. Real systems define address maps according to processor width, buses, alignment, peripherals and memory-controller architecture.",icon="info")),
        sec("6","Expansion design checklist",
            rx.unordered_list(
                rx.list_item("Required total depth: how many addressable words?"),
                rx.list_item("Required word width: how many data bits per access?"),
                rx.list_item("Available chip organisation: depth × width?"),
                rx.list_item("Width expansion factor = required width ÷ chip width."),
                rx.list_item("Depth expansion factor = required depth ÷ chip depth."),
                rx.list_item("Decode high-order address bits for mutually exclusive chip selects."),
                rx.list_item("Check loading, enable polarity, bus contention and timing in the actual device specification.")),
            rx.callout("When both depth and width must grow, arrange devices as a bank matrix: devices in parallel increase width; selectable banks increase depth.",icon="lightbulb",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← SRAM vs DRAM",variant="soft"),href="/academy/unit-6/sram-dram"),rx.spacer(),rx.text("Path 06 · Lesson 4",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/cache-memory"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")


def cache_memory_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 05",color_scheme="purple"),
        rx.heading("Cache Memory & Locality",size="8"),
        rx.text("A cache is a small, fast memory level that keeps copies of recently or nearby used blocks so the processor can avoid many slower accesses to the next memory level.",size="4",color="#475569",line_height="1.6"),
        sec("1","Why a cache helps",
            rx.text("Processors can request data much faster than large memory systems can always deliver it. A cache reduces average access time when many requests can be satisfied from a faster nearby level."),
            rx.code_block("""CPU request
    │
    ▼
[ CACHE ] ── hit ──► data returned quickly
    │
   miss
    ▼
[ next memory level ] ─► fetch block ─► fill cache""",language="markup"),
            rx.callout("A cache does not make every access fast. Its benefit depends on hit rate, hit time and miss penalty.",icon="info")),
        sec("2","Locality: the reason caches work",
            table(("Locality","Idea","Example"),(("Temporal locality","Recently used items may be used again soon","Loop variable or repeatedly executed instruction"),("Spatial locality","Nearby addresses may be used soon","Sequential instructions or array elements"))),
            rx.text("Which locality describes reusing an item that was accessed recently?"),
            rx.hstack(rx.input(value=MemoryFoundationState.cache_locality_answer,on_change=MemoryFoundationState.set_cache_locality_answer,placeholder="Locality type",max_width="210px"),rx.button("Check",on_click=MemoryFoundationState.check_cache_locality)),
            rx.cond(MemoryFoundationState.cache_locality_feedback!="",rx.callout(MemoryFoundationState.cache_locality_feedback,icon="brain"),rx.box())),
        sec("3","Cache lines and block transfers",
            rx.text("Caches normally move data in fixed-size blocks rather than one isolated byte or word at a time. A stored block is commonly called a cache line."),
            rx.code_block("""Main memory block
+------+------+------+------+
| word | word | word | word |  ──► one cache line
+------+------+------+------+

The block size is a design parameter; real processors use architecture-specific values.""",language="markup"),
            rx.text("What is the common name for the fixed-size block held in one cache entry?"),
            rx.hstack(rx.input(value=MemoryFoundationState.cache_line_answer,on_change=MemoryFoundationState.set_cache_line_answer,placeholder="Answer",max_width="200px"),rx.button("Check",on_click=MemoryFoundationState.check_cache_line)),
            rx.cond(MemoryFoundationState.cache_line_feedback!="",rx.callout(MemoryFoundationState.cache_line_feedback,icon="brain"),rx.box())),
        sec("4","Hits and misses",
            table(("Event","Meaning","Action"),(("Cache hit","Requested block is present","Return data from cache"),("Cache miss","Requested block is absent","Obtain block from next level, then continue"))),
            rx.text("What do we call an access when the requested block is already present in the cache?"),
            rx.hstack(rx.input(value=MemoryFoundationState.cache_hit_answer,on_change=MemoryFoundationState.set_cache_hit_answer,placeholder="Hit or miss?",max_width="180px"),rx.button("Check",on_click=MemoryFoundationState.check_cache_hit)),
            rx.cond(MemoryFoundationState.cache_hit_feedback!="",rx.callout(MemoryFoundationState.cache_hit_feedback,icon="brain"),rx.box())),
        sec("5","Average memory access time",
            rx.text("A simple two-level model combines the fast hit path with the extra cost of misses."),
            rx.code_block("""AMAT = hit time + (miss rate × miss penalty)

Example:
hit time = 1 ns
miss rate = 5% = 0.05
miss penalty = 40 ns
AMAT = 1 + (0.05 × 40) = 3 ns""",language="markup"),
            rx.callout("This formula is a simplified educational model. Multi-level caches, overlapping operations, memory-level parallelism and hardware prefetching can make real performance analysis more involved.",icon="triangle-alert",color_scheme="amber")),
        sec("6","Where SRAM fits",
            rx.text("On-chip caches are commonly built from SRAM-like storage because fast access is more important than maximum density. Large main memory is commonly DRAM because density and cost per bit matter more at that level."),
            table(("Level","Typical goal","Common storage technology"),(("Registers","Immediate operand/state access","Flip-flops / register structures"),("Cache","Very fast reusable working set","SRAM-like arrays"),("Main memory","Large active program/data capacity","DRAM"))),
            rx.callout("Exact cache sizes, levels, associativity, latency and implementation differ by processor. Use the processor documentation for real numbers.",icon="info")),
        rx.hstack(rx.link(rx.button("← Memory organisation",variant="soft"),href="/academy/unit-6/memory-organisation"),rx.spacer(),rx.text("Path 06 · Lesson 5",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/cache-mapping"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")

def cache_mapping_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 06",color_scheme="purple"),
        rx.heading("Cache Mapping, Hits & Misses",size="8"),
        rx.text("Once data is divided into blocks, a cache needs rules that determine where each memory block may be stored and how the hardware recognises whether the requested block is present.",size="4",color="#475569",line_height="1.6"),
        sec("1","The cache-address idea",
            rx.text("A cache lookup commonly interprets address bits as a block offset plus placement information and a tag. The exact split depends on cache size, line size and associativity."),
            rx.code_block("""address
+----------------+-----------+--------------+
|      TAG       | INDEX/SET | BLOCK OFFSET |
+----------------+-----------+--------------+
       │               │            │
 identifies block   chooses place   byte/word inside line""",language="markup"),
            rx.callout("Do not assume fixed bit positions from this diagram. Address-field widths are calculated from the actual cache organisation.",icon="info")),
        sec("2","Direct-mapped cache",
            rx.text("In a direct-mapped cache, each memory block has exactly one permitted cache line."),
            rx.code_block("""cache line = memory block number mod number of cache lines

8-line cache:
block 0  → line 0
block 8  → line 0
block 13 → line 5   because 13 mod 8 = 5""",language="markup"),
            rx.text("In an 8-line direct-mapped cache, which line receives memory block 13?"),
            rx.hstack(rx.input(value=MemoryFoundationState.direct_map_answer,on_change=MemoryFoundationState.set_direct_map_answer,placeholder="Line",max_width="160px"),rx.button("Check",on_click=MemoryFoundationState.check_direct_map)),
            rx.cond(MemoryFoundationState.direct_map_feedback!="",rx.callout(MemoryFoundationState.direct_map_feedback,icon="calculator"),rx.box())),
        sec("3","Why the tag is necessary",
            rx.text("Many different memory blocks can map to the same line or set. The stored tag records which candidate block currently occupies that location."),
            rx.code_block("""Requested address: tag = T2, index = 3
                         │          │
                         │          └─► read cache line/set 3
                         └────────────► compare with stored tag

valid = 1 and tags match → HIT
otherwise                → MISS""",language="markup"),
            rx.text("Which address field distinguishes different memory blocks that map to the same cache location?"),
            rx.hstack(rx.input(value=MemoryFoundationState.tag_answer,on_change=MemoryFoundationState.set_tag_answer,placeholder="Field",max_width="170px"),rx.button("Check",on_click=MemoryFoundationState.check_tag)),
            rx.cond(MemoryFoundationState.tag_feedback!="",rx.callout(MemoryFoundationState.tag_feedback,icon="brain"),rx.box())),
        sec("4","Associative alternatives",
            table(("Mapping","Possible locations for a block","Trade-off"),(("Direct mapped","One line","Simple and fast, but more placement conflicts"),("Set associative","Any way inside one selected set","Balances flexibility and lookup hardware"),("Fully associative","Any cache line","Maximum placement flexibility, more comparison hardware"))),
            rx.text("A 4-way set-associative cache gives each selected set four candidate lines (ways). Tag comparisons determine whether one of those ways contains the requested block."),
            rx.callout("Associativity reduces some conflict misses, but it can increase lookup complexity, metadata and implementation cost.",icon="lightbulb",color_scheme="amber")),
        sec("5","Three classic miss categories",
            table(("Miss type","Cause"),(("Compulsory (cold)","First reference to a block"),("Capacity","Working set exceeds usable cache capacity"),("Conflict","Placement restrictions make blocks evict one another even though other cache space may exist"))),
            rx.text("What is the traditional name for a miss caused by the very first access to a block?"),
            rx.hstack(rx.input(value=MemoryFoundationState.miss_answer,on_change=MemoryFoundationState.set_miss_answer,placeholder="Miss type",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_miss)),
            rx.cond(MemoryFoundationState.miss_feedback!="",rx.callout(MemoryFoundationState.miss_feedback,icon="brain"),rx.box())),
        sec("6","Replacement and write policies",
            rx.text("When a set has several candidate ways and all are occupied, a replacement policy chooses which line to evict. Common teaching examples include LRU-like, FIFO and random policies, although real hardware may use approximations or other strategies."),
            table(("Write policy","Core idea"),(("Write-through","Update cache and next memory level as part of the write path"),("Write-back","Update cache first; modified (dirty) data is written to the next level when required"))),
            rx.callout("Replacement rules, allocation on a write miss, coherence behaviour and write-buffer details are architecture-specific. Consult the target processor documentation before predicting exact behaviour.",icon="triangle-alert",color_scheme="amber")),
        rx.hstack(rx.link(rx.button("← Cache memory",variant="soft"),href="/academy/unit-6/cache-memory"),rx.spacer(),rx.text("Path 06 · Lesson 6",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/virtual-memory"),width="100%",padding_y="16px"),
        spacing="5",align="stretch",max_width="1100px",width="100%",margin="0 auto",padding=rx.breakpoints(initial="20px",md="36px")),min_height="100vh",background="#f8fafc")


def virtual_memory_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 07",color_scheme="purple"),
        rx.heading("Virtual Memory & Address Translation",size="8"),
        rx.text("Virtual memory gives software an address space that is translated to physical memory locations. The translation machinery supports protection, relocation and controlled sharing while letting the operating system manage physical memory.",size="4",color="#475569",line_height="1.6"),
        sec("1","Virtual and physical addresses",
            rx.text("A processor-generated virtual address is translated before the memory system uses the corresponding physical address. The exact hardware and operating-system design varies by architecture."),
            rx.code_block("""CPU virtual address
        │
        ▼
[ translation machinery ] ──► physical address ──► cache / memory
        ▲
  page-table information""",language="markup"),
            rx.callout("Virtual memory is not simply 'extra RAM'. It is an address-translation and memory-management mechanism; secondary storage may participate when pages are not resident.",icon="info")),
        sec("2","Pages, frames and offsets",
            rx.text("Virtual address spaces are commonly divided into fixed-size pages. Physical memory is divided into page-sized frames. Translation changes the page-number portion while preserving the offset within the page."),
            rx.code_block("""Virtual address:  [ virtual page number | page offset ]
                                  │
                                  ▼ translate
Physical address: [ physical frame number | page offset ]""",language="markup"),
            rx.text("What is a fixed-size block of virtual address space called?"),
            rx.hstack(rx.input(value=MemoryFoundationState.page_answer,on_change=MemoryFoundationState.set_page_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_page)),
            rx.cond(MemoryFoundationState.page_feedback!="",rx.callout(MemoryFoundationState.page_feedback,icon="brain"),rx.box())),
        sec("3","Page tables",
            rx.text("A page table records translation and status information for virtual pages. Entries can include a physical-frame number plus control information such as valid/present, access permission, accessed/reference and modified/dirty state, depending on the architecture."),
            table(("Virtual page","Example state","Meaning"),(("VP 0","present → frame 5","Translation available"),("VP 1","not present","OS action may be required"),("VP 2","read-only → frame 9","Writes are not permitted by that mapping"))),
            rx.callout("Page-table formats and flag names are architecture-specific. Treat this as a conceptual model, not a fixed hardware layout.",icon="triangle-alert",color_scheme="amber")),
        sec("4","The TLB",
            rx.text("A Translation Lookaside Buffer (TLB) is a small cache of recently used translation information. A TLB hit can avoid consulting the page-table hierarchy for that translation."),
            rx.code_block("""virtual page number ─► [ TLB ]
                         │ hit → frame number
                         └ miss → page-table lookup / walk""",language="markup"),
            rx.text("What is the small cache of recently used translations called?"),
            rx.hstack(rx.input(value=MemoryFoundationState.tlb_answer,on_change=MemoryFoundationState.set_tlb_answer,placeholder="Acronym or name",max_width="230px"),rx.button("Check",on_click=MemoryFoundationState.check_tlb)),
            rx.cond(MemoryFoundationState.tlb_feedback!="",rx.callout(MemoryFoundationState.tlb_feedback,icon="brain"),rx.box())),
        sec("5","Page faults",
            rx.text("If an access cannot proceed because the required page is not resident or the mapping requires operating-system handling, the processor raises a page-fault exception. The OS examines the cause and may reject the access, establish a mapping, or bring data into memory."),
            rx.text("What is this operating-system-handled event commonly called?"),
            rx.hstack(rx.input(value=MemoryFoundationState.page_fault_answer,on_change=MemoryFoundationState.set_page_fault_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_page_fault)),
            rx.cond(MemoryFoundationState.page_fault_feedback!="",rx.callout(MemoryFoundationState.page_fault_feedback,icon="brain"),rx.box())),
        sec("6","Translation journey",
            rx.code_block("""1. CPU produces virtual address
2. Translation information is sought (often TLB first)
3. On a TLB miss, page-table information is obtained
4. Valid translation yields a physical address
5. Exceptional conditions transfer control for OS handling""",language="markup"),
            rx.callout("Real processors may use multi-level page tables, multiple TLBs, huge pages, nested translation and other optimisations. The lesson focuses on the invariant concepts.",icon="info")),
        rx.hstack(rx.link(rx.button("← Cache mapping",variant="soft"),href="/academy/unit-6/cache-mapping"),rx.spacer(),rx.text("Path 06 · Lesson 7",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/memory-reliability"),width="100%",padding_y="16px"),
        width="min(1180px, 94vw)",margin="0 auto",padding_y="28px",spacing="5",align="stretch"))


def memory_reliability_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 08",color_scheme="purple"),
        rx.heading("Memory Reliability, Parity & ECC",size="8"),
        rx.text("Stored bits can be corrupted by electrical noise, radiation-induced events, device faults or signal-integrity problems. Memory systems can add redundant check bits to detect — and with suitable codes, correct — selected error patterns.",size="4",color="#475569",line_height="1.6"),
        sec("1","Why redundancy helps",
            rx.text("Error-control coding stores extra information derived from the data. When data is read, the system recomputes or checks that information. A mismatch can reveal that the protected codeword has changed."),
            rx.code_block("""data bits ─► [ encoder ] ─► data + check bits ─► memory
                                                │
read codeword ───────────────► [ checker/decoder ] ─► status / corrected data""",language="markup")),
        sec("2","Simple parity",
            rx.text("Even parity chooses a parity bit so the total number of 1s in the protected group is even; odd parity does the opposite. Any odd number of flipped bits changes the parity relationship and is detectable."),
            table(("Data","Even-parity bit","Protected word"),(("1011","1","10111"),("1001","0","10010"))),
            rx.callout("Simple parity cannot correct an error by itself, and an even number of bit flips can leave the parity relationship unchanged.",icon="triangle-alert",color_scheme="amber"),
            rx.text("Does simple parity primarily detect or correct errors?"),
            rx.hstack(rx.input(value=MemoryFoundationState.parity_answer,on_change=MemoryFoundationState.set_parity_answer,placeholder="Detect / correct",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_parity)),
            rx.cond(MemoryFoundationState.parity_feedback!="",rx.callout(MemoryFoundationState.parity_feedback,icon="brain"),rx.box())),
        sec("3","Hamming-style ECC idea",
            rx.text("Error-correcting codes use multiple check relationships. The pattern of failed checks forms a syndrome. For a suitable Hamming code, a non-zero syndrome can identify the position of a single-bit error so it can be corrected."),
            rx.code_block("""received codeword
      │
      ▼
recompute parity checks
      │
      ▼
 syndrome ──► no indicated error / locate supported error pattern""",language="markup"),
            rx.text("What is the check-result pattern commonly called?"),
            rx.hstack(rx.input(value=MemoryFoundationState.ecc_answer,on_change=MemoryFoundationState.set_ecc_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_ecc)),
            rx.cond(MemoryFoundationState.ecc_feedback!="",rx.callout(MemoryFoundationState.ecc_feedback,icon="brain"),rx.box())),
        sec("4","SECDED",
            rx.text("A common memory-protection arrangement extends single-error-correcting Hamming-style coding with an additional overall parity relationship. This is commonly described as SECDED: single-error correction, double-error detection."),
            rx.text("Enter the acronym for single-error correction, double-error detection."),
            rx.hstack(rx.input(value=MemoryFoundationState.secded_answer,on_change=MemoryFoundationState.set_secded_answer,placeholder="Acronym",max_width="170px"),rx.button("Check",on_click=MemoryFoundationState.check_secded)),
            rx.cond(MemoryFoundationState.secded_feedback!="",rx.callout(MemoryFoundationState.secded_feedback,icon="brain"),rx.box()),
            rx.callout("SECDED guarantees are defined for the codeword/error model of the code. More complex multi-bit faults are not automatically correctable and may be misclassified by schemes not designed for them.",icon="info")),
        sec("5","Reliability is a system property",
            table(("Technique","Purpose"),(("Parity","Low-cost detection of odd-count bit errors in a protected group"),("ECC","Use redundant check bits to detect/correct supported error patterns"),("Scrubbing","Periodically read/check and, when possible, rewrite corrected data"),("Redundancy","Keep additional copies/components so a fault need not immediately lose information"))),
            rx.text("Reliable systems combine coding with diagnostics, physical design, testing, monitoring and recovery policy. ECC is one layer rather than a guarantee that memory can never fail.")),
        sec("6","Connect the memory hierarchy",
            rx.code_block("""registers → caches → main memory → secondary storage
     fast        larger / slower

Across the hierarchy:
addressing + translation + protection + reliability
work together to deliver usable stored information.""",language="markup"),
            rx.callout("The exact protection used in processor caches, DRAM modules, controllers and storage devices varies by product. Consult device documentation when a specific correction capability matters.",icon="info")),
        rx.hstack(rx.link(rx.button("← Virtual memory",variant="soft"),href="/academy/unit-6/virtual-memory"),rx.spacer(),rx.text("Path 06 · Lesson 8",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Next lesson →",variant="soft"),href="/academy/unit-6/memory-hierarchy-performance"),width="100%",padding_y="16px"),
        width="min(1180px, 94vw)",margin="0 auto",padding_y="28px",spacing="5",align="stretch"))


def memory_hierarchy_performance_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 09",color_scheme="purple"),
        rx.heading("Memory Hierarchy & Performance",size="8"),
        rx.text("Computer memory is organised as a hierarchy because no single technology simultaneously gives minimum latency, maximum capacity and minimum cost. Fast small levels work with larger slower levels to reduce the average cost of accesses.",size="4",color="#475569",line_height="1.6"),
        sec("1","The hierarchy",
            rx.code_block("""fast / small / expensive per bit
        registers
           ↓
        L1 cache
           ↓
        L2 / L3 cache
           ↓
        main memory
           ↓
        secondary storage
large / persistent / slower""",language="markup"),
            rx.text("Which level is normally closest to the executing CPU core?"),
            rx.hstack(rx.input(value=MemoryFoundationState.hierarchy_answer,on_change=MemoryFoundationState.set_hierarchy_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_hierarchy)),
            rx.cond(MemoryFoundationState.hierarchy_feedback!="",rx.callout(MemoryFoundationState.hierarchy_feedback,icon="brain"),rx.box())),
        sec("2","Latency and bandwidth",
            rx.text("Latency is the delay associated with completing an access or operation. Bandwidth is a rate: how much data can be transferred in a unit of time. A system can have high bandwidth while an individual access still has significant latency."),
            table(("Metric","Question it answers"),(("Latency","How long does this access take?"),("Bandwidth","How much data can move per unit time?"))),
            rx.text("What term describes data transferred per unit time?"),
            rx.hstack(rx.input(value=MemoryFoundationState.bandwidth_answer,on_change=MemoryFoundationState.set_bandwidth_answer,placeholder="Answer",max_width="190px"),rx.button("Check",on_click=MemoryFoundationState.check_bandwidth)),
            rx.cond(MemoryFoundationState.bandwidth_feedback!="",rx.callout(MemoryFoundationState.bandwidth_feedback,icon="brain"),rx.box())),
        sec("3","Average memory access time",
            rx.text("A simple cache model separates common hits from less common misses. The average access cost depends on hit time, miss frequency and the additional miss penalty."),
            rx.code_block("AMAT = hit time + miss rate × miss penalty",language="markup"),
            rx.callout("This is a teaching model. Real systems may overlap accesses, have several cache levels and distinguish multiple kinds of misses and penalties.",icon="info")),
        sec("4","Locality makes hierarchy useful",
            rx.text("Temporal locality means recently used information is likely to be useful again. Spatial locality means nearby addresses are often accessed close together in time. Caches exploit both patterns by retaining blocks of data."),
            table(("Pattern","Example"),(("Temporal","Repeatedly updating the same loop variable"),("Spatial","Reading consecutive array elements")))),
        sec("5","Performance trade-offs",
            rx.text("Larger caches can retain more working data but may have different latency, energy and implementation costs. Larger transfer blocks can exploit spatial locality but also consume bandwidth and cache capacity. There is no universally best configuration."),
            rx.callout("Performance claims are workload- and implementation-dependent. Measurements must specify the processor, memory configuration, workload and metric.",icon="triangle-alert",color_scheme="amber")),
        sec("6","Follow an access",
            rx.code_block("""CPU request
   │
   ├─ cache hit ─► data returned from fast level
   │
   └─ cache miss ─► search/fetch from lower level
                         │
                         └─ fill cache, then continue""",language="markup")),
        rx.hstack(rx.link(rx.button("← Reliability",variant="soft"),href="/academy/unit-6/memory-reliability"),rx.spacer(),rx.text("Path 06 · Lesson 9",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Final lesson →",variant="soft"),href="/academy/unit-6/memory-system-integration"),width="100%",padding_y="16px"),
        width="min(1180px, 94vw)",margin="0 auto",padding_y="28px",spacing="5",align="stretch"))


def memory_system_integration_lesson():
    return rx.box(app_header("academy"),rx.vstack(
        rx.badge("PATH 06 · LESSON 10 · PATH FINALE",color_scheme="green"),
        rx.heading("Memory System Integration & Design Challenge",size="8"),
        rx.text("Bring the whole path together: storage cells, RAM and ROM, organisation, cache, virtual memory, reliability and performance all cooperate to turn addresses into dependable stored information.",size="4",color="#475569",line_height="1.6"),
        sec("1","The complete memory journey",
            rx.code_block("""program virtual address
        │
        ▼
 translation / protection (TLB + page tables)
        │ physical address
        ▼
 cache hierarchy ── hit ─► requested data
        │ miss
        ▼
 main memory ──► protected storage / ECC as implemented
        │
        └─ OS-managed backing storage may participate in virtual memory""",language="markup")),
        sec("2","Choose technology for the job",
            table(("Need","Typical concept"),(("Very fast working storage near logic","Registers / SRAM-based cache"),("Large volatile working memory","DRAM"),("Non-volatile fixed or updateable contents","ROM / non-volatile memory technologies"),("Address-space abstraction and protection","Virtual memory"),("Detect/correct supported memory errors","Parity / ECC"))),
            rx.callout("Technology choices vary across products. 'Typical' describes common architecture, not a rule that every system must implement the same hierarchy.",icon="info")),
        sec("3","Design challenge",
            rx.text("Imagine a processor repeatedly scans a table larger than L1 cache but smaller than a lower cache level. Predict which ideas matter: spatial locality, block transfers, cache capacity, mapping, hit/miss behaviour, bandwidth and latency."),
            rx.text("Which principle explains why recently or nearby used data is worth keeping in faster memory?"),
            rx.hstack(rx.input(value=MemoryFoundationState.final_answer,on_change=MemoryFoundationState.set_final_answer,placeholder="Answer",max_width="210px"),rx.button("Check",on_click=MemoryFoundationState.check_final)),
            rx.cond(MemoryFoundationState.final_feedback!="",rx.callout(MemoryFoundationState.final_feedback,icon="brain"),rx.box())),
        sec("4","Path 06 concept map",
            rx.code_block("""memory cells
   ├─ SRAM / DRAM ─► RAM organisation ─► address decoding / expansion
   ├─ ROM / non-volatile storage
   ├─ cache ─► locality ─► mapping ─► hits & misses
   ├─ virtual memory ─► pages / frames / TLB / faults
   └─ reliability ─► parity / ECC
                         │
                         ▼
                memory-system performance""",language="markup")),
        sec("5","Engineering checklist",
            table(("Question","Why it matters"),(("How much capacity?","Sets address-space and device requirements"),("What word width?","Determines parallel data organisation"),("What latency/bandwidth?","Shapes performance"),("What volatility/persistence?","Determines whether contents survive power loss"),("What protection?","Defines detection/correction and access-control needs"),("What workload locality?","Influences cache effectiveness")))),
        sec("6","Path complete",
            rx.callout("You have connected individual memory cells to a complete memory hierarchy: organisation, expansion, caching, translation, reliability and performance.",icon="graduation-cap",color_scheme="green"),
            rx.text("Path 06 is now ready to serve as the memory foundation for later processor, architecture and system-design learning.",font_weight="600")),
        rx.hstack(rx.link(rx.button("← Memory performance",variant="soft"),href="/academy/unit-6/memory-hierarchy-performance"),rx.spacer(),rx.text("Path 06 · Complete",size="2",color="#64748b"),rx.spacer(),rx.link(rx.button("Return to Academy",color_scheme="green"),href="/academy"),width="100%",padding_y="16px"),
        width="min(1180px, 94vw)",margin="0 auto",padding_y="28px",spacing="5",align="stretch"))
