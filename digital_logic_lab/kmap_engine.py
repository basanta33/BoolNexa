"""Mano-style Karnaugh-map engine for BoolNexa.

Supports 2–6 variables using one textbook Gray-code map:
- 2 variables: 2×2
- 3 variables: 2×4
- 4 variables: 4×4
- 5 variables: 4×8 (AB rows, CDE columns)
- 6 variables: 8×8 (ABC rows, DEF columns)
"""

from __future__ import annotations

from dataclasses import dataclass

from .boolean_engine import BooleanExpressionError, generate_truth_table
from .boolean_simplifier import (
    Implicant,
    _format_sop,
    _prime_implicants,
    _select_cover,
)
from .gray_code import gray_code


@dataclass(frozen=True)
class KMapCell:
    facet: int
    row: int
    column: int
    minterm: int
    value: str


@dataclass(frozen=True)
class KMapGroup:
    index: int
    pattern: str
    term: str
    minterms: tuple[int, ...]
    cells: tuple[tuple[int, int, int], ...]
    size: int
    essential: bool


@dataclass(frozen=True)
class KMapResult:
    expression: str
    variables: list[str]
    row_variables: list[str]
    column_variables: list[str]
    facet_variables: list[str]
    row_codes: list[str]
    column_codes: list[str]
    facet_codes: list[str]
    rows: int
    columns: int
    facets: int
    cells: list[KMapCell]
    groups: list[KMapGroup]
    minterms: list[int]
    simplified_expression: str


def _split_variables(variables: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Split variables into textbook row/column axes.

    BoolNexa deliberately renders 5- and 6-variable K-maps as a single
    Gray-code map rather than separate facets:
      5 variables -> AB rows × CDE columns (4×8)
      6 variables -> ABC rows × DEF columns (8×8)
    """
    count = len(variables)
    if count == 2:
        return variables[:1], variables[1:], []
    if count == 3:
        return variables[:1], variables[1:], []
    if count == 4:
        return variables[:2], variables[2:], []
    if count == 5:
        return variables[:2], variables[2:], []
    if count == 6:
        return variables[:3], variables[3:], []
    raise BooleanExpressionError("Karnaugh maps require 2 to 6 variables.")


def _minterm_for_codes(
    facet_code: str,
    row_code: str,
    column_code: str,
) -> int:
    bits = facet_code + row_code + column_code
    return int(bits, 2)


def _term_for_pattern(pattern: str, variables: list[str]) -> str:
    literals: list[str] = []
    for bit, variable in zip(pattern, variables):
        if bit == "1":
            literals.append(variable)
        elif bit == "0":
            literals.append(f"{variable}'")
    return "1" if not literals else "".join(literals)


def _group_cells(
    implicant: Implicant,
    facet_codes: list[str],
    row_codes: list[str],
    column_codes: list[str],
) -> tuple[tuple[int, int, int], ...]:
    positions: list[tuple[int, int, int]] = []
    for facet_index, facet_code in enumerate(facet_codes):
        for row_index, row_code in enumerate(row_codes):
            for column_index, column_code in enumerate(column_codes):
                minterm = _minterm_for_codes(facet_code, row_code, column_code)
                if minterm in implicant.covers:
                    positions.append((facet_index, row_index, column_index))
    return tuple(positions)


def _essential_indices(primes: list[Implicant], minterms: list[int]) -> set[int]:
    essential: set[int] = set()
    for minterm in minterms:
        covering = [
            index
            for index, prime in enumerate(primes)
            if minterm in prime.covers
        ]
        if len(covering) == 1:
            essential.add(covering[0])
    return essential


def build_kmap(expression: str) -> KMapResult:
    table = generate_truth_table(
        expression,
        include_intermediate=False,
        max_variables=6,
    )
    variables = table.variables
    if len(variables) < 2 or len(variables) > 6:
        raise BooleanExpressionError("Karnaugh maps require 2 to 6 variables.")

    row_variables, column_variables, facet_variables = _split_variables(variables)
    row_codes = gray_code(len(row_variables))
    column_codes = gray_code(len(column_variables))
    facet_codes = gray_code(len(facet_variables))

    minterms = table.minterms
    minterm_set = set(minterms)

    cells: list[KMapCell] = []
    for facet_index, facet_code in enumerate(facet_codes):
        for row_index, row_code in enumerate(row_codes):
            for column_index, column_code in enumerate(column_codes):
                minterm = _minterm_for_codes(facet_code, row_code, column_code)
                cells.append(
                    KMapCell(
                        facet=facet_index,
                        row=row_index,
                        column=column_index,
                        minterm=minterm,
                        value="1" if minterm in minterm_set else "0",
                    )
                )

    if not minterms:
        selected: list[Implicant] = []
        primes: list[Implicant] = []
        simplified = "0"
    elif len(minterms) == 2 ** len(variables):
        selected = [Implicant("-" * len(variables), frozenset(minterms))]
        primes = selected
        simplified = "1"
    else:
        primes, _ = _prime_implicants(minterms, len(variables))
        selected = _select_cover(primes, minterms)
        simplified = _format_sop(selected, variables)

    essentials = _essential_indices(primes, minterms)
    prime_index_by_pattern = {prime.pattern: index for index, prime in enumerate(primes)}

    groups: list[KMapGroup] = []
    for group_index, implicant in enumerate(selected, start=1):
        prime_index = prime_index_by_pattern.get(implicant.pattern, -1)
        groups.append(
            KMapGroup(
                index=group_index,
                pattern=implicant.pattern,
                term=_term_for_pattern(implicant.pattern, variables),
                minterms=tuple(sorted(implicant.covers)),
                cells=_group_cells(
                    implicant,
                    facet_codes,
                    row_codes,
                    column_codes,
                ),
                size=len(implicant.covers),
                essential=prime_index in essentials,
            )
        )

    return KMapResult(
        expression=expression,
        variables=variables,
        row_variables=row_variables,
        column_variables=column_variables,
        facet_variables=facet_variables,
        row_codes=row_codes,
        column_codes=column_codes,
        facet_codes=facet_codes,
        rows=len(row_codes),
        columns=len(column_codes),
        facets=len(facet_codes),
        cells=cells,
        groups=groups,
        minterms=minterms,
        simplified_expression=simplified,
    )
