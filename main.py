import sys

import pygame
from pygame.locals import *

import player
from globals import *

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.delta = 0.0

        self.player = None
        self.enemies = None
        self.walls = []

        self.events = None
        self.keys = None
        self.mpos = None
        self.mbut = None

        self.playing = False
        self.paused = False
        self.debug = False

        # For debugging
        self.tmpfont16 = pygame.font.Font(None, 16)
        self.tmpfont32 = pygame.font.Font(None, 32)
        self.tmpfont64 = pygame.font.Font(None, 64)

        # Load images, sounds, fonts, etc.
        self.wall_img = pygame.image.load("img/wall.png").convert()
        self.floor_img = pygame.image.load("img/floor.png").convert()
        self.player_img = None

    def handle_events(self):
        self.events = pygame.event.get()
        for e in self.events:
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.quit()
                elif e.key == K_p:
                    self.paused = not self.paused
                elif e.key == K_F1:
                    self.debug = not self.debug
        self.player.handle_events()

    def update(self):
        # Get current state of input devices
        self.keys = pygame.key.get_pressed()
        self.mpos = pygame.mouse.get_pos()
        self.mbut = pygame.mouse.get_pressed()

        self.player.update()
        if self.player.hp <= 0:
            self.playing = False

    def draw(self):
        self.draw_level()

        self.player.draw()

        pygame.display.flip()

    def draw_level(self):
        y = 0
        for row in LEVEL_1:
            x = 0
            for tile in row:
                if tile == "@":
                    # Draw a wall tile
                    img = self.wall_img
                elif tile == ".":
                    # Draw a floor tile
                    img = self.floor_img
                self.screen.blit(img, (x, y))
                if self.debug:
                    pygame.draw.rect(
                        self.screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 1)
                x += TILE_SIZE
            y += TILE_SIZE

    def draw_text(self, text, font, color, pos, align="topleft"):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(**{align: pos})
        self.screen.blit(text_surf, text_rect)

    def new(self):
        """Reset all game variables to their initial values."""
        self.player = player.Player(self)

    def run(self):
        self.playing = True
        # pygame.mixer.music.load("snd/level_theme.ogg")
        # pygame.mixer.music.play(-1)
        while self.playing:
            self.delta = self.clock.tick() / 1000.0
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def show_start_screen(self):
        # pygame.mixer.music.load("snd/start_theme.ogg")
        # pygame.mixer.music.play(-1)
        self.screen.fill(BLUE)
        self.draw_text(
            "Press any key to begin!", self.tmpfont64, WHITE,
            (WIN_WIDTH / 2, WIN_HEIGHT / 2), "center")
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # pygame.mixer.music.load("snd/game_over_theme.ogg")
        # pygame.mixer.music.play(-1)
        self.screen.fill(BLUE)
        self.draw_text(
            "Game over!", self.tmpfont64, WHITE,
            (WIN_WIDTH / 2, WIN_HEIGHT / 2), "center")
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.clear()
        waiting = True
        while waiting:
            self.clock.tick()
            e = pygame.event.wait()
            if e.type == QUIT:
                self.quit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                self.quit()
            elif e.type == KEYUP:
                waiting = False

if __name__ == "__main__":
    g = Game()
    while True:
        g.show_start_screen()
        g.new()
        g.run()
        g.show_game_over_screen()
