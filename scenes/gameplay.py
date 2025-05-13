import pygame, sys
from pygame.locals import *
from settings import *


class Gameplay():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
    def handle_events(self, events):
        pass

    def update(self):
        
        pygame.display.update();
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0));
        pygame.draw.line(self.game.screen, (255, 0, 0), (200, 240), (450, 240))
        pass
        
        