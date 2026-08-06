from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ACADEMY_DIR = ROOT / "digital_logic_lab"


def _state_classes():
    classes = {}
    for path in ACADEMY_DIR.glob("academy*.py"):
        text = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"(?m)^class\s+([A-Za-z_]\w*)\(rx\.State\):\n", text))
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            top_def = re.search(r"(?m)^def\s+[A-Za-z_]\w*\s*\(", text[start:end])
            if top_def:
                end = start + top_def.start()
            body = text[start:end]
            methods = set(re.findall(r"(?m)^    def\s+([A-Za-z_]\w*)\s*\(", body))
            classes[match.group(1)] = (path.name, methods)
    return classes


def test_every_academy_state_setter_reference_is_explicitly_defined():
    classes = _state_classes()
    missing = []
    for path in ACADEMY_DIR.glob("academy*.py"):
        text = path.read_text(encoding="utf-8")
        for state_name, field in re.findall(
            r"\b([A-Za-z_]\w*)\.set_([A-Za-z_]\w*)\b", text
        ):
            if state_name not in classes:
                continue
            source, methods = classes[state_name]
            method = f"set_{field}"
            if method not in methods:
                missing.append((path.name, state_name, method, source))
    assert not missing, f"Missing explicit Reflex state setters: {missing}"


def test_binary_conversion_decimal_value_setter_exists():
    path = ACADEMY_DIR / "academy_binary_conversions.py"
    text = path.read_text(encoding="utf-8")
    assert "def set_decimal_value(" in text
    assert "self.decimal_value = value" in text
