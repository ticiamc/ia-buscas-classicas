from problemas.robo_grid import RoboGridProblem, RoboState
from search_lib.algorithms.bfs_tree import BFS

def test_solucao_robo_bfs():
    """Testa se o robô consegue virar e andar até o objetivo."""
    # Começa no ponto (0,0) virado para o Norte (N)
    inicial = (0, 0, 'N')
    # O objetivo é chegar no ponto (1, 1) num grid de tamanho 3x3
    objetivo = (1, 1)
    limites = (3, 3)
    
    problema = RoboGridProblem(inicial, objetivo, limites)
    estrategia = BFS(problema)
    resultado = estrategia.search(problema.start_state())
    
    assert resultado.solution_node is not None, "O BFS não encontrou solução para o robô"
    assert problema.is_goal(resultado.solution_node.state) == True


def test_robo_na_borda_nao_cai():
    """Verifica se o robô não gera ações que o fariam sair do mapa."""
    # Robô na quina superior direita (2, 2) num mapa 3x3, virado pro Norte.
    # O próximo passo pra frente seria (2, 3), que é fora do grid.
    inicial = (2, 2, 'N')
    objetivo = (0, 0)
    limites = (3, 3) 
    
    problema = RoboGridProblem(inicial, objetivo, limites)
    estado_borda = problema.start_state()
    
    acoes = problema.actions(estado_borda)
    
    # Ele só deve ter 2 ações válidas (Girar horário e Girar anti-horário).
    # A ação MoverFrente deve ter sido descartada pelo return None.
    assert len(acoes) == 2
    # Confirma que nenhuma das ações disponíveis é MoverFrente
    from problemas.robo_grid import MoverFrenteAction
    for acao in acoes:
        assert not isinstance(acao, MoverFrenteAction)

def test_mover_frente_fora_do_grid_retorna_none():
    """A própria ação recusa o movimento que tira o robô do grid."""
    from problemas.robo_grid import MoverFrenteAction
    acao = MoverFrenteAction(limites=(3, 3))

    assert acao.apply(RoboState(2, 2, 'N')) is None
    assert acao.apply(RoboState(0, 0, 'O')) is None
    assert acao.apply(RoboState(1, 1, 'N')) == (RoboState(1, 2, 'N'), 1.0)


def test_solucao_robo_bfs_caminho_minimo():
    """De (0,0) virado para o Norte até (1,1): avançar, girar e avançar."""
    problema = RoboGridProblem((0, 0, 'N'), (1, 1), (3, 3))
    resultado = BFS(problema).search(problema.start_state())

    assert resultado.solution_node is not None
    assert resultado.solution_node.depth == 3
