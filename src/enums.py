"""
enums.py - Chess Components Representation

This file defines various enumerations used in a chess implementation.

- PieceType: Enumeration representing the type of a chess piece.
- Color: Enumeration representing the color of a chess piece.
- Rank: Enumeration representing the ranks (rows) on a chessboard.
- File: Enumeration representing the files (columns) on a chessboard.
"""

from enum import IntEnum

class PieceType(IntEnum):
    """Enumeration representing the type of a chess piece."""
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def to_char(self) -> str:
        """Convert the PieceType enum value to its corresponding character representation.

        Returns:
            str: The character representation of the PieceType ('p', 'n', 'b', 'r', 'q', or 'k').
        """
        if self == PieceType.PAWN:
            return 'p'
        elif self == PieceType.KNIGHT:
            return 'n'
        elif self == PieceType.BISHOP:
            return 'b'
        elif self == PieceType.ROOK:
            return 'r'
        elif self == PieceType.QUEEN:
            return 'q'
        elif self == PieceType.KING:
            return 'k'

    @classmethod
    def from_char(cls, char_repr: str) -> 'PieceType':
        """Convert the character representation to the corresponding PieceType enum value.

        Args:
            char_repr (str): The character representation of the PieceType ('p', 'n', 'b', 'r', 'q', or 'k').

        Returns:
            PieceType: The corresponding PieceType enum value.
        
        Raises:
            ValueError: If the provided character representation is not a valid PieceType.
        """
        if char_repr == 'p':
            return PieceType.PAWN
        elif char_repr == 'n':
            return PieceType.KNIGHT
        elif char_repr == 'b':
            return PieceType.BISHOP
        elif char_repr == 'r':
            return PieceType.ROOK
        elif char_repr == 'q':
            return PieceType.QUEEN
        elif char_repr == 'k':
            return PieceType.KING
        else:
            raise ValueError(f"Invalid character representation '{char_repr}' for PieceType.")

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
