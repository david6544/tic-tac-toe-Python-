# tic_tac_toe/game/engine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeAlias

from tic_tac_toe.game.players import Player
from tic_tac_toe.game.renderers import Renderer
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Grid, Mark
from tic_tac_toe.logic.validators import validate_players

ErrorHandler: TypeAlias = Callable[[Exception], None]



@dataclass(frozen=True)
class TicTacToe:

    #defines the players, renderer and error handler from the files
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None


    #validates whehter or not the players are correct
    def __post_init__(self):
        validate_players(self.player1, self.player2)


    #Creates the gamestate
    def play(self, starting_mark: Mark = Mark("X")) -> None:
        game_state = GameState(Grid(), starting_mark)

        #While the gamestate is valid
        while True:

            #renders the game state / breaks if game over
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)

            # Sees if a move can be made
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)


    #returns which is the current player to make a move
    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2
