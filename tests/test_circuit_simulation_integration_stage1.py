from digital_logic_lab.circuit_simulator_transfer import circuit_graph_to_simulator_project
from digital_logic_lab.logic_core import evaluate_circuit
from digital_logic_lab.realization_policy import OptimizationObjective, RealizationPreset
from digital_logic_lab.realization_strategy import realize_preset


def _project(expression, preset):
    graph = realize_preset(expression, preset, objective=OptimizationObjective.BALANCED).graph
    return circuit_graph_to_simulator_project(graph)


def _evaluate(project, **values):
    gates = project["gates"]
    for gate in gates.values():
        if gate["type"] == "INPUT":
            gate["value"] = int(values[gate["label"]])
    return evaluate_circuit(gates)


def _out(gates):
    values = [g["value"] for g in gates.values() if g["type"] == "OUTPUT"]
    assert len(values) == 1
    return values[0]


def test_nand_xor_live_evaluation_all_combinations():
    project = _project("A^B", RealizationPreset.NAND_ONLY)
    for a,b,expected in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)):
        assert _out(_evaluate(project,A=a,B=b)) == expected


def test_nor_xor_live_evaluation_all_combinations():
    project = _project("A^B", RealizationPreset.NOR_ONLY)
    for a,b,expected in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)):
        assert _out(_evaluate(project,A=a,B=b)) == expected


def test_generated_internal_gates_have_compact_net_and_semantic_expression():
    project = _project("A^B", RealizationPreset.NOR_ONLY)
    internal = [g for g in project["gates"].values() if g["type"] not in {"INPUT","OUTPUT"}]
    assert internal
    assert all(g["generated_net"].startswith("N") for g in internal)
    assert all(g["label"] == g["generated_net"] for g in internal)
    assert all(g["generated_expression"] for g in internal)


def test_basic_generated_circuit_live_evaluation():
    project = _project("AB+AC'", RealizationPreset.BASIC_ONLY)
    for a in (0,1):
        for b in (0,1):
            for c in (0,1):
                expected = int((a and b) or (a and not c))
                assert _out(_evaluate(project,A=a,B=b,C=c)) == expected
