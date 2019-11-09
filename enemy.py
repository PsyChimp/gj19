import pygame
from enum import Enum
from pygame.locals import *

from globals import *

class Enemy(object):
    class AIState(Enum):
        Idle = 0
        Aggro = 1
    def __init__(self,game):
        self.game = game
        self.pos = pygame.math.Vector2(WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.img = self.game.player_img
        self.radius = 16
        self.can_move_x = True
        self.can_move_y = True
        self.state = self.AIState.Idle
    def update(self):
        # Update velocity
        self.vel.x = (self.game.keys[K_RIGHT] - self.game.keys[K_LEFT])
        self.vel.y = (self.game.keys[K_DOWN] - self.game.keys[K_UP])
        if self.vel.x != 0 or self.vel.y != 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED

        # Calculate new position
        new_pos = self.pos + (self.vel * self.game.delta)
        new_xrect = Rect(
            new_pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2)
        new_yrect = Rect(
            self.pos.x - self.radius,
            new_pos.y - self.radius,
            self.radius * 2,
            self.radius * 2)

        # Check for collisions with walls
        for w in self.game.walls:
            if self.can_move_x and new_xrect.colliderect(w):
                self.can_move_x = False
            if self.can_move_y and new_yrect.colliderect(w):
                self.can_move_y = False

        # Update position
        if self.can_move_x:
            self.pos.x = new_pos.x
        if self.can_move_y:
            self.pos.y = new_pos.y
        self.can_move_x, self.can_move_y = True, True
        
        print(self.get_player_tile_pos())
        
    def draw(self):
        x, y = self.pos.x - 16, self.pos.y - 16
        pygame.draw.rect(self.game.screen, RED, (x, y, 32, 32))
    def get_player_tile_pos(self):
        return self.game.get_tile_pos(self.game.player.pos)