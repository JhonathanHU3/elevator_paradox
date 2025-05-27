import pygame
import math
import time

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.Surface((32, 48))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lifePoints = 10;
        self.speed = 2
        self.last_hit_time = 0 
        self.damage = 2

    def update(self, player, walls, enemies):
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize()

        dx = direction.x * self.speed
        dy = direction.y * self.speed

    # Move no X e verifica colisão com parede
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

    # Colisão com outros inimigos (não andar dentro deles)
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                if dx > 0: self.rect.right = enemy.rect.left
                if dx < 0: self.rect.left = enemy.rect.right

    # Move no Y e verifica colisão
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

    # Colisão com outros inimigos
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                if dy > 0: self.rect.bottom = enemy.rect.top
                if dy < 0: self.rect.top = enemy.rect.bottom

    # Dano ao player
        if self.rect.colliderect(player.rect):
            current_time = time.time()
            if current_time - self.last_hit_time >= 1:
                player.lifePoints -= self.damage
                print("👹 Inimigo causou dano! Vida restante:", player.lifePoints)
                self.last_hit_time = current_time


    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
