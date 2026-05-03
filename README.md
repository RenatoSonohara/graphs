# Atividade A1 - Grafos

Arquivos principais:
- `graph.py`: biblioteca de grafos reutilizada por todos os itens.
- `A1_2.py`: busca em largura.
- `A1_3.py`: ciclo euleriano.
- `A1_4.py`: Dijkstra.
- `A1_5.py`: Floyd-Warshall.
- `tests/test_graph_algorithms.py`: testes unitários.
- `relatorio.tex`: relatório em LaTeX pronto para Overleaf.

## Como executar os testes

```bash
python3 -m unittest discover -s tests -v
```

## Como executar cada questão

```bash
python3 "A1_2.py" exemplo.net 1
python3 "A1_3.py" exemplo.net
python3 "A1_4.py" exemplo.net 1
python3 "A1_5.py" exemplo.net
```
