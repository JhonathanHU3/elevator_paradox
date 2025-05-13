import pygame, sys
from pygame.locals import *
from settings import *
from entities.player import *;


class Gameplay():
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.player = Player();
        
    def handle_events(self, events):
            
        pass

    def update(self):
        self.player.move();
        pygame.display.update();
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0));
        self.player.draw(self.game.screen);
        pass
        
        