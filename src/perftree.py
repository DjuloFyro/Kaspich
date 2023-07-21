import numpy as np
from board import Board
from move import Move
from move_generation import *
import sys

def perft(board, depth):
    if depth == 0:
        return 1
    total_nodes = 0
    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        total_nodes += perft(new_board, depth - 1)

    return total_nodes


def main():
    if len(sys.argv) < 3:
        print("Usage: python our_perft_script.py <depth> <fen> [<moves>]")
        sys.exit(1)

    depth = int(sys.argv[1])
    fen = sys.argv[2]
    moves = sys.argv[3:]

    board = Board.from_fen(fen)

    #if moves != []:
    #    moves = map(lambda m: Move.from_str(m), moves)
    #else:
    moves = generate_legal_moves(board)

    total_count = 0
    for move in moves:
        new_board = board.apply_move(move)
        count = perft(board=new_board, depth=depth-1)
        total_count += count
        print(f"{str(move)} {count}")
    print()
    print(total_count)

if __name__ == "__main__":
    main()
