import numpy as np
from board import Board
from move import Move
from move_generation import *
import sys

def perft(board, depth):
    if depth == 0:
        return 1

    total_nodes = 0
    original_en_passant = board.en_passant_square[board.color_turn]  # Store the original en-passant square

    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        total_nodes += perft(new_board, depth - 1)

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
        print(f"{str(move)} {count}")

    board.en_passant_square[board.color_turn] = original_en_passant  # Restore the en-passant square
    print()
    print(total_nodes)

if __name__ == "__main__":
    main()
