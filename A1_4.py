from __future__ import annotations

import heapq
import sys
from math import inf, isinf
from typing import List, Tuple

from graph import Graph


def dijkstra(graph: Graph, source: int) -> Tuple[List[float], List[int | None]]:
    dist = [inf] * (graph.qtdVertices() + 1)
    parent: List[int | None] = [None] * (graph.qtdVertices() + 1)
    dist[source] = 0.0
    heap: list[tuple[float, int]] = [(0.0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v in graph.vizinhos(u):
            weight = graph.peso(u, v)
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))
    return dist, parent


def reconstruct_path(parent: List[int | None], target: int) -> List[int]:
    path: List[int] = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def _format_distance(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def format_dijkstra_output(graph: Graph, source: int) -> str:
    dist, parent = dijkstra(graph, source)
    lines: List[str] = []
    for v in graph.vertices():
        if isinf(dist[v]):
            lines.append(f"{v}: -; d=inf")
        else:
            path = reconstruct_path(parent, v)
            lines.append(f"{v}: {','.join(map(str, path))}; d={_format_distance(dist[v])}")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python3 'A1_4.py' <arquivo_grafo> <vertice_s>")

    graph = Graph(sys.argv[1])
    source = int(sys.argv[2])
    print(format_dijkstra_output(graph, source))


if __name__ == "__main__":
    main()
