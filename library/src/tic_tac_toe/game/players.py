# tic_tac_toe/game/players.py
from __future__ import annotations

import abc
import time

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import (find_best, find_best_optimized, find_best_precomputed,)
from tic_tac_toe.logic.models import GameState, Mark, Move


#abstract Player class
class Player(metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    #function to make a move on the current board
    def make_move(self, game_state: GameState) -> GameState:

        #checks if the current player is the right one / else invalid
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more available moves")
        else:
            raise InvalidMove("It's the other players turn")

    # Abstract method to get the move
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""

# Computer's abstract class
class ComputerPlayer(Player, metaclass=abc.ABCMeta):

    # creates mark and initialises the slight delay to make it feel more natural
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    # returns current computer move
    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    #Abstract method to get computer move
    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer's Move in the given game state."""


    # Random Computer Player Type, only makes random moves
class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
            return game_state.make_random_move()


    # minimax computer player type, makes unbeatable moves by
    # either making a random move to start or finding the best move

    #Simple Minimax (No random move first)
class MinimaxPlayerV1(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return find_best(game_state)
        
    # Minimax + Alpha_beta (No random move first)
class MinimaxPlayerV2(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return find_best_optimized(game_state)
    
    # Random move first with AlphaBeta and Minimax
class MinimaxPlayerV3(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_optimized(game_state)
    
    # Precomputed Movelist
class MinimaxPlayerV4(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_precomputed(game_state)
        
#Set which version of minimax the program will use
MinimaxPlayer = MinimaxPlayerV4