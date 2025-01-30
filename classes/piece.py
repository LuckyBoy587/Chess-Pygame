class BasePiece:
    def __init__(self, color: str):
        self.size = 80
        self.color = color
        self.image_index = -1

    def is_white(self):
        return self.color == "white"
