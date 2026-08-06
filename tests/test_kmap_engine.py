from digital_logic_lab.kmap_engine import build_kmap


def test_three_variable_mano_layout() -> None:
    result = build_kmap("A(B+C')")
    assert result.row_variables == ["A"]
    assert result.column_variables == ["B", "C"]
    assert result.row_codes == ["0", "1"]
    assert result.column_codes == ["00", "01", "11", "10"]
    assert [cell.minterm for cell in result.cells[:4]] == [0, 1, 3, 2]
    assert [cell.minterm for cell in result.cells[4:8]] == [4, 5, 7, 6]


def test_four_variable_layout() -> None:
    result = build_kmap("AB + CD")
    assert result.rows == 4
    assert result.columns == 4
    assert result.facets == 1
    assert result.row_codes == ["00", "01", "11", "10"]
    assert result.column_codes == ["00", "01", "11", "10"]


def test_five_variable_uses_single_textbook_4_by_8_map() -> None:
    result = build_kmap("ABCDE + A'BCDE")
    assert result.facets == 1
    assert result.rows == 4
    assert result.columns == 8
    assert result.row_variables == ["A", "B"]
    assert result.column_variables == ["C", "D", "E"]
    assert result.facet_variables == []
    assert result.row_codes == ["00", "01", "11", "10"]
    assert result.column_codes == [
        "000", "001", "011", "010",
        "110", "111", "101", "100",
    ]


def test_six_variable_uses_single_textbook_8_by_8_map() -> None:
    result = build_kmap("ABCDEF")
    assert result.facets == 1
    assert result.rows == 8
    assert result.columns == 8
    assert result.row_variables == ["A", "B", "C"]
    assert result.column_variables == ["D", "E", "F"]
    assert result.facet_variables == []
    expected_gray3 = [
        "000", "001", "011", "010",
        "110", "111", "101", "100",
    ]
    assert result.row_codes == expected_gray3
    assert result.column_codes == expected_gray3


def test_grouping_and_simplification() -> None:
    result = build_kmap("AB + AB'")
    assert result.simplified_expression == "A"
    assert result.groups
    assert result.groups[0].term == "A"


def test_wraparound_group_exists() -> None:
    result = build_kmap("B' + AB'")
    assert result.variables == ["A", "B"]
    assert result.simplified_expression == "B'"
    assert result.groups[0].size == 2
