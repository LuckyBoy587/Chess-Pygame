import pygame

from classes.constants import PIECE_SIZE


def highlight_cell(surface: pygame.Surface, cell: tuple[int, int], colour: tuple[int, int, int]):
    rect = pygame.Rect(cell[1] * PIECE_SIZE, cell[0] * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE)
    pygame.draw.rect(surface, colour, rect, 2)


class PieceDrawer:
    def __init__(self):
        self.image = pygame.image.load("images/pieces.png").convert_alpha()
        self.rect = self.image.get_rect()
        w = self.rect.width // 6
        h = self.rect.height // 2
        self.cells = list([(i % 6 * w, i // 6 * h, w, h) for i in range(12)])
        self.cell_width = self.cell_height = 80

    def draw(self, surface, coords: tuple[int, int], image_index: int):
        offset = 2
        surface.blit(self.image, (coords[0] - offset, coords[1] - offset), self.cells[image_index])
