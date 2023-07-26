import numpy as np
from board import *
from move import Move
from move_generation import *
import sys

def perft(board, depth):
    """
    Perform a perft search to count the number of legal positions at a given depth.

    Parameters:
        board (Board): The current chessboard state.
        depth (int): The depth to search for legal positions.

    Returns:
        int: The number of legal positions at the given depth.
    """
    if depth == 0:
        return 1

    total_nodes = 0
    original_en_passant = board.en_passant_square[board.color_turn]  # Store the original en-passant square

    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        total_nodes += perft(new_board, depth - 1)
        
        # Check if the move involves the king or rook and update their moved status (for the castling availability)
        piece = new_board.piece_on(move.src)

        if piece == PieceType.KING:
            new_board.king_moved[new_board.color_turn] = True
        elif piece == PieceType.ROOK:
            if move.src == Square(0):
                new_board.rook_moved[Color.WHITE]["queen_side"] = True
            if move.src == Square(7):
                new_board.rook_moved[Color.WHITE]["king_side"] = True
            if move.src == Square(56):
                new_board.rook_moved[Color.BLACK]["queen_side"] = True
            if move.src == Square(63):
                new_board.rook_moved[Color.BLACK]["king_side"] = True


    board.en_passant_square[board.color_turn] = original_en_passant  # Restore the en-passant square

    return total_nodes


def main():
    if len(sys.argv) < 3:
        print("Usage: python our_perft_script.py <depth> <fen> [<moves>]")
        sys.exit(1)

    depth = int(sys.argv[1])
    fen = sys.argv[2]
    moves = sys.argv[3:]

    board = Board()
    board.from_fen(fen)

   
    total_nodes = 0
    original_en_passant = board.en_passant_square[board.color_turn]  # Store the original en-passant square

    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        count = perft(new_board, depth - 1)
        total_nodes += count
        # Check if the move involves the king or rook and update their moved status (for the castling availability)
        piece = new_board.piece_on(move.src)

        if piece == PieceType.KING:
            new_board.king_moved[new_board.color_turn] = True
        elif piece == PieceType.ROOK:
            if move.src == Square(0):
                new_board.rook_moved[Color.WHITE]["queen_side"] = True
            if move.src == Square(7):
                new_board.rook_moved[Color.WHITE]["king_side"] = True
            if move.src == Square(56):
                new_board.rook_moved[Color.BLACK]["queen_side"] = True
            if move.src == Square(63):
                new_board.rook_moved[Color.BLACK]["king_side"] = True
        print(f"{str(move)} {count}")

    board.en_passant_square[board.color_turn] = original_en_passant  # Restore the en-passant square
    print()
    print(total_nodes)

if __name__ == "__main__":
    main()
