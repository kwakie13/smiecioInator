import time

import pygame as pg

from Classes import Searching
from variables import *


class Truck(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.x = x
        self.y = y
        self.rotation = 0  # 0 - right, 1 - down, 2 - left, 3 - up

        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.truck_image(self.rotation)
        self.rect = self.image.get_rect()

        self.move_list = []

        self.mass = 0
        self.space = 0

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
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.truck_image(self.rotation)

    def start_search(self, destination, search_type=1):
        goal = [Searching.State(destination.x, destination.y, 0), Searching.State(destination.x, destination.y, 1),
                Searching.State(destination.x, destination.y, 2), Searching.State(destination.x, destination.y, 3)]
        istate = Searching.State(self.x, self.y, self.rotation)
        searching_object = Searching.Search(istate, goal, self.game.borders, self.game.houses, self.game.holes)

        if search_type == 1:
            self.move_list = searching_object.search_a_star()
        else:
            self.move_list = searching_object.search_BFS()

        return searching_object.end_cost

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
            time.sleep(TIME_BETWEEN_AUTO_MOVES)

        self.move_list = []

    def truck_image(self, rotation=0):
        self.image = pg.image.load(TRUCK_PICS[rotation])
