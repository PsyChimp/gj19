import pygame
from pygame.locals import *

from globals import *


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
        self.game.PLAYER_SPEED *= 0.5


class EnemySpeedDowngrade(Downgrade):
    def apply(self):
        self.game.ENEMY_SPEED *= 2


class EnemyHPDowngrade(Downgrade):
    def apply(self):
        self.game.ENEMY_MAX_HEALTH *= 2
