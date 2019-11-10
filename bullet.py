import pygame
from pygame.locals import *

from globals import *
class Bullet(object):
    def __init__(self, game, pos, dir, player = False):
        self.game = game
        if(player):
            self.img = self.game.player_bullet_img
        else:
            self.img = self.game.enemy_bullet_img
        self.rect = Rect(0, 0, 20, 20)
        self.pos = pos
        self.dir = dir
        self.radius = 10
    def update(self):
        self.pos += self.dir * BULLET_SPEED * self.game.delta
        self.rect.center = self.pos
        for t in self.game.obstacles:
            if t.rect.colliderect(self.rect):
                return False
        for e in self.game.enemies:
            if self.pos.distance_squared_to(e.pos) <= (self.radius + e.radius) ** 2:
                e.hp -= 1
                return False
        return True
    def enemyUpdate(self):
        self.pos += self.dir * BULLET_SPEED * self.game.delta
        self.rect.center = self.pos
        for t in self.game.obstacles:
            if t.rect.colliderect(self.rect):
                return False
        if self.pos.distance_squared_to(self.game.player.pos) <= (self.radius + self.game.player.radius) ** 2:
            self.game.player.hp -= 1
            return False
        return True
    def draw(self):
        self.game.screen.blit(self.img, self.pos - (10, 10))
