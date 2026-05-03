from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from graph import Graph


def load_module(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, BASE_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


A1_2 = load_module("A1_2.py", "a1_2")
A1_3 = load_module("A1_3.py", "a1_3")
A1_4 = load_module("A1_4.py", "a1_4")
A1_5 = load_module("A1_5.py", "a1_5")


GRAPH_CONTENT = textwrap.dedent(
    """\
    *vertices 5
    1 A
    2 B
    3 C
    4 D
    5 E
    *edges
    1 2 2
    1 3 5
    2 3 1
    2 4 2
    3 5 3
    4 5 1
    """
)

EULER_GRAPH_CONTENT = textwrap.dedent(
    """\
    *vertices 4
    1 A
    2 B
    3 C
    4 D
    *edges
    1 2 1
    2 3 1
    3 4 1
    4 1 1
    """
)


def create_temp_graph(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile("w", delete=False, suffix=".net", encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return tmp.name


class TestGraphRepresentation(unittest.TestCase):
    def setUp(self) -> None:
        self.graph_file = create_temp_graph(GRAPH_CONTENT)
        self.graph = Graph(self.graph_file)

    def test_basic_properties(self) -> None:
        self.assertEqual(self.graph.qtdVertices(), 5)
        self.assertEqual(self.graph.qtdArestas(), 6)
        self.assertEqual(self.graph.grau(2), 3)
        self.assertEqual(self.graph.rotulo(3), "C")
        self.assertEqual(self.graph.vizinhos(2), [1, 3, 4])
        self.assertTrue(self.graph.haAresta(1, 2))
        self.assertFalse(self.graph.haAresta(1, 5))
        self.assertEqual(self.graph.peso(2, 4), 2.0)
        self.assertEqual(self.graph.peso(1, 5), float("inf"))


class TestBFS(unittest.TestCase):
    def test_bfs_output(self) -> None:
        graph = Graph(create_temp_graph(GRAPH_CONTENT))
        output = A1_2.format_bfs_output(A1_2.bfs_levels(graph, 1))
        self.assertEqual(output, "0: 1\n1: 2,3\n2: 4,5")


class TestEulerianCycle(unittest.TestCase):
    def test_has_cycle_and_output(self) -> None:
        graph = Graph(create_temp_graph(EULER_GRAPH_CONTENT))
        cycle = A1_3.find_eulerian_cycle(graph)
        self.assertTrue(cycle)
        self.assertEqual(cycle[0], cycle[-1])
        self.assertEqual(len(cycle), graph.qtdArestas() + 1)
        self.assertTrue(A1_3.format_euler_output(cycle).startswith("1\n"))

    def test_no_cycle(self) -> None:
        graph = Graph(create_temp_graph(GRAPH_CONTENT))
        self.assertEqual(A1_3.find_eulerian_cycle(graph), [])
        self.assertEqual(A1_3.format_euler_output([]), "0")


class TestDijkstra(unittest.TestCase):
    def test_shortest_paths(self) -> None:
        graph = Graph(create_temp_graph(GRAPH_CONTENT))
        output = A1_4.format_dijkstra_output(graph, 1)
        expected = "\n".join([
            "1: 1; d=0",
            "2: 1,2; d=2",
            "3: 1,2,3; d=3",
            "4: 1,2,4; d=4",
            "5: 1,2,4,5; d=5",
        ])
        self.assertEqual(output, expected)


class TestFloydWarshall(unittest.TestCase):
    def test_all_pairs(self) -> None:
        graph = Graph(create_temp_graph(GRAPH_CONTENT))
        output = A1_5.format_floyd_output(graph)
        expected = "\n".join([
            "1:0,2,3,4,5",
            "2:2,0,1,2,3",
            "3:3,1,0,3,3",
            "4:4,2,3,0,1",
            "5:5,3,3,1,0",
        ])
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
