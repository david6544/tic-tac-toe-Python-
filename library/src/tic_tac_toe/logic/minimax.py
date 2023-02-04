# tic_tac_toe/logic/minimax.py

from functools import partial

from tic_tac_toe.logic.models import Mark, Move, GameState

def find_best(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(minimax,maximizer = maximizer)
    return max(game_state.possible_moves, key = bound_minimax)


def minimax (
        move: Move, maximizer: Mark, choose_highest: bool = False
) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    return (max if choose_highest else min) (
        minimax(next_move, maximizer, not choose_highest)
        for next_move in move.after_state.possible_moves
    )