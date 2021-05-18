import pygame as pg

from variables import *


class House(pg.sprite.Sprite):
    def __init__(self, game, x, y, version=0):
        self.groups = game.all_sprites, game.houses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pg.image.load(HOUSE_PICS[version])
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
