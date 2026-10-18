from typing import Tuple, List, Optional
from search_lib.core import State, Action, Problem

class RoboState(State):
    """Guarda a posição e a direção do robô (N, S, E, O)."""
    def __init__(self, x: int, y: int, direcao: str):
        self.x = x
        self.y = y
        self.direcao = direcao

    def __hash__(self):
        return hash((self.x, self.y, self.direcao))

    def __eq__(self, other):
        return isinstance(other, RoboState) and \
               self.x == other.x and self.y == other.y and self.direcao == other.direcao

class GirarAction(Action):
    """Roda o robô 90 graus (sentido horário ou anti-horário)[cite: 12]."""
    def __init__(self, sentido: str):
        self.sentido = sentido # 'horario' ou 'anti-horario'
        self.bussola = ['N', 'E', 'S', 'O']

    def apply(self, state: RoboState) -> Optional[Tuple[RoboState, float]]:
        idx = self.bussola.index(state.direcao)
        if self.sentido == 'horario':
            nova_direcao = self.bussola[(idx + 1) % 4]
        else:
            nova_direcao = self.bussola[(idx - 1) % 4]
        
        # O custo de girar é 1
        return RoboState(state.x, state.y, nova_direcao), 1.0

class MoverFrenteAction(Action):
    """Move o robô uma célula na direção para a qual está virado[cite: 12]."""
    def apply(self, state: RoboState) -> Optional[Tuple[RoboState, float]]:
        dx, dy = 0, 0
        if state.direcao == 'N': dy = 1
        elif state.direcao == 'S': dy = -1
        elif state.direcao == 'E': dx = 1
        elif state.direcao == 'O': dx = -1

        # NOTA: Numa versão final, deves validar se o robô não sai dos limites do grid (map_limits).
        # Custo de avançar é 1
        return RoboState(state.x + dx, state.y + dy, state.direcao), 1.0

class RoboGridProblem(Problem):
    """Problema de navegação do robô no grid[cite: 12]."""
    def __init__(self, inicial: Tuple[int, int, str], objetivo_xy: Tuple[int, int], limites: Tuple[int, int]):
        self.estado_inicial = RoboState(inicial[0], inicial[1], inicial[2])
        self.objetivo_xy = objetivo_xy # Apenas a posição importa para o objetivo
        self.limites_x, self.limites_y = limites
        
        self._acoes_disponiveis = [
            GirarAction('horario'),
            GirarAction('anti-horario'),
            MoverFrenteAction()
        ]

    def start_state(self) -> State:
        return self.estado_inicial

    def is_goal(self, state: RoboState) -> bool:
        """Chegou ao destino (não importa a direção)."""
        return (state.x, state.y) == self.objetivo_xy

    def actions(self, state: RoboState) -> List[Action]:
        acoes_validas = []
        for acao in self._acoes_disponiveis:
            resultado = acao.apply(state)
            if resultado is not None:
                novo_estado, _ = resultado
                # Valida os limites do mapa
                if 0 <= novo_estado.x < self.limites_x and 0 <= novo_estado.y < self.limites_y:
                    acoes_validas.append(acao)
        return acoes_validas