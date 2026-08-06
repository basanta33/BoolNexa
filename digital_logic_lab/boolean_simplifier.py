"""Exact Boolean minimization for BoolNexa.

The engine uses the existing parser/truth-table engine, then performs
Quine-McCluskey prime-implicant generation and an exact cover search.
This guarantees an equivalent minimal SOP for interactive expressions
up to the Boolean Lab's existing variable limit.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .boolean_engine import BooleanExpressionError, generate_truth_table, parse_expression
from .boolean_laws import get_law
from .simplification_steps import SimplificationResult, SimplificationStep


@dataclass(frozen=True)
class Implicant:
    pattern: str
    covers: frozenset[int]

    @property
    def literal_count(self) -> int:
        return sum(char != "-" for char in self.pattern)


def _combine(a: Implicant, b: Implicant) -> Implicant | None:
    differences = 0
    chars: list[str] = []
    for left, right in zip(a.pattern, b.pattern):
        if left == right:
            chars.append(left)
        elif left != "-" and right != "-":
            differences += 1
            chars.append("-")
        else:
            return None
    if differences != 1:
        return None
    return Implicant("".join(chars), a.covers | b.covers)


def _dedupe(implicants: list[Implicant]) -> list[Implicant]:
    merged: dict[str, set[int]] = {}
    for item in implicants:
        merged.setdefault(item.pattern, set()).update(item.covers)
    return [
        Implicant(pattern, frozenset(sorted(covers)))
        for pattern, covers in sorted(merged.items())
    ]


def _prime_implicants(minterms: list[int], width: int) -> tuple[list[Implicant], list[list[Implicant]]]:
    current = [
        Implicant(f"{value:0{width}b}", frozenset({value}))
        for value in sorted(set(minterms))
    ]
    rounds: list[list[Implicant]] = [current]
    primes: list[Implicant] = []

    while current:
        used: set[int] = set()
        next_round: list[Implicant] = []
        for i, j in combinations(range(len(current)), 2):
            combined = _combine(current[i], current[j])
            if combined is not None:
                used.add(i)
                used.add(j)
                next_round.append(combined)

        primes.extend(item for index, item in enumerate(current) if index not in used)
        next_round = _dedupe(next_round)
        if not next_round:
            break
        rounds.append(next_round)
        current = next_round

    return _dedupe(primes), rounds


def _cover_cost(indices: tuple[int, ...], primes: list[Implicant]) -> tuple[int, int, tuple[str, ...]]:
    chosen = [primes[index] for index in indices]
    return (
        len(chosen),
        sum(item.literal_count for item in chosen),
        tuple(sorted(item.pattern for item in chosen)),
    )


def _select_cover(primes: list[Implicant], minterms: list[int]) -> list[Implicant]:
    required = set(minterms)
    if not required:
        return []

    chart: dict[int, list[int]] = {
        minterm: [
            index for index, prime in enumerate(primes)
            if minterm in prime.covers
        ]
        for minterm in required
    }

    essential_indices: set[int] = {
        indices[0]
        for indices in chart.values()
        if len(indices) == 1
    }
    covered = set().union(
        *(primes[index].covers for index in essential_indices)
    ) if essential_indices else set()

    remaining = required - covered
    if not remaining:
        return [primes[index] for index in sorted(essential_indices)]

    candidate_indices = sorted(
        {
            index
            for minterm in remaining
            for index in chart[minterm]
            if index not in essential_indices
        }
    )

    best: tuple[int, ...] | None = None
    for size in range(len(candidate_indices) + 1):
        for candidate in combinations(candidate_indices, size):
            selected = set(essential_indices) | set(candidate)
            candidate_cover = set().union(
                *(primes[index].covers for index in selected)
            ) if selected else set()
            if required <= candidate_cover:
                full = tuple(sorted(selected))
                if best is None or _cover_cost(full, primes) < _cover_cost(best, primes):
                    best = full
        if best is not None:
            break

    if best is None:
        raise BooleanExpressionError("Unable to cover all minterms.")
    return [primes[index] for index in best]


def _pattern_to_term(pattern: str, variables: list[str]) -> str:
    literals: list[str] = []
    for bit, variable in zip(pattern, variables):
        if bit == "1":
            literals.append(variable)
        elif bit == "0":
            literals.append(f"{variable}'")
    return "1" if not literals else "".join(literals)


def _format_sop(implicants: list[Implicant], variables: list[str]) -> str:
    if not implicants:
        return "0"
    terms = [_pattern_to_term(item.pattern, variables) for item in implicants]
    if "1" in terms:
        return "1"
    return " + ".join(sorted(terms, key=lambda term: (len(term), term)))


def _parser_text(expression: str) -> str:
    """Convert display symbols back to parser-supported operators."""
    return expression.replace("·", ".").replace("⊕", "^")


def _literal_count(expression: str) -> int:
    node = parse_expression(_parser_text(expression))

    def visit(current) -> int:
        if current.op == "VAR":
            return 1
        if current.op == "CONST":
            return 0
        if current.op == "NOT":
            return visit(current.left)
        return visit(current.left) + visit(current.right)

    return visit(node)


def _top_level_term_count(expression: str) -> int:
    node = parse_expression(_parser_text(expression))

    def flatten_or(current) -> int:
        if current.op == "OR":
            return flatten_or(current.left) + flatten_or(current.right)
        return 1

    return flatten_or(node)


def _step(number: int, before: str, after: str, law_key: str) -> SimplificationStep:
    law = get_law(law_key)
    return SimplificationStep(
        number=number,
        before=before,
        after=after,
        law_key=law.key,
        law_name=law.name,
        formula=law.formula,
        explanation=law.explanation,
    )


def simplify_expression(expression: str, max_variables: int = 8) -> SimplificationResult:
    table = generate_truth_table(
        expression,
        include_intermediate=False,
        max_variables=max_variables,
    )
    normalized = table.normalized_expression
    variables = table.variables
    minterms = table.minterms

    if not minterms:
        simplified = "0"
        steps = [_step(1, normalized, simplified, "domination")]
    elif len(minterms) == 2 ** len(variables):
        simplified = "1"
        steps = [_step(1, normalized, simplified, "complement")]
    else:
        primes, rounds = _prime_implicants(minterms, len(variables))
        selected = _select_cover(primes, minterms)
        simplified = _format_sop(selected, variables)

        steps: list[SimplificationStep] = []
        current = normalized
        if table.canonical_sop != current:
            steps.append(_step(len(steps) + 1, current, table.canonical_sop, "canonical_sop"))
            current = table.canonical_sop

        if len(rounds) > 1:
            combined_text = " + ".join(
                _pattern_to_term(item.pattern, variables)
                for item in rounds[-1]
            )
            if combined_text and combined_text != current and combined_text != simplified:
                steps.append(
                    _step(
                        len(steps) + 1,
                        current,
                        combined_text,
                        "adjacent_combination",
                    )
                )
                current = combined_text

        if current != simplified:
            steps.append(
                _step(
                    len(steps) + 1,
                    current,
                    simplified,
                    "prime_implicant",
                )
            )

        if not steps:
            steps.append(
                _step(
                    1,
                    normalized,
                    simplified,
                    "equivalent_minimum",
                )
            )

    return SimplificationResult(
        original=expression,
        normalized=normalized,
        simplified=simplified,
        variables=variables,
        minterms=minterms,
        steps=steps,
        literal_count_before=_literal_count(normalized),
        literal_count_after=_literal_count(simplified),
        term_count_before=_top_level_term_count(normalized),
        term_count_after=_top_level_term_count(simplified),
    )
