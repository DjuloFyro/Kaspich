import unittest
import sys
import os

# Add the path to the 'src' folder to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

from board import Board
from move_generation import *

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
        # Base case: reached the desired depth, return 1 for the current position.
        return 1

    count = 0
    moves = generate_legal_moves(board)
    for m in moves:
        # For each legal move, recursively calculate the number of legal positions at the next depth.
        count += perft(board.apply_move(m), depth-1)

    return count

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the Board instance and initialize the chessboard for each test case.
        """
        self.board = Board()
        self.board.board_initialization()

    def test_from_depth0_to_depth3(self) -> None:
        """
        Test the perft function for depths 0 to 3 and compare the results with known values.
        """
        depth0 = perft(self.board, 0)
        depth1 = perft(self.board, 1)
        depth2 = perft(self.board, 2)
        depth3 = perft(self.board, 3)

        # The expected number of legal positions at each depth based on chess perft values.
        self.assertEqual(depth0, 1)
        self.assertEqual(depth1, 20)
        self.assertEqual(depth2, 400)
        self.assertEqual(depth3, 8902)

    def test_from_depth4(self) -> None:
        """
        Test the perft function for depth 4 and compare the result with the known value.
        """
        depth4 = perft(self.board, 4)
        #depth5 = perft(self.board, 5)

        # The expected number of legal positions at depth 4 and 5 based on chess perft values.
        self.assertEqual(depth4, 197281)
        #self.assertEqual(depth5, 4865609)

if __name__ == "__main__":
    # Run the test cases
    unittest.main()
