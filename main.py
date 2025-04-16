import pygame, sys;
from pygame.locals import *;
from settings import *;

class Game:
    def __init__(self):
        pygame.init();
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT));
        
        self.gameOn = True;
        self.clock = pygame.time.Clock()
        
        while self.gameOn:
            self.clock.tick(FPS);
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.gameOn = False;

                elif e.type == QUIT:
                    self.gameOn = False;
        

            pygame.display.update();



        pygame.quit();
        
        pass

if __name__ == "__main__":
    game = Game()
    game.run()