import sys

import pygame
from pygame.locals import *

import player
import enemy
from globals import *

class Game(object):
    def __init__(self):
        sys.setrecursionlimit(2000)
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH_PX, WIN_HEIGHT_PX))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.delta = 0.0
        self.cur_room = 0

        self.player = None
        self.enemies = []
        self.walls = None

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
        self.room_tiles = {
            "floor": pygame.image.load("img/level/floor.png").convert(),
            "wall_top_left": pygame.image.load("img/level/wall_top_left.png").convert(),
            "wall_top_right": pygame.image.load("img/level/wall_top_right.png").convert(),
            "wall_bottom_left": pygame.image.load("img/level/wall_bottom_left.png").convert(),
            "wall_bottom_right": pygame.image.load("img/level/wall_bottom_right.png").convert(),
            "wall_top": pygame.image.load("img/level/wall_top.png").convert(),
            "wall_bottom": pygame.image.load("img/level/wall_bottom.png").convert(),
            "wall_left": pygame.image.load("img/level/wall_left.png").convert(),
            "wall_right": pygame.image.load("img/level/wall_right.png").convert(),
            "wall_square": pygame.image.load("img/level/wall_square.png").convert()}

        player_walk_n = [
            pygame.image.load("img/player/player_walk_n1.png").convert(),
            pygame.image.load("img/player/player_walk_n2.png").convert()]
        player_walk_ne = []
        player_walk_e = [
            pygame.image.load("img/player/player_walk_e1.png").convert(),
            pygame.image.load("img/player/player_walk_e2.png").convert(),
            pygame.image.load("img/player/player_walk_e3.png").convert(),
            pygame.image.load("img/player/player_walk_e4.png").convert()]
        player_walk_se = []
        player_walk_s = [
            pygame.image.load("img/player/player_walk_s1.png").convert(),
            pygame.image.load("img/player/player_walk_s2.png").convert()]
        player_walk_sw = []
        player_walk_w = [
            pygame.transform.flip(img, True, False) for img in player_walk_e]
        player_walk_nw = []
        self.player_imgs = {
            ( 0, -1): player_walk_n,
            ( 1, -1): player_walk_ne,
            ( 1,  0): player_walk_e,
            ( 1,  1): player_walk_se,
            ( 0,  1): player_walk_s,
            (-1,  1): player_walk_sw,
            (-1,  0): player_walk_w,
            (-1, -1): player_walk_nw}

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
                elif e.key == K_l:
                    self.cur_room = (self.cur_room + 1) % len(ROOMS)
                    self.load_room()
        self.player.handle_events()

    def update(self):
        # Get current state of input devices
        self.keys = pygame.key.get_pressed()
        self.mpos = pygame.mouse.get_pos()
        self.mbut = pygame.mouse.get_pressed()

        self.player.update()
        for e in self.enemies:
            e.update()
        if self.player.hp <= 0:
            self.playing = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.debug:
            for w in self.walls:
                pygame.draw.rect(self.screen, RED, w, 1)
        self.player.draw()
        for e in self.enemies:
            e.draw()
        pygame.display.flip()

    def draw_text(self, text, font, color, pos, align="topleft"):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(**{align: pos})
        self.screen.blit(text_surf, text_rect)

    def load_room(self):
        self.background = pygame.Surface((WIN_WIDTH_PX, WIN_HEIGHT_PX))
        self.walls = []
        y = 0
        for row in ROOMS[self.cur_room]:
            x = 0
            for tile in row:
                if tile == "W":
                    self.walls.append(Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    if y == 0:
                        if x == 0:
                            img = self.room_tiles["wall_top_left"]
                        elif x == WIN_WIDTH_T - 1:
                            img = self.room_tiles["wall_top_right"]
                        else:
                            img = self.room_tiles["wall_top"]
                    elif y == WIN_HEIGHT_T - 1:
                        if x == 0:
                            img = self.room_tiles["wall_bottom_left"]
                        elif x == WIN_WIDTH_T - 1:
                            img = self.room_tiles["wall_bottom_right"]
                        else:
                            img = self.room_tiles["wall_bottom"]
                    else:
                        if x == 0:
                            img = self.room_tiles["wall_left"]
                        elif x == WIN_WIDTH_T - 1:
                            img = self.room_tiles["wall_right"]
                        else:
                            img = self.room_tiles["wall_square"]
                elif tile == ".":
                    img = self.room_tiles["floor"]
                self.background.blit(img, (x * TILE_SIZE, y * TILE_SIZE))
                x += 1
            y += 1

    def new(self):
        """Reset all game variables to their initial values."""
        self.cur_room = 0
        self.load_room()
        self.player = player.Player(self)
        self.enemies.append(enemy.Enemy(self))
        
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
            (WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2), "center")
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # pygame.mixer.music.load("snd/game_over_theme.ogg")
        # pygame.mixer.music.play(-1)
        self.screen.fill(BLUE)
        self.draw_text(
            "Game over!", self.tmpfont64, WHITE,
            (WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2), "center")
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

    def get_tile_pos(self, pos):
        return (pos.x // TILE_SIZE, pos.y // TILE_SIZE)

if __name__ == "__main__":
    g = Game()
    while True:
        g.show_start_screen()
        g.new()
        g.run()
        g.show_game_over_screen()
