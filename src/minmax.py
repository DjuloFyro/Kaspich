from board import *
from evaluation import *

def minimax(board, depth, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning to find the best move using recursive search.

    Parameters:
        board (Board): The current state of the game board.
        depth (int): The remaining depth of the search.
        alpha (float): The best score that the maximizing player can achieve.
        beta (float): The best score that the minimizing player can achieve.

    Returns:
        float: The estimated score of the best move for the current player.
    """
    if depth == 0:
        return evaluate(board)
    
    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        score = -minimax(new_board, depth - 1, -beta, -alpha)
        
        # Update alpha with the maximum score found so far
        alpha = max(alpha, score)
        
        # Prune the search if beta <= alpha (cut-off condition)
        if beta <= alpha:
            break
        
    return alpha


def best_move(board, depth):
    """
    Find the best move using the minimax algorithm with alpha-beta pruning.

    Parameters:
        board (Board): The current state of the game board.
        depth (int): The depth of the search.

    Returns:
        Move: The best move to make based on the minimax search.
    """
    max_score = -1000000
    best_move = None
    
    for move in generate_legal_moves(board):
        new_board = board.apply_move(move)
        score = -minimax(new_board, depth - 1, -1000000, 1000000)  # Initial alpha and beta values
        if score > max_score:
            max_score = score
            best_move = move
    
    return best_move
