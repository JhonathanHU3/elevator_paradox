import pygame, sys
from pygame.locals import *
from settings import *


class Cutscene():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        