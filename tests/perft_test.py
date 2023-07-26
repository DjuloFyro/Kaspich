import unittest
import sys
import os

# Add the path to the 'src' folder to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

from board import *

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
        #depth6 = perft(self.board, 6)

        # The expected number of legal positions at depth 4 and 5 based on chess perft values.
        self.assertEqual(depth4, 197281)
        #self.assertEqual(depth5, 4865609)
        #self.assertEqual(depth6, 119060324)

if __name__ == "__main__":
    # Run the test cases
    unittest.main()
