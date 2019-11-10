import pygame
from enum import Enum
import random
from pygame.locals import *

from main import *

from queue import *

import bullet

class Enemy(object):
    def __init__(self,game,tile_pos,turret = False):
        self.game = game
        self.pos = pygame.math.Vector2((tile_pos[0] * Game.TILE_SIZE) + (Game.TILE_SIZE/2),
        (tile_pos[1] * Game.TILE_SIZE) + (Game.TILE_SIZE/2))
        self.vel = pygame.math.Vector2(0, 0)
        self.radius = 10
        self.can_move_x = True
        self.can_move_y = True
        self.dir = pygame.math.Vector2(round(random.uniform(-1, 1)), round(random.uniform(-1, 1)))
        self.prev_dir = pygame.math.Vector2(0, 1)
        self.imgs = self.game.enemy_imgs
        self.anim_timer = 0.0
        self.cur_frame = 0
        self.prev_direction = pygame.math.Vector2(0, 1)
        self.player_pos = self.get_player_tile_pos()
        self.path = []
        self.d_point = self.pos
        self.hp = Game.ENEMY_MAX_HEALTH
        self.turret = turret
        if self.turret:
            self.dir = pygame.math.Vector2(0, 1)
            self.imgs = self.game.turret_imgs
            self.cardinal = True
            self.bullets = []
            self.spin_index = 0
            self.spin_timer = 0.0
            self.atk_timer = 0.0
            #calculate directions:
            self.card_dirs = []
            self.diag_dirs = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if(i == 0 and j == 0):
                        continue
                    if(abs(i) == abs(j)):
                        self.diag_dirs.append(pygame.math.Vector2(i,j))
                    else:
                        self.card_dirs.append(pygame.math.Vector2(i,j))
    def update(self):
        if not self.turret:
            #check for explosion
            dist = self.game.player.pos - self.pos
            if(dist.length() <= self.game.TILE_SIZE/2):
                self.game.explo.append(Explosion(self.game,self.pos))
                self.game.player.hp -= 5
                return False
            # Update velocity
            self.path = self.get_path_to_tile(self.get_self_tile_pos(),self.get_player_tile_pos())
            for i in range(len(self.path)):
                self.path[i] = pygame.math.Vector2((self.path[i][0] * Game.TILE_SIZE) + (Game.TILE_SIZE/2),
                (self.path[i][1] * Game.TILE_SIZE) + (Game.TILE_SIZE/2))
                    
            for p in self.path:
                dist = p - self.pos
                q = dist.length()
                if q <= 1:
                    self.path.remove(p)
                    
            if(len(self.path) > 0):
                self.d_point = pygame.math.Vector2(self.path[0])
                
            #print(self.pos, self.d_point)
            self.vel = self.d_point - self.pos
            if self.vel.length() != 0:
                self.vel = self.vel.normalize()
            #print(self.vel)
            
            self.dir.x = (round(self.vel.x))
            self.dir.y = (round(self.vel.y))
            
            self.vel *= self.game.ENEMY_SPEED
            
            if self.dir.x != 0 or self.dir.y != 0:
                self.prev_direction = pygame.math.Vector2(self.dir)
                self.prev_dir = pygame.math.Vector2(self.dir)
            # Update animation
            self.anim_timer += self.game.delta
            if self.anim_timer >= Game.ENEMY_ANIM_DELAY:
                self.cur_frame = (self.cur_frame + 1) % 2
                self.anim_timer = 0.0
            
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
            for tile in self.game.obstacles:
                if self.can_move_x and new_xrect.colliderect(tile.rect):
                    self.can_move_x = False
                if self.can_move_y and new_yrect.colliderect(tile.rect):
                    self.can_move_y = False
                    
            # Update position
            if self.can_move_x:
                self.pos.x = new_pos.x
            if self.can_move_y:
                self.pos.y = new_pos.y
            self.can_move_x, self.can_move_y = True, True
        else:
            #spin dat boi
            self.spin_timer += self.game.delta
            if(self.spin_timer >= Game.ENEMY_SPIN_DELAY):
                self.spin_timer = 0.0
                self.spin_index+=1
                if(self.spin_index == len(self.imgs.keys())):
                    self.spin_index = 0
                self.dir = list(self.imgs.keys())[self.spin_index]
                
            self.atk_timer += self.game.delta
            if self.atk_timer >= Game.ENEMY_ATTACK_DELAY:
                
                self.atk_timer = 0.0
                dirs = []
                if(self.cardinal):
                    dirs = self.card_dirs
                else:
                    dirs = self.diag_dirs
                self.cardinal = not self.cardinal
                for d in dirs:
                    self.bullets.append(bullet.Bullet(
                    self.game, pygame.math.Vector2(self.pos),
                    pygame.math.Vector2(d)))
            self.bullets[:] = [b for b in self.bullets if b.enemyUpdate() == True]
        return self.hp > 0            
    def draw(self):
        x, y = self.pos.x - 16, self.pos.y - 16
        #for k in self.came_from.keys():
            #pygame.draw.circle(self.game.screen, BLUE, tuple(map(lambda x:int((x * 32) + 16),k)), 10)
        #for p in self.path:
            #pygame.draw.circle(self.game.screen, WHITE, tuple(map(int,p)), 3)
        
        if self.turret:
            self.game.screen.blit(
            self.imgs[tuple(self.dir)][0], (x, y))
        else:
            if self.dir.x != 0 or self.dir.y != 0:
                self.game.screen.blit(
                self.imgs[tuple(self.dir)][self.cur_frame], (x, y))
            else:
                self.game.screen.blit(
                self.imgs[tuple(self.prev_dir)][2], (x, y))
        if(self.turret):
            for b in self.bullets:
                b.draw()
    def get_player_tile_pos(self):
        return self.game.get_tile_pos(self.game.player.pos)
    
    def get_self_tile_pos(self):
        return self.game.get_tile_pos(self.pos)
    
    def get_map_tile_pos(self):
        closed = []
        map = Game.ROOMS[self.game.cur_room]
        y = 0
        for row in map:
            x = 0
            for tile in row:
                if(tile != '.' and tile != 'E'):
                    closed.append((x,y))
                x+=1
            y+=1
        for e in self.game.enemies:
            p = e.get_self_tile_pos()
            closed.append(p)
        return closed
        
    def get_open_neighbors(self,pos):
        closed = self.get_map_tile_pos()
        #print(closed)
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1,2):
                if abs(j) != abs(i):
                    n = (pos[0] + i, pos[1] + j)
                    if n not in closed:
                        neighbors.append(n)
        return neighbors
        
    def get_path_to_tile(self,start,end):
        if(start == end):
            return [end]
        frontier = Queue()
        frontier.put(start)
        self.came_from = {}
        self.came_from[start] = None
        while(not frontier.empty()):
            current = frontier.get()
            
            neighbors = self.get_open_neighbors(current)
            for next in neighbors:
                if next not in self.came_from:
                    frontier.put(next)
                    self.came_from[next] = current
            if current == end:
                break
        current = end
        path = []
        while current != start:
            path.append(current)
            if(current in self.came_from):
                current = self.came_from[current]
            else:
                break
        path.reverse()
        return path
        
class Explosion(object):
    def __init__(self,game,pos):
        self.pos = pos
        self.game = game
        self.cur_frame = 0
        self.anim_timer = 0.0
        self.imgs = self.game.explosion
    def update(self):
        self.anim_timer += self.game.delta
        if(self.anim_timer > Game.EXPLOSION_ANIM_DELAY):
            self.anim_timer = 0.0
            self.cur_frame += 1
            if(self.cur_frame == len(self.imgs)):
                return False
        return True
    def draw(self):
        x, y = self.pos.x - 16, self.pos.y - 16
        self.game.screen.blit(
        self.imgs[self.cur_frame], (x, y))