from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACADEMY_DIR = ROOT / "digital_logic_lab"


def test_academy_code_blocks_do_not_use_unsupported_text_language():
    offenders = []
    for path in ACADEMY_DIR.glob("academy*.py"):
        text = path.read_text(encoding="utf-8")
        if 'language="text"' in text or "language='text'" in text:
            offenders.append(path.name)
    assert not offenders, f"Unsupported Reflex CodeBlock language='text' in: {offenders}"


def test_academy_uses_supported_markup_language_for_plain_diagrams():
    matched = 0
    for path in ACADEMY_DIR.glob("academy*.py"):
        text = path.read_text(encoding="utf-8")
        matched += text.count('language="markup"')
        matched += text.count("language='markup'")
    assert matched > 0
