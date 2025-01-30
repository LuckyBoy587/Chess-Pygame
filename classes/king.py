from classes.piece import BasePiece


class King(BasePiece):
    def __init__(self, color):
        super().__init__(color)


class BlackKing(King):
    def __init__(self, ):
        super().__init__("black")
        self.image_index = 6


class WhiteKing(King):
    def __init__(self, ):
        super().__init__("white")
        self.image_index = 0
