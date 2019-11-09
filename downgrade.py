import pygame
from pygame.locals import *

from globals import *

class Downgrade(object):
    def __init__(self, name):
        self.name = name

    def apply(self):
        return NotImplementedError
