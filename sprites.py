import pygame as pg
from variables import *
import random


class Truck(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.collision(dx, dy):
            self.x += dx
            self.y += dy

    def collision(self, dx=0, dy=0):
        for border in self.game.borders:
            if border.x == self.x + dx and border.y == self.y + dy:
                return True

        for house in self.game.houses:
            if house.x == self.x + dx and house.y == self.y + dy:
                return True

        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Border(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.borders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_border(self):
        return self.x, self.y


class House(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.houses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Trash(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.random_type()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

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
        new_type = TYPES_COLOR[TYPES_DICT[random_num]]
        self.image.fill(new_type)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
