import numpy as np
import itertools

from board import Board
from square import Square
from precomputed_move import *
from enums import PieceType
from move import Move

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

    # For captures, filter out moves that do not capture an opponent's piece
    capture = PAWN_CAPTURE[board.color_turn][square.position] & board.same_color[Board.opposite_color(board.color_turn)]
    move = EMPTY_BB

    # Filter out moves that collide with friendly pieces
    white_free = Square(square.position + np.uint8(8)).to_bitboard() & board.all_pieces == EMPTY_BB 
    black_free = Square(square.position - np.uint8(8)).to_bitboard() & board.all_pieces == EMPTY_BB 
    if (board.color_turn == Color.WHITE and white_free) or (board.color_turn == Color.BLACK and black_free):
        move = PAWN_MOVE[board.color_turn][square.position] & ~board.all_pieces
    return move | capture


def get_diag_moves_bb(i, occ):
    """
    i is index of square
    occ is the combined occupancy of the board
    """
    f = i & np.uint8(7)
    occ = DIAG_MASKS[i] & occ # isolate diagonal occupancy
    occ = (FILES[File.A] * occ) >> np.uint8(56) # map to first rank
    occ = FILES[File.A] * FIRST_RANK_MOVES[f][occ] # lookup and map back to diagonal
    return DIAG_MASKS[i] & occ


def get_antidiag_moves_bb(i, occ):
    """
    i is index of square
    occ is the combined occupancy of the board
    """
    f = i & np.uint8(7)
    occ = ANTIDIAG_MASKS[i] & occ # isolate antidiagonal occupancy
    occ = (FILES[File.A] * occ) >> np.uint8(56) # map to first rank
    occ = FILES[File.A] * FIRST_RANK_MOVES[f][occ] # lookup and map back to antidiagonal
    return ANTIDIAG_MASKS[i] & occ


def get_rank_moves_bb(i, occ):
    """
    i is index of square
    occ is the combined occupancy of the board
    """
    f = i & np.uint8(7)
    occ = RANK_MASKS[i] & occ # isolate rank occupancy
    occ = (FILES[File.A] * occ) >> np.uint8(56) # map to first rank
    occ = FILES[File.A] * FIRST_RANK_MOVES[f][occ] # lookup and map back to rank
    return RANK_MASKS[i] & occ


def get_file_moves_bb(i, occ):
    """
    i is index of square
    occ is the combined occupancy of the board
    """
    f = i & np.uint8(7)
    # Shift to A file
    occ = FILES[File.A] & (occ >> f)
    # Map occupancy and index to first rank
    occ = (DIAG * occ) >> np.uint8(56)
    first_rank_index = (i ^ np.uint8(56)) >> np.uint8(3)
    # Lookup moveset and map back to H file
    occ = DIAG * FIRST_RANK_MOVES[first_rank_index][occ]
    # Isolate H file and shift back to original file
    return (FILES[File.H] & occ) >> (f ^ np.uint8(7))

def generate_bishop_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the bishop on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the bishop.

    Returns:
        np.array: An array of bitboards representing all legal moves for the bishop.
    """
    return ((get_diag_moves_bb(square.position, board.all_pieces) 
        ^ get_antidiag_moves_bb(square.position, board.all_pieces))
        & ~board.same_color[board.color_turn])

def generate_rook_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the rook on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the rook.

    Returns:
        np.array: An array of bitboards representing all legal moves for the rook.
    """
    return ((get_rank_moves_bb(square.position, board.all_pieces)
        ^ get_file_moves_bb(square.position, board.all_pieces))
        & ~board.same_color[board.color_turn])

def generate_queen_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the queen on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the queen.

    Returns:
        np.array: An array of bitboards representing all legal moves for the queen.
    """
    return generate_bishop_moves(square=square, board=board) | generate_rook_moves(square=square, board=board)

def generate_moves(square: Square, board: Board, piece_type: PieceType) -> np.uint64:
    # Define a dictionary that maps each piece type to its corresponding move generation function
    move_generators = {
        PieceType.PAWN: generate_pawn_moves,
        PieceType.KNIGHT: generate_knight_moves,
        PieceType.BISHOP: generate_bishop_moves,
        PieceType.ROOK: generate_rook_moves,
        PieceType.QUEEN: generate_queen_moves,
        PieceType.KING: generate_king_moves
    }

    # Get the move generation function for the given piece type
    move_generator = move_generators.get(piece_type)
    if move_generator is None:
        raise RuntimeError("Invalid piece")

    # Generate all possible moves for the given piece type on the board
    possible_moves = move_generator(board, square)

    # Handle pawn promotion moves if the piece is a pawn
    if piece_type == PieceType.PAWN:
        white_promotion = square.to_bitboard() & RANKS[Rank.SEVEN] != EMPTY_BB
        black_promotion = square.to_bitboard() & RANKS[Rank.TWO] != EMPTY_BB
        if (board.color_turn == Color.WHITE and white_promotion) or (board.color_turn == Color.BLACK and black_promotion):
            for dest in utils.occupied_squares(possible_moves):
                yield Move(square, dest, PieceType.QUEEN)
                yield Move(square, dest, PieceType.ROOK)
                yield Move(square, dest, PieceType.KNIGHT)
                yield Move(square, dest, PieceType.BISHOP)
            return

    # Yield regular moves for each destination square
    for dest in utils.occupied_squares(possible_moves):
        yield Move(square, dest)


def gen_moves(board: Board):
    # NOTE: generates pseudo-legal moves
    for piece in PieceType:
        piece_bb = board.get_piece_bb(piece)
        for src in utils.occupied_squares(piece_bb):
            yield from generate_moves(src, board, piece)


def gen_legal_moves(board):
    return itertools.filterfalse(lambda m: leaves_in_check(board, m), gen_moves(board))

def leaves_in_check(board: Board, move: Move):
    """
    Applies move to board and returns True iff king is left in check

    Uses symmetry of attack e.g. if white knight attacks black king, then black knight on king sq would attack white knight
    So it suffices to look at attacks of various pieces from king sq; if these hit opponent piece of same type then it's check
    """
    board = board.apply_move(move=move)
    board.color_turn = Board.opposite_color(board.color_turn)
    my_king_sq = Square(utils.lsb_bitscan(board.get_piece_bb(PieceType.KING)))

    opp_color = Board.opposite_color(board.color_turn)
    opp_pawns = board.get_piece_bb(PieceType.PAWN, color=opp_color)
    if (PAWN_CAPTURE[board.color_turn][my_king_sq.position] & opp_pawns) != EMPTY_BB: 
        return True

    opp_knights = board.get_piece_bb(PieceType.KNIGHT, color=opp_color)
    if (generate_knight_moves(board, my_king_sq) & opp_knights) != EMPTY_BB:
        return True

    opp_king = board.get_piece_bb(PieceType.KING, color=opp_color)
    if (generate_king_moves(board, my_king_sq) & opp_king) != EMPTY_BB:
        return True

    opp_bishops = board.get_piece_bb(PieceType.BISHOP, color=opp_color)
    opp_queens = board.get_piece_bb(PieceType.QUEEN, color=opp_color)
    if (generate_bishop_moves(board, my_king_sq) & (opp_bishops | opp_queens)) != EMPTY_BB:
        return True

    opp_rooks = board.get_piece_bb(PieceType.ROOK, color=opp_color)
    if (generate_rook_moves(board, my_king_sq) & (opp_rooks | opp_queens)) != EMPTY_BB:
        return True

    return False



def main():
    board = Board()
    square = Square(1)
    print(generate_pawn_moves(board=board, square=square))

if __name__ == "__main__":
    main()