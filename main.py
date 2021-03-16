import pygame
import os

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crate")
FPS = 60
VEL = 10

TRUCK_IMAGE = pygame.image.load(os.path.join('Assets', 'truck.png'))
TRUCK_WIDTH, TRUCK_HEIGHT = 31, 15
TRUCK = pygame.transform.scale(TRUCK_IMAGE, (TRUCK_WIDTH, TRUCK_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_grid():
    block_size = 50
    for x in range(WIDTH // block_size):
        for y in range(HEIGHT // block_size):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(WIN, BLACK, rect, 1)


def draw_window(truck):
    WIN.fill(WHITE)
    draw_grid()
    WIN.blit(TRUCK, (truck.x, truck.y))
    pygame.display.update()


def truck_movement(keys_pressed, truck):
    if keys_pressed[pygame.K_LEFT] and truck.x - VEL > 0:
        truck.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and truck.x + VEL < WIDTH - TRUCK.get_width():
        truck.x += VEL
    if keys_pressed[pygame.K_UP] and truck.y - VEL > 0:
        truck.y -= VEL
    if keys_pressed[pygame.K_DOWN] and truck.y + VEL < HEIGHT - TRUCK.get_height():
        truck.y += VEL


def main():
    truck = pygame.Rect(10, 10, TRUCK_WIDTH, TRUCK_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        truck_movement(keys_pressed, truck)

        draw_window(truck)

    pygame.quit()


if __name__ == '__main__':
    main()
