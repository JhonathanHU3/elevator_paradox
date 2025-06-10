import pygame, sys
from pygame.locals import *
from settings import *

class GameOver:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None

        self.font_button = pygame.font.SysFont(None, 50)

        # Carrega a imagem de Game Over
        self.background_image = pygame.image.load('assets/backgrounds/gameover.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        # Botão customizado
        self.button_rect = pygame.Rect(WIDTH // 2 - 218, HEIGHT // 2 + 255, 408, 55)
        self.ORANGE = (255, 100, 0)
        self.HOVER_COLOR = (200, 200, 200, 50)

    def draw_button(self, rect, hovered):
        if hovered:
            s = pygame.Surface(rect.size, pygame.SRCALPHA)
            s.fill(self.HOVER_COLOR)
            self.screen.blit(s, rect.topleft)
        # Sem texto

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.next_scene_name = "STARTSCREEN"
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(e.pos):
                    self.next_scene_name = "STARTSCREEN"

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button_rect.collidepoint(mouse_pos)
        self.draw_button(self.button_rect, hovered)