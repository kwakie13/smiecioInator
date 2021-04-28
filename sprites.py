import random
import time

import pygame as pg

from graph_search import *
from variables import *


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
        self.rotation = 0  # 0 - right, 1 - down, 2 - left, 3 - up
        self.move_list = []

    def move(self, rotation=0):
        if not self.collision(rotation):
            if rotation == 0:
                self.x += 1
            elif rotation == 1:
                self.y += 1
            elif rotation == 2:
                self.x -= 1
            elif rotation == 3:
                self.y -= 1

    def rotate(self, direction=1):  # 1 - right, -1 - left
        if self.rotation == 0 and direction == -1:
            self.rotation = 3
        elif self.rotation == 3 and direction == 1:
            self.rotation = 0
        else:
            self.rotation += direction

    def collision(self, rotation=0):
        dx = 0
        dy = 0

        if rotation == 0:
            dx = 1
        elif rotation == 1:
            dy = 1
        elif rotation == 2:
            dx = -1
        elif rotation == 3:
            dy = -1

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

    def start_search(self, trash, search_type=1):
        goal = [State(trash.x, trash.y, 0), State(trash.x, trash.y, 1), State(trash.x, trash.y, 2), State(trash.x, trash.y, 3)]
        istate = State(self.x, self.y, self.rotation)
        searching_object = Search(istate, goal, self.game.borders, self.game.houses, self.game.holes)
        print("Searching started...")
        if search_type == 1:
            self.move_list = searching_object.search_aStar()
        else:
            self.move_list = searching_object.search()
        print(self.move_list)

    def move_truck(self):
        for move in self.move_list:
            if move == "forward":
                self.move(self.rotation)
            if move == "rotate_right":
                self.rotate(1)
            if move == "rotate_left":
                self.rotate(-1)

            self.update()
            self.game.draw()
            time.sleep(0.3)

        self.move_list = []


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


class Hole(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.holes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(MEDIUM_GREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
