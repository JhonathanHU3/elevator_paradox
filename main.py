import pygame, sys;
from pygame.locals import *;
from settings import *;

class Screen:
    def __init__(self, type):
        self.type = type;
        
        pygame.init();
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        
        font_title = pygame.font.SysFont(None, 100)
        font_button = pygame.font.SysFont(None, 50)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT));
        
        self.gameOn = True;
        self.clock = pygame.time.Clock()
        
        
        
        if self.type == "MENU":
            title_text = font_title.render("Elevator Paradox", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

            start_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
            exit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 60)

            def draw_button(rect, text):
                pygame.draw.rect(self.screen, DARK_GRAY, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 3)
                label = font_button.render(text, True, WHITE)
                label_rect = label.get_rect(center=rect.center)
                self.screen.blit(label, label_rect)
            
            while self.gameOn:
                self.clock.tick(FPS)
                self.screen.fill(BLACK)

                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.gameOn = False
                    elif e.type == MOUSEBUTTONDOWN:
                        if start_button_rect.collidepoint(e.pos):
                            print("Começar o jogo!")  
                        elif exit_button_rect.collidepoint(e.pos):
                            pygame.quit()
                            sys.exit()

                self.screen.blit(title_text, title_rect)
                draw_button(start_button_rect, "Começar")
                draw_button(exit_button_rect, "Sair")

                pygame.display.update()

            
            
        elif self.type == "GAME": 
            
            while self.gameOn:
                self.clock.tick(FPS);
                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.gameOn = False;
        

                pygame.display.update();


            pygame.quit();
        
        pass

if __name__ == "__main__":
    game = Screen("MENU")
    game.run()