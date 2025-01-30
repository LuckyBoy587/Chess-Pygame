from classes.piece import BasePiece


class Queen(BasePiece):
    def __init__(self,  color):
        super().__init__(color)

class BlackQueen(Queen):
    def __init__(self):
        super().__init__("black")
        self.image_index = 7

class WhiteQueen(Queen):
    def __init__(self):
        super().__init__("white")
        self.image_index = 1