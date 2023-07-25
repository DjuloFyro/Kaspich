"""
move_generation.py - Chess Moves Generation

This file contains functions for generating legal moves for different chess pieces on the board.
It also includes a function to check if a move leaves the king in check after applying it to the board.
"""

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

def generate_pawn_enpassant_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the pawn on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the pawn.

    Returns:
        np.array: An array of bitboards representing all legal moves for the pawn.
    """

    # For captures, filter out moves that do not capture an opponent's piece

    en_passant = EMPTY_BB
    en_passant_square_color = board.en_passant_square[Board.opposite_color(board.color_turn)]
    if en_passant_square_color != None:
        if board.color_turn == Color.BLACK:
            cond = Square(en_passant_square_color.position - np.uint8(8)).to_bitboard()
        else:
            cond = Square(en_passant_square_color.position + np.uint8(8)).to_bitboard()

        #if board.en_passant_square[1] == Color.WHITE:
        #    cond = Square(board.en_passant_square[0].position - np.uint8(8)).to_bitboard()
        #else:
        #    cond = Square(board.en_passant_square[0].position + np.uint8(8)).to_bitboard()
        en_passant = PAWN_ENPASSANT[board.color_turn][square.position] & cond
    
    return en_passant


def generate_diag_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible diagonal moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible diagonal moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = DIAG_MASKS[index] & occupancy # isolate diagonal occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to diagonal
    return DIAG_MASKS[index] & occupancy


def generate_antidiag_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible antidiagonal moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible antidiagonal moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = ANTIDIAG_MASKS[index] & occupancy # isolate antidiagonal occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to antidiagonal
    return ANTIDIAG_MASKS[index] & occupancy


def generate_rank_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible rank moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible rank moves for the given square.
    """
    file = index & np.uint8(7)
    occupancy = RANK_MASKS[index] & occupancy # isolate rank occupancy
    occupancy = (FILES[File.A] * occupancy) >> np.uint8(56) # map to first rank
    occupancy = FILES[File.A] * FIRST_RANK_MOVES[file][occupancy] # lookup and map back to rank
    return RANK_MASKS[index] & occupancy


def generate_file_moves(index: np.uint8, occupancy: np.uint64) -> np.uint64:
    """
    Generate the possible file moves for the square 'i' on the chessboard.

    Parameters:
        index (np.uint8): Index of the square (0 to 63).
        occupancy (np.uint64): Combined occupancy of the chessboard.

    Returns:
        np.uint64: Bitboard representing the possible file moves for the given square.
    """
    file = index & np.uint8(7)
    # Shift to A file
    occupancy = FILES[File.A] & (occupancy >> file)
    # Map occupancy and index to first rank
    occupancy = (DIAG * occupancy) >> np.uint8(56)
    first_rank_index = (index ^ np.uint8(56)) >> np.uint8(3)
    # Lookup moveset and map back to H file
    occupancy = DIAG * FIRST_RANK_MOVES[first_rank_index][occupancy]
    # Isolate H file and shift back to original file
    return (FILES[File.H] & occupancy) >> (file ^ np.uint8(7))

def generate_bishop_moves(board: Board, square: Square) -> np.uint64:
    """
    Generate legal moves for the bishop on the given square.

    Parameters:
        board (Board): The chessboard.
        square (Square): The square containing the bishop.

    Returns:
        np.array: An array of bitboards representing all legal moves for the bishop.
    """
    return ((generate_diag_moves(square.position, board.all_pieces) 
        ^ generate_antidiag_moves(square.position, board.all_pieces))
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
    return ((generate_rank_moves(square.position, board.all_pieces)
        ^ generate_file_moves(square.position, board.all_pieces))
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

def generate_piece_moves(square: Square, board: Board, piece_type: PieceType):
    """
    Generate all possible moves for the given piece type on the board from the given square.

    Parameters:
        square (Square): The starting square of the piece.
        board (Board): The chessboard state.
        piece_type (PieceType): The type of the piece.

    Yields:
        Move: A move object representing a possible legal move.
    """
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
        # Handle promotion
        white_promotion = square.to_bitboard() & RANKS[Rank.SEVEN] != EMPTY_BB
        black_promotion = square.to_bitboard() & RANKS[Rank.TWO] != EMPTY_BB
        if (board.color_turn == Color.WHITE and white_promotion) or (board.color_turn == Color.BLACK and black_promotion):
            for dest in utils.occupied_squares(possible_moves):
                yield Move(square, dest, PieceType.QUEEN)
                yield Move(square, dest, PieceType.ROOK)
                yield Move(square, dest, PieceType.KNIGHT)
                yield Move(square, dest, PieceType.BISHOP)
            return
        
        en_passant_moves = generate_pawn_enpassant_moves(board, square)
        for dest in utils.occupied_squares(en_passant_moves):
            yield Move(square, dest, en_passant=True)

    # Yield regular moves for each destination square
    for dest in utils.occupied_squares(possible_moves):
        yield Move(square, dest)


def generate_pseudo_legal_moves(board: Board):
    """
    Generate pseudo-legal moves for all pieces on the board.

    Parameters:
        board (Board): The chessboard state.

    Yields:
        Move: A move object representing a possible pseudo-legal move.
    """
    for piece in PieceType:
        piece_bb = board.get_piece_bb(piece)
        for src in utils.occupied_squares(piece_bb):
            yield from generate_piece_moves(src, board, piece)


def generate_legal_moves(board: Board):
    """
    Generate legal moves for the current player on the board.

    Parameters:
        board (Board): The chessboard state.

    Yields:
        Move: A move object representing a possible legal move.
    """
    return itertools.filterfalse(lambda m: leaves_in_check(board, m), generate_pseudo_legal_moves(board))

def leaves_in_check(board: Board, move: Move) -> bool:
    """
    Check if applying the given move to the board leaves the king in check.

    Parameters:
        board (Board): The chessboard state.
        move (Move): The move to apply.

    Returns:
        bool: True if the move leaves the king in check, False otherwise.
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
        print(f"move choosen= {move} and color turn= {new_board.color_turn}")
        new_board.print_board()
        print(f"en-passant= {new_board.en_passant_square}")
        new_board = board.apply_move(move)
        total_nodes += perft(new_board, depth - 1)

    board.en_passant_square[board.color_turn] = original_en_passant  # Restore the en-passant square

    return total_nodes

def main():
    board = Board()
    board.from_fen("8/8/K2p4/1Pp4r/1R3p1k/8/4P1P1/8 w - c6 0 1")
    print(perft(board=board, depth=2))

if __name__ == "__main__":
    main()