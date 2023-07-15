import numpy as np


class Board:
    def __init__(self):
        self.kings = {"white": np.uint64(0), "black": np.uint64(0)}
        self.queens = {"white": np.uint64(0), "black": np.uint64(0)}
        self.knights = {"white": np.uint64(0), "black": np.uint64(0)}
        self.bishops = {"white": np.uint64(0), "black": np.uint64(0)}
        self.rooks = {"white": np.uint64(0), "black": np.uint64(0)}
        self.pawns = {"white": np.uint64(0), "black": np.uint64(0)}

        self.white_pieces = np.uint64(0)
        self.black_pieces = np.uint64(0)

        self.all_pieces = np.uint64(0)

        
    def board_initialization(self):
        self.kings["white"] = np.uint64(0x0000000000000010)
        self.queens["white"] = np.uint64(0x0000000000000008)
        self.knights["white"] = np.uint64(0x0000000000000042)
        self.bishops["white"] = np.uint64(0x0000000000000024)
        self.rooks["white"] = np.uint64(0x0000000000000081)
        self.pawns["white"] = np.uint64(0x000000000000FF00)

        self.kings["black"] = np.uint64(0x1000000000000000)
        self.queens["black"] = np.uint64(0x0800000000000000)
        self.knights["black"] = np.uint64(0x4200000000000000)
        self.bishops["black"] = np.uint64(0x2400000000000000)
        self.rooks["black"] = np.uint64(0x8100000000000000)
        self.pawns["black"] = np.uint64(0x00FF000000000000)

        self.white_pieces = self.kings["white"] | self.queens["white"] | self.knights["white"] | self.bishops["white"] | self.rooks["white"] | self.pawns["white"]
        self.black_pieces = self.kings["black"] | self.queens["black"] | self.knights["black"] | self.bishops["black"] | self.rooks["black"] | self.pawns["black"]

        self.all_pieces = self.white_pieces | self.black_pieces

    def print_board(self):
        for rank in range(7, -1, -1):
            for file in range(8):
                square = np.uint64(rank * 8 + file)
                piece = "."
                if self.all_pieces & (np.uint64(1) << square):
                    for color in ("white", "black"):
                        if self.kings[color] & (np.uint64(1) << square):
                            piece = "K" if color == "white" else "k"
                        if self.queens[color] & (np.uint64(1) << square):
                            piece = "Q" if color == "white" else "q"
                        if self.knights[color] & (np.uint64(1) << square):
                            piece = "N" if color == "white" else "n"
                        if self.bishops[color] & (np.uint64(1) << square):
                            piece = "B" if color == "white" else "b"
                        if self.rooks[color] & (np.uint64(1) << square):
                            piece = "R" if color == "white" else "r"
                        if self.pawns[color] & (np.uint64(1) << square):
                            piece = "P" if color == "white" else "p"
                print(piece, end=' ')
            print()
                        
                        
                        
                        
                        




        