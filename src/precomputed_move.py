import numpy as np

EMPTY_BB = np.uint64(0)

RANKS = np.uint64(0x00000000000000FF) << np.arange(8, dtype=np.uint64) * 8
FILES = np.uint64(0x0101010101010101) << np.arange(8, dtype=np.uint64)

RANK_MASKS = RANKS.repeat(8)
FILE_MASKS = np.tile(FILES, 8)

def precomputed_kings_move(index):
    print("----")


if __name__ == "__main__":
    precomputed_kings_move(0)