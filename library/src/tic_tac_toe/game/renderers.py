# tic_tac_toe/game/renderers.py

import abc

from tic_tac_toe.logic.models import GameState

#abstract renderer for the UI
class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, game_state: GameState) -> None:
        """Render the current game state"""
