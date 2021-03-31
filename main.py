import pygame
import os

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crate")
FPS = 60
VEL = 50


TRUCK_RIGHT_IMAGE = pygame.image.load(os.path.join('Assets', 'truck.png'))
TRUCK_LEFT_IMAGE = pygame.image.load(os.path.join('Assets', 'truck_2.png'))
# TRASH_IMAGE = pygame.image.load(os.path.join('Assets', 'trash.png'))
# GRASS_IMAGE = pygame.image.load(os.path.join('Assets', 'grass.png'))

TRUCK_WIDTH, TRUCK_HEIGHT = 31, 15
TRUCK_RIGHT = pygame.transform.scale(TRUCK_RIGHT_IMAGE, (TRUCK_WIDTH, TRUCK_HEIGHT))
TRUCK_LEFT = pygame.transform.scale(TRUCK_LEFT_IMAGE, (TRUCK_WIDTH, TRUCK_HEIGHT))

# GRASS_WIDTH, GRASS_HEIGHT = 50, 50
# GRASS = pygame.transform.scale(GRASS_IMAGE, (GRASS_WIDTH, GRASS_HEIGHT))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

mapElements = []


def check_if_position_empty(position):
    for i in mapElements:
        if i.position == position:
            return False
        return True


# def add_bins():
#     for i in range(0, ):
#         rightPosition = False
#         while not rightPosition:
#             x = randint(0, )
#             y = randint(0,)
#             if checkIfPositionEmpty([x,y]):
#                 rightPosition = True
#         element = Trash(x, y)
#         mapElements.append(element)
#         # dodac do gridu
#
# def add_grass():
#     for i in range (0, WIDTH ):
#         for j in range (0, HEIGHT):
#             if checkIfPositionEmpty([i.j]):
#                 element =
#                 mapElements.append(element)
#                 # dodac do gridu
#


def draw_grid():
    block_size = 50
    for x in range(WIDTH // block_size):
        for y in range(HEIGHT // block_size):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(WIN, BLACK, rect, 1)


def draw_window(truck, photo):
    WIN.fill(WHITE)
    draw_grid()
    WIN.blit(photo, (truck.x, truck.y))

    pygame.display.update()


def truck_movement(event, truck):
    if event.key == pygame.K_LEFT and truck.x - VEL > 0:
        truck.x -= VEL
        draw_window(truck, TRUCK_LEFT)
    if event.key == pygame.K_RIGHT and truck.x + VEL < WIDTH - TRUCK_RIGHT.get_width():
        truck.x += VEL
        draw_window(truck, TRUCK_RIGHT)
    if event.key == pygame.K_UP and truck.y - VEL > 0:
        truck.y -= VEL
        draw_window(truck, TRUCK_RIGHT)
    if event.key == pygame.K_DOWN and truck.y + VEL < HEIGHT - TRUCK_RIGHT.get_height():
        truck.y += VEL
        draw_window(truck, TRUCK_RIGHT)


def main():
    truck = pygame.Rect(10, 15, TRUCK_WIDTH, TRUCK_HEIGHT)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                truck_movement(event, truck)

    pygame.quit()


if __name__ == '__main__':
    main()
