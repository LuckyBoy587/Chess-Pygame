from classes.piece import BasePiece


class Rook(BasePiece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

class BlackRook(Rook):
    def __init__(self):
        super().__init__("black")
        self.image_index = 10

class WhiteRook(Rook):
    def __init__(self):
        super().__init__("white")
        self.image_index = 4