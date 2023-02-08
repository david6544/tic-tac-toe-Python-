# tic_tac_toe/logic/minimax.py

import json
from functools import cache, partial
from importlib import resources

from tic_tac_toe.logic.models import Mark, Move, GameState, Grid


# Used in order to precompute the scores from minmax.json
class MinimaxSerializer:
    DEFAULT_FILENAME = "minimax.json"

    @staticmethod
    def key(move: Move) ->str:
        return move.before_state.grid.cells + move.after_state.grid.cells
    
    #loads the json
    @staticmethod
    @cache
    def load(filename: str = DEFAULT_FILENAME) ->dict:
        with resources.open_text(__package__,filename) as file:
            return json.load(file)
    
    #Precomputes which move with whichever Mark the computer is playing as
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

# Finds the best move by using minimax
def find_best(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(minimax,maximizer = maximizer)
    return max(game_state.possible_moves, key = bound_minimax)



# Alpha-beta method
def find_best_optimized(game_state:GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark

    # sets alpha and beta to -2 and 2 respectively
    def alpha_beta_prune(
            move: Move, alpha= -2, beta = 2, choose_highest : bool = False
    ) -> int:
        
        #evaluates the score if its the last possibility
        if move.after_state.game_over:
            return move.after_state.evaluate_score(maximizer)
        
        # if choose highest is true, evalutes the position
        if choose_highest:
            score = -2
            
            # goes through the possible moves, sets the score to the best evaluation, 
            # sets alpha to this, if alpha is better than beta immediately breaks, not looking further
            for next_move in move.after_state.possible_moves:
                evaluation = alpha_beta_prune(next_move,alpha,beta,False)
                score = max(score,evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return score
        else:
            # goes through possible moves and sets alpha beta to true, finding the smallest negative value
            score = 2
            for next_move in move.after_state.possible_moves:
                evaluation = alpha_beta_prune(next_move,alpha,beta,True)
                score = min(score,evaluation)
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            return score
    
    #returns the best possible move
    return max(game_state.possible_moves,key = alpha_beta_prune)

# goes through the precomputed list and correlated with possible moves
# immediately returns the best possible list
def find_best_precomputed(game_state: GameState) -> Move | None:
    scores = MinimaxSerializer.load()
    maximizer: Mark = game_state.current_mark
    return max(
        game_state.possible_moves,
        key = lambda move : scores[MinimaxSerializer.key(move)] [
                0 if maximizer == "X" else 1
            ],
        )


#standard minimax function
def minimax (
        move: Move, maximizer: Mark, choose_highest: bool = False
) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    return (max if choose_highest else min) (
        minimax(next_move, maximizer, not choose_highest)
        for next_move in move.after_state.possible_moves
    )