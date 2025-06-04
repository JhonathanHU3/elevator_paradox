import pygame
import time
from entities.projectile import Projectile
from pygame.locals import *

class Player:
    def __init__(self, start_x, start_y):
        self.lifePoints = 20
        self.damage = 3
        self.contactDamage = 5
        self.x = 640
        self.y = 360

        self.attack_cooldown = 0
        self.last_attack_time = 0
        self.attacking = False
        self.attack_duration = 0.6
        self.attack_start_time = 0

        # 🎨 Carrega e redimensiona os sprites
        self.sprites = [
            pygame.transform.scale(pygame.image.load('assets/sprites/player/sprite_0.png').convert_alpha(), (82, 82)),
            pygame.transform.scale(pygame.image.load('assets/sprites/player/sprite_1.png').convert_alpha(), (82, 82)),
            pygame.transform.scale(pygame.image.load('assets/sprites/player/sprite_2.png').convert_alpha(), (82, 82)),
            pygame.transform.scale(pygame.image.load('assets/sprites/player/sprite_3.png').convert_alpha(), (82, 82))
        ]

        self.current_sprite = 0
        self.animation_speed = 0.1

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(start_x, start_y))
        self.speed = 5

        self.facing_right = True
        self.moving = False  # ✅ Novo atributo

    def move(self, walls):
        if self.attacking:
            self.moving = False
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_right = True

        if dx != 0 or dy != 0:
            self.moving = True
        else:
            self.moving = False
            self.current_sprite = 0  # ✅ Reseta animação ao parar

        # Move em X
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right

        # Move em Y
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

    def draw(self, screen, offset):
        self.image = self.sprites[int(self.current_sprite)]

        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect.topleft - offset)
        else:
            screen.blit(self.image, self.rect.topleft - offset)

    def update(self):
        current_time = time.time()

        if self.attacking:
            if current_time - self.attack_start_time >= self.attack_duration:
                self.attacking = False

        # ✅ Só anima se estiver se movendo
        if self.moving:
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

    def attack(self, game):
        current_time = time.time()

        if not self.attacking and current_time - self.last_attack_time >= self.attack_cooldown:
            self.attacking = True
            self.attack_start_time = current_time
            self.last_attack_time = current_time

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
            attack_rect.center = (
                self.rect.centerx + direction.x * attack_range,
                self.rect.centery + direction.y * attack_range
            )

            for enemy in game.enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.lifePoints -= self.contactDamage
                    print("💥 Acertou um inimigo! Vida restante:", enemy.lifePoints)

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

    def die(self, game):
        game.next_scene_name = "GAMEOVERSCREEN"
