import pygame, sys;
from pygame.locals import *;
from settings import *;
from core.states import *;

class Game():
    def __init__(self):
        pygame.init();
        self.gameRunning = True;
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT));
        self.clock = pygame.time.Clock();
        
        self.states = {
        "STARTSCREEN": StartScreenState(self),
        }
        
        self.state_name = "STARTSCREEN"
        self.state = self.states[self.state_name]

        pass
    
    def run(self):
        while(self.gameRunning):
            events = pygame.event.get();
            self.clock.tick(FPS);
            
            self.state.handle_events(events);
            
            if self.state.done:
                self.new_state_name = self.state.next_state
                self.state = self.states[self.new_state_name]
    
    def change_state(self, new_state_name):
        self.state_name = new_state_name
        self.state = self.states[self.state_name]