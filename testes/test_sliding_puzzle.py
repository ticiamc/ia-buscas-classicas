from problemas.sliding_puzzle import SlidingPuzzle, SlidingPuzzleState
from search_lib.algorithms.bfs_tree import BFS
from search_lib.algorithms.dls_tree import DLS


def test_estado_objetivo():
    # Tabuleiro inicial já igual ao objetivo
    inicial = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    
    problema = SlidingPuzzle(inicial, objetivo)
    estado_inicial = problema.start_state()
    
    # Verifica se a classe reconhece que a meta foi atingida
    assert problema.is_goal(estado_inicial) == True

def test_acoes_possiveis_meio_tabuleiro():
    # Peça vazia (0) no meio: pode mover para CIMA, BAIXO, ESQUERDA e DIREITA
    inicial = ((1, 2, 3), (4, 0, 5), (6, 7, 8))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    
    problema = SlidingPuzzle(inicial, objetivo)
    estado_inicial = problema.start_state()
    acoes = problema.actions(estado_inicial)
    
    assert len(acoes) == 4

def test_acoes_possiveis_canto():
    # Peça vazia (0) no canto inferior direito: só pode mover CIMA e ESQUERDA
    inicial = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    
    problema = SlidingPuzzle(inicial, objetivo)
    estado_inicial = problema.start_state()
    acoes = problema.actions(estado_inicial)
    
    assert len(acoes) == 2

def test_solucao_bfs_um_passo():
    # O 8 move-se para a esquerda para resolver
    inicial = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    
    problema = SlidingPuzzle(inicial, objetivo)
    estado_inicial = problema.start_state()
    
    # Instancia a estratégia e executa a busca
    estrategia = BFS(problema)
    resultado = estrategia.search(estado_inicial)
    
    # Validações estruturadas 
    assert resultado.solution_node is not None, "O BFS não encontrou solução"
    assert problema.is_goal(resultado.solution_node.state) == True
    
    # Verifica se as métricas foram registadas corretamente
    assert resultado.metrics.nodes_generated > 0
    assert resultado.metrics.execution_time > 0


def test_solucao_bfs_4x4_um_passo():
    """Testa um tabuleiro 4x4 a um movimento de distância do objetivo."""
    # O espaço (0) está na última linha, penúltima coluna. Deve mover o 15 para a esquerda.
    inicial = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 0, 15)
    )
    objetivo = (
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14, 15, 0)
    )
    
    problema = SlidingPuzzle(inicial, objetivo)
    resultado = BFS(problema).search(problema.start_state())
    
    assert resultado.solution_node is not None
    assert problema.is_goal(resultado.solution_node.state) == True

def test_solucao_bfs_caminho_minimo():
    """O BFS deve encontrar o caminho com o menor número de movimentos."""
    # O vazio precisa ir para a DIREITA, DIREITA e BAIXO: 3 movimentos.
    inicial = ((1, 2, 3), (0, 4, 5), (7, 8, 6))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    problema = SlidingPuzzle(inicial, objetivo)
    resultado = BFS(problema).search(problema.start_state())

    assert resultado.solution_node is not None
    caminho = [acao.direction for acao in resultado.solution_node.get_path()]
    assert caminho == ["DIREITA", "DIREITA", "BAIXO"]
    assert resultado.solution_node.cost == 3.0


def test_solucao_dls_dentro_do_limite():
    """
    O DFS em árvore não guarda estados visitados e pode entrar em loop no puzzle
    (ex.: ESQUERDA, DIREITA, ESQUERDA...). O DLS limita a profundidade e sempre termina.
    """
    inicial = ((1, 2, 3), (0, 4, 5), (7, 8, 6))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    problema = SlidingPuzzle(inicial, objetivo)
    resultado = DLS(problema, depth_limit=3).search(problema.start_state())

    assert resultado.solution_node is not None
    assert problema.is_goal(resultado.solution_node.state) == True
    assert resultado.solution_node.depth <= 3


def test_dls_limite_insuficiente():
    """Com limite menor que a distância da solução, o DLS termina sem encontrá-la."""
    inicial = ((1, 2, 3), (0, 4, 5), (7, 8, 6))
    objetivo = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    problema = SlidingPuzzle(inicial, objetivo)
    resultado = DLS(problema, depth_limit=2).search(problema.start_state())

    assert resultado.solution_node is None
