import numpy as np
from square import Square
from enums import File, Rank

# Define an empty bitboard to represent an empty chessboard
EMPTY_BITBOARD = np.uint64(0)

# Precompute De Bruijn constant for efficient bit scanning
DEBRUIJN_CONSTANT = np.uint64(0x03f79d71b4cb0a89)

# Precomputed lookup tables for least significant bit (LSB) and most significant bit (MSB) indexing
LSB_LOOKUP = np.array(
    [0, 1, 48, 2, 57, 49, 28, 3, 61, 58, 50, 42, 38, 29, 17, 4,
     62, 55, 59, 36, 53, 51, 43, 22, 45, 39, 33, 30, 24, 18, 12, 5,
     63, 47, 56, 27, 60, 41, 37, 16, 54, 35, 52, 21, 44, 32, 23, 11,
     46, 26, 40, 15, 34, 20, 31, 10, 25, 14, 19, 9, 13, 8, 7, 6],
    dtype=np.uint8
)

MSB_LOOKUP = np.array(
    [0, 47, 1, 56, 48, 27, 2, 60, 57, 49, 41, 37, 28, 16, 3, 61,
     54, 58, 35, 52, 50, 42, 21, 44, 38, 32, 29, 23, 17, 11, 4, 62,
     46, 55, 26, 59, 40, 36, 15, 53, 34, 51, 20, 43, 31, 22, 10, 45,
     25, 39, 14, 33, 19, 30, 9, 24, 13, 18, 8, 12, 7, 6, 5, 63],
    dtype=np.uint8
)

def lsb_bitscan(bitboard: np.uint64):
    """Find the position of the least significant bit (LSB) set to 1 in the bitboard."""
    return LSB_LOOKUP[((bitboard & -bitboard) * DEBRUIJN_CONSTANT) >> np.uint8(58)]

def msb_bitscan(bitboard: np.uint64):
    """Find the position of the most significant bit (MSB) set to 1 in the bitboard."""
    bitboard |= bitboard >> np.uint8(1)
    bitboard |= bitboard >> np.uint8(2)
    bitboard |= bitboard >> np.uint8(4)
    bitboard |= bitboard >> np.uint8(8)
    bitboard |= bitboard >> np.uint8(16)
    bitboard |= bitboard >> np.uint8(32)
    return MSB_LOOKUP[(bitboard * DEBRUIJN_CONSTANT) >> np.uint8(58)]

def occupied_squares(bitboard: np.uint64):
    """
    Generate occupied squares (squares with a set bit - 1) in the given bitboard.

    Parameters:
        bitboard (np.uint64): The 64-bit integer representing a bitboard.

    Yields:
        Square: A Square object representing each occupied square in the bitboard.
    """
    while bitboard != EMPTY_BITBOARD:
        lsb_square = Square(lsb_bitscan(bitboard))
        yield lsb_square
        bitboard ^= lsb_square.to_bitboard()


def pop_count(bb):
    count = np.uint8(0)
    while bb != EMPTY_BITBOARD:
        count += np.uint8(1)
        bb &= bb - np.uint64(1)
    return count


# Precomputed lookup table for counting set bits in 16-bit parts
BIT_COUNT_LOOKUP = np.array(
    [bin(i).count("1") for i in range(65536)],
    dtype=np.uint8
)

def population_count(bb: np.uint64) -> np.uint8:
    """
    Calculate the population count (Hamming weight) of a 64-bit integer/bitboard.

    Parameters:
        bb (np.uint64): The 64-bit integer representing a bitboard.

    Returns:
        np.uint8: The number of bits set to 1 in the input bitboard.
    """
    # Count the number of set bits in 16-bit parts of the bitboard using lookup table
    count = BIT_COUNT_LOOKUP[bb & 0xFFFF]
    count += BIT_COUNT_LOOKUP[(bb >> 16) & 0xFFFF]
    count += BIT_COUNT_LOOKUP[(bb >> 32) & 0xFFFF]
    count += BIT_COUNT_LOOKUP[(bb >> 48) & 0xFFFF]
    return count



def is_set(bitboard: np.uint64, square: Square):
    """
    Check if a particular square is set (has a bit value of 1) in the given bitboard.

    Parameters:
        bitboard (np.uint64): The 64-bit integer representing a bitboard.
        square (Square): The square to check.

    Returns:
        bool: True if the square is set in the bitboard, False otherwise.
    """
    # Perform a bitwise AND operation between the bitboard representation of the square and the given bitboard
    # If the result is not an empty bitboard, it means the square is set in the given bitboard
    return (square.to_bitboard() & bitboard) != EMPTY_BITBOARD


def clear_square(bitboard: np.uint64, square: Square):
    """
    Clear (set to 0) the bit corresponding to a particular square in the given bitboard.

    Parameters:
        bitboard (np.uint64): The 64-bit integer representing a bitboard.
        square (Square): The square to clear.

    Returns:
        np.uint64: The modified bitboard with the square's bit cleared.
    """
    # Perform a bitwise NOT operation on the bitboard representation of the square
    # Then perform a bitwise AND operation with the given bitboard to clear the square's bit
    return (~square.to_bitboard()) & bitboard


def set_square(bitboard: np.uint64, square: Square):
    """
    Set (set to 1) the bit corresponding to a particular square in the given bitboard.

    Parameters:
        bb (np.uint64): The 64-bit integer representing a bitboard.
        square (Square): The square to set.

    Returns:
        np.uint64: The modified bitboard with the square's bit set.
    """
    # Perform a bitwise OR operation between the bitboard representation of the square and the given bitboard
    # This sets the bit corresponding to the square to 1
    return square.to_bitboard() | bitboard