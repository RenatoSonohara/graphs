from __future__ import annotations

import sys
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

from graph import Graph


Edge = Tuple[int, int]


def _normalize_edge(u: int, v: int) -> Edge:
    return (u, v) if u <= v else (v, u)


def has_eulerian_cycle(graph: Graph) -> bool:
    non_zero = [v for v in graph.vertices() if graph.grau(v) > 0]
    if not non_zero:
        return False
    if any(graph.grau(v) % 2 != 0 for v in graph.vertices()):
        return False

    start = non_zero[0]
    stack = [start]
    visited = set()
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in graph.vizinhos(u):
            if graph.grau(v) > 0 and v not in visited:
                stack.append(v)
    return len(visited) == len(non_zero)


def find_eulerian_cycle(graph: Graph) -> List[int]:
    if not has_eulerian_cycle(graph):
        return []

    if graph.qtdArestas() == 0:
        return [1] if graph.qtdVertices() > 0 else []

    adjacency: DefaultDict[int, List[int]] = defaultdict(list)
    edge_count: Dict[Edge, int] = defaultdict(int)

    for u, v, _ in graph.edges():
        adjacency[u].append(v)
        adjacency[v].append(u)
        edge_count[_normalize_edge(u, v)] += 1

    for v in adjacency:
        adjacency[v].sort(reverse=True)

    start = next(v for v in graph.vertices() if graph.grau(v) > 0)
    stack = [start]
    circuit: List[int] = []

    while stack:
        u = stack[-1]
        while adjacency[u] and edge_count[_normalize_edge(u, adjacency[u][-1])] == 0:
            adjacency[u].pop()
        if adjacency[u]:
            v = adjacency[u].pop()
            edge = _normalize_edge(u, v)
            if edge_count[edge] > 0:
                edge_count[edge] -= 1
                stack.append(v)
        else:
            circuit.append(stack.pop())

    circuit.reverse()
    return circuit


def format_euler_output(cycle: List[int]) -> str:
    if not cycle:
        return "0"
    return "1\n" + ",".join(map(str, cycle))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 'A1 3.py' <arquivo_grafo>")

    graph = Graph(sys.argv[1])
    print(format_euler_output(find_eulerian_cycle(graph)))


if __name__ == "__main__":
    main()
