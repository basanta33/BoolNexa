from digital_logic_lab.gate import GateKind
from digital_logic_lab.gate_library import GATE_LIBRARY, get_gate_definition
def test_library_contains_required_gates():
    required={GateKind.AND,GateKind.OR,GateKind.NOT,GateKind.NAND,GateKind.NOR,GateKind.XOR,GateKind.XNOR,GateKind.BUFFER}
    assert required <= set(GATE_LIBRARY)
def test_gate_definitions_are_educational():
    for kind in (GateKind.AND,GateKind.OR,GateKind.NOT):
        d=get_gate_definition(kind); assert d.display_name and d.explanation
