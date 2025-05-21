import pygame
import math
import time

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.Surface((32, 48))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.last_hit_time = 0 
        self.damage = 2

    def update(self, player, walls):
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize()

        dx = direction.x * self.speed
        dy = direction.y * self.speed

        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom


        if self.rect.colliderect(player.rect):
            overlap = self.rect.clip(player.rect)
            if overlap.width > overlap.height:
                if self.rect.centery < player.rect.centery:
                    self.rect.top = player.rect.top - self.rect.height
                else:
                    self.rect.bottom = player.rect.bottom + self.rect.height
            else:
                if self.rect.centerx < player.rect.centerx:
                    self.rect.left = player.rect.left - self.rect.width
                else:
                    self.rect.right = player.rect.right + self.rect.width

            current_time = time.time()
            if current_time - self.last_hit_time >= 1:  
                player.lifePoints -= self.damage
                print("👹 Inimigo causou dano! Vida restante:", player.lifePoints)
                self.last_hit_time = current_time

    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
