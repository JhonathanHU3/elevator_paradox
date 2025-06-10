import pygame, sys;
from pygame.locals import *;
from settings import *;
from scenes.startscreen import StartScreenScene;
from scenes.cutscene import Cutscene;
from scenes.gameplay import Gameplay
from scenes.gameover import GameOver

class Game:
    def __init__(self):
        print("Initializing pygame...")
        pygame.init()
        print("Setting up display...")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Elevator Paradox")
        self.clock = pygame.time.Clock()
        self.running = True
        
        print("Loading scenes...")
        self.scenes = {
            "STARTSCREEN": StartScreenScene,
            "CUTSCENE": Cutscene,
            "GAMEPLAY": Gameplay,
            "GAMEOVERSCREEN": GameOver        }

        print("Starting with STARTSCREEN...")
        self.scene_name = "STARTSCREEN"
        self.scene = self.scenes[self.scene_name](self)
        print("Game initialization complete!")
        
    def change_scene(self, new_name):
        if new_name in self.scenes:
            print(f"Changing scene to: {new_name}")
            self.scene_name = new_name
            self.scene = self.scenes[new_name](self)
        else:
            print(f"Warning: Scene {new_name} not found!")

    def run(self):
        print("Starting game loop...")
        while self.running:
            try:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False

                self.scene.handle_events(events)
                self.scene.update()
                self.scene.draw()
                
                if hasattr(self.scene, "next_scene_name") and self.scene.next_scene_name:
                    print(f"Scene requested change to: {self.scene.next_scene_name}")
                    self.screen.fill((0, 0, 0))
                    pygame.display.flip()
                    self.change_scene(self.scene.next_scene_name)

                pygame.display.flip()
                self.clock.tick(FPS)
            except Exception as e:
                print(f"Error in game loop: {str(e)}")
                import traceback
                traceback.print_exc()
                self.running = False

        print("Cleaning up...")
        pygame.quit()
        sys.exit()            
    