"""
square.py - Chess Square Representation

This module defines the Square class representing a position on the chessboard and provides methods to convert the square's position 
to a bitboard representation and obtain its string representation in algebraic notation.
"""

import numpy as np

class Square:
    def __init__(self, position) -> None:
        """
        Create a Square object representing a position on the chessboard.

        Parameters:
            position (int): The position of the square on the chessboard (0 to 63).
        """
        self.position = np.uint8(position)

    @property
    def rank(self):
        """
        Get the rank (row) of the square.

        Returns:
            int: The rank of the square (0 to 7).
        """
        return int(self.position // 8)

    @property
    def file(self):
        """
        Get the file (column) of the square.

        Returns:
            int: The file of the square (0 to 7).
        """
        return int(self.position % 8)

    def to_bitboard(self) -> np.uint64:
        """
        Convert the square's position to a bitboard representation.

        Returns:
            np.uint64: A 64-bit unsigned integer with only the bit corresponding to the square set to 1.
        """
        return np.uint64(1) << self.position

    def __str__(self):
        r = self.position // 8
        f = self.position % 8
        return "%s%d" % (chr(ord('a')+f), 1+r)

    @classmethod
    def from_string(cls, square_str):
        """
        Create a Square object from a string representation.

        Parameters:
            square_str (str): The string representation of the square, e.g., "d6".

        Returns:
            Square: The Square object corresponding to the given string representation.
        """
        file_char, rank_str = square_str[0], square_str[1:]
        file = ord(file_char) - ord('a')
        rank = int(rank_str) - 1
        position = rank * 8 + file
        return cls(position)
