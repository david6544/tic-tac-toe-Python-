# tic_tac_toe/game/renderers.py

import abc

from tic_tac_toe.logic.models import GameState


class Rendered(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def renderer(self,game_state: GameState) -> None:
        """Render the current game state"""

