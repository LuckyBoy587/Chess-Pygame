import pygame

from classes.utils import Position

pygame.init()

width, height = 640, 640
window = pygame.display.set_mode((width, height))
board_image = pygame.image.load("./images/board.png")
pygame.display.set_caption('Basic Pygame Window')

from classes.game import Game

game = Game()
clock = pygame.time.Clock()

def main():
    while True:
        clock.tick(60)
        window.blit(board_image, (0, 0))
        game.draw_board(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // (height // 8)
                col = x // (width // 8)
                game.handle_mouse_click(Position(row, col))

        pygame.display.flip()


if __name__ == '__main__':
    main()
