from typing import Tuple, List, Optional
from search_lib.core import State, Action, Problem

class SlidingPuzzleState(State):
    """
    Guarda as informações do estado (a matriz do tabuleiro).
    Usamos tuplas em vez de listas para que o estado seja imutável e 
    possa ser usado em conjuntos (sets) durante a verificação de repetições.
    """
    def __init__(self, board: Tuple[Tuple[int, ...], ...]):
        self.board = board
        self.empty_pos = self._find_empty()

    def _find_empty(self) -> Tuple[int, int]:
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0:  # 0 representa o espaço vazio
                    return (i, j)
        return (-1, -1)

    def __hash__(self):
        return hash(self.board)

    def __eq__(self, other):
        return isinstance(other, SlidingPuzzleState) and self.board == other.board

class MoveAction(Action):
    """
    Representa o movimento da peça vazia.
    """
    def __init__(self, direction: str, d_row: int, d_col: int):
        self.direction = direction
        self.d_row = d_row
        self.d_col = d_col

    def apply(self, state: SlidingPuzzleState) -> Optional[Tuple[SlidingPuzzleState, float]]:
        r, c = state.empty_pos
        new_r, new_c = r + self.d_row, c + self.d_col
        n = len(state.board)

        if 0 <= new_r < n and 0 <= new_c < n:
            new_board = [list(row) for row in state.board]
            new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
            tuple_board = tuple(tuple(row) for row in new_board)
            
            # Retorna agora uma tupla: (novo_estado, custo_da_acao)
            return SlidingPuzzleState(tuple_board), 1.0 
        
        return None

class SlidingPuzzle(Problem):
    """
    Especialização do utilizador da biblioteca que representa um espaço de estados
    Pode ser parametrizada para tabuleiros maiores ou menores
    """
    def __init__(self, initial_board: Tuple[Tuple[int, ...], ...], goal_board: Tuple[Tuple[int, ...], ...]):
        self.initial_state = SlidingPuzzleState(initial_board)
        self.goal_state = SlidingPuzzleState(goal_board)
        
        self._all_actions = [
            MoveAction("CIMA", -1, 0),
            MoveAction("BAIXO", 1, 0),
            MoveAction("ESQUERDA", 0, -1),
            MoveAction("DIREITA", 0, 1)
        ]

    def start_state(self) -> State:
        return self.initial_state

    def is_goal(self, state: SlidingPuzzleState) -> bool:
        """Teste de objetivo."""
        return state == self.goal_state

    def actions(self, state: SlidingPuzzleState) -> List[Action]:
        """Retorna o conjunto de ações possíveis num dado estado."""
        valid_actions = []
        for action in self._all_actions:
            if action.apply(state) is not None:
                valid_actions.append(action)
        return valid_actions