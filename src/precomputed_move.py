import numpy as np
from square import Square
from enums import File, Rank, Color

# Define an empty bitboard to represent an empty chessboard
EMPTY_BB = np.uint64(0)

# Precompute RANKS and FILES bitboards for efficient move generation
RANKS = np.uint64(0x00000000000000FF) << np.arange(8, dtype=np.uint64) * 8
FILES = np.uint64(0x0101010101010101) << np.arange(8, dtype=np.uint64)

# Precompute masks for each rank and file
RANK_MASKS = RANKS.repeat(8)
FILE_MASKS = np.tile(FILES, 8)

def precompute_kings_move(index):
    """
    Precompute the king's moves for a given square index on the chessboard.

    Parameters:
        index (int): The index of the square on the chessboard (0 to 63).

    Returns:
        np.uint64: A bitboard representing all possible moves for the king from the given square.
    """
    square = Square(index)
    bitboard = square.to_bitboard()

    # Calculate possible moves in different directions using bitwise operations
    w = (bitboard & ~FILES[File.A]) >> np.uint8(1)
    nw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.EIGHT]) << np.uint8(7)
    n = (bitboard & ~RANKS[Rank.EIGHT]) << np.uint8(8)
    ne = (bitboard & ~FILES[File.H] & ~RANKS[Rank.EIGHT]) << np.uint8(9)
    e = (bitboard & ~FILES[File.H]) << np.uint8(1)
    se = (bitboard & ~FILES[File.H] & ~RANKS[Rank.ONE]) >> np.uint8(7)
    s = (bitboard & ~RANKS[Rank.ONE]) >> np.uint8(8)
    sw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.ONE]) >> np.uint8(9)

    # Combine all possible moves to get the final moves for the king from the given square
    return w | nw | n | ne | e | se | s | sw

# Precompute king moves for all squares on the chessboard
KING_MOVES = np.fromiter(
    (precompute_kings_move(i) for i in range(64)),
    dtype=np.uint64,
    count=64
)

if __name__ == "__main__":
    print(str(Color.BLACK))
