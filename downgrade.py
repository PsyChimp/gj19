import pygame
from pygame.locals import *

import globals


class Downgrade(object):
    def __init__(self, game):
        self.game = game

    def apply(self):
        return NotImplementedError


class OneHPDowngrade(Downgrade):
    def apply(self):
        self.game.player.hp = 1


class MoveSpeedDowngrade(Downgrade):
    def apply(self):
        globals.PLAYER_SPEED *= 0.5


class EnemySpeedDowngrade(Downgrade):
    def apply(self):
        globals.ENEMY_SPEED *= 2


class EnemyHPDowngrade(Downgrade):
    def apply(self):
        globals.ENEMY_MAX_HEALTH *= 2





