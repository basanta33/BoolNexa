"""Gate metadata used by BoolNexa renderers and lessons."""
from __future__ import annotations
from dataclasses import dataclass
from .gate import GateKind

@dataclass(frozen=True)
class GateDefinition:
    kind: GateKind
    display_name: str
    operator: str
    minimum_inputs: int
    maximum_inputs: int | None
    explanation: str

GATE_LIBRARY = {
    GateKind.INPUT: GateDefinition(GateKind.INPUT,"Input","",0,0,"A primary Boolean input."),
    GateKind.CONSTANT: GateDefinition(GateKind.CONSTANT,"Constant","",0,0,"A fixed logic 0 or logic 1."),
    GateKind.BUFFER: GateDefinition(GateKind.BUFFER,"Buffer","",1,1,"Passes the input without inversion."),
    GateKind.NOT: GateDefinition(GateKind.NOT,"NOT","'",1,1,"Produces the complement of its input."),
    GateKind.AND: GateDefinition(GateKind.AND,"AND","·",2,None,"HIGH only when every input is HIGH."),
    GateKind.OR: GateDefinition(GateKind.OR,"OR","+",2,None,"HIGH when at least one input is HIGH."),
    GateKind.XOR: GateDefinition(GateKind.XOR,"XOR","⊕",2,None,"HIGH when an odd number of inputs are HIGH."),
    GateKind.NAND: GateDefinition(GateKind.NAND,"NAND","NAND",2,None,"The complement of an AND operation."),
    GateKind.NOR: GateDefinition(GateKind.NOR,"NOR","NOR",2,None,"The complement of an OR operation."),
    GateKind.XNOR: GateDefinition(GateKind.XNOR,"XNOR","XNOR",2,None,"The complement of an XOR operation."),
    GateKind.OUTPUT: GateDefinition(GateKind.OUTPUT,"Output","",1,1,"The final circuit output."),
}
def get_gate_definition(kind: GateKind) -> GateDefinition:
    return GATE_LIBRARY[kind]
