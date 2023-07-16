import unittest
import numpy as np
from io import StringIO
import sys
import os

# Add the path to the 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

from board import Board

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.board.board_initialization()


    def test_piece_placement(self) -> None:
        self.assertEqual(self.board.kings['white'], np.uint64(0x0000000000000010))
        self.assertEqual(self.board.queens['white'], np.uint64(0x0000000000000008))
        self.assertEqual(self.board.knights['white'], np.uint64(0x0000000000000042))
        self.assertEqual(self.board.bishops['white'], np.uint64(0x0000000000000024))
        self.assertEqual(self.board.rooks['white'], np.uint64(0x0000000000000081))
        self.assertEqual(self.board.pawns['white'], np.uint64(0x000000000000FF00))

        self.assertEqual(self.board.kings['black'], np.uint64(0x1000000000000000))
        self.assertEqual(self.board.queens['black'], np.uint64(0x0800000000000000))
        self.assertEqual(self.board.knights['black'], np.uint64(0x4200000000000000))
        self.assertEqual(self.board.bishops['black'], np.uint64(0x2400000000000000))
        self.assertEqual(self.board.rooks['black'], np.uint64(0x8100000000000000))
        self.assertEqual(self.board.pawns['black'], np.uint64(0x00FF000000000000))


    def test_print_board(self) -> None:
        captured_output = StringIO()
        sys.stdout = captured_output

        self.board.print_board()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected_output = (
            'r n b q k b n r \n'
            'p p p p p p p p \n'
            '. . . . . . . . \n'
            '. . . . . . . . \n'
            '. . . . . . . . \n'
            '. . . . . . . . \n'
            'P P P P P P P P \n'
            'R N B Q K B N R'
        )

        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()