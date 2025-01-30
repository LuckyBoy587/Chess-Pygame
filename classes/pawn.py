from classes.piece import BasePiece


def is_at_base(i: int, color: str) -> bool:
    if color == "white":
        return i == 6
    else:
        return i == 1


class Pawn(BasePiece):
    def __init__(self,color: str):
        super().__init__(color)
        self.direction = 1


class BlackPawn(Pawn):
    def __init__(self):
        super().__init__("black")
        self.image_index = 11
        self.direction = 1


class WhitePawn(Pawn):
    def __init__(self):
        super().__init__("white")
        self.image_index = 5
        self.direction = -1
