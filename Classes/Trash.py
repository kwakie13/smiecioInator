import random

import pygame as pg

from variables import *


class Trash(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.random_type()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mass = None
        self.space = None
        self.random_size()

    def change_details(self):
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
        self.random_type()
        self.random_size()

    def collision(self, x, y):
        for border in self.game.borders:
            if border.x == x and border.y == y:
                return True

        for house in self.game.houses:
            if house.x == x and house.y == y:
                return True

        return False

    def random_type(self):
        random_num = random.randint(0, 3)
        new_type = TYPES_PICS[TYPES_DICT[random_num]]
        self.image = pg.image.load(new_type)

    def random_size(self):
        self.mass = random.randint(0, 25)
        self.space = random.randint(0, 25)

    def update(self):
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
