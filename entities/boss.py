import pygame
import time
from entities.enemy import Enemy

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Boss stats
        self.maxLifePoints = 500
        self.lifePoints = self.maxLifePoints
        self.damage = 10
        self.speed = 5.0
        
        # Make boss larger
        self.image = pygame.transform.scale(self.image, (64, 96))  # Double the size
        self.rect = self.image.get_rect(center=(x, y))
        
        # Scale up attack sprites
        self.attack_sprites = [pygame.transform.scale(sprite, (76, 96)) for sprite in self.attack_sprites]
        # Scale up walk sprites
        self.walk_sprites = [pygame.transform.scale(sprite, (64, 96)) for sprite in self.walk_sprites]
        
        # Boss specific attributes
        self.is_boss = True
        self.last_attack_time = 0
        self.attack_cooldown = 1.5  # 1 second between attacks
        
    def draw_health_bar(self, screen, offset):
        # Health bar dimensions
        bar_width = 200
        bar_height = 20
        bar_padding = 2
        
        # Calculate position (above the boss)
        bar_x = self.rect.centerx - bar_width//2
        bar_y = self.rect.top - bar_height - 10
        
        # Draw background (dark red)
        pygame.draw.rect(screen, (100, 0, 0), 
                        (bar_x - offset.x, bar_y - offset.y, 
                         bar_width, bar_height))
        
        # Calculate current health width
        health_ratio = self.lifePoints / self.maxLifePoints
        current_width = int(bar_width * health_ratio)
        
        # Draw health (bright red)
        if current_width > 0:
            pygame.draw.rect(screen, (255, 0, 0), 
                           (bar_x - offset.x, bar_y - offset.y, 
                            current_width, bar_height))
            
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), 
                        (bar_x - offset.x, bar_y - offset.y, 
                         bar_width, bar_height), 2)
        
        # Draw boss name
        font = pygame.font.SysFont(None, 24)
        name_text = font.render("BOSS", True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(bar_x + bar_width//2 - offset.x, bar_y - 15 - offset.y))
        screen.blit(name_text, name_rect)
        
    def update(self, player, walls, enemies, world):
        super().update(player, walls, enemies, world)
        
        # Boss specific update logic can be added here
        # For example, special attacks or behaviors 