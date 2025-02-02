import pygame

from classes.constants import PIECE_SIZE


class Position:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.i == other.i and self.j == other.j
        return False

    def __hash__(self):
        return hash((self.i, self.j))

    def __repr__(self):
        return f"Position(i={self.i}, j={self.j})"

    def getX(self):
        return self.j * PIECE_SIZE

    def getY(self):
        return self.i * PIECE_SIZE


def highlight_cell(surface: pygame.Surface, cell: Position, colour: tuple[int, int, int]):
    rect = pygame.Rect(cell.getX(), cell.getY(), PIECE_SIZE, PIECE_SIZE)
    pygame.draw.rect(surface, colour, rect, 2)


class PieceDrawer:
    def __init__(self):
        self.image = pygame.image.load("images/pieces.png").convert_alpha()
        self.rect = self.image.get_rect()
        w = self.rect.width // 6
        h = self.rect.height // 2
        self.cells = list([(i % 6 * w, i // 6 * h, w, h) for i in range(12)])
        self.cell_width = self.cell_height = 80

    def draw(self, surface, coords: Position, image_index: int):
        offset = 2
        surface.blit(self.image, (coords.getX() - offset, coords.getY() - offset), self.cells[image_index])


class CastlingMove:
    def __init__(self, king_pos: Position, direction: int):
        self.king_from_pos = king_pos
        self.king_to_pos = Position(king_pos.i, king_pos.j + 2 * direction)
        self.rook_from_pos = Position(king_pos.i, 0 if direction == -1 else 7)
        self.rook_to_pos = Position(king_pos.i, king_pos.j + direction)

    def __eq__(self, __value):
        if isinstance(__value, Position):
            return __value == self.king_to_pos

        return False
