import unittest
import numpy as np
import sys
import os

# Add the path to the 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..", "src")
sys.path.insert(0, src_dir)

from precomputed_move import *

class TestPrecomputedMode(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the test environment before running each test case.
        """
        return super().setUp()

    def test_precomputed_kings_mode(self) -> None:
        """
        Test if the precomputed king moves are calculated correctly.

        The precomputed king moves are compared with the expected moves for each square on the chessboard.
        """
        # Define the expected king moves for each square on the chessboard
        expected_king_moves = np.array([770, 1797, 3594, 7188, 14376, 28752, 57504, 49216, 197123, 460039, 920078, 1840156, 3680312, 7360624, 14721248, 12599488, 50463488, 117769984, 235539968, 471079936, 942159872, 1884319744, 3768639488, 3225468928, 12918652928, 30149115904, 60298231808, 120596463616, 241192927232, 482385854464, 964771708928, 825720045568, 3307175149568, 7718173671424, 15436347342848, 30872694685696, 61745389371392, 123490778742784, 246981557485568, 211384331665408, 846636838289408, 1975852459884544, 3951704919769088, 7903409839538176, 15806819679076352, 31613639358152704, 63227278716305408, 54114388906344448, 216739030602088448, 505818229730443264, 1011636459460886528, 2023272918921773056, 4046545837843546112, 8093091675687092224, 16186183351374184448, 13853283560024178688, 144959613005987840, 362258295026614272, 724516590053228544, 1449033180106457088, 2898066360212914176, 5796132720425828352, 11592265440851656704, 4665729213955833856])

        # Compare the precomputed king moves with the expected moves
        self.assertTrue(np.array_equal(expected_king_moves, KING_MOVES))

if __name__ == "__main__":
    unittest.main()
