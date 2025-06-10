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

        # Damage flash effect
        self.damage_timer = 0
        self.damage_flash_duration = 0.3  # seconds

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
        # Criar um hitbox menor que o sprite
        self.rect = pygame.Rect(0, 0, 50, 50)  # Hitbox de 50x50 pixels
        self.rect.center = (start_x + 41, start_y + 41)  # Centraliza o hitbox no sprite (82/2 = 41)
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
            if self.damage_timer > 0:
                # Create a copy of the image
                flash_image = flipped_image.copy()
                # Add red tint by increasing red channel
                flash_image.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(flash_image, self.rect.topleft - offset)
            else:
                screen.blit(flipped_image, self.rect.topleft - offset)
        else:
            if self.damage_timer > 0:
                # Create a copy of the image
                flash_image = self.image.copy()
                # Add red tint by increasing red channel
                flash_image.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(flash_image, self.rect.topleft - offset)
            else:
                screen.blit(self.image, self.rect.topleft - offset)
        
        # Draw health bar
        self.draw_health_bar(screen, offset)

    def draw_health_bar(self, screen, offset):
        # Health bar dimensions
        bar_width = 50
        bar_height = 5
        bar_padding = 2  # Space between bar and border
        
        # Calculate position (above the player)
        sprite_center_x = self.rect.centerx + (41 - 25)  # Ajusta para o centro do sprite (82/2 - 50/2)
        bar_x = sprite_center_x - bar_width//2
        bar_y = self.rect.top - bar_height - 5  # 5 pixels above the hitbox
        
        # Draw background (gray)
        pygame.draw.rect(screen, (100, 100, 100), 
                        (bar_x - offset.x, bar_y - offset.y, 
                         bar_width, bar_height))
        
        # Calculate current health width
        health_ratio = self.lifePoints / 20  # 20 is max health
        current_width = int(bar_width * health_ratio)
        
        # Draw health (green)
        if current_width > 0:
            pygame.draw.rect(screen, (0, 255, 0), 
                           (bar_x - offset.x, bar_y - offset.y, 
                            current_width, bar_height))

    def update(self):
        current_time = time.time()

        if self.attacking:
            if current_time - self.attack_start_time >= self.attack_duration:
                self.attacking = False

        # Update damage flash timer
        if self.damage_timer > 0:
            self.damage_timer -= 1/60  # Assuming 60 FPS
            if self.damage_timer < 0:
                self.damage_timer = 0

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

    def take_damage(self, amount):
        self.lifePoints -= amount
        self.damage_timer = self.damage_flash_duration
