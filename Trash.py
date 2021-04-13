import pygame
import main
import random

TYPES_DICT = {0: "metal", 1: "plastic", 2: "paper", 3: "glass"}
TYPES_COLOR = {"metal": (123, 123, 123), "plastic": (255, 255, 0), "paper": (0, 102, 255), "glass": (51, 204, 51)}


class Trash:  # śmieci, które będziemy odbierać i zawozić na wysypisko
    def __init__(self):
        self.position = (0, 0)
        self.type = TYPES_COLOR["metal"]
        self.randomize()

    def randomize(self):
        self.random_position()
        self.random_type()

    def random_position(self):
        random_x = random.randint(0, 9) * main.BLOCK_SIZE
        random_y = random.randint(0, 9) * main.BLOCK_SIZE

        self.position = (random_x, random_y)

    def random_type(self):
        random_num = random.randint(0, 3)
        new_type = TYPES_COLOR[TYPES_DICT[random_num]]

        self.type = new_type

    def put_on_map(self, surface):
        x, y = self.position[0], self.position[1]
        rect = pygame.Rect(x, y, main.BLOCK_SIZE, main.BLOCK_SIZE)
        pygame.draw.rect(surface, self.type, rect, 0, border_radius=10)
