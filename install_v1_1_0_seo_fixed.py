"""Install BoolNexa v1.1.0 SEO integration safely.

Run from D:\Projects\BoolNexa:
    python install_v1_1_0_seo_fixed.py
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP_FILE = ROOT / "digital_logic_lab" / "digital_logic_lab.py"
SEO_SOURCE = ROOT / "seo.py"
SEO_TARGET = ROOT / "digital_logic_lab" / "seo.py"
BACKUP_FILE = ROOT / "digital_logic_lab" / "digital_logic_lab.py.v1.0.2.bak"

IMPORT_LINE = "import reflex as rx\n"
SEO_IMPORT = (
    "import reflex as rx\n\n"
    "from .seo import PAGE_DESCRIPTION, PAGE_TITLE, seo_head_components, seo_meta\n"
)

OLD_APP_BLOCK = """app = rx.App(
    head_components=[
        rx.script(src="/logic_interactions.js"),
    ],
)
app.add_page(index)
"""

NEW_APP_BLOCK = """app = rx.App(
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
"""


def stop(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    if not APP_FILE.exists():
        stop(f"Cannot find {APP_FILE}")

    if not SEO_SOURCE.exists():
        stop(f"Cannot find {SEO_SOURCE}")

    source = APP_FILE.read_text(encoding="utf-8")

    if "from .seo import PAGE_DESCRIPTION" in source:
        stop("SEO integration already appears to be installed.")

    if OLD_APP_BLOCK not in source:
        stop(
            "The current app configuration does not match the expected BoolNexa file. "
            "No project file was changed."
        )

    if source.count(IMPORT_LINE) != 1:
        stop("Could not identify the Reflex import safely. No file was changed.")

    shutil.copy2(APP_FILE, BACKUP_FILE)
    shutil.copy2(SEO_SOURCE, SEO_TARGET)

    updated = source.replace(IMPORT_LINE, SEO_IMPORT, 1)
    updated = updated.replace(OLD_APP_BLOCK, NEW_APP_BLOCK, 1)
    APP_FILE.write_text(updated, encoding="utf-8")

    print("BoolNexa v1.1.0 SEO integration installed successfully.")
    print(f"Backup: {BACKUP_FILE}")
    print(f"Created: {SEO_TARGET}")
    print(f"Updated: {APP_FILE}")


if __name__ == "__main__":
    main()
