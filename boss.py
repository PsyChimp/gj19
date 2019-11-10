import random

import pygame
from pygame.locals import *

import bullet
from globals import *

CENTER_X = WIN_WIDTH_PX / 2
EYE_OFFSET_X = 32
EYE_OFFSET_Y = -3
HAND_OFFSET_X = 200
HAND_OFFSET_Y = 50
ANIM_DELAY = 0.2
ATTACK_DELAY = 0.5
MAX_HP = 20

class Boss(object):
    def __init__(self, game):
        self.game = game

        # Images
        self.head_img = self.game.boss_head_img
        self.eye_img = self.game.boss_eye_img
        self.right_hand_imgs = self.game.boss_hand_imgs
        self.left_hand_imgs = [
            pygame.transform.flip(img, True, False) for img in self.game.boss_hand_imgs]

        # Head position
        self.head_pos = pygame.math.Vector2(CENTER_X, 150)

        # Eye positions
        self.left_eye_dir = pygame.math.Vector2(0, 1)
        self.right_eye_dir = pygame.math.Vector2(0, 1)
        self.left_eye_anchor = self.head_pos + (-EYE_OFFSET_X, EYE_OFFSET_Y)
        self.right_eye_anchor = self.head_pos + (EYE_OFFSET_X, EYE_OFFSET_Y)
        self.left_eye_pos = self.left_eye_anchor + self.left_eye_dir * 8
        self.right_eye_pos = self.right_eye_anchor + self.right_eye_dir * 8

        # Hand positions
        self.left_hand_pos = self.head_pos + (-HAND_OFFSET_X, HAND_OFFSET_Y)
        self.right_hand_pos = self.head_pos + (HAND_OFFSET_X, HAND_OFFSET_Y)

        # Rects
        self.head_rect = self.head_img.get_rect()
        self.left_eye_rect = self.eye_img.get_rect()
        self.right_eye_rect = self.eye_img.get_rect()
        self.left_hand_rect = self.left_hand_imgs[0].get_rect()
        self.right_hand_rect = self.right_hand_imgs[0].get_rect()

        self.anim_timer = 0.0
        self.atk_timer = 0.0
        self.cur_frame = 0
        self.left_hand_hp = 5
        self.right_hand_hp = 5
        self.head_hp = 10
        self.hp = self.left_hand_hp + self.right_hand_hp + self.head_hp
        self.head_radius = 150
        self.hand_radius = 50
        self.can_attack = True
        self.bullets = []

    def update(self):
        # Update animations
        self.anim_timer += self.game.delta
        if self.anim_timer >= ANIM_DELAY:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.anim_timer = 0.0

        # Update eye directions/positions
        self.left_eye_dir = (self.game.player.pos - self.left_eye_anchor).normalize()
        self.right_eye_dir = (self.game.player.pos - self.right_eye_anchor).normalize()
        self.left_eye_pos = self.left_eye_anchor + self.left_eye_dir * 8
        self.right_eye_pos = self.right_eye_anchor + self.right_eye_dir * 8

        self.head_rect.center = self.head_pos
        self.left_hand_rect.center = self.left_hand_pos
        self.right_hand_rect.center = self.right_hand_pos
        self.left_eye_rect.center = self.left_eye_pos
        self.right_eye_rect.center = self.right_eye_pos

        self.hp = self.left_hand_hp + self.right_hand_hp + self.head_hp

        # Spawn bullets
        if self.can_attack:
            rand_pos = pygame.math.Vector2(
                random.randint(100, WIN_WIDTH_PX - 100), 300)
            self.bullets.append(bullet.Bullet(
                self.game, rand_pos, pygame.math.Vector2(0, 1)))
            self.can_attack = False
        else:
            self.atk_timer += self.game.delta
            if self.atk_timer >= ATTACK_DELAY:
                self.can_attack = True
                self.atk_timer = 0.0

        for b in self.bullets:
            b.enemyUpdate()

    def draw(self):
        self.game.screen.blit(self.head_img, self.head_rect)
        self.game.screen.blit(
            self.left_hand_imgs[self.cur_frame], self.left_hand_rect)
        self.game.screen.blit(
            self.right_hand_imgs[self.cur_frame], self.right_hand_rect)
        self.game.screen.blit(self.eye_img, self.left_eye_rect)
        self.game.screen.blit(self.eye_img, self.right_eye_rect)

        if self.game.debug:
            # Draw eye anchor points
            ix, iy = int(self.left_eye_anchor.x), int(self.left_eye_anchor.y)
            pygame.draw.circle(self.game.screen, BLUE, (ix, iy), 3)
            ix, iy = int(self.right_eye_anchor.x), int(self.right_eye_anchor.y)
            pygame.draw.circle(self.game.screen, BLUE, (ix, iy), 3)

            # Draw hit circles
            ix, iy = int(self.head_pos.x), int(self.head_pos.y)
            pygame.draw.circle(self.game.screen, WHITE, (ix, iy), self.head_radius, 1)
            ix, iy = int(self.left_hand_pos.x), int(self.left_hand_pos.y)
            pygame.draw.circle(self.game.screen, WHITE, (ix, iy), self.hand_radius, 1)
            ix, iy = int(self.right_hand_pos.x), int(self.right_hand_pos.y)
            pygame.draw.circle(self.game.screen, WHITE, (ix, iy), self.hand_radius, 1)

        for b in self.bullets:
            b.draw()

        # Draw HP bar
        w, h = WIN_WIDTH_PX, 15
        x, y = 0, WIN_HEIGHT_PX - h
        w_ = self.hp * (w / MAX_HP)
        pygame.draw.rect(self.game.screen, BLACK, (x, y, w, h))
        pygame.draw.rect(self.game.screen, RED, (x, y, w_, h))
