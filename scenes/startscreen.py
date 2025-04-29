import pygame, sys;
from pygame import *;
from core.states import *;
from settings import *;

class StartScreenState():
    def __init__(self, game):
        self.game = game
        self.done = False
        self.next_state = None
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        
        font_title = pygame.font.SysFont(None, 100)
        font_button = pygame.font.SysFont(None, 50)
        
        title_text = font_title.render("Elevator Paradox", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        self.start_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
        self.exit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 60)

        def draw_button(rect, text):
                pygame.draw.rect(self.screen, DARK_GRAY, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 3)
                label = font_button.render(text, True, WHITE)
                label_rect = label.get_rect(center=rect.center)
                self.screen.blit(label, label_rect)
        
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.next_state = "GAMEPLAY"
                self.done = True
            
            if e.type == MOUSEBUTTONDOWN:
                        if self.start_button_rect.collidepoint(e.pos):
                            self.next_state = "GAMEPLAY"
                            self.done = True
                        elif self.exit_button_rect.collidepoint(e.pos):
                            pygame.quit()
                            sys.exit()