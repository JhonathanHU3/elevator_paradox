import pygame, sys;
from pygame.locals import *;
from settings import *;
from scenes.startscreen import StartScreenScene;
from scenes.cutscene import Cutscene;

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Elevator Paradox")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.scenes = {
            "STARTSCREEN": StartScreenScene,
            "CUTSCENE": Cutscene
        }

        self.scene_name = "STARTSCREEN"
        self.scene = self.scenes[self.scene_name](self)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene.handle_events(events)
            self.scene.update()
            self.scene.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()            
    