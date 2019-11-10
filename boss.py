import pygame
from pygame.locals import *

from globals import *

class Boss(object):
    def __init__(self, game):
        self.game = game
        self.head_img = self.game.boss_head_img
        self.eyes_img = self.game.boss_eyes_img
        self.right_hand_imgs = self.game.boss_hand_imgs
        self.left_hand_imgs = [
            pygame.transform.flip(img, True, False) for img in self.game.boss_hand_imgs]

        self.head_pos = pygame.math.Vector2()
        self.left_eye_anchor = pygame.math.Vector2()
        self.right_eye_anchor = pygame.math.Vector2()
        self.left_hand_pos = pygame.math.Vector2()
        self.right_hand_pos = pygame.math.Vector2()

        self.left_eye_dir = pygame.math.Vector2(0, 1)
        self.right_eye_dir = pygame.math.Vector2(0, 1)

        self.head_rect = self.head_img.get_rect()
        self.eyes_rect = self.eyes_img.get_rect()
        self.left_hand_rect = self.left_hand_imgs[0].get_rect()
        self.right_hand_rect = self.right_hand_imgs[0].get_rect()

        self.cur_frame = 0

    def update(self):
        # ...
        self.head_rect.center = self.head_pos
        self.left_hand_rect.center = self.left_hand_pos
        self.right_hand_rect.center = self.right_hand_pos

    def draw(self):
        self.game.screen.blit(
            self.left_hand_imgs[self.cur_frame], self.left_hand_rect.topleft)
        self.game.screen.blit(
            self.right_hand_imgs[self.cur_frame], self.right_hand_rect.topleft)
        self.game.screen.blit(self.head_img, self.head_rect.topleft)
        self.game.screen.blit(self.eyes_img, self.eyes_rect.topleft)
