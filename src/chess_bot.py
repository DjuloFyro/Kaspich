"""
chess_bot.py - Multiple Bot playing chess implementation

You can find:
    - Random bot (taking random moves)
    - MTCS bot (using monte carlo tree search to make decision)
"""

from board import *
from mtcs import *
import random

def random_bot(board: Board) -> Board:
    """ Random bot making a random move

    Parameters:
        board(Board) : Current state of the board

    Return:
        Board : The new board after the random bot move
    """

    # Generate all the possible moves
    possible_moves = list(generate_legal_moves(board))

    # Choose a random move among all the possible moves
    move = random.choice(possible_moves)

    return board.apply_move(move=move)

def mtcs_bot(board: Board) -> Board:
    """ MTCS bot making a move using monte carlo tree search algorithm

    Parameters:
        board(Board) : Current state of the board
    
    Return:
        Board : The new board afther the MTCS bot move
    """

    # Construct the monte carlo search with a time limit of search 
    mcts = MTCS(state=board)
    mcts.mtcs_search(3)

    # Get and print the statistics
    num_rollouts, run_time = mcts.statistics()
    print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")

    # Choose the best move to do
    best_move = mcts.choose_best_move()
    
    return board.apply_move(move=best_move)

