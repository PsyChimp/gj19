import pygame
from pygame.locals import *

import main
import enemy


class Downgrade(object):
    def __init__(self, game):
        self.activated = False
        self.game = game

    def apply(self):
        return NotImplementedError


class OneHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        print("onehp")
        self.game.player.hp = 1


class MoveSpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        print("pspeed")
        self.game.PLAYER_SPEED = self.game.PLAYER_SPEED * 0.5


class EnemySpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        print("espeed")
        self.game.ENEMY_SPEED = self.game.ENEMY_SPEED * 2


class EnemyHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        print("ehp")
        self.game.ENEMY_MAX_HEALTH = self.game.ENEMY_MAX_HEALTH * 2





