import pygame
from pygame.locals import *

import main
import enemy


class Downgrade(object):
    def __init__(self, game):
        self.activated = False
        self.img = None
        self.game = game

    def apply(self):
        return NotImplementedError


class OneHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        self.img = pygame.image.load("./img/icons/1hp.png")
        print("onehp")
        self.game.player.hp = 1


class MoveSpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        self.img = pygame.image.load("./img/icons/slow_mov_speed.png")
        print("pspeed")
        self.game.PLAYER_SPEED = self.game.PLAYER_SPEED * 0.5


class EnemySpeedDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        self.img = pygame.image.load("./img/icons/plus_enemy_speed.png")
        print("espeed")
        self.game.ENEMY_SPEED = self.game.ENEMY_SPEED * 2


class EnemyHPDowngrade(Downgrade):
    def apply(self):
        self.activated = True
        self.img = pygame.image.load("./img/icons/plus_enemy_health.png")
        print("ehp")
        self.game.ENEMY_MAX_HEALTH = self.game.ENEMY_MAX_HEALTH * 2





