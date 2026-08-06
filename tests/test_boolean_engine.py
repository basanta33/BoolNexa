from digital_logic_lab.boolean_engine import evaluate_expression, generate_truth_table, parse_expression

def test_implicit_and_and_postfix_not():
    node = parse_expression("A(B+C')")
    assert node.evaluate({"A": True, "B": False, "C": False}) is True
    assert node.evaluate({"A": True, "B": False, "C": True}) is False

def test_identity_table():
    table = generate_truth_table("AB + AB'")
    assert table.variables == ["A", "B"]
    assert table.minterms == [2, 3]

def test_xor():
    assert evaluate_expression("A XOR B", {"A": False, "B": True}) is True
    assert evaluate_expression("A ⊕ B", {"A": True, "B": True}) is False

def test_canonical_forms():
    table = generate_truth_table("A+B", include_intermediate=False)
    assert table.minterms == [1, 2, 3]
    assert table.maxterms == [0]
    assert table.canonical_pos == "(A + B)"
