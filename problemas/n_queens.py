from typing import Tuple, List, Optional
from search_lib.core import State, Action, Problem

class NQueensState(State):
    """
    Guarda o estado do tabuleiro. 
    A tupla 'queens' guarda a linha de cada rainha. O índice é a coluna.
    Ex: (1, 3, 0) -> Rainha na col 0 linha 1, col 1 linha 3, col 2 linha 0.
    """
    def __init__(self, queens: Tuple[int, ...], n: int):
        self.queens = queens
        self.n = n

    def __hash__(self):
        return hash(self.queens)

    def __eq__(self, other):
        return isinstance(other, NQueensState) and self.queens == other.queens

class PutQueenAction(Action):
    """Ação de colocar uma rainha numa linha segura da próxima coluna."""
    def __init__(self, row: int):
        self.row = row

    def apply(self, state: NQueensState) -> Optional[Tuple[NQueensState, float]]:
        coluna_atual = len(state.queens)
        
        # Verifica se a nova rainha sofrerá ataque das anteriores
        for c, r in enumerate(state.queens):
            # Sofre ataque se estiver na mesma linha ou na mesma diagonal
            if r == self.row or abs(r - self.row) == abs(c - coluna_atual):
                return None # Ação inválida, gera ataque
        
        novas_rainhas = state.queens + (self.row,)
        return NQueensState(novas_rainhas, state.n), 1.0

class NQueensProblem(Problem):
    def __init__(self, n: int = 8):
        self.n = n
        self.initial_state = NQueensState((), n) # Começa com tabuleiro vazio

    def start_state(self) -> State:
        """Atalho para o atributo initial_state (o mesmo nome usado nos exemplos da search_lib)."""
        return self.initial_state

    def is_goal(self, state: NQueensState) -> bool:
        # O objetivo é ter colocado as N rainhas com sucesso
        return len(state.queens) == self.n

    def actions(self, state: NQueensState) -> List[Action]:
        if self.is_goal(state):
            return []
        
        acoes_validas = []
        # Tenta colocar uma rainha em cada uma das 'n' linhas da próxima coluna
        for r in range(self.n):
            acao = PutQueenAction(r)
            if acao.apply(state) is not None:
                acoes_validas.append(acao)
        return acoes_validas