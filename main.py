import sys

import pygame

import Trash
import Truck

BLOCK_SIZE = 50
WIDTH, HEIGHT = BLOCK_SIZE * 10, BLOCK_SIZE * 10

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_grid(surface):
    surface.fill(BLACK)
    for x in range(WIDTH // BLOCK_SIZE):
        for y in range(HEIGHT // BLOCK_SIZE):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(BLACK)
    pygame.display.set_caption("Crate")

    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    draw_grid(surface)

    clock = pygame.time.Clock()

    truck = Truck.Truck()
    trash = Trash.Trash()

    run = True

    while run:
        clock.tick(FPS)
        truck.handling_navigation()
        draw_grid(surface)

        if truck.position == trash.position:
            trash.randomize()

        truck.put_on_map(surface)
        trash.put_on_map(surface)

        window.blit(surface, (0, 0))
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
