import pygame
import sys
from os import path
from sprites import *


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
        with open(path.join(game_folder, 'map.txt'), 'rt') as file:
            for line in file:
                self.map_data.append(line)

    def new(self):  # initialize variables and setup a new game
        self.all_sprites = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Border(self, col, row)
                if tile == 'T':
                    self.truck = Truck(self, col, row)
                if tile == 'H':
                    House(self, col, row)
                if tile == 'R':
                    self.trash = Trash(self, col, row)


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
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, GREY, (0, y), (WIDTH, y))

    def draw_missing_borders(self):
        pygame.draw.line(self.screen, GREY, (640, 64), (640, 640))
        pygame.draw.line(self.screen, GREY, (64, 640), (640, 640))

    def draw(self):
        self.screen.fill(BGCOLOR)
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
                    self.truck.move(dx=-1)
                if event.key == pygame.K_RIGHT:
                    self.truck.move(dx=1)
                if event.key == pygame.K_UP:
                    self.truck.move(dy=-1)
                if event.key == pygame.K_DOWN:
                    self.truck.move(dy=1)
            if self.truck.x == self.trash.x and self.truck.y == self.trash.y:
                self.trash.change_details()


g = Game()
while True:
    g.new()
    g.run()
