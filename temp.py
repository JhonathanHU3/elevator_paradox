import pygame
import time

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.speed = 1.5
        self.lifePoints = 10
        self.last_hit_time = 0
        self.damage = 1

        # ✅ Animações
        self.walk_sprites = [
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/sprite_0.png").convert_alpha(), (32, 48)),
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/sprite_1.png").convert_alpha(), (32, 48)),
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/sprite_2.png").convert_alpha(), (32, 48)),
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/sprite_3.png").convert_alpha(), (32, 48))
        ]

        self.attack_sprites = [
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/attack/Zombie_ataque0.png").convert_alpha(), (38, 48)),
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/attack/Zombie_ataque1.png").convert_alpha(), (38, 48)),
            pygame.transform.scale(pygame.image.load("assets/sprites/enemy/attack/Zombie_ataque2.png").convert_alpha(), (38, 48)),
        ]

        self.current_sprite = 0
        self.walk_animation_speed = 0.1
        self.image = self.walk_sprites[0]
        self.facing_right = True

        # ⏱ Estado de ataque
        self.attack_animation_speed = 0.07
        self.attacking = False
        self.attack_duration = 1.2 # segundos
        self.attack_start_time = 0

    def update(self, player, walls, enemies, world):
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize()

        dx = direction.x * self.speed
        dy = direction.y * self.speed

        # 👉 Define a direção que o inimigo está olhando
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        # 🌍 Limite do mundo
        if (self.rect.left < 0 or self.rect.top < 0 or
            self.rect.right > world.width or self.rect.bottom > world.height):
            self.lifePoints = 0

        # 💥 Colisão com o player → entra no modo ataque
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
            if not self.attacking:
                self.attacking = True
                self.attack_start_time = time.time()
            current_time = time.time()
            if current_time - self.last_hit_time >= 1:
                player.take_damage(self.damage)
                print("👹 Inimigo causou dano! Vida restante:", player.lifePoints)
                self.last_hit_time = current_time

        # ⏳ Sai do modo ataque após o tempo acabar
        if self.attacking:
            if time.time() - self.attack_start_time >= self.attack_duration:
                self.attacking = False
        else:
            # ✅ Só se move se não estiver atacando
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

        # 🎞️ Atualizar sprite (sempre!)
        self.current_sprite += self.attack_animation_speed if self.attacking else self.walk_animation_speed
        if self.attacking and self.current_sprite >= len(self.attack_sprites):
            self.current_sprite = 0
        elif not self.attacking and self.current_sprite >= len(self.walk_sprites):
            self.current_sprite = 0

        # Define sprite atual
        if self.attacking:
            self.image = self.attack_sprites[int(self.current_sprite)]
        else:
            self.image = self.walk_sprites[int(self.current_sprite)]


    def draw(self, screen, offset):
        # 🪞 Inverte se necessário
        if self.facing_right:
            screen.blit(self.image, self.rect.topleft - offset)
        else:
            flipped = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped, self.rect.topleft - offset)
