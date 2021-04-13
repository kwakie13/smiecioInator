import pygame
import main
import os

TRUCK_IMAGE = pygame.image.load(os.path.join('Assets', 'truck.png'))
TRUCK_WIDTH, TRUCK_HEIGHT = 50, 50
TRUCK = pygame.transform.scale(TRUCK_IMAGE, (TRUCK_WIDTH, TRUCK_HEIGHT))


class Truck:
    def __init__(self):
        self.position = (0, 0)

    def put_on_map(self, window):
        x, y = self.position[0], self.position[1]
        rect = pygame.Rect(x, y, TRUCK_WIDTH, TRUCK_HEIGHT)
        pygame.draw.rect(window, main.WHITE, rect, 0, border_radius=10)

    def handling_navigation(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.truck_movement(event)

    def truck_movement(self, event):
        if event.key == pygame.K_LEFT and self.position[0] - main.BLOCK_SIZE >= 0:
            self.alt_position("x", "neg")
        if event.key == pygame.K_RIGHT and self.position[0] + main.BLOCK_SIZE < 500:
            self.alt_position("x", "pos")
        if event.key == pygame.K_UP and self.position[1] - main.BLOCK_SIZE >= 0:
            self.alt_position("y", "neg")
        if event.key == pygame.K_DOWN and self.position[1] + main.BLOCK_SIZE < 500:
            self.alt_position("y", "pos")

    def alt_position(self, axis, symbol):
        x = self.position[0]
        y = self.position[1]

        if axis == "x":
            if symbol == "pos":
                self.position = (x + main.BLOCK_SIZE, y)
            elif symbol == "neg":
                self.position = (x - main.BLOCK_SIZE, y)
        elif axis == "y":
            if symbol == "pos":
                self.position = (x, y + main.BLOCK_SIZE)
            elif symbol == "neg":
                self.position = (x, y - main.BLOCK_SIZE)
