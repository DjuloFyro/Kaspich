import numpy as np

class Square:
    def __init__(self, position) -> None:
        """
        Create a Square object representing a position on the chessboard.

        Parameters:
            position (int): The position of the square on the chessboard (0 to 63).
        """
        self.position = np.uint8(position)

    def to_bitboard(self) -> np.uint64:
        """
        Convert the square's position to a bitboard representation.

        Returns:
            np.uint64: A 64-bit unsigned integer with only the bit corresponding to the square set to 1.
        """
        return np.uint64(1) << self.position