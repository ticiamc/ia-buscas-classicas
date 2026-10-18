from problemas.n_queens import NQueensProblem
from search_lib.algorithms.dfs_tree import DFS

def test_n_queens_4x4():
    """Testa a solução para um tabuleiro 4x4 (n=4)."""
    problema = NQueensProblem(n=4)
    estrategia = DFS(problema)
    resultado = estrategia.search(problema.start_state())
    
    assert resultado.solution_node is not None
    assert problema.is_goal(resultado.solution_node.state) == True
    assert len(resultado.solution_node.state.queens) == 4