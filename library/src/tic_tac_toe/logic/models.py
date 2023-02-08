# tic_tac_toe/logic/models.py

import enum
import random
import re
from dataclasses import dataclass
from functools import  cached_property


from tic_tac_toe.logic.exceptions import InvalidMove, UnkownGameScore
from tic_tac_toe.logic.validators import validate_game_state,validate_grid


# all winning patterns by a side
WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)


# Mark class, strings of X or O
class Mark(str, enum.Enum):
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT


# Sets up the Grid, in a linear string form, "_________"
@dataclass(frozen=True)
class Grid:
    cells: str = " " * 9

    #validates the grid
    def __post_init__(self) -> None:
        validate_grid(self)

    # counts for how many X's and O's
    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")

    @cached_property
    def o_count(self) -> int:
        return self.cells.count("O")

    # Counts how many empty cells
    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")


# Move class, 
@dataclass(frozen=True)
class Move:
    mark: Mark
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"


# current Game State
@dataclass(frozen=True)
class GameState:
    #Initialises the Grid and sets the starting mark to X
    grid: Grid
    starting_mark: Mark = Mark("X")


    def __post_init__(self) -> None:
        validate_game_state(self)

    # Checks who's turn it is and checks whether or not the amount of X and Os is valid
    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other

    #function to check if the game is started or not
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9

    #function to make sure game is over, validating winner
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie

    # tie function
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0

    # goes through and checks the winner among Winnning Patterns
    @cached_property
    def winner(self) -> Mark | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None

    # Replaces cells with the current mark, checks for win
    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start() for match in re.finditer(r"\?", pattern)
                    ]
        return []

    #lists out possible moves that the player can make
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves

    # returns a random choice among possible moves
    def make_random_move(self) -> Move | None:
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None

    # Checks whether or not a cell is empty before making a move
    def make_move_to(self, index: int) -> Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(

            # makes a move by changing the existing grid
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=GameState(
                Grid(
                    self.grid.cells[:index]
                    + self.current_mark
                    + self.grid.cells[index + 1 :]
                ),
                self.starting_mark,
            ),
        )
    
    # evaluates the winner, called by various functions
    def evaluate_score(self, mark: Mark) -> int:
        if self.game_over:
            if self.tie:
                return 0
            if self.winner is mark:
                return 1
            else:
                return -1
        raise UnkownGameScore("Game is not over yet")


