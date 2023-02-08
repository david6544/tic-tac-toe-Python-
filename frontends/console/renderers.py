# frontends/console/renderers.py

import textwrap
from typing import Iterable

from tic_tac_toe.game.renderers import Renderer
from tic_tac_toe.logic.models import GameState


# renders the ui for the terminal
class ConsoleRenderer(Renderer):
    def render(self, game_state: GameState) -> None:
        # clears the screen on start
        clear_screen()

        # upon win of the player or draw
        if game_state.winner:
            print_blinking(game_state.grid.cells, game_state.winning_cells)
            print(f"{game_state.winner} wins \N{party popper}")
        else:
            print_solid(game_state.grid.cells)
            if game_state.tie:
                print("No one wins this time \N{neutral face}")


#clears the screen
def clear_screen() -> None:
    print("\033c", end="")


# blinks on waiting input
def blink(text: str) -> str:
    return f"\033[5m{text}\033[0m"


# prints out the mutable cells
def print_blinking(cells: Iterable[str], positions: Iterable[int]) -> None:
    mutable_cells = list(cells)
    for position in positions:
        mutable_cells[position] = blink(mutable_cells[position])
    print_solid(mutable_cells)


# prints the solid cells and their index
def print_solid(cells: Iterable[str]) -> None:
    print(
        textwrap.dedent(
            """\
             A   B   C
           ------------
        1 ┆  {0} │ {1} │ {2}
          ┆ ───┼───┼───
        2 ┆  {3} │ {4} │ {5}
          ┆ ───┼───┼───
        3 ┆  {6} │ {7} │ {8}
    """
        ).format(*cells)
    )
