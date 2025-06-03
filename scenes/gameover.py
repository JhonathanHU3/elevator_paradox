import pygame, sys
from pygame.locals import *
from settings import *

class GameOver:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None

        self.WHITE = (255, 255, 255)
        self.DARK_GRAY = (50, 50, 50)
        self.BLACK = (0, 0, 0)

        self.font_title = pygame.font.SysFont(None, 100)
        self.font_button = pygame.font.SysFont(None, 50)

        self.title_text = self.font_title.render("GAME OVER!", True, self.WHITE)
        self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        self.start_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
        self.exit_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 60)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, self.DARK_GRAY, rect)
        pygame.draw.rect(self.screen, self.WHITE, rect, 3)
        label = self.font_button.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.next_scene_name = "STARTSCREEN"
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(e.pos):
                    self.next_scene_name = "STARTSCREEN"
                    
                elif self.exit_button_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.title_text, self.title_rect)
        self.draw_button(self.start_button_rect, "Voltar")