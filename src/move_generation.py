import numpy as np

from board import Board
from square import Square
from precomputed_move import *


def opposite_color(color):
    """
    Get the oppsite color (WHITE -> BLACK) (BLACK -> WHITE).

    Parameters:
        color (Color): The Color.

    Returns:
        Color: The opposite color.
    """
    return Color.WHITE if color == Color.BLACK else Color.BLACK

def generate_king_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the king on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the king.

    Returns:
        np.array: An array of bitboards representing all legal moves for the king.
    """
    return KING_MOVES[square.position] & ~board.same_color[board.color_turn]

def generate_knight_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the knight on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the knight.

    Returns:
        np.array: An array of bitboards representing all legal moves for the knight.
    """
    return KNIGHT_MOVES[square.position] & ~board.same_color[board.color_turn]

def generate_pawn_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the pawn on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the pawn.

    Returns:
        np.array: An array of bitboards representing all legal moves for the pawn.
    """

    # Filter out moves that collide with friendly pieces
    pawn_moves = PAWN_MOVE[board.color_turn][square.position] & ~board.all_pieces

    # For captures, filter out moves that do not capture an opponent's piece
    captures = PAWN_CAPTURE[board.color_turn][square.position] & board.same_color[opposite_color(board.color_turn)]

    return pawn_moves | captures

def generate_bishop_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the bishop on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the bishop.

    Returns:
        np.array: An array of bitboards representing all legal moves for the bishop.
    """
    pass

def generate_rook_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the rook on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the rook.

    Returns:
        np.array: An array of bitboards representing all legal moves for the rook.
    """
    pass

def generate_queen_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the queen on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the queen.

    Returns:
        np.array: An array of bitboards representing all legal moves for the queen.
    """
    pass

def generate_moves(board: Board, piece_type: str) -> np.uint64:
    # Generate legal moves for all pieces of the given type on the board
    pass


def main():
    board = Board()
    square = Square(1)
    print(generate_pawn_moves(board=board, square=square))

if __name__ == "__main__":
    main()