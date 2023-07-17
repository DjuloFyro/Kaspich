import unittest
import numpy as np
import sys
import os

# Add the path to the 'src' folder to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

from board import Board
from move_generation import *

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the Board instance and initialize the chessboard for each test case.
        """
        self.board = Board()

    def test_generate_king_moves(self) -> None:
        square_1 = Square(1)
        square_3 = Square(3)
        expected_position_1 = 1797
        expected_position_3 = 7188

        get_position_1 = generate_king_moves(self.board, square_1)
        get_position_3 = generate_king_moves(self.board, square_3)

        self.assertEqual(expected_position_1, get_position_1)
        self.assertEqual(expected_position_3, get_position_3)

    def test_generate_knight_moves(self) -> None:
        square_1 = Square(1)
        square_3 = Square(3)
        expected_position_1 = 329728
        expected_position_3 = 1319424

        get_position_1 = generate_knight_moves(self.board, square_1)
        get_position_3 = generate_knight_moves(self.board, square_3)

        self.assertEqual(expected_position_1, get_position_1)
        self.assertEqual(expected_position_3, get_position_3)

if __name__ == "__main__":
    unittest.main()