import pygame;
from pygame.locals import *;

class Player:
    def __init__(self):
        self.lifePoints = 20;
        self.damage = 3;
        self.contactDamage = 5;
        
        pass
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            print("W");
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            print("A");
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            print("S");
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            print("D");
            
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 150, 150), (640, 360, 40, 70))
        pass
    
    def attack():
        
        pass
    
    def throwProjectile():
        
        pass