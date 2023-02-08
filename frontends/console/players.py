# fronends/console/players.py

import re

from tic_tac_toe.game.players import Player
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Move

# sets up the player
class ConsolePlayer(Player):

    def get_move(self, game_state: GameState) -> Move | None:

        # while the game isnt over, allows the player to make a move and validates it
        while not game_state.game_over:
            try:
                index = grid_to_index(input(f"{self.mark}'s move: ").strip())
            except ValueError:
                print("Please provide coordinates in the form A1 or 1A")
            else:
                try:
                    return game_state.make_move_to(index)
                except InvalidMove:
                    print("That cell is already occupied.")
        return None
    
    # checks whether or not a valid move was played, A1, a1 etc.
def grid_to_index(grid: str) -> int:
    if re.match(r"[abcABC][123]", grid):
        col,row = grid
    elif re.match(r"[123][abcABC]", grid):
        col,row = grid
    else:
        raise ValueError("Invalid Grid Coordinates. ")
    return 3 * (int(row) - 1) + (ord(col.upper()) - ord("A"))


