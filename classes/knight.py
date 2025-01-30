from classes.piece import BasePiece


class Knight(BasePiece):
    def __init__(self, color):
        super().__init__(color)

class BlackKnight(Knight):
    def __init__(self):
        super().__init__("black")
        self.image_index = 9

class WhiteKnight(Knight):
    def __init__(self):
        super().__init__("white")
        self.image_index = 3