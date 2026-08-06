"""Validation and graph helpers for BoolNexa circuits."""
from __future__ import annotations
from collections import defaultdict, deque
from .gate import CircuitGraph

class CircuitGraphError(ValueError): pass

def has_cycle(graph: CircuitGraph) -> bool:
    adjacency=defaultdict(list); indegree={n.id:0 for n in graph.nodes}
    for w in graph.wires:
        adjacency[w.source].append(w.target); indegree[w.target]+=1
    q=deque(n for n,d in indegree.items() if d==0); visited=0
    while q:
        node=q.popleft(); visited+=1
        for target in adjacency[node]:
            indegree[target]-=1
            if indegree[target]==0: q.append(target)
    return visited != len(graph.nodes)

def validate_circuit(graph: CircuitGraph) -> None:
    ids=[n.id for n in graph.nodes]
    if len(ids)!=len(set(ids)): raise CircuitGraphError("Circuit contains duplicate node IDs.")
    node_ids=set(ids)
    if graph.output_node not in node_ids: raise CircuitGraphError("Circuit output node is missing.")
    incoming=defaultdict(int)
    for w in graph.wires:
        if w.source not in node_ids: raise CircuitGraphError(f"Unknown wire source: {w.source}")
        if w.target not in node_ids: raise CircuitGraphError(f"Unknown wire target: {w.target}")
        incoming[w.target]+=1
    for n in graph.nodes:
        if incoming[n.id] != len(n.inputs):
            raise CircuitGraphError(f"{n.id} expects {len(n.inputs)} incoming wires, found {incoming[n.id]}.")
    if has_cycle(graph): raise CircuitGraphError("Circuit graph contains a cycle.")

def topological_order(graph: CircuitGraph) -> list[str]:
    validate_circuit(graph)
    adjacency=defaultdict(list); indegree={n.id:0 for n in graph.nodes}
    for w in graph.wires:
        adjacency[w.source].append(w.target); indegree[w.target]+=1
    q=deque(sorted(n for n,d in indegree.items() if d==0)); result=[]
    while q:
        node=q.popleft(); result.append(node)
        for target in sorted(adjacency[node]):
            indegree[target]-=1
            if indegree[target]==0: q.append(target)
    return result
