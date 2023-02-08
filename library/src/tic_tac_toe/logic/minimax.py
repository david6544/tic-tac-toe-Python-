# tic_tac_toe/logic/minimax.py

import json
from functools import cache, partial
from importlib import resources

from tic_tac_toe.logic.models import Mark, Move, GameState, Grid

class MinimaxSerializer:
    DEFAULT_FILENAME = "minimax.json"

    @staticmethod
    def key(move: Move) ->str:
        return move.before_state.grid.cells + move.after_state.grid.cells
    
    @staticmethod
    @cache
    def load(filename: str = DEFAULT_FILENAME) ->dict:
        with resources.open_text(__package__,filename) as file:
            return json.load(file)
        
    @staticmethod
    def precompute_scores() -> dict[str, list[int]]:
        scores = {}

        def traverse(game_state: GameState) -> None:
            for move in game_state.possible_moves:
                scores[MinimaxSerializer.key(move)] = [
                    minimax(move, Mark("X")),
                    minimax(move, Mark("O")),
                ]
                traverse(move.after_state)

        traverse(GameState(Grid(),Mark("X")))
        traverse(GameState(Grid(),Mark("X")))
        
        return scores

def find_best(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(minimax,maximizer = maximizer)
    return max(game_state.possible_moves, key = bound_minimax)


def find_best_optimized(game_state:GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark

    def alpha_beta_prune(
            move: Move, alpha= -2, beta = 2, choose_highest : bool = False
    ) -> int:
        if move.after_state.game_over:
            return move.after_state.evaluate_score(maximizer)
        
        if choose_highest:
            score = -2
            for next_move in move.after_state.possible_moves:
                evaluation = alpha_beta_prune(next_move,alpha,beta,False)
                score = max(score,evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return score
        else:
            score = 2
            for next_move in move.after_state.possible_moves:
                evaluation = alpha_beta_prune(next_move,alpha,beta,True)
                score = min(score,evaluation)
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            return score
        
    return max(game_state.possible_moves,key = alpha_beta_prune)

def find_best_precomputed(game_state: GameState) -> Move | None:
    scores = MinimaxSerializer.load()
    maximizer: Mark = game_state.current_mark
    return max(
        game_state.possible_moves,
        key = lambda move : scores[MinimaxSerializer.key(move)] [
                0 if maximizer == "X" else 1
            ],
        )

def minimax (
        move: Move, maximizer: Mark, choose_highest: bool = False
) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    return (max if choose_highest else min) (
        minimax(next_move, maximizer, not choose_highest)
        for next_move in move.after_state.possible_moves
    )