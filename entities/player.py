import pygame;
import time;
from entities.projectile import Projectile;
from pygame.locals import *;

class Player:
    def __init__(self, start_x, start_y):
        self.lifePoints = 20;
        self.damage = 3;
        self.contactDamage = 5;
        self.x = 640;
        self.y = 360;
        
        self.attack_cooldown = 0  # segundos
        self.last_attack_time = 0
        self.attacking = False
        self.attack_duration = 0.6
        self.attack_start_time = 0
        
        self.image = pygame.Surface((32, 48))  
        self.image.fill((100, 150, 150))

        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.speed = 5

    def move(self, walls):
        if self.attacking:
            return
        
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
        current_time = time.time()

        if self.attacking:
            if current_time - self.attack_start_time >= self.attack_duration:
                self.attacking = False
        pass
    
    def attack(self, game):
        current_time = time.time()

        # Só ataca se não estiver no meio de um ataque e se passou o cooldown
        if not self.attacking and current_time - self.last_attack_time >= self.attack_cooldown:
            self.attacking = True
            self.attack_start_time = current_time
            self.last_attack_time = current_time

            # Mesmo código de ataque
            mouse_x, mouse_y = pygame.mouse.get_pos()
        
            offset = pygame.Vector2(
                self.rect.centerx - game.screen.get_width() // 2,
                self.rect.centery - game.screen.get_height() // 2
            )
            mouse_pos_world = pygame.Vector2(mouse_x, mouse_y) + offset

            direction = pygame.Vector2(mouse_pos_world) - pygame.Vector2(self.rect.center)
        
            if direction.length() == 0:
                return

            direction = direction.normalize()

            attack_range = 50
            attack_rect = pygame.Rect(0, 0, 40, 40)
            attack_rect.center = (self.rect.centerx + direction.x * attack_range,
                              self.rect.centery + direction.y * attack_range)

            for enemy in game.enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.lifePoints -= self.contactDamage
                    print("💥 Acertou um inimigo! Vida restante:", enemy.lifePoints)
        pass

    def throwProjectile(self, game):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset = pygame.Vector2(
            self.rect.centerx - game.screen.get_width() // 2,
            self.rect.centery - game.screen.get_height() // 2
        )
        mouse_pos_world = pygame.Vector2(mouse_x, mouse_y) + offset

        direction = mouse_pos_world - pygame.Vector2(self.rect.center)

        if direction.length() == 0:
            return

        projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
        game.projectiles.append(projectile)

        pass
    
    def die(self, game):
        game.next_scene_name = "GAMEOVERSCREEN"
    