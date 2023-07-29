"""
move.py - Chess Move Representation

This file defines the Move class, representing a chess move, along with related functions.

The Move class encapsulates information about a single chess move, including the source square,
destination square, and any promotion that may occur. It provides methods to convert a Move object
to a human-readable algebraic notation string and to create a Move object from a string representation.
"""

import numpy as np
from square import Square

class Move:
    def __init__(self, src: Square, dest: Square, promo=None, en_passant: bool = False, is_castling: bool = False):
        """
        src is Square representing source square
        dst is Square representing destination square
        promo is Piece representing promotion
        """
        self.src = src
        self.dest = dest
        self.promo = promo
        self.en_passant = en_passant
        self.is_castling = is_castling

    def __str__(self):
        if self.promo:
            return "%s%s = %s" % (str(self.src), str(self.dest), self.promo.name)
        else:
            return "%s%s" % (str(self.src), str(self.dest))
    
    def from_str(s):
        """
        Convert a string representation of a chess move to a Move object.

        Parameters:
            s (str): The string representation of the move in algebraic notation, e.g., 'e2e4'.

        Returns:
            Move: The Move object representing the chess move.
        """
        src_file = np.uint8(ord(s[0]) - 97)
        src_rank = np.uint8(s[1])
        dest_file = np.uint8(ord(s[2]) - 97)
        dest_rank = np.uint8(s[3])

        square_src = Square(src_rank * 8 + src_file - 1)
        square_dest = Square(dest_rank * 8 + dest_file - 1)

        return Move(src=square_src, dest=square_dest)
    
    def is_double_push(self):
        return abs(self.src.rank - self.dest.rank) == 2
    
    def __eq__(self, other):
        """
        Override the equality operator to compare moves based on their properties.
        """
        if isinstance(other, Move):
            return self.src == other.src and self.dest == other.dest
        return False






