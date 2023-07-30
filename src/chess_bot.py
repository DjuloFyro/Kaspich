
from board import *
import random

def random_bot(board, color):
    possible_moves = list(generate_legal_moves(board))
    move = random.choice(possible_moves)
    return board.apply_move(move=move)
