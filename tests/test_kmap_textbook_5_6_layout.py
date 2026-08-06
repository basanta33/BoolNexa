from digital_logic_lab.kmap_engine import build_kmap


def _canonical_sop(variable_count: int, minterms: list[int]) -> str:
    variables = "ABCDEF"[:variable_count]
    terms = []
    for minterm in minterms:
        bits = f"{minterm:0{variable_count}b}"
        terms.append(
            "".join(
                variable if bit == "1" else variable + "'"
                for variable, bit in zip(variables, bits)
            )
        )
    return " + ".join(terms)


def test_five_variable_map_is_one_4_by_8_gray_map():
    result = build_kmap(_canonical_sop(5, [0, 1, 2, 3, 10, 16]))
    assert result.rows == 4
    assert result.columns == 8
    assert result.facets == 1
    assert result.row_variables == ["A", "B"]
    assert result.column_variables == ["C", "D", "E"]
    assert result.row_codes == ["00", "01", "11", "10"]
    assert result.column_codes == ["000", "001", "011", "010", "110", "111", "101", "100"]


def test_six_variable_map_is_one_8_by_8_gray_map():
    result = build_kmap(_canonical_sop(6, [0, 1, 2, 3, 32, 33, 63]))
    assert result.rows == 8
    assert result.columns == 8
    assert result.facets == 1
    assert result.row_variables == ["A", "B", "C"]
    assert result.column_variables == ["D", "E", "F"]
    gray3 = ["000", "001", "011", "010", "110", "111", "101", "100"]
    assert result.row_codes == gray3
    assert result.column_codes == gray3
