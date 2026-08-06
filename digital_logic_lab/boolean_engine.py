"""BoolNexa Boolean expression engine."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import re
from typing import Mapping, Sequence

class BooleanExpressionError(ValueError):
    pass

@dataclass(frozen=True)
class Node:
    op: str
    value: str = ""
    left: "Node | None" = None
    right: "Node | None" = None

    def evaluate(self, values: Mapping[str, bool]) -> bool:
        if self.op == "VAR":
            if self.value not in values:
                raise BooleanExpressionError(f"Missing value for {self.value}.")
            return bool(values[self.value])
        if self.op == "CONST":
            return self.value == "1"
        if self.op == "NOT":
            return not self.left.evaluate(values)

        a, b = self.left.evaluate(values), self.right.evaluate(values)

        if self.op == "AND":
            return a and b
        if self.op == "OR":
            return a or b
        if self.op == "XOR":
            return a != b
        if self.op == "NAND":
            return not (a and b)
        if self.op == "NOR":
            return not (a or b)
        if self.op == "XNOR":
            return a == b

        raise BooleanExpressionError(f"Unsupported operation {self.op}.")

    def variables(self) -> set[str]:
        if self.op == "VAR":
            return {self.value}
        if self.op == "CONST":
            return set()
        if self.op == "NOT":
            return self.left.variables()
        return self.left.variables() | self.right.variables()

    def display(self) -> str:
        if self.op in {"VAR", "CONST"}:
            return self.value

        if self.op == "NOT":
            child = self.left.display()
            if self.left.op in {"AND", "OR", "XOR", "NAND", "NOR", "XNOR"}:
                child = f"({child})"
            return f"{child}'"

        # BoolNexa presentation invariant: user-visible Boolean notation never
        # exposes technology shorthand such as NAND/NOR arrows.  Universal
        # gates are written as the complemented ordinary operation instead:
        # NAND(A,B) -> (A·B)' and NOR(A,B) -> (A + B)'.
        left, right = self.left.display(), self.right.display()

        def factor(text: str, child: "Node") -> str:
            if child.op in {"OR", "XOR", "NOR", "XNOR"}:
                return f"({text})"
            return text

        if self.op == "AND":
            return f"{factor(left, self.left)}·{factor(right, self.right)}"
        if self.op == "OR":
            return f"{left} + {right}"
        if self.op == "XOR":
            return f"{left} ⊕ {right}"
        if self.op == "NAND":
            product = f"{factor(left, self.left)}·{factor(right, self.right)}"
            return f"({product})'"
        if self.op == "NOR":
            return f"({left} + {right})'"
        if self.op == "XNOR":
            return f"({left} ⊕ {right})'"

        raise BooleanExpressionError(f"Unsupported operation {self.op}.")

@dataclass(frozen=True)
class Token:
    kind: str
    value: str



CANONICAL_SUM_RE = re.compile(
    r"^\s*(?:(?P<name>[A-Za-z][A-Za-z0-9_]*)\s*(?:\(\s*(?P<vars>[^)]*)\s*\))?\s*=\s*)?"
    r"(?:Σ|SIGMA|SUM)\s*[mM]\s*\(\s*(?P<mins>[^)]*)\s*\)\s*$",
    re.IGNORECASE,
)


def _canonical_variable_list(text: str) -> list[str]:
    variables = [item.strip() for item in text.split(",") if item.strip()]
    if not variables:
        raise BooleanExpressionError("List the variables in the function header, for example F(A,B,C) = Σm(4,6,7).")
    for variable in variables:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", variable):
            raise BooleanExpressionError(f"Invalid variable name {variable!r} in canonical function header.")
    if len(set(variables)) != len(variables):
        raise BooleanExpressionError("Variable names in the function header must be unique.")
    return variables


def _canonical_minterm_list(text: str) -> list[int]:
    stripped = text.strip()
    if not stripped or stripped in {"∅", "{}"}:
        return []
    items = [item.strip() for item in stripped.split(",")]
    if any(not item for item in items):
        raise BooleanExpressionError("Minterm list contains an empty entry.")
    try:
        values = [int(item, 10) for item in items]
    except ValueError as exc:
        raise BooleanExpressionError("Minterms must be non-negative decimal integers.") from exc
    if any(value < 0 for value in values):
        raise BooleanExpressionError("Minterms must be non-negative decimal integers.")
    if len(set(values)) != len(values):
        raise BooleanExpressionError("Minterms must not be repeated.")
    return sorted(values)


def canonical_sum_to_expression(expression: str) -> tuple[str, list[str], list[int]] | None:
    """Convert ``F(A,B,C)=Σm(...)`` notation to a parser expression.

    A bare ``F = Σm(...)`` is also accepted.  In that form BoolNexa infers
    the minimum A, B, C... variable width required by the largest minterm.
    Explicit variable headers remain the preferred, unambiguous form.
    """
    match = CANONICAL_SUM_RE.fullmatch(expression.strip())
    if match is None:
        return None

    minterms = _canonical_minterm_list(match.group("mins"))
    variables_text = match.group("vars")
    if variables_text is not None:
        variables = _canonical_variable_list(variables_text)
    else:
        if not minterms:
            raise BooleanExpressionError(
                "Use an explicit variable header for an empty minterm set, for example F(A,B)=Σm(∅)."
            )
        width = max(1, max(minterms).bit_length())
        if width > 26:
            raise BooleanExpressionError("Automatic canonical variable inference supports at most 26 variables.")
        variables = [chr(ord("A") + index) for index in range(width)]

    limit = 2 ** len(variables)
    invalid = [value for value in minterms if value >= limit]
    if invalid:
        raise BooleanExpressionError(
            f"Minterm m{invalid[0]} is outside the range for {len(variables)} variables (0 to {limit - 1})."
        )

    if not minterms:
        parser_expression = "0"
    elif len(minterms) == limit:
        parser_expression = "1"
    else:
        terms: list[str] = []
        for minterm in minterms:
            bits = f"{minterm:0{len(variables)}b}"
            literals = [
                variable if bit == "1" else f"{variable}'"
                for variable, bit in zip(variables, bits)
            ]
            terms.append("*".join(literals))
        parser_expression = " + ".join(terms)

    return parser_expression, variables, minterms


def resolve_function_input(expression: str) -> str:
    """Return a parser-ready expression for Boolean or Σm input notation."""
    canonical = canonical_sum_to_expression(expression)
    return canonical[0] if canonical is not None else expression

TOKEN_RE = re.compile(
    r"\s*(?:(?P<ID>[A-Za-z][A-Za-z0-9_]*)|(?P<CONST>[01])|(?P<OP>[+.*&|^⊕'!~()]))"
)

def _raw_tokens(expression: str) -> list[Token]:
    if not expression or not expression.strip():
        raise BooleanExpressionError("Enter a Boolean expression.")
    text, tokens, pos = expression.strip(), [], 0
    while pos < len(text):
        match = TOKEN_RE.match(text, pos)
        if not match:
            raise BooleanExpressionError(
                f"Unexpected character near position {pos + 1}: {text[pos]!r}"
            )
        pos = match.end()
        if match.lastgroup == "ID":
            word = match.group("ID")
            upper = word.upper()
            if upper in {"AND", "OR", "XOR", "NOT"}:
                tokens.append(Token("OP", upper))
            elif word.isupper() and len(word) > 1 and word.isalpha():
                tokens.extend(Token("ID", ch) for ch in word)
            else:
                tokens.append(Token("ID", word))
        elif match.lastgroup == "CONST":
            tokens.append(Token("CONST", match.group("CONST")))
        else:
            tokens.append(Token("OP", match.group("OP")))
    return tokens

def _can_end(t: Token) -> bool:
    return t.kind in {"ID", "CONST"} or t.value in {")", "'"}

def _can_start(t: Token) -> bool:
    return t.kind in {"ID", "CONST"} or t.value in {"(", "!", "~", "NOT"}

def tokenize(expression: str) -> list[Token]:
    raw, result = _raw_tokens(expression), []
    for token in raw:
        if result and _can_end(result[-1]) and _can_start(token):
            result.append(Token("OP", "AND"))
        result.append(token)
    return result

class _Parser:
    def __init__(self, tokens: Sequence[Token]):
        self.tokens, self.index = list(tokens), 0

    def current(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def accept(self, *values):
        token = self.current()
        if token is not None and token.value in values:
            self.index += 1
            return token
        return None

    def parse(self):
        node = self.parse_or()
        if self.current() is not None:
            raise BooleanExpressionError(
                f"Unexpected token {self.current().value!r}."
            )
        return node

    def parse_or(self):
        node = self.parse_xor()
        while self.accept("+", "|", "OR"):
            node = Node("OR", left=node, right=self.parse_xor())
        return node

    def parse_xor(self):
        node = self.parse_and()
        while self.accept("^", "⊕", "XOR"):
            node = Node("XOR", left=node, right=self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_unary()
        while self.accept(".", "*", "&", "AND"):
            node = Node("AND", left=node, right=self.parse_unary())
        return node

    def parse_unary(self):
        count = 0
        while self.accept("!", "~", "NOT"):
            count += 1
        node = self.parse_primary()
        while self.accept("'"):
            node = Node("NOT", left=node)
        for _ in range(count):
            node = Node("NOT", left=node)
        return node

    def parse_primary(self):
        token = self.current()
        if token is None:
            raise BooleanExpressionError("Expression ended unexpectedly.")
        if token.kind == "ID":
            self.index += 1
            return Node("VAR", value=token.value)
        if token.kind == "CONST":
            self.index += 1
            return Node("CONST", value=token.value)
        if self.accept("("):
            node = self.parse_or()
            if not self.accept(")"):
                raise BooleanExpressionError("Missing closing parenthesis.")
            return node
        raise BooleanExpressionError(
            f"Expected a variable, constant or '(', got {token.value!r}."
        )

def parse_expression(expression: str) -> Node:
    return _Parser(tokenize(expression)).parse()

def evaluate_expression(expression: str, values: Mapping[str, bool]) -> bool:
    return parse_expression(expression).evaluate(values)

def variables_for(node: Node) -> list[str]:
    return sorted(node.variables(), key=lambda n: (n.upper(), n))

def _subexpressions(node: Node) -> list[Node]:
    result, seen = [], set()

    def visit(current):
        if current.left is not None:
            visit(current.left)
        if current.right is not None:
            visit(current.right)
        if current.op not in {"VAR", "CONST"} and current.display() not in seen:
            seen.add(current.display())
            result.append(current)

    visit(node)
    return result

@dataclass(frozen=True)
class TruthTable:
    expression: str
    normalized_expression: str
    variables: list[str]
    intermediate_headers: list[str]
    rows: list[dict[str, str]]
    minterms: list[int]
    maxterms: list[int]
    canonical_sop: str
    canonical_pos: str

def _sop(vars, mins):
    if not mins:
        return "0"
    if len(mins) == 2 ** len(vars):
        return "1"
    out = []
    for i in mins:
        bits = f"{i:0{len(vars)}b}"
        out.append(
            "".join(v if b == "1" else f"{v}'" for v, b in zip(vars, bits))
        )
    return " + ".join(out)

def _pos(vars, maxs):
    if not maxs:
        return "1"
    if len(maxs) == 2 ** len(vars):
        return "0"
    out = []
    for i in maxs:
        bits = f"{i:0{len(vars)}b}"
        out.append(
            "("
            + " + ".join(
                f"{v}'" if b == "1" else v
                for v, b in zip(vars, bits)
            )
            + ")"
        )
    return "".join(out)

def generate_truth_table(
    expression: str,
    *,
    include_intermediate: bool = True,
    max_variables: int = 8,
) -> TruthTable:
    resolved_expression = resolve_function_input(expression)
    canonical = canonical_sum_to_expression(expression)
    node = parse_expression(resolved_expression)
    variables = canonical[1] if canonical is not None else variables_for(node)
    if len(variables) > max_variables:
        raise BooleanExpressionError(
            f"Limit expressions to {max_variables} variables in the interactive lab."
        )
    final = node.display()
    inter = [
        n
        for n in (_subexpressions(node) if include_intermediate else [])
        if n.display() != final
    ]
    headers = [n.display() for n in inter]
    rows = []
    mins = []
    maxs = []

    for index, bits in enumerate(product((False, True), repeat=len(variables))):
        values = dict(zip(variables, bits))
        result = node.evaluate(values)
        row = {v: ("1" if values[v] else "0") for v in variables}
        for n in inter:
            row[n.display()] = "1" if n.evaluate(values) else "0"
        row["F"] = "1" if result else "0"
        rows.append(row)
        (mins if result else maxs).append(index)

    return TruthTable(
        expression,
        final,
        variables,
        headers,
        rows,
        mins,
        maxs,
        _sop(variables, mins),
        _pos(variables, maxs),
    )

def classify_expression(table: TruthTable) -> str:
    if not table.minterms:
        return "Contradiction (always 0)"
    if not table.maxterms:
        return "Tautology (always 1)"
    return "Contingent expression"
