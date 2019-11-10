import pygame
from enum import Enum
import random
from pygame.locals import *

from globals import *

from queue import *

class Enemy(object):
    def __init__(self,game):
        self.game = game
        self.pos = pygame.math.Vector2(WIN_WIDTH_PX / 2, WIN_HEIGHT_PX / 2)
        self.vel = pygame.math.Vector2(0, 0)
        #self.img = self.game.player_img
        self.radius = 10
        self.can_move_x = True
        self.can_move_y = True
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.prev_direction = pygame.math.Vector2(0, 1)
        self.player_pos = self.get_player_tile_pos()
        self.path = []
        self.d_point = self.pos
        self.hp = 1
        self.came_from = {}
    def betweenRange(self, x, r1, r2):
        return (x >= r1) and (x <= r2)
        
    def update(self):
        # Update velocity
        self.path = self.get_path_to_tile(self.get_self_tile_pos(),self.get_player_tile_pos())
        for i in range(len(self.path)):
            self.path[i] = pygame.math.Vector2((self.path[i][0] * TILE_SIZE) + (TILE_SIZE/2),
            (self.path[i][1] * TILE_SIZE) + (TILE_SIZE/2))
                
        for p in self.path:
            dist = p - self.pos
            q = dist.magnitude()
            if q <= 1:
                self.path.remove(p)
                
        if(len(self.path) > 0):
            self.d_point = pygame.math.Vector2(self.path[0])
            
        #print(self.pos, self.d_point)
        self.vel = self.d_point - self.pos
        if self.vel.magnitude() != 0:
            self.vel = self.vel.normalize() * (PLAYER_SPEED / 2)
        #print(self.vel)
        self.direction.x = (self.game.player.pos[0] - self.pos[0])
        self.direction.y = (self.game.player.pos[1] - self.pos[1])
        if self.direction.x != 0 or self.direction.y != 0:
            self.prev_direction = pygame.math.Vector2(self.direction)
        
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
        
    def draw(self):
        x, y = self.pos.x - 16, self.pos.y - 16
        for k in self.came_from.keys():
            pygame.draw.circle(self.game.screen, BLUE, tuple(map(lambda x:int((x * 32) + 16),k)), 10)
        for p in self.path:
            pygame.draw.circle(self.game.screen, WHITE, tuple(map(int,p)), 3)
        
        pygame.draw.rect(self.game.screen, RED, (x, y, 32, 32))
        
    def get_player_tile_pos(self):
        return self.game.get_tile_pos(self.game.player.pos)
    
    def get_self_tile_pos(self):
        return self.game.get_tile_pos(self.pos)
    
    def get_map_tile_pos(self):
        closed = []
        map = ROOMS[self.game.cur_room]
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
            current = self.came_from[current]
        path.reverse()
        return path
        