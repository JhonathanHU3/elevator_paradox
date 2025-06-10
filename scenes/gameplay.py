import pygame, sys
import random
import time
from pygame.locals import *
from settings import *
from entities.player import *
from worlds.secondfloor import World
from entities.enemy import *


class Gameplay:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.world = World()
        self.player = Player(self.world.start_pos.x, self.world.start_pos.y)
        self.next_scene_name = None
        
        self.enemies = []
        self.projectiles = []
        self.max_enemies = 20
        self.spawn_duration = 120  # segundos
        self.spawn_start_time = time.time()

        for _ in range(self.max_enemies):
            self.spawn_enemy()

    def spawn_enemy(self):
        while True:
            x = random.randint(0, self.world.width - self.world.tile_size)
            y = random.randint(0, self.world.height - self.world.tile_size)

            enemy_rect = pygame.Rect(x, y, 32, 48)

            # Evita spawn dentro de parede
            collision = any(enemy_rect.colliderect(wall) for wall in self.world.walls)

            # Evita spawn muito perto do player
            safe_distance = 200
            player_distance = pygame.Vector2(self.player.rect.center) - pygame.Vector2(x, y)

            if collision or player_distance.length() < safe_distance:
                continue

            # Se passou nos testes, cria
            enemy = Enemy(x, y)
            self.enemies.append(enemy)
            break

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.attack(self)
                elif event.button == 3:
                    self.player.throwProjectile(self)

    def update(self):
        self.player.update()
        self.player.move(self.world.walls)

        for enemy in self.enemies:
            enemy.update(self.player, self.world.walls, self.enemies, self.world)

        # Remove inimigos mortos
        self.enemies = [e for e in self.enemies if e.lifePoints > 0]

        # Se tiver menos que o máximo e dentro do tempo, spawna outro
        if len(self.enemies) < self.max_enemies and time.time() - self.spawn_start_time < self.spawn_duration:
            self.spawn_enemy()
            
        if(self.player.lifePoints <= 0):
            self.player.die(self)

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        # Câmera segue o jogador
        offset = pygame.Vector2(
            self.player.rect.centerx - self.game.screen.get_width() // 2,
            self.player.rect.centery - self.game.screen.get_height() // 2
        )

        self.world.draw(self.game.screen, offset)
        self.player.draw(self.game.screen, offset)

        for projectile in self.projectiles:
            projectile.draw(self.screen, offset)

        for projectile in self.projectiles[:]:
            projectile.update(self)
            if not projectile.alive:
                self.projectiles.remove(projectile)

        for enemy in self.enemies:
            # Só desenha se está dentro do mundo
            if (0 <= enemy.rect.left <= self.world.width and
                0 <= enemy.rect.top <= self.world.height and
                0 <= enemy.rect.right <= self.world.width and
                0 <= enemy.rect.bottom <= self.world.height):
                enemy.draw(self.screen, offset)
