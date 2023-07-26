"""
move_generation.py - Chess Moves Generation

This file contains functions for generating rank, file, diag and antidiag moves for different chess pieces on the board.
"""

import numpy as np
from precomputed_move import *


def generate_diag_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible diagonal moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible diagonal moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = DIAG_MASKS[index] & occupancy # isolate diagonal occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to diagonal
    return DIAG_MASKS[index] & occupancy


def generate_antidiag_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible antidiagonal moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible antidiagonal moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = ANTIDIAG_MASKS[index] & occupancy # isolate antidiagonal occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to antidiagonal
    return ANTIDIAG_MASKS[index] & occupancy


def generate_rank_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible rank moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible rank moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = RANK_MASKS[index] & occupancy # isolate rank occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to rank
    return RANK_MASKS[index] & occupancy


def generate_file_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible file moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible file moves for the given square.
    """
    file = index & np.uint8(7)
    # Shift to A file
    occupancy = FILES[File.A] & (occupancy >> file)
    # Map occupancy and index to first rank
    occupancy = (DIAG * occupancy) >> np.uint8(56)
    first_rank_index = (index ^ np.uint8(56)) >> np.uint8(3)
    # Lookup moveset and map back to H file
    occupancy = DIAG * FIRST_RANK_MOVES[first_rank_index][occupancy]
    # Isolate H file and shift back to original file
    return (FILES[File.H] & occupancy) >> (file ^ np.uint8(7))

