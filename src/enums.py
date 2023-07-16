from enum import IntEnum

class PieceType(IntEnum):
    """Enumeration representing the type of a chess piece."""
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

class Color(IntEnum):
    """Enumeration representing the color of a chess piece."""
    WHITE = 0
    BLACK = 1

class Rank(IntEnum):
    """Enumeration representing the ranks (rows) on a chessboard."""
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7

class File(IntEnum):
    """Enumeration representing the files (columns) on a chessboard."""
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
