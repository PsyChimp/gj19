import sys

import pygame
from pygame.locals import *

import enemy
import player
import tile
from globals import *

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH_PX, WIN_HEIGHT_PX))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.delta = 0.0
        self.cur_room = 0
        self.doors_open = False

        self.player = None
        self.enemies = None
        self.tiles = None
        self.obstacles = None

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

        self.missing_frame = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.missing_frame.fill(MAGENTA)

        # Load images, sounds, fonts, etc.
        # ROOM TILES
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
            "wall_square": pygame.image.load("img/level/wall_square.png").convert(),
            "door_open": pygame.image.load("img/level/door_open.png").convert(),
            "door_closed": pygame.image.load("img/level/door_closed.png").convert()}

        # PLAYER
        player_walk_n = [
            pygame.image.load("img/player/player_walk_n1.png").convert_alpha(),
            pygame.image.load("img/player/player_walk_n2.png").convert_alpha(),
            pygame.image.load("img/player/player_idle_n.png").convert_alpha()]
        player_walk_ne = [
            pygame.image.load("img/player/player_walk_ne1.png").convert_alpha(),
            pygame.image.load("img/player/player_walk_ne2.png").convert_alpha(),
            pygame.image.load("img/player/player_idle_ne.png").convert_alpha()]
        player_walk_e = [
            pygame.image.load("img/player/player_walk_e1.png").convert_alpha(),
            pygame.image.load("img/player/player_walk_e2.png").convert_alpha(),
            pygame.image.load("img/player/player_idle_e.png").convert_alpha()]
        player_walk_se = [
            pygame.image.load("img/player/player_walk_se1.png").convert_alpha(),
            pygame.image.load("img/player/player_walk_se2.png"),
            pygame.image.load("img/player/player_idle_se.png").convert_alpha()]
        player_walk_s = [
            pygame.image.load("img/player/player_walk_s1.png").convert_alpha(),
            pygame.image.load("img/player/player_walk_s2.png").convert_alpha(),
            pygame.image.load("img/player/player_idle_s.png").convert_alpha()]
        player_walk_sw = [
            pygame.transform.flip(img, True, False) for img in player_walk_se]
        player_walk_w = [
            pygame.transform.flip(img, True, False) for img in player_walk_e]
        player_walk_nw = [
            pygame.transform.flip(img, True, False) for img in player_walk_ne]
        self.player_imgs = {
            ( 0, -1): player_walk_n,
            ( 1, -1): player_walk_ne,
            ( 1,  0): player_walk_e,
            ( 1,  1): player_walk_se,
            ( 0,  1): player_walk_s,
            (-1,  1): player_walk_sw,
            (-1,  0): player_walk_w,
            (-1, -1): player_walk_nw}

        # BULLETS
        self.player_bullet_img = pygame.image.load(
            "img/player/player_bullet.png").convert_alpha()
        self.enemy_bullet_img = pygame.image.load(
            "img/hazards_and_enemies/enemy_bullet.png").convert_alpha()

        # BOSS
        self.boss_head_img = pygame.image.load(
            "img/hazards_and_enemies/jim_head.png").convert_alpha()
        self.boss_eyes_img = pygame.image.load(
            "img/hazards_and_enemies/jim_eyes.png").convert_alpha()
        self.boss_hand_imgs = [
            pygame.image.load(
                "img/hazards_and_enemies/boss_hands_animation/hand_0000.png").convert_alpha(),
            pygame.image.load(
                "img/hazards_and_enemies/boss_hands_animation/hand_0001.png").convert_alpha(),
            pygame.image.load(
                "img/hazards_and_enemies/boss_hands_animation/hand_0002.png").convert_alpha(),
            pygame.image.load(
                "img/hazards_and_enemies/boss_hands_animation/hand_0003.png").convert_alpha()]

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
                elif e.key == K_r:
                    # Skip to the next room
                    self.cur_room += 1
                    self.load_room()
                elif e.key == K_c:
                    # Delete all enemies
                    self.enemies.clear()
        self.player.handle_events()

    def update(self):
        # Get current state of input devices
        self.keys = pygame.key.get_pressed()
        self.mpos = pygame.mouse.get_pos()
        self.mbut = pygame.mouse.get_pressed()

        self.player.update()
        if self.player.hp <= 0:
            self.playing = False

        for e in self.enemies:
            e.update()
        if not self.doors_open and len(self.enemies) == 0:
            self.obstacles[:] = [t for t in self.obstacles if t.type != "door"]
            for i, t in enumerate(self.tiles):
                if i < 20 and t.type == "door":
                    t.img = self.room_tiles["door_open"]
            self.doors_open = True

        # Check for player entering a door
        if self.player.pos.y < TILE_SIZE:
            self.cur_room += 1
            self.load_room()

    def draw(self):
        for t in self.tiles:
            t.draw()
            if self.debug:
                pygame.draw.rect(self.screen, RED, t.rect, 1)

        self.player.draw()

        for e in self.enemies:
            e.draw()

        pygame.display.flip()

    def draw_text(self, text, font, color, pos, align="topleft"):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(**{align: pos})
        self.screen.blit(text_surf, text_rect)

    def load_room(self):
        if self.cur_room >= len(ROOMS):
            self.playing = False
            return
        self.player.bullets.clear()
        self.tiles = []
        self.obstacles = []
        y = 0
        for cur_row in ROOMS[self.cur_room]:
            x = 0
            for cur_tile in cur_row:
                rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cur_tile == "@":
                    type = "wall"
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
                elif cur_tile == "_":
                    type = "door"
                    if y == 0:
                        img = self.room_tiles["door_closed"]
                    elif y == WIN_HEIGHT_T - 1:
                        img = pygame.transform.flip(
                            self.room_tiles["door_closed"], False, True)
                elif cur_tile == ".":
                    type = "floor"
                    img = self.room_tiles["floor"]
                elif cur_tile == "E":
                    self.enemies.append(enemy.Enemy(self,(x,y)))
                    type = "floor"
                    img = self.room_tiles["floor"]
                elif cur_tile == "T":
                    self.enemies.append(enemy.Enemy(self,(x,y),True))
                    type = "floor"
                    img = self.room_tiles["floor"]
                self.tiles.append(tile.Tile(self, type, rect, img))
                x += 1
            y += 1
        self.obstacles[:] = [
            t for t in self.tiles if t.type == "wall" or t.type == "door"]
        self.player.pos = pygame.math.Vector2(PLAYER_SPAWN)
        self.doors_open = False

    def new(self):
        """Reset all game variables to their initial values."""
        self.player = player.Player(self)

        self.cur_room = 0
        self.enemies = []
        self.load_room()

        
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
        self.screen.fill(BLUE)
        self.draw_text(
            "Game over!", self.tmpfont64, WHITE,
            (WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2), "center")
        pygame.display.flip()
        pygame.time.wait(3000)
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
        return ((pos.x // TILE_SIZE), (pos.y // TILE_SIZE))

if __name__ == "__main__":
    g = Game()
    while True:
        g.show_start_screen()
        g.new()
        g.run()
        g.show_game_over_screen()
        g.quit()
