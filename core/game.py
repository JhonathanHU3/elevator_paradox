import pygame, sys;
from pygame.locals import *;
from settings import *;
from scenes.startscreen import StartScreenScene;
from scenes.cutscene import Cutscene;
from scenes.gameplay import Gameplay
from scenes.gameover import GameOver

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Elevator Paradox")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.scenes = {
            "STARTSCREEN": StartScreenScene,
            "CUTSCENE": Cutscene,
            "GAMEPLAY": Gameplay,
            "GAMEOVERSCREEN": GameOver        }

        self.scene_name = "STARTSCREEN"
        self.scene = self.scenes[self.scene_name](self)
        
        
    def change_scene(self, new_name):
        if new_name in self.scenes:
            self.scene_name = new_name
            self.scene = self.scenes[new_name](self)
            print(f"Trocar para cena: {new_name}")

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene.handle_events(events)
            self.scene.update()
            self.scene.draw()
            
            if hasattr(self.scene, "next_scene_name") and self.scene.next_scene_name:
                self.screen.fill((0, 0, 0)) # Fill screen with black before changing scene
                pygame.display.flip() # Force display update to black
                self.change_scene(self.scene.next_scene_name);

            pygame.display.flip();
            self.clock.tick(FPS);

        pygame.quit()
        sys.exit()            
    