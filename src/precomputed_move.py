"""
precomputed_move.py - Chess Moves Precomputation

This module provides functions and precomputed data for generating legal moves for different chess pieces on a chessboard.
The precomputed data includes masks for each rank and file, diagonal and anti-diagonal masks, and precomputed moves for kings and knights.
The module also defines functions for precomputing pawn moves and captures, as well as calculating first rank moves for pieces based on the occupancy of the rank.
"""


import numpy as np
from square import Square
from enums import File, Rank, Color
import utils

# Define an empty bitboard to represent an empty chessboard
EMPTY_BB = np.uint64(0)

# Precompute RANKS and FILES bitboards for efficient move generation
RANKS = np.uint64(0x00000000000000FF) << np.arange(8, dtype=np.uint64) * 8
FILES = np.uint64(0x0101010101010101) << np.arange(8, dtype=np.uint64)

# Precompute masks for each rank and file
RANK_MASKS = RANKS.repeat(8)
FILE_MASKS = np.tile(FILES, 8)

DIAG = np.uint64(0x8040201008040201)
ANTIDIAG = np.uint64(0x0102040810204080)

CENTER = np.uint64(0x00003C3C3C3C0000)

def compute_diag_mask(index: np.uint8) -> np.uint64:
    """
    Compute the diagonal mask for the given index 'i'.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).

    Returns:
        np.uint64: Bitboard representing the diagonal mask for the given index.
    """
    diag = 8*(index & 7) - (index & 56)
    n = -diag & (diag >> 31)
    s = diag & (-diag >> 31)
    return (DIAG >> np.uint8(s)) << np.uint8(n)

DIAG_MASKS = np.fromiter(
        (compute_diag_mask(i) for i in range(64)),
        dtype=np.uint64,
        count=64)

def compute_antidiag_mask(index: np.uint8) -> np.uint64:
    """
    Compute the anti-diagonal mask for the given index 'i'.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).

    Returns:
        np.uint64: Bitboard representing the anti-diagonal mask for the given index.
    """
    diag = 56 - 8*(index & 7) - (index & 56)
    n = -diag & (diag >> 31)
    s = diag & (-diag >> 31)
    return (ANTIDIAG >> np.uint8(s)) << np.uint8(n)

ANTIDIAG_MASKS = np.fromiter(
        (compute_antidiag_mask(i) for i in range(64)),
        dtype=np.uint64,
        count=64)

def precompute_kings_move(index: np.uint8) -> np.uint64:
    """
    Precompute the king's moves for a given square index on the chessboard.

    Parameters:
        index (np.uint8): The index of the square on the chessboard (0 to 63).
s
    Returns:
        np.uint64: A bitboard representing all possible moves for the king from the given square.
    """
    square = Square(index)
    bitboard = square.to_bitboard()

    # Calculate possible moves in different directions using bitwise operations
    w = (bitboard & ~FILES[File.A]) >> np.uint8(1)
    nw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.EIGHT]) << np.uint8(7)
    n = (bitboard & ~RANKS[Rank.EIGHT]) << np.uint8(8)
    ne = (bitboard & ~FILES[File.H] & ~RANKS[Rank.EIGHT]) << np.uint8(9)
    e = (bitboard & ~FILES[File.H]) << np.uint8(1)
    se = (bitboard & ~FILES[File.H] & ~RANKS[Rank.ONE]) >> np.uint8(7)
    s = (bitboard & ~RANKS[Rank.ONE]) >> np.uint8(8)
    sw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.ONE]) >> np.uint8(9)

    # Combine all possible moves to get the final moves for the king from the given square
    return w | nw | n | ne | e | se | s | sw

# Precompute king moves for all squares on the chessboard
KING_MOVES = np.fromiter(
    (precompute_kings_move(i) for i in range(64)),
    dtype=np.uint64,
    count=64
)

def precompute_knights_move(index: np.uint8) -> np.uint64:
    """
    Precompute the knight's moves for a given square index on the chessboard.

    Parameters:
        index (np.uint8): The index of the square on the chessboard (0 to 63).

    Returns:
        np.uint64: A bitboard representing all possible moves for the knight from the given square.
    """
    square = Square(index)
    bitboard = square.to_bitboard()

    # Calculate possible moves in different directions using bitwise operations
    wn = (bitboard & ~FILES[File.A] & ~FILES[File.B] & ~RANKS[Rank.EIGHT]) << np.uint8(6)
    ws = (bitboard & ~FILES[File.A] & ~FILES[File.B] & ~RANKS[Rank.ONE]) >> np.uint8(10)

    nw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.SEVEN] & ~RANKS[Rank.EIGHT]) << np.uint8(15)
    ne = (bitboard & ~FILES[File.H] & ~RANKS[Rank.SEVEN] & ~RANKS[Rank.EIGHT]) << np.uint8(17)

    en = (bitboard & ~FILES[File.G] & ~FILES[File.H] & ~RANKS[Rank.EIGHT]) << np.uint8(10)
    es = (bitboard & ~FILES[File.G] & ~FILES[File.H] & ~RANKS[Rank.ONE]) >> np.uint8(6)

    se = (bitboard & ~FILES[File.H] & ~RANKS[Rank.ONE] & ~RANKS[Rank.TWO]) >> np.uint8(15)
    sw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.ONE] & ~RANKS[Rank.TWO]) >> np.uint8(17)

    return wn | ws | nw | ne | en | es | se | sw

KNIGHT_MOVES = np.fromiter(
    (precompute_knights_move(i) for i in range(64)),
    dtype=np.uint64,
    count=64
)

def precompute_pawns_move(index: np.uint8, color: Color) -> np.uint64:
    """
    Precompute the pawn's moves for a given square index on the chessboard.

    Parameters:
        index (np.uint8): The index of the square on the chessboard (0 to 63).
        color (Color): The color of the pawn

    Returns:
        np.uint64: A bitboard representing all possible moves for the pawn from the given square.
    """
    square = Square(index)
    bitboard = square.to_bitboard()

    if color == Color.WHITE:
        single_push = (bitboard & ~RANKS[Rank.EIGHT]) << np.uint8(8)
        double_push = (single_push & RANKS[Rank.THREE]) << np.uint8(8)
    else: # Color = BLACK
        single_push = (bitboard & ~RANKS[Rank.ONE]) >> np.uint8(8)
        double_push = (single_push & RANKS[Rank.SIX]) >> np.uint8(8)
    
    return single_push | double_push

def precompute_pawns_capture(index: np.uint8, color: Color) -> np.uint64:
    """
    Precompute the pawn's capture for a given square index on the chessboard.

    Parameters:
        index (np.uint8): The index of the square on the chessboard (0 to 63).
        color (Color): The color of the pawn

    Returns:
        np.uint64: A bitboard representing all possible moves for the pawn from the given square.
    """
    square = Square(index)
    bitboard = square.to_bitboard()
    
    if color == Color.WHITE:
        capture = ((bitboard & ~FILES[File.A] & ~RANKS[Rank.EIGHT]) << np.uint8(7) | (bitboard & ~FILES[File.H] & ~RANKS[Rank.EIGHT]) << np.uint8(9))
    else: # Color = BLACK
        capture = ((bitboard & ~FILES[File.A] & ~RANKS[Rank.ONE]) >> np.uint8(9) | (bitboard & ~FILES[File.H] & ~RANKS[Rank.ONE]) >> np.uint8(7))

    return capture

PAWN_MOVE = np.fromiter(
    (precompute_pawns_move(i, color)  for color in Color for i in range(64)),
    dtype=np.uint64,
    count=2*64
)
PAWN_MOVE.shape = (2,64)

PAWN_CAPTURE = np.fromiter(
    (precompute_pawns_capture(i, color)  for color in Color for i in range(64)),
    dtype=np.uint64,
    count=2*64
)
PAWN_CAPTURE.shape = (2,64)

def compute_first_rank_moves(square_index: np.uint8, occupancy: np.uint8) -> np.uint8:
    """
    Calculate the first rank moves for a given square on a rank based on the occupancy of the rank.

    Parameters:
        square_index (np.uint8): The index of the square (0 to 7).
        occupancy (np.uint8): 8-bit number representing the occupancy of the rank.

    Returns:
        np.uint8: First rank moves (as uint8).

    """

    # Define left_ray and right_ray lambda functions to handle the shifts
    move_left = lambda x: x - np.uint8(1)
    move_right = lambda x: (~x) & ~(x - np.uint8(1))

    # Create a bitboard representing the square and cast the occupancy to np.uint8
    square_bitboard = np.uint8(1) << np.uint8(square_index)
    occupancy = np.uint8(occupancy)

    # Calculate left attacks and left blockers
    left_attacks = move_left(square_bitboard)
    left_blockers = left_attacks & occupancy

    # If there are left blockers, find the leftmost blocker and remove it from left_attacks
    if left_blockers != np.uint8(0):
        leftmost_blocker = np.uint8(1) << utils.msb_bitscan(np.uint64(left_blockers))
        left_garbage = move_left(leftmost_blocker)
        left_attacks ^= left_garbage

    # Calculate right attacks and right blockers
    right_attacks = move_right(square_bitboard)
    right_blockers = right_attacks & occupancy

    # If there are right blockers, find the rightmost blocker and remove it from right_attacks
    if right_blockers != np.uint8(0):
        rightmost_blocker = np.uint8(1) << utils.lsb_bitscan(np.uint64(right_blockers))
        right_garbage = move_right(rightmost_blocker)
        right_attacks ^= right_garbage

    # Combine left_attacks and right_attacks to get the final result
    return left_attacks ^ right_attacks

FIRST_RANK_MOVES = np.fromiter(
        (compute_first_rank_moves(i, occ)
            for i in range(8) # 8 squares in a rank 
            for occ in range(256)), # 2^8 = 256 possible occupancies of a rank
        dtype=np.uint8,
        count=8*256)
FIRST_RANK_MOVES.shape = (8,256)


if __name__ == "__main__":
    print(DIAG)

