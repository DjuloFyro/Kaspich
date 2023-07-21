import numpy as np
from square import Square

class Move:
    def __init__(self, src, dest, promo=None):
        """
        src is Square representing source square
        dst is Square representing destination square
        promo is Piece representing promotion
        """
        self.src = src
        self.dest = dest
        self.promo = promo

    def __str__(self):
        if self.promo:
            return "%s%s = %s" % (str(self.src), str(self.dest), self.promo.name)
        else:
            return "%s%s" % (str(self.src), str(self.dest))
    
    def from_str(s):
        src_file = np.uint8(ord(s[0]) - 97)
        src_rank = np.uint8(s[1])
        dest_file = np.uint8(ord(s[2]) - 97)
        dest_rank = np.uint8(s[3])

        square_src = Square(src_rank * 8 + src_file - 1)
        square_dest = Square(dest_rank * 8 + dest_file - 1)

        return Move(src=square_src, dest=square_dest)





