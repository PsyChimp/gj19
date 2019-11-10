import pygame
from pygame.locals import *

from globals import *

class Boss(object):
    def __init__(self, game):
        self.game = game
        self.head_img = self.game.boss_head_img
        self.eyes_img = self.game.boss_eyes_img
        self.left_hand_sprites = self.game.boss_hand_imgs
        self.right_hand_sprites = [
            pygame.transform.flip(img, True, False) for img in self.game.boss_hand_imgs]
        self.head_pos = pygame.math.Vector2()
        self.left_hand_pos = pygame.math.Vector2()
        self.right_hand_pos = pygame.math.Vector2()

        self.head_rect = self.head_img.get_rect()
        self.eyes_rect = self.eyes_img.get_rect()
        self.left_hand_rect = self.left_hand_sprites[0].get_rect()
        self.right_hand_rect = self.right_hand_sprites[0].get_rect()

    def update(self):
        # ...
        self.head_rect.center = self.head_pos
        self.left_hand_rect.center = self.left_hand_pos
        self.right_hand_rect.center = self.right_hand_pos

    def draw(self):
        self.game.screen.blit(
            self.left_hand_sprites[self.cur_frame], self.left_hand_rect.topleft)
        self.game.screen.blit(
            self.right_hand_sprites[self.cur_frame], self.right_hand_rect.topleft)
        self.game.screen.blit(self.head_img, self.head_rect.topleft)
        self.game.screen.blit(self.eyes_img, self.eyes_rect.topleft)
