"""Install BoolNexa v1.1.0 SEO integration safely.

Run from D:\\Projects\\BoolNexa with:
    python install_v1_1_0_seo.py
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP_FILE = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
SEO_SOURCE = ROOT / "seo.py"
SEO_TARGET = ROOT / "digital_logic_lab" / "seo.py"
BACKUP_FILE = ROOT / "digital_logic_lab" / "digital_logic_lab.py.v1.0.2.bak"

OLD_IMPORT = "import reflex as rx\n"
NEW_IMPORT = (
    "import reflex as rx\n\n"
    "from .seo import PAGE_DESCRIPTION, PAGE_TITLE, seo_head_components, seo_meta\n"
)

OLD_APP_BLOCK = '''app = rx.App(
    head_components=[
        rx.script(src="/logic_interactions.js"),
    ],
)
app.add_page(
    index,
    title="BoolNexa - Free Online Digital Logic Simulator",
    description=(
        "Design, connect, and simulate digital logic circuits online with BoolNexa. "
        "Explore logic gates, flip-flops, adders, subtractors, multiplexers, "
        "demultiplexers, encoders, and decoders for free."
    ),
    meta=[
        {"name": "robots", "content": "index, follow"},
        {"property": "og:title", "content": "BoolNexa - Free Online Digital Logic Simulator"},
        {"property": "og:description", "content": "Design and simulate digital logic circuits online with BoolNexa."},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": "https://boolnexa-teal-ring.reflex.run/"},
    ],
)
'''

NEW_APP_BLOCK = '''app = rx.App(
    head_components=[
        rx.script(src="/logic_interactions.js"),
        *seo_head_components(),
    ],
)
app.add_page(
    index,
    title=PAGE_TITLE,
    description=PAGE_DESCRIPTION,
    meta=seo_meta(),
)
'''


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    if not APP_FILE.exists():
        fail(f"Cannot find {APP_FILE}")

    if not SEO_SOURCE.exists():
        fail(f"Cannot find {SEO_SOURCE}")

    source = APP_FILE.read_text(encoding="utf-8")

    if "from .seo import PAGE_DESCRIPTION" in source:
        fail("SEO integration already appears to be installed.")

    if OLD_APP_BLOCK not in source:
        fail(
            "The expected existing app configuration was not found. "
            "No project file was changed."
        )

    if source.count(OLD_IMPORT) != 1:
        fail(
            "Could not identify the Reflex import safely. "
            "No project file was changed."
        )

    shutil.copy2(APP_FILE, BACKUP_FILE)
    shutil.copy2(SEO_SOURCE, SEO_TARGET)

    updated = source.replace(OLD_IMPORT, NEW_IMPORT, 1)
    updated = updated.replace(OLD_APP_BLOCK, NEW_APP_BLOCK, 1)
    APP_FILE.write_text(updated, encoding="utf-8")

    print("BoolNexa v1.1.0 SEO integration installed successfully.")
    print(f"Backup created: {BACKUP_FILE}")
    print(f"SEO module created: {SEO_TARGET}")
    print(f"Updated app file: {APP_FILE}")
    print()
    print("Next run:")
    print("  python -m compileall digital_logic_lab")
    print("  reflex run")


if __name__ == "__main__":
    main()
