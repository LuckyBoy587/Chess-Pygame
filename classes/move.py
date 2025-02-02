from classes.utils import Position


class Move:
    def __init__(self, from_pos: Position, to_pos: Position, piece, captured_piece=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured_piece = captured_piece

    def __repr__(self):
        return f"Move({self.piece}, {self.from_pos} -> {self.to_pos}, Captured: {self.captured_piece})"
