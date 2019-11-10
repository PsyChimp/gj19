import pygame
from pygame.locals import *

from globals import *

class Tile(object):
    def __init__(self, game, type, rect, img):
        self.game = game
        self.type = type
        self.rect = rect
        self.img = img

    def draw(self):
        self.game.screen.blit(self.img, self.rect)
