import numpy as np

from board import Board
from square import Square
from precomputed_move import *

def generate_king_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the king on the given square
    return KING_MOVES[square.position] & ~board.same_color[board.color_turn]

def generate_knight_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the knight on the given square
    return KNIGHT_MOVES[square.position] & ~board.same_color[board.color_turn]

def generate_pawn_moves(board: Board, square: Square) -> np.array:
    """
    Generate legal moves for the pawn on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the pawn.

    Returns:
        np.array: An array of bitboards representing all legal moves for the pawn.
    """
    pawn_moves = precompute_pawns_move(square.position, board.color_turn)

    # Filter out moves that collide with friendly pieces
    valid_moves = pawn_moves & ~board.all_pieces

    # For captures, filter out moves that do not capture an opponent's piece
    captures = pawn_moves & board.same_color[board.color_turn]

    return valid_moves | captures

def generate_bishop_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the bishop on the given square
    pass

def generate_rook_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the rook on the given square
    pass

def generate_queen_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the queen on the given square
    pass

def generate_moves(board: Board, piece_type: str) -> np.array:
    # Generate legal moves for all pieces of the given type on the board
    pass


