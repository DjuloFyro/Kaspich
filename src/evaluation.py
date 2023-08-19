from enum import Enum
from utils import pop_count
from board import *
import numpy as np
from enums import PieceType

class Heuristic(Enum):
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    CHECKMATE = -10000
    MOVE = 0.05


def evaluate(board):
    return eval_pieces(board) + eval_moves(board)

def piece_diff(board: Board, piece):
    if piece == PieceType.KING:
        return np.int32(pop_count(board.kings[board.color_turn])) - np.int32(pop_count(board.kings[Board.opposite_color(board.color_turn)]))
    elif piece == PieceType.QUEEN:
        return np.int32(pop_count(board.queens[board.color_turn])) - np.int32(pop_count(board.queens[Board.opposite_color(board.color_turn)]))
    elif piece == PieceType.KNIGHT:
        return np.int32(pop_count(board.knights[board.color_turn])) - np.int32(pop_count(board.knights[Board.opposite_color(board.color_turn)]))
    elif piece == PieceType.BISHOP:
        return np.int32(pop_count(board.bishops[board.color_turn])) - np.int32(pop_count(board.bishops[Board.opposite_color(board.color_turn)]))
    elif piece == PieceType.ROOK:
        return np.int32(pop_count(board.rooks[board.color_turn])) - np.int32(pop_count(board.rooks[Board.opposite_color(board.color_turn)]))
    elif piece == PieceType.PAWN:
        return np.int32(pop_count(board.pawns[board.color_turn])) - np.int32(pop_count(board.pawns[Board.opposite_color(board.color_turn)]))
    else:
        raise ValueError("Invalid piece type")

def eval_pieces(board):
    return (Heuristic.PAWN.value * piece_diff(board, PieceType.PAWN)
        + Heuristic.KNIGHT.value * piece_diff(board, PieceType.KNIGHT)
        + Heuristic.BISHOP.value * piece_diff(board, PieceType.BISHOP)
        + Heuristic.ROOK.value * piece_diff(board, PieceType.ROOK)
        + Heuristic.QUEEN.value * piece_diff(board, PieceType.QUEEN))


def eval_moves(board):
    num = len(list(generate_legal_moves(board)))
    if num == 0:
        return Heuristic.CHECKMATE.value
    else:
        return Heuristic.MOVE.value * np.int32(num)