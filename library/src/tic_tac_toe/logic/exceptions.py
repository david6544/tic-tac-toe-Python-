# tic_tac_toe/logic/exceptions.py


#Exception for an Invalid Game State
class InvalidGameState(Exception):
    """Raised when the game state is invalid."""

#Exception for when the player makes an invalid move
class InvalidMove(Exception):
    """Raised when the move is invalid"""

#Exception for when the game score is still not known
class UnkownGameScore(Exception):
    """Raised when the game score is still unkown"""