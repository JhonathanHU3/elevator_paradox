import pygame, sys
from pygame.locals import *
from settings import *
import time

class BossCutscene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        
        # Initialize audio
        pygame.mixer.init()
        
        # Load boss appearance sound
        try:
            self.boss_sound = pygame.mixer.Sound("assets/sounds/boss_appear.wav")
            self.boss_sound.play()
        except:
            print("Warning: Could not load boss sound")
        
        # Cutscene timing
        self.start_time = time.time()
        self.duration = 3.0  # 3 seconds cutscene
        
        # Text settings
        self.font = pygame.font.SysFont(None, 72)
        self.text = self.font.render("O BOSS ESTÁ CHEGANDO!", True, self.RED)
        self.text_rect = self.text.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Flash effect
        self.flash_duration = 0.2
        self.last_flash = 0
        self.flash_on = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.next_scene_name = "GAMEPLAY"

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Flash effect
        if current_time - self.last_flash >= self.flash_duration:
            self.flash_on = not self.flash_on
            self.last_flash = current_time
        
        # End cutscene after duration
        if elapsed >= self.duration:
            self.next_scene_name = "GAMEPLAY"

    def draw(self):
        # Fill screen with black
        self.screen.fill(self.BLACK)
        
        # Draw flashing text
        if self.flash_on:
            self.screen.blit(self.text, self.text_rect)
        
        # Draw warning text
        warning_font = pygame.font.SysFont(None, 36)
        warning_text = warning_font.render("Press SPACE to skip", True, (100, 100, 100))
        warning_rect = warning_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
        self.screen.blit(warning_text, warning_rect) 