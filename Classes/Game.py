import os
import random
import sys
from os import path

import numpy as np
import pygame

from Classes import Border, Hole, House, Trash, Truck, Dump
from DecisionTree import tree
from NeuralNetwork import network
from variables import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)

        self.playing = True
        self.dt = None

        # map elements
        self.all_sprites = None
        self.borders = None
        self.houses = None
        self.holes = None
        self.trashes = None

        self.dump = None
        self.trash = None
        self.truck = None

        self.map_data = []

        # parameters for decision tree
        self.distance_to_dump = None
        self.distance_to_trash = None

        self.decision_tree = None
        self.made_decision = []

        # variable to keep neural network inside class
        self.neural_network = None

        # elements used for genetic algorithm
        self.route = None

        self.spawn_coords = []
        self.removed_trash = 0

        self.iter = 0
        self.trash_list = list()

        print("\nPress L on your keyboard to load neccessary assets (machine learning methods)\n")

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, '../Assets/map.txt'), 'rt') as file:
            for line in file:
                self.map_data.append(line)

    def new(self):  # initialize variables and setup a new game
        self.all_sprites = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.trashes = pygame.sprite.Group()
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
                    Trash.Trash(self, col, row)
                if tile == 'T':
                    var_x, var_y = col, row

        self.truck = Truck.Truck(self, var_x, var_y)
        self.trash_list = self.split_trash()

    def run(self):  # game loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def split_trash(self):
        trash_list = []
        for trash in self.trashes:
            trash_list.append(trash)

        return trash_list

    @staticmethod
    def quit():
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

                # ===== A* and BFS disabled - more than 1 trash is on the map =====
                #
                # if event.key == pygame.K_a:  # run A*
                #     self.truck.start_search(self.trash, 1)
                #     self.truck.move_truck()
                #     pygame.event.clear()

                # if event.key == pygame.K_b:  # run BFS
                #     self.truck.start_search(self.trash, 2)
                #     self.truck.move_truck()
                #     pygame.event.clear()

                if event.key == pygame.K_l:  # load machine learning methods
                    # DECISION TREE
                    if path.isfile('./DecisionTree/tree_model') and not os.stat(
                            './DecisionTree/tree_model').st_size == 0:
                        self.decision_tree = tree.load_tree_from_structure('./DecisionTree/tree_model')
                        print("Tree model loaded!")

                    else:
                        print("Problem with loading decision tree!")

                    # NEURAL NETWORK
                    if path.isfile('./NeuralNetwork/network_model.pth') and not os.stat(
                            './NeuralNetwork/network_model.pth').st_size == 0:
                        self.neural_network = network.Net()
                        network.load_network_from_structure(self.neural_network)
                        self.neural_network.eval()
                        print("Neural network loaded!")

                    else:
                        print("Problem with loading neural network!")

                    # GENETIC ALGORITHM
                    if path.isfile('./GeneticAlgorithm/algorithm_model.npy') and not os.stat(
                            './GeneticAlgorithm/algorithm_model.npy').st_size == 0:
                        self.route = np.load('./GeneticAlgorithm/algorithm_model.npy').tolist()
                        print("Genetic algorithm result loaded!")

                    else:
                        print("Problem with loading genetic algorithm result!")

                    print("")

                    pygame.event.clear()

                if event.key == pygame.K_g:
                    element = self.iter

                    self.get_distance_to_dump()
                    self.get_distance_to_trash(element)

                    self.print_information(element)

                    if self.distance_to_dump == 1:
                        self.made_decision = [1]

                    elif self.removed_trash == 10:
                        self.made_decision = [0]

                    else:
                        self.made_decision = tree.making_decision(self.decision_tree,
                                                                  self.distance_to_dump // 40 + 1,
                                                                  self.distance_to_trash // 40 + 1,
                                                                  self.truck.mass // 20 + 1, self.truck.space // 20 + 1,
                                                                  self.trash_list[element].mass // 20 + 1,
                                                                  self.trash_list[element].space // 20 + 1)

                    if self.made_decision[0] == 0:
                        print("\n==DECISION TREE - DECISION==\nGo to dump, free the truck!\n")

                        self.truck.start_search(self.dump, 1)
                        self.truck.move_truck()

                        self.truck.empty_truck()

                        self.truck.start_search(self.trash_list[element], 1)
                        self.truck.move_truck()

                        pygame.event.clear()

                    elif self.made_decision[0] == 1:
                        print("\n==DECISION TREE - DECISION==\nGo to trash, pick it up!\n")

                        self.truck.start_search(self.trash_list[element], 1)
                        self.truck.move_truck()

                        pygame.event.clear()

                    else:
                        print("Decision tree error!\n")

                    self.iter += 1

                pygame.event.clear()

            self.truck.pickup_trash()

            self.truck.empty_truck()

            self.respawn_trashes()

    def get_distance_to_dump(self):
        if self.truck.x == self.dump.x and self.truck.y == self.dump.y:
            self.distance_to_dump = 1
        else:
            self.distance_to_dump = self.truck.start_search(self.dump, 1)

    def get_distance_to_trash(self, index):
        self.distance_to_trash = self.truck.start_search(self.trash_list[index], 1)

    def print_information(self, index):
        print("==PARAMETERS TAKEN TO DECISION MAKING PROCESS==")
        print("Dump distance: {0}\nTrash distance: {1}".format(self.distance_to_dump, self.distance_to_trash),
              "\nTruck filled (mass): {0}\nTruck filled (space): {1}".format(self.truck.mass, self.truck.space),
              "\nTrash mass: {0}\nTrash volume: {1}".format(self.trash_list[index].mass, self.trash_list[index].space))

    def respawn_trashes(self):
        if self.removed_trash == 10 and len(self.spawn_coords) == 10 and (
                self.spawn_coords[9][0] != self.truck.x or self.spawn_coords[9][1] != self.truck.y):
            for coords in self.spawn_coords:
                Trash.Trash(self, coords[0], coords[1])

            self.spawn_coords = []
            self.removed_trash = 0
