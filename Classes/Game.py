import os
import random
import sys
from os import path

import pygame

from Classes import Border, Hole, House, Trash, Truck, Dump
from DecisionTree import tree
from variables import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, '../Assets/map.txt'), 'rt') as file:
            for line in file:
                self.map_data.append(line)

    def new(self):  # initialize variables and setup a new game
        self.all_sprites = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        var_x, var_y = 0, 0
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Border.Border(self, col, row)
                if tile == 'H':
                    House.House(self, col, row, random.randint(0, 2))
                if tile == 'O':
                    Hole.Hole(self, col, row)
                if tile == 'D':
                    self.dump = Dump.Dump(self, col, row)
                if tile == 'R':
                    self.trash = Trash.Trash(self, col, row)
                if tile == 'T':
                    var_x, var_y = col, row

        self.truck = Truck.Truck(self, var_x, var_y)

    def run(self):  # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):  # update game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (WIDTH, y))

    def draw_missing_borders(self):
        pygame.draw.line(self.screen, GREY, (704, 64), (704, 704))
        pygame.draw.line(self.screen, GREY, (64, 704), (704, 704))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_missing_borders()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                if event.key == pygame.K_LEFT:
                    self.truck.rotate(direction=-1)

                if event.key == pygame.K_RIGHT:
                    self.truck.rotate(direction=1)

                if event.key == pygame.K_UP:
                    self.truck.move(rotation=self.truck.rotation)

                if event.key == pygame.K_a:  # run A*
                    self.truck.start_search(self.trash, 1)
                    self.truck.move_truck()
                    pygame.event.clear()

                if event.key == pygame.K_b:  # run BFS
                    self.truck.start_search(self.trash, 2)
                    self.truck.move_truck()
                    pygame.event.clear()

                if event.key == pygame.K_d:  # decision tree
                    self.distance_to_dump = self.truck.start_search(self.dump, 1)
                    self.distance_to_trash = self.truck.start_search(self.trash, 1)

                    print(
                        "Dump distance: {0}\nTrash distance: {1}\nTruck filled (mass): {2}\nTruck filled (space): {3}\nTrash mass: {4}\nTrash volume: {5}".format(
                            self.distance_to_dump, self.distance_to_trash, self.truck.mass, self.truck.space,
                            self.trash.mass, self.trash.space))

                    self.made_decision = tree.making_decision(self.decision_tree, self.distance_to_dump,
                                                              self.distance_to_trash, self.truck.mass // 20 + 1,
                                                              self.truck.space // 20 + 1, self.trash.mass // 20 + 1,
                                                              self.trash.space // 20 + 1)

                    if self.made_decision[0] == 0:
                        print("Go to dump, free the truck!\n")
                    elif self.made_decision[0] == 1:
                        print("Go to trash, pick it up!\n")

                # if event.key == pygame.K_g:
                #     if self.made_decision[0] == 0:
                #         self.truck.start_search(self.dump, 1)
                #
                #     self.truck.move_truck()
                #     pygame.event.clear()

                if event.key == pygame.K_l:  # learn the tree
                    if path.isfile('./DecisionTree/tree_model') and not os.stat(
                            './DecisionTree/tree_model').st_size == 0:
                        self.decision_tree = tree.load_tree_from_structure('./DecisionTree/tree_model')
                        print("Tree model already exists!\n")
                    else:
                        gen_tree = tree.learning_tree()
                        tree.save_tree_to_txt(gen_tree)
                        tree.save_tree_to_png(gen_tree)
                        tree.save_tree_to_structure(gen_tree)
                        self.decision_tree = tree.load_tree_from_structure('./DecisionTree/tree_model')
                        print("Tree model created!\n")

            if self.truck.x == self.trash.x and self.truck.y == self.trash.y:
                self.truck.mass += self.trash.mass
                self.truck.space += self.trash.space
                self.trash.change_details()

            if self.truck.x == self.dump.x and self.truck.x == self.dump.y and self.truck.mass > 0 and self.truck.space > 0:
                self.truck.mass = 0
                self.truck.space = 0
