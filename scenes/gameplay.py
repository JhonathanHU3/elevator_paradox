import pygame, sys
import random
import time
from pygame.locals import *
from settings import *
from entities.player import *;
from worlds.secondfloor import World;
from entities.enemy import *;


class Gameplay():
    def __init__(self, game):
        self.game = game;
        self.screen = game.screen;
        self.world = World();
        self.player = Player(self.world.start_pos.x, self.world.start_pos.y)
        
        self.enemies = []
        self.max_enemies = 10
        self.spawn_duration = 120  # 2 minutos
        self.spawn_start_time = time.time()
        
        for _ in range(self.max_enemies):
            self.spawn_enemy()

    def spawn_enemy(self):
        map_width, map_height = self.world.get_size()

        while True:
            x = random.randint(0, map_width - self.world.tile_size)
            y = random.randint(0, map_height - self.world.tile_size)
        
            enemy_rect = pygame.Rect(x, y, 32, 48)
        
            # Evita spawn dentro de parede
            collision = any(enemy_rect.colliderect(wall) for wall in self.world.walls)
        
        # Evita spawn muito perto do player
            safe_distance = 200
            player_distance = self.player.rect.centerx - x, self.player.rect.centery - y
            if collision or abs(player_distance[0]) < safe_distance and abs(player_distance[1]) < safe_distance:
                continue
        
        # Se passou nos testes, cria
            enemy = Enemy(x, y)
            self.enemies.append(enemy)
            break

        
    def handle_events(self, events):
        
        pass

    def update(self):
        self.player.update()
        self.player.move(self.world.walls)
        
        for enemy in self.enemies:
            enemy.update(self.player, self.world.walls, self.enemies)

        # Remove inimigos mortos
        self.enemies = [e for e in self.enemies if e.lifePoints > 0]

        # Se tiver menos que o máximo e dentro do tempo, spawna outro
        if len(self.enemies) < self.max_enemies:
            if time.time() - self.spawn_start_time < self.spawn_duration:
                self.spawn_enemy()
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        # Câmera segue o jogador
        offset = pygame.Vector2(
            self.player.rect.centerx - self.game.screen.get_width() // 2,
            self.player.rect.centery - self.game.screen.get_height() // 2
        )

        self.world.draw(self.game.screen, offset)
        self.player.draw(self.game.screen, offset)
        for enemy in self.enemies:
            enemy.draw(self.screen, offset)
        pass
        
        