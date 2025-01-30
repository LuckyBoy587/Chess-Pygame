from classes.piece import BasePiece


class Bishop(BasePiece):
    def __init__(self, color):
        super().__init__(color)

class BlackBishop(Bishop):
    def __init__(self):
        super().__init__("black")
        self.image_index = 8

class WhiteBishop(Bishop):
    def __init__(self):
        super().__init__("white")
        self.image_index = 2