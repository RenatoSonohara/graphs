from __future__ import annotations

from collections.abc import Iterable
from math import inf
from typing import Dict, List, Tuple


class Graph:
    """Representa um grafo não-dirigido e ponderado com vértices 1..n.

    Estruturas principais:
    - _labels[v] -> rótulo do vértice v (lista 1-indexada)
    - _adj[u][v] -> peso da aresta {u, v}

    Essa escolha permite O(1) médio para haAresta(u,v), peso(u,v), grau(v),
    rotulo(v) e acesso aos vizinhos.
    """

    def __init__(self, file_path: str | None = None) -> None:
        self._n: int = 0
        self._m: int = 0
        self._labels: List[str] = [""]
        self._adj: List[Dict[int, float]] = [dict()]
        if file_path is not None:
            self.ler(file_path)

    def qtdVertices(self) -> int:
        return self._n

    def qtdArestas(self) -> int:
        return self._m

    def grau(self, v: int) -> int:
        self._validate_vertex(v)
        return len(self._adj[v])

    def rotulo(self, v: int) -> str:
        self._validate_vertex(v)
        return self._labels[v]

    def vizinhos(self, v: int) -> List[int]:
        self._validate_vertex(v)
        return sorted(self._adj[v].keys())

    def haAresta(self, u: int, v: int) -> bool:
        self._validate_vertex(u)
        self._validate_vertex(v)
        return v in self._adj[u]

    def peso(self, u: int, v: int) -> float:
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._adj[u].get(v, inf)

    def ler(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("Arquivo de grafo vazio.")
        if not lines[0].lower().startswith("*vertices"):
            raise ValueError("Primeira linha deve estar no formato '*vertices n'.")

        parts = lines[0].split()
        if len(parts) != 2:
            raise ValueError("Linha '*vertices' inválida.")

        self._n = int(parts[1])
        self._m = 0
        self._labels = [""] * (self._n + 1)
        self._adj = [dict() for _ in range(self._n + 1)]

        i = 1
        while i < len(lines) and lines[i].lower() != "*edges":
            idx_str, label = self._parse_vertex_line(lines[i])
            idx = int(idx_str)
            if not 1 <= idx <= self._n:
                raise ValueError(f"Índice de vértice fora do intervalo: {idx}")
            self._labels[idx] = label
            i += 1

        if i == len(lines) or lines[i].lower() != "*edges":
            raise ValueError("Arquivo deve conter a linha '*edges'.")

        for v in range(1, self._n + 1):
            if self._labels[v] == "":
                raise ValueError(f"Rótulo ausente para o vértice {v}.")

        for edge_line in lines[i + 1 :]:
            u, v, w = self._parse_edge_line(edge_line)
            self._add_edge(u, v, w)

    def vertices(self) -> range:
        return range(1, self._n + 1)

    def edges(self) -> Iterable[Tuple[int, int, float]]:
        for u in self.vertices():
            for v, w in self._adj[u].items():
                if u < v:
                    yield u, v, w

    def _add_edge(self, u: int, v: int, w: float) -> None:
        self._validate_vertex(u)
        self._validate_vertex(v)
        if u == v:
            if v not in self._adj[u]:
                self._m += 1
            self._adj[u][v] = w
            return
        if v not in self._adj[u]:
            self._m += 1
        self._adj[u][v] = w
        self._adj[v][u] = w

    @staticmethod
    def _parse_vertex_line(line: str) -> Tuple[str, str]:
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Linha de vértice inválida: {line}")
        return parts[0], parts[1].strip().strip('"')

    @staticmethod
    def _parse_edge_line(line: str) -> Tuple[int, int, float]:
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Linha de aresta inválida: {line}")
        u = int(parts[0])
        v = int(parts[1])
        w = float(parts[2].replace(",", "."))
        return u, v, w

    def _validate_vertex(self, v: int) -> None:
        if not 1 <= v <= self._n:
            raise ValueError(f"Vértice inválido: {v}")
