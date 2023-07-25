"""
board.py - Chess Board Representation

This file defines a chessboard representation and various operations related to it.

The Board class provides methods to initialize the chessboard with starting positions, set and clear pieces on squares,
and apply moves to the chessboard, among other utility functions. It also includes methods to convert the chessboard
representation to and from Forsyth-Edwards Notation (FEN) strings, which is a standard notation to represent the state
of a chess game.
"""

import numpy as np

from enums import Color
import utils
from enums import PieceType
from square import Square
from move import Move

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
        # TODO

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
            str_fen += " w"
        else:
            str_fen += " b"

        # Castling (to change)
        str_fen += " KQkq"

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


def main():
    fen = "8/8/8/4p1K1/2k1P3/8/8/8 b - - 0 1"
    board = Board.from_fen(fen=fen)
    board.print_board()

if __name__ == "__main__":
    main()