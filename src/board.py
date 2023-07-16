import numpy as np

from enums import Color

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
