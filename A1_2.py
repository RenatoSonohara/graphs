from __future__ import annotations

import sys
from collections import deque
from typing import List

from graph import Graph


def bfs_levels(graph: Graph, source: int) -> List[List[int]]:
    visited = [False] * (graph.qtdVertices() + 1)
    level = [-1] * (graph.qtdVertices() + 1)
    queue: deque[int] = deque([source])
    visited[source] = True
    level[source] = 0
    levels: List[List[int]] = [[source]]

    while queue:
        u = queue.popleft()
        for v in graph.vizinhos(u):
            if not visited[v]:
                visited[v] = True
                level[v] = level[u] + 1
                if len(levels) <= level[v]:
                    levels.append([])
                levels[level[v]].append(v)
                queue.append(v)
    return levels


def format_bfs_output(levels: List[List[int]]) -> str:
    return "\n".join(f"{i}: {','.join(map(str, vertices))}" for i, vertices in enumerate(levels))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python3 'A1_2.py' <arquivo_grafo> <vertice_s>")

    graph_file = sys.argv[1]
    source = int(sys.argv[2])

    graph = Graph(graph_file)
    output = format_bfs_output(bfs_levels(graph, source))
    print(output)


if __name__ == "__main__":
    main()
