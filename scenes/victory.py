import pygame
from settings import *

class VictoryScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None
        self.font = pygame.font.SysFont(None, 80)
        self.text = self.font.render("VOCÊ ESCAPOU!", True, (0, 255, 0))
        self.text_rect = self.text.get_rect(center=(WIDTH//2, HEIGHT//2))

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.next_scene_name = "STARTSCREEN"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.text, self.text_rect) 