import pygame
from pygame.locals import *

from globals import *

class Downgrade(object):
    def __init__(self, game):
        self.game = game

    def apply(self):
        return NotImplementedError

class OneHpDowngrade(Downgrade):
    def apply(self):
        self.game.player.hp = 1
