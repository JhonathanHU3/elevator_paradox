import pygame;
from pygame import *;
from scenes.startscreen import StartScreenState;

class State:
    def __init__(self, game):
        self.game = game
        self.done = False 
        self.next_state = None 


    def handle_events(self, events):
        for e in events.get():
                    if e.type == QUIT:
                        self.gameRunning = False
        pass

    def update(self):
        
        pass

    def draw(self, screen):
        
        pass
    
