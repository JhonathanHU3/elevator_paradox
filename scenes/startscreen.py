import pygame, sys
from pygame.locals import *
from settings import *

class StartScreenScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.next_scene_name = None

        self.WHITE = (255, 255, 255)
        self.DARK_GRAY = (50, 50, 50)
        self.BLACK = (0, 0, 0)

        # Load background image
        self.background_image = pygame.image.load('assets/backgrounds/menu_background.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.font_button = pygame.font.SysFont(None, 50)

        # Fine-tuning button positions to align with background image text
        self.start_button_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 70, 210, 55) # Adjusted position for START
        self.exit_button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 185, 140, 55) # Adjusted position for EXIT

        self.ORANGE = (255, 100, 0) # Define an orange color
        self.HOVER_COLOR = (200, 200, 200, 50) # Light gray with some transparency

        # Música de fundo do menu
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('assets/sounds/menu_music.mp3')  # ou .ogg
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop infinito

    def draw_button(self, rect, text):
        # Removed button background and border drawing
        # pygame.draw.rect(self.screen, self.DARK_GRAY, rect)
        # pygame.draw.rect(self.screen, self.WHITE, rect, 3)
        # label = self.font_button.render(text, True, self.ORANGE) # Changed text color to orange
        # label_rect = label.get_rect(center=rect.center)
        # self.screen.blit(label, label_rect)
        pass # No visual drawing for the button

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                print("Iniciar o jogo (pressionou Enter)")
                # Aqui você pode mudar de cena futuramente
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(e.pos):
                    print("Iniciar o jogo (clicou no botão)")
                    self.next_scene_name = "CUTSCENE"
                    
                elif self.exit_button_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background_image, (0, 0)) # Draw background

        mouse_pos = pygame.mouse.get_pos()

        # Hover effect for START button
        if self.start_button_rect.collidepoint(mouse_pos):
            s = pygame.Surface(self.start_button_rect.size, pygame.SRCALPHA) # Create a surface with alpha
            s.fill(self.HOVER_COLOR) # Fill with hover color
            self.screen.blit(s, self.start_button_rect.topleft) # Blit onto the screen

        # Hover effect for EXIT button
        if self.exit_button_rect.collidepoint(mouse_pos):
            s = pygame.Surface(self.exit_button_rect.size, pygame.SRCALPHA) # Create a surface with alpha
            s.fill(self.HOVER_COLOR) # Fill with hover color
            self.screen.blit(s, self.exit_button_rect.topleft) # Blit onto the screen

        # Removed title text drawing
        # self.screen.blit(self.title_text, self.title_rect)
        self.draw_button(self.start_button_rect, "START")
        self.draw_button(self.exit_button_rect, "EXIT")