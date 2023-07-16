import numpy as np

class Square():
    def __init__(self, position) -> None:
        self.position = np.uint8(position)

    def to_bitboard(self) -> np.uint64:
        return np.uint64(1) << self.position