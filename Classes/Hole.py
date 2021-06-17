import pygame

from variables import *


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.holes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load('./Assets/hole_big.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
