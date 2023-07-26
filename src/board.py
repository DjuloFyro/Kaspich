"""
board.py - Chess Board Representation

This file defines a chessboard representation and various operations related to it.

The Board class provides methods to initialize the chessboard with starting positions, set and clear pieces on squares,
and apply moves to the chessboard, among other utility functions. It also includes methods to convert the chessboard
representation to and from Forsyth-Edwards Notation (FEN) strings, which is a standard notation to represent the state
of a chess game.

This file contains functions for generating legal moves for different chess pieces on the board.
It also includes a function to check if a move leaves the king in check after applying it to the board.
"""

import numpy as np

from enums import Color
import utils
from enums import PieceType
from square import Square
from move import Move
import itertools
from move_generation import *

class Board:
    def __init__(self):
        """
        Initialize the chessboard and piece positions for both players.
        """
        # Initialize dictionaries to hold the position of each piece for each color
        self.kings = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}
        self.queens = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}
        self.knights = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}
        self.bishops = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}
        self.rooks = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}
        self.pawns = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}

        # Initialize variables to store the bitboard representation of all white and black pieces
        self.same_color = {Color.WHITE: np.uint64(0), Color.BLACK: np.uint64(0)}

        # Initialize a variable to store the bitboard representation of all pieces on the board
        self.all_pieces = np.uint64(0)

        # Color to play
        self.color_turn = Color.WHITE

        # Initialize the en passant square attribute to None
        self.en_passant_square = {Color.WHITE: None, Color.BLACK: None}

        # Initialize attributes to track whether the king and rooks have moved for both colors
        self.king_moved = {Color.WHITE: False, Color.BLACK: False}
        self.rook_moved = {Color.WHITE: {"queen_side": False, "king_side": False},
                           Color.BLACK: {"queen_side": False, "king_side": False}}
        
        # Define the initial positions of kings and rooks for both colors for castling
        self.king_initial_positions = {
            Color.WHITE: Square(4),  # Starting position of the white king (e1)
            Color.BLACK: Square(60),  # Starting position of the black king (e8)
        }
        self.rook_initial_positions = {
            Color.WHITE: {
                "king_side": Square(7),  # Starting position of the white king-side rook (h1)
                "queen_side": Square(0),  # Starting position of the white queen-side rook (a1)
            },
            Color.BLACK: {
                "king_side": Square(63),  # Starting position of the black king-side rook (h8)
                "queen_side": Square(56),  # Starting position of the black queen-side rook (a8)
            },
        }
    
    def opposite_color(color):
        """
        Get the oppsite color (WHITE -> BLACK) (BLACK -> WHITE).

        Parameters:
            color (Color): The Color.

        Returns:
            Color: The opposite color.
        """
        return Color.WHITE if color == Color.BLACK else Color.BLACK

    def board_initialization(self):
        """
        Set up the initial positions of the pieces on the chessboard.
        """
        # Define the starting positions of each piece for white and black
        self.kings[Color.WHITE] = np.uint64(0x0000000000000010)
        self.queens[Color.WHITE] = np.uint64(0x0000000000000008)
        self.knights[Color.WHITE] = np.uint64(0x0000000000000042)
        self.bishops[Color.WHITE] = np.uint64(0x0000000000000024)
        self.rooks[Color.WHITE] = np.uint64(0x0000000000000081)
        self.pawns[Color.WHITE] = np.uint64(0x000000000000FF00)

        self.kings[Color.BLACK] = np.uint64(0x1000000000000000)
        self.queens[Color.BLACK] = np.uint64(0x0800000000000000)
        self.knights[Color.BLACK] = np.uint64(0x4200000000000000)
        self.bishops[Color.BLACK] = np.uint64(0x2400000000000000)
        self.rooks[Color.BLACK] = np.uint64(0x8100000000000000)
        self.pawns[Color.BLACK] = np.uint64(0x00FF000000000000)

        # Combine all white and black pieces to get the bitboard representation
        self.same_color[Color.WHITE] = self.kings[Color.WHITE] | self.queens[Color.WHITE] | self.knights[Color.WHITE] | self.bishops[Color.WHITE] | self.rooks[Color.WHITE] | self.pawns[Color.WHITE]
        self.same_color[Color.BLACK] = self.kings[Color.BLACK] | self.queens[Color.BLACK] | self.knights[Color.BLACK] | self.bishops[Color.BLACK] | self.rooks[Color.BLACK] | self.pawns[Color.BLACK]

        # Combine both white and black pieces to get the bitboard representation of all pieces on the board
        self.all_pieces = self.same_color[Color.WHITE] | self.same_color[Color.BLACK]


    '''---------------------------------------------------------- Representation for chess board ---------------------------------------------------------------'''
    '''---------------------------------------------------------------------------------------------------------------------------------------------------------'''

    def print_board(self):
        """
        Print the current chessboard with the pieces' positions.
        """
        for rank in range(7, -1, -1):
            for file in range(8):
                square = np.uint64(rank * 8 + file)
                piece = "."
                if self.all_pieces & (np.uint64(1) << square):
                    for color in (Color.WHITE, Color.BLACK):
                        if self.kings[color] & (np.uint64(1) << square):
                            piece = "K" if color == Color.WHITE else "k"
                        if self.queens[color] & (np.uint64(1) << square):
                            piece = "Q" if color == Color.WHITE else "q"
                        if self.knights[color] & (np.uint64(1) << square):
                            piece = "N" if color == Color.WHITE else "n"
                        if self.bishops[color] & (np.uint64(1) << square):
                            piece = "B" if color == Color.WHITE else "b"
                        if self.rooks[color] & (np.uint64(1) << square):
                            piece = "R" if color == Color.WHITE else "r"
                        if self.pawns[color] & (np.uint64(1) << square):
                            piece = "P" if color == Color.WHITE else "p"
                print(piece, end=' ')
            print()

    def from_fen(self, fen):
        """
        Create a Board instance from a FEN string.

        Parameters:
            fen (str): The FEN string representing the board position.

        Returns:
            Board: The Board instance initialized from the FEN string.
        """

        # Split the FEN string into parts: position, turn, castling, en passant, and half move clock
        parts = fen.split(" ")

        # Set the piece positions on the board
        rank = 7
        file = 0
        for char in parts[0]:
            if char == '/':
                rank -= 1
                file = 0
            elif char.isdigit():
                file += int(char)
            else:
                color = Color.WHITE if char.isupper() else Color.BLACK
                piece = PieceType.from_char(char.lower())
                square = Square(rank * 8 + file)
                self.set_square(square, piece, color)
                file += 1

        # Set the color to play
        if parts[1].lower() == 'w':
            self.color_turn = Color.WHITE
        else:
            self.color_turn = color.BLACK

        # Castling
        # Change nothing with our implementation

        # En passant
        if parts[3] != "-":
            if self.color_turn == Color.WHITE:
                self.en_passant_square[Board.opposite_color(self.color_turn)] = Square(Square.from_string(parts[3]).position - np.uint8(8))
            else:
                self.en_passant_square[Board.opposite_color(self.color_turn)] = Square(Square.from_string(parts[3]).position + np.uint8(8))


        # Halfmove Clock
        # TODO

        #FullMove number
        # TODO

        return

    def to_fen(self):
        """
        Create a Fen string from a new chessboard instance.

        Returns:
            String: The Fen string corresponding to the Board class initialized.
        """
        fen = []
        for rank in range(7, -1, -1):
            empty_square = 0
            fen_row = ""

            for file in range(0, 8):
                square = Square(rank * 8 + file)
                color = Color.WHITE
                piece = self.piece_on(square, color)
                if piece == None:
                    color = Color.BLACK
                    piece = self.piece_on(square, color)

                if piece == None:
                    empty_square += 1
                else:
                    if empty_square > 0:
                        fen_row += str(empty_square)
                        empty_square = 0
                    fen_row += piece.to_char() if color == Color.BLACK else piece.to_char().upper()
            
            if empty_square > 0:
                fen_row += str(empty_square)
            
            fen.append(fen_row)

        str_fen = "/".join(fen)

        if self.color_turn == Color.WHITE:
            str_fen += " w "
        else:
            str_fen += " b "

        # Castling
        if self.can_castle_kingside(Color.WHITE) and self.is_valid_castling(color.WHITE, king_side=True):
            str_fen += "K"
        if self.can_castle_queenside(Color.WHITE) and self.is_valid_castling(color.WHITE, king_side=False):
            str_fen += "Q"
        if self.can_castle_kingside(Color.BLACK) and self.is_valid_castling(color.BLACK, king_side=True):
            str_fen += "k"
        if self.can_castle_queenside(Color.BLACK) and self.is_valid_castling(color.BLACK, king_side=False):
            str_fen += "q"
        

        # En passant
        en_passant_square_color = self.en_passant_square[self.color_turn]
        if en_passant_square_color != None:
            str_fen += " " + str(en_passant_square_color)
        else:
            str_fen += " -"

        # Halfmove Clock (to change)
        str_fen += " 0"

        #FullMove number
        str_fen += " 1"

        return str_fen

    def can_castle_kingside(self, color: Color) -> bool:
        """
        Check if the player with the given color can castle kingside.

        Parameters:
            color (Color): The color of the player (Color.WHITE or Color.BLACK).

        Returns:
            bool: True if castling kingside is possible, False otherwise.
        """
        return not self.king_moved[color] and not self.rook_moved[color]["king_side"]

    def can_castle_queenside(self, color: Color) -> bool:
        """
        Check if the player with the given color can castle queenside.

        Parameters:
            color (Color): The color of the player (Color.WHITE or Color.BLACK).

        Returns:
            bool: True if castling queenside is possible, False otherwise.
        """
        return not self.king_moved[color] and not self.rook_moved[color]["queen_side"]
    

    def is_valid_castling(self, color: Color, king_side: bool = True):
        """
        Check if castling is a valid move for the given color.

        Parameters:
            color (Color): The color of the king (Color.WHITE or Color.BLACK).
            king_side (bool): If True, check for king-side castling; otherwise, check for queen-side castling.

        Returns:
            bool: True if castling is valid; otherwise, False.
        """
        # Check if the king and the corresponding rook are in their initial positions
        king_pos = self.king_initial_positions[color]
        rook_pos = (
            self.rook_initial_positions[color]["king_side"]
            if king_side
            else self.rook_initial_positions[color]["queen_side"]
        )

        king = self.piece_on(king_pos, color)
        rook = self.piece_on(rook_pos, color)

        if king != PieceType.KING or rook != PieceType.ROOK:
            return False
        
        # Check if there are no pieces between the king and the rook
        squares_between = utils.squares_between(king_pos, rook_pos)
        is_pieces_between = any(self.piece_on(square, color) is not None for square in squares_between for color in (Color.WHITE, Color.BLACK))
        if is_pieces_between:
            return False
        
        traversed_squares = (
            Square(rook_pos.position - np.uint8(1))
            if king_side
            else Square(rook_pos.position + np.uint8(2))
        )

        # Check if the squares the king moves over are not under attack
        squares_to_check = (
            [king_pos] + utils.squares_between(king_pos, traversed_squares) + [traversed_squares]
        )
        for square in squares_to_check:
            if self.is_square_attacked(square):
                return False

        return True


    '''----------------------------------------------------- Pieces manipulation for chess board ---------------------------------------------------------------'''
    '''---------------------------------------------------------------------------------------------------------------------------------------------------------'''

    def get_piece_bb(self, piece_type: PieceType, color: Color = None):
        """
        Get the bitboard representation of a specific piece for the given color on the chessboard.

        Parameters:
            piece (PieceType): The type of piece to retrieve the bitboard for.
            color (Color): The color of the pieces to be considered (Color.WHITE or Color.BLACK).
                          If not provided, the default is the current color of the chessboard.

        Returns:
            np.uint64: The bitboard representation of the specified piece for the given color.
        """
        if color is None:
            color = self.color_turn
        
        if piece_type == PieceType.KING:
            return self.kings[color]
        if piece_type == PieceType.KNIGHT:
            return self.knights[color]
        if piece_type == PieceType.PAWN:
            return self.pawns[color]
        if piece_type == PieceType.BISHOP:
            return self.bishops[color]
        if piece_type == PieceType.ROOK:
            return self.rooks[color]
        if piece_type == PieceType.QUEEN:
            return self.queens[color]
        else:
            raise ValueError("Invalid piece type")


    def piece_on(self, square: Square, color: Color = None):
        """
        Check if there is a piece on the given square for the specified color.

        Parameters:
            sq (Square): The square to check for the presence of a piece.
            color (Color): The color of the pieces to be considered (Color.WHITE or Color.BLACK).
                          If not provided, the default is the current turn's color.

        Returns:
            PieceType or None: The type of the piece on the square (PieceType) if present, or None if the square is empty.
        """
        if color is None:
            color = self.color_turn

        # Iterate through all piece types and check if the square is set in their corresponding bitboards
        return next(
            (piece for piece in PieceType if 
                utils.is_set(self.get_piece_bb(piece, color), square)),
            None)
    
    '''----------------------------------------------------- Square manipulation for chess board ---------------------------------------------------------------'''
    '''---------------------------------------------------------------------------------------------------------------------------------------------------------'''

    def is_square_attacked(self, square: Square) -> bool:
        """
        Check if a square is attacked by any of the opponent's pieces.

        Parameters:
            self (Board): The chessboard state.
            square (Square): The square to check for attacks.

        Returns:
            bool: True if the square is attacked; otherwise, False.
        """
        opp_color = Board.opposite_color(self.color_turn)
    
        opp_pawns = self.get_piece_bb(PieceType.PAWN, color=opp_color)
        if (PAWN_CAPTURE[self.color_turn][square.position] & opp_pawns) != EMPTY_BB: 
            return True

        opp_knights = self.get_piece_bb(PieceType.KNIGHT, color=opp_color)
        if (generate_knight_moves(self, square) & opp_knights) != EMPTY_BB:
            return True

        opp_king = self.get_piece_bb(PieceType.KING, color=opp_color)
        if (generate_king_moves(self, square) & opp_king) != EMPTY_BB:
            return True

        opp_bishops = self.get_piece_bb(PieceType.BISHOP, color=opp_color)
        opp_queens = self.get_piece_bb(PieceType.QUEEN, color=opp_color)
        if (generate_bishop_moves(self, square) & (opp_bishops | opp_queens)) != EMPTY_BB:
            return True

        opp_rooks = self.get_piece_bb(PieceType.ROOK, color=opp_color)
        if (generate_rook_moves(self, square) & (opp_rooks | opp_queens)) != EMPTY_BB:
            return True

        return False
    

    def set_square(self, square: Square, piece: PieceType, color: Color = None):
        """
        Set the given piece on the specified square for the specified color.

        Parameters:
            square (Square): The square to set the piece on.
            piece (PieceType): The type of the piece to be set.
            color (Color, optional): The color of the piece (Color.WHITE or Color.BLACK). 
                                     Defaults to the current turn's color.

        Raises:
            ValueError: If an invalid piece type is provided.

        Note:
            This method updates the corresponding piece dictionary with the modified bitboard.
            It also updates the same_color and all_pieces bitboards with the modified bitboards.
        """
         
        if color is None:
            color = self.color_turn

        # Get the current bitboard representing the given piece type for the specified color
        piece_bb = self.get_piece_bb(piece, color)

        # Get the current bitboard representing all pieces of the same color
        combined_bb = self.same_color[color]

        # Get the current bitboard representing all pieces on the board
        all_bb = self.all_pieces

        # Update the corresponding piece dictionary with the modified bitboard
        if piece == PieceType.KING:
            self.kings[color] = utils.set_square(piece_bb, square)
        elif piece == PieceType.QUEEN:
            self.queens[color] = utils.set_square(piece_bb, square)
        elif piece == PieceType.KNIGHT:
            self.knights[color] = utils.set_square(piece_bb, square)
        elif piece == PieceType.BISHOP:
            self.bishops[color] = utils.set_square(piece_bb, square)
        elif piece == PieceType.ROOK:
            self.rooks[color] = utils.set_square(piece_bb, square)
        elif piece == PieceType.PAWN:
            self.pawns[color] = utils.set_square(piece_bb, square)
        else:
            raise ValueError("Invalid piece type")
        
        # Update the same_color and combined_all bitboards with the modified bitboards
        self.same_color[color] = utils.set_square(combined_bb, square)
        self.all_pieces = utils.set_square(all_bb, square)

    def clear_square(self, square: Square, color: Color = None):
        """
        Clear the piece from the specified square for the specified color.

        Parameters:
            square (Square): The square to clear the piece from.
            color (Color, optional): The color of the piece (Color.WHITE or Color.BLACK). 
                                     Defaults to the current turn's color.

        Note:
            This method updates the corresponding piece dictionary with the modified bitboard.
            It also updates the same_color and all_pieces bitboards with the modified bitboards.
        """
        if color is None:
            color = self.color_turn

        piece = self.piece_on(square, color)
        if piece is None:
            return

        piece_bb = self.get_piece_bb(piece, color)
        combined_bb = self.same_color[color]
        all_bb = self.all_pieces

        # Update the corresponding piece dictionary with the modified bitboard
        if piece == PieceType.KING:
            self.kings[color] = utils.clear_square(piece_bb, square)
        elif piece == PieceType.QUEEN:
            self.queens[color] = utils.clear_square(piece_bb, square)
        elif piece == PieceType.KNIGHT:
            self.knights[color] = utils.clear_square(piece_bb, square)
        elif piece == PieceType.BISHOP:
            self.bishops[color] = utils.clear_square(piece_bb, square)
        elif piece == PieceType.ROOK:
            self.rooks[color] = utils.clear_square(piece_bb, square)
        elif piece == PieceType.PAWN:
            self.pawns[color] = utils.clear_square(piece_bb, square)
        else:
            raise ValueError("Invalid piece type")

        # Update the same_color and all_pieces bitboards with the modified bitboards
        self.same_color[color] = utils.clear_square(combined_bb, square)
        self.all_pieces = utils.clear_square(all_bb, square)

    def apply_move(self, move: Move):
        """
        Applies a move to the chessboard and returns a new board without modifying the original.
        Parameters:
            move (Move): The move to be applied to the chessboard.
        Returns:
            Board: A new board with the move applied.
        Note:
            This method creates a new board and copies the piece positions, color, and combined bitboards
            from the original board to the new board. It then applies the move to the new board and returns it.
        """
        # Create a new board and copy the piece positions, color, and combined bitboards from the original board
        new_board = Board()
        new_board.kings = dict.copy(self.kings)
        new_board.knights = dict.copy(self.knights)
        new_board.pawns = dict.copy(self.pawns)
        new_board.bishops = dict.copy(self.bishops)
        new_board.rooks = dict.copy(self.rooks)
        new_board.queens = dict.copy(self.queens)
        new_board.same_color = dict.copy(self.same_color)
        new_board.all_pieces = np.copy(self.all_pieces)
        new_board.color_turn = self.color_turn

        # Copy en-passant_square
        new_board.en_passant_square = self.en_passant_square

        # Set the en_passant_square of the current color to None
        # Because we can only take en-passant directly after the opposite color played double pushes
        new_board.en_passant_square[new_board.color_turn] = None

        # Get the piece at the source square of the move
        piece = self.piece_on(move.src)

        # If there is an en-passant possibillity and it is a pawn and it choose to take en-passant move
        if move.en_passant:
            new_board.clear_square(move.src)
            # We clear the square behind the destination (en-passant rule)
            if new_board.color_turn == Color.WHITE:
                new_board.clear_square(Square(move.dest.position - np.uint8(8)), Board.opposite_color(new_board.color_turn))
            else:
                clearing_square = Square(move.dest.position + np.uint8(8))
                new_board.clear_square(clearing_square, Board.opposite_color(new_board.color_turn))
        elif move.is_castling: # Apply castling move if the move is a castling move
            king_side = move.dest.file > move.src.file

            # Clear the king position
            king_pos = move.src
            new_board.clear_square(king_pos, new_board.color_turn)

            # Clear the rook position
            rook_pos = (
                new_board.rook_initial_positions[new_board.color_turn]["king_side"]
                if king_side
                else new_board.rook_initial_positions[new_board.color_turn]["queen_side"]
            )
            new_board.clear_square(rook_pos, new_board.color_turn)

            # Move the king
            new_board.set_square(move.dest, PieceType.KING, new_board.color_turn)

            # Move the rook
            new_rook_pos = Square(
                king_pos.position + np.uint8(1) if king_side else king_pos.position - np.uint8(1)
            )
            new_board.set_square(new_rook_pos, PieceType.ROOK, new_board.color_turn)

        else: # Normal clear
            # Clear the source square and the destination square (in case of a capture) on the new board
            new_board.clear_square(move.src)
            new_board.clear_square(move.dest, Board.opposite_color(new_board.color_turn))  # Clear the destination square for the opponent's color

        # Set the en passant square attribute if the move is a double pawn move
        if piece == PieceType.PAWN and move.is_double_push():
            new_board.en_passant_square[new_board.color_turn] = move.dest
    
        # Set the piece on the destination square, considering promotion if applicable
        new_board.set_square(move.dest, piece if move.promo is None else move.promo)

        # Update the color turn on the new board
        new_board.color_turn = Board.opposite_color(new_board.color_turn)
        
        # Return the new board with the move applied
        return new_board
    

'''-------------------------------------------------------- Pieces move generation -----------------------------------------------------------------------------------'''
'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

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
    
    # Check for castling
    if piece_type == PieceType.KING:
        # King side castling
        if board.can_castle_kingside(board.color_turn): # Check if rook and king have not move
            if board.is_valid_castling(board.color_turn, king_side=True): # check if the castling is valid
                yield Move(src=board.king_initial_positions[board.color_turn], dest=Square(board.king_initial_positions[board.color_turn].position + np.uint8(2)), is_castling=True)
        # Queen side castling
        if board.can_castle_queenside(board.color_turn):
            if board.is_valid_castling(board.color_turn, king_side=False):
                yield Move(src=board.king_initial_positions[board.color_turn], dest=Square(board.king_initial_positions[board.color_turn].position - np.uint8(2)), is_castling=True)

    # Yield regular moves for each destination square
    for dest in utils.occupied_squares(possible_moves):
        yield Move(square, dest)


'''------------------------------------------------------------- Legals move generation ------------------------------------------------------------------------------'''
'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

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


'''---------------------------------------------------------------- Perft and test -----------------------------------------------------------------------------------'''
'''-------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

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
        print(f"move choosen= {move} and color turn= {board.color_turn}")
        board.print_board()
        print(f"en-passant= {board.en_passant_square}")
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
    board = Board()
    board.from_fen("r3k2r/p1ppqpb1/1n2pnp1/3PN3/1p2P3/2N2Q1p/PPPB1PPP/R2BKB1R w kq -")
    print(perft(board=board, depth=1))

if __name__ == "__main__":
    main()