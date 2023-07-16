import numpy as np

from board import Board
from square import Square
from precomputed_move import *


def generate_pawn_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the pawn on the given square
    pass

def generate_knight_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the knight on the given square
    pass

def generate_bishop_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the bishop on the given square
    pass

def generate_rook_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the rook on the given square
    pass

def generate_queen_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the queen on the given square
    pass

def generate_king_moves(board: Board, square: Square) -> np.array:
    # Generate legal moves for the king on the given square
    KING_MOVES[square.position] & ~board.same_color[board.color_turn]
    pass

def generate_moves(board: Board, piece_type: str) -> np.array:
    # Generate legal moves for all pieces of the given type on the board
    pass
