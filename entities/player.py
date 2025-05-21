import pygame;
from pygame.locals import *;

class Player:
    def __init__(self, start_x, start_y):
        self.lifePoints = 20;
        self.damage = 3;
        self.contactDamage = 5;
        self.x = 640;
        self.y = 360;
        
        self.image = pygame.Surface((32, 48)) 
        self.image.fill((100, 150, 150))

        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.speed = 5

    def move(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed

    # Move em X e verifica colisão
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:  # indo para direita
                    self.rect.right = wall.left
                if dx < 0:  # indo para esquerda
                    self.rect.left = wall.right

    # Move em Y e verifica colisão
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:  # descendo
                    self.rect.bottom = wall.top
                if dy < 0:  # subindo
                    self.rect.top = wall.bottom
        
    
    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
    
    def update(self):
        pass
    
    def attack():
        
        pass
    
    def throwProjectile():
        
        pass