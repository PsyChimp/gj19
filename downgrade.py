import pygame
from pygame.locals import *

import globals


class Downgrade(object):
    def __init__(self, game):
        self.activated = False
        self.game = game

    def apply(self):
        return NotImplementedError


class OneHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        globals.PLAYER_MAX_HEALTH = 1


class MoveSpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        globals.PLAYER_SPEED *= 0.5


class EnemySpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        globals.ENEMY_SPEED *= 2


class EnemyHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        globals.ENEMY_MAX_HEALTH *= 2





