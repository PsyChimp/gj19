import pygame
from pygame.locals import *

from globals import *

class Player(object):
    def __init__(self, game):
        self.game = game
        self.pos = pygame.math.Vector2(WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2)
        self.dir = pygame.math.Vector2(0, 0)
        self.prev_dir = pygame.math.Vector2(0, 1)
        self.sprites = self.game.player_imgs
        self.radius = 16
        self.hp = PLAYER_MAX_HEALTH
        self.can_move_x = True
        self.can_move_y = True
        self.anim_timer = 0.0
        self.cur_frame = 0

    def handle_events(self):
        pass

    def update(self):
        # Update velocity
        self.dir.x = (self.game.keys[K_d] - self.game.keys[K_a])
        self.dir.y = (self.game.keys[K_s] - self.game.keys[K_w])
        if self.dir.x != 0 or self.dir.y != 0:
            self.prev_dir = pygame.math.Vector2(self.dir)
            self.anim_timer += self.game.delta
            if self.anim_timer >= PLAYER_ANIM_DELAY:
                num_frames = len(self.sprites[tuple(self.dir)])
                self.cur_frame = (self.cur_frame + 1) % 2
                self.anim_timer = 0.0
        else:
            self.cur_frame = 0

        # Calculate new position
        new_pos = self.pos + (self.dir * PLAYER_SPEED * self.game.delta)
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

    def draw(self):
        x, y = self.pos.x - 16, self.pos.y - 16
        if self.dir.x != 0 or self.dir.y != 0:
            self.game.screen.blit(
                self.sprites[tuple(self.dir)][self.cur_frame], (x, y))
        else:
            #print("prev_dir =", self.prev_dir)
            self.game.screen.blit(
                self.sprites[tuple(self.prev_dir)][2], (x, y))
        if self.game.debug:
            pygame.draw.rect(
                self.game.screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 1)
