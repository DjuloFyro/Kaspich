import numpy as np

from square import Square
from enums import File, Rank

EMPTY_BB = np.uint64(0)

RANKS = np.uint64(0x00000000000000FF) << np.arange(8, dtype=np.uint64) * 8
FILES = np.uint64(0x0101010101010101) << np.arange(8, dtype=np.uint64)

RANK_MASKS = RANKS.repeat(8)
FILE_MASKS = np.tile(FILES, 8)

def precompute_kings_move(index):
    square = Square(index)
    bitboard = square.to_bitboard()

    w = (bitboard & ~FILES[File.A]) >> np.uint8(1)
    nw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.EIGHT]) << np.uint8(7)
    n = (bitboard & ~RANKS[Rank.EIGHT]) << np.uint8(8)
    ne = (bitboard & ~FILES[File.H] & ~RANKS[Rank.EIGHT]) << np.uint8(9)
    e = (bitboard & ~FILES[File.H]) << np.uint8(1)
    se = (bitboard & ~FILES[File.H] & ~RANKS[Rank.ONE]) >> np.uint8(7)
    s = (bitboard & ~RANKS[Rank.ONE]) >> np.uint8(8)
    sw = (bitboard & ~FILES[File.A] & ~RANKS[Rank.ONE]) >> np.uint8(9)

    return w | nw | n | ne | e | se | s | sw


KING_MOVES = np.fromiter(
        (precompute_kings_move(i) for i in range(64)),
        dtype=np.uint64,
        count=64)


if __name__ == "__main__":
    print(KING_MOVES)
