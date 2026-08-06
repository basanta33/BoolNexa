from digital_logic_lab.gray_code import gray_code, gray_index


def test_gray_sequences() -> None:
    assert gray_code(0) == [""]
    assert gray_code(1) == ["0", "1"]
    assert gray_code(2) == ["00", "01", "11", "10"]


def test_gray_index() -> None:
    assert [gray_index(value) for value in range(4)] == [0, 1, 3, 2]
