import os
import random

import pygame

from variables import *


class Trash(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.trashes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.type = str()
        self.image_path = str()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.mass = None
        self.space = None

        self.change_details()

    def change_details(self):
        # self.random_position() - commented as we use static positions for genetic algorithm
        self.random_type()
        self.random_file()
        self.random_size()

    def collision(self, x, y):
        for border in self.game.borders:
            if border.x == x and border.y == y:
                return True

        for house in self.game.houses:
            if house.x == x and house.y == y:
                return True

        for hole in self.game.holes:
            if hole.x == x and hole.y == y:
                return True

        return False

    def random_position(self):
        bad_coordinates = True

        rand_x = random.randint(1, 9)
        rand_y = random.randint(1, 9)

        while bad_coordinates:
            rand_x = random.randint(1, 9)
            rand_y = random.randint(1, 9)

            if not self.collision(rand_x, rand_y):
                bad_coordinates = False

        self.x = rand_x
        self.y = rand_y

    def random_type(self):
        random_num = random.randint(0, 3)
        new_type = TYPES_DICT[random_num]
        self.type = new_type

    def random_file(self):
        pics_folder = TYPES_PICS_SETS[self.type]
        selected_file = random.choice(os.listdir(pics_folder))

        self.image_path = pics_folder + '/' + selected_file
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def random_size(self):
        self.mass = random.randint(0, 25)
        self.space = random.randint(0, 25)

    def update(self):
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
