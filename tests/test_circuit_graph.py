from digital_logic_lab.circuit_engine import build_circuit
from digital_logic_lab.circuit_graph import topological_order, validate_circuit
def test_generated_graph_is_valid():
    g=build_circuit("AB + AC'"); validate_circuit(g)
def test_output_is_last_in_topological_order():
    g=build_circuit("AB + AC'"); assert topological_order(g)[-1]==g.output_node
