
from board import *
from mtcs import *
import random

def random_bot(board, color):
    possible_moves = list(generate_legal_moves(board))
    move = random.choice(possible_moves)
    return board.apply_move(move=move)

def mtcs_bot(board, color):
    mcts = MTCS(state=board)
    mcts.mtcs_search(5)
    best_move = mcts.choose_best_move()
    return board.apply_move(move=best_move)

