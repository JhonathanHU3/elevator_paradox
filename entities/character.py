import pygame, sys;
from pygame.locals import *;

class Screen:
    def __init__(self, type):
        self.type = type;
        
        pygame.init();
        
        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        
        # Fonts
        font_title = pygame.font.SysFont(None, 100)
        font_button = pygame.font.SysFont(None, 50)
        
        self.screen = pygame.display.set_mode((1280, 720));
        self.gameOn = True;
        self.clock = pygame.time.Clock()
        
        # Menu Screen
        if self.type == "MENU":
            title_text = font_title.render("Elevator Paradox", True, WHITE)
            title_rect = title_text.get_rect(center=(1280 // 2, 720 // 4))

            start_button_rect = pygame.Rect(1280 // 2 - 150, 720 // 2 - 50, 300, 60)
            exit_button_rect = pygame.Rect(1280 // 2 - 150, 720 // 2 + 30, 300, 60)

            def draw_button(rect, text):
                pygame.draw.rect(self.screen, DARK_GRAY, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 3)
                label = font_button.render(text, True, WHITE)
                label_rect = label.get_rect(center=rect.center)
                self.screen.blit(label, label_rect)
            
            while self.gameOn:
                self.clock.tick(60)
                self.screen.fill(BLACK)

                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.gameOn = False
                    elif e.type == MOUSEBUTTONDOWN:
                        if start_button_rect.collidepoint(e.pos):
                                game = Screen("GAME")
                                game.run()
                        elif exit_button_rect.collidepoint(e.pos):
                            pygame.quit()
                            sys.exit()

                self.screen.blit(title_text, title_rect)
                draw_button(start_button_rect, "Começar")
                draw_button(exit_button_rect, "Sair")

                pygame.display.update()

            
        # Game screen    
        elif self.type == "GAME": 
            
            while self.gameOn:
                self.clock.tick(60);
                for e in pygame.event.get():
                    if e.type == QUIT:
                        self.gameOn = False;
        

                pygame.display.update();


            pygame.quit();
        
        pass


game = Screen("MENU")
game.run()