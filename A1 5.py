from __future__ import annotations

import sys
from math import inf, isinf
from typing import List

from graph import Graph


def floyd_warshall(graph: Graph) -> List[List[float]]:
    n = graph.qtdVertices()
    dist = [[inf] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dist[i][i] = 0.0

    for u, v, w in graph.edges():
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            dik = dist[i][k]
            if isinf(dik):
                continue
            row_i = dist[i]
            row_k = dist[k]
            for j in range(1, n + 1):
                candidate = dik + row_k[j]
                if candidate < row_i[j]:
                    row_i[j] = candidate
    return dist


def _format_distance(value: float) -> str:
    if isinf(value):
        return "inf"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def format_floyd_output(graph: Graph) -> str:
    dist = floyd_warshall(graph)
    lines = []
    for i in graph.vertices():
        line = ",".join(_format_distance(dist[i][j]) for j in graph.vertices())
        lines.append(f"{i}:{line}")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 'A1 5.py' <arquivo_grafo>")

    graph = Graph(sys.argv[1])
    print(format_floyd_output(graph))


if __name__ == "__main__":
    main()
