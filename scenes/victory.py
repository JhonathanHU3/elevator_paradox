import pygame
from settings import *

class VictoryScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None
        # Carrega a imagem de fundo da vitória
        self.background_image = pygame.image.load('assets/backgrounds/victory.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        # Botão transparente, sem texto, mais para baixo
        self.button_width = 408
        self.button_height = 80  # altura aumentada
        self.button_rect = pygame.Rect(WIDTH // 2 - self.button_width // 2, HEIGHT // 2 + 200, self.button_width, self.button_height)
        self.button_border_color = (0, 0, 0)
        self.button_hover_alpha = 50  # Transparência ao passar o mouse

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
        # Botão transparente
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button_rect.collidepoint(mouse_pos)
        if hovered:
            s = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
            s.fill((200, 200, 200, self.button_hover_alpha))
            self.screen.blit(s, self.button_rect.topleft)
        # Não desenha borda 