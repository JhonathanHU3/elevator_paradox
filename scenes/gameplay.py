import pygame, sys
import random
import time
from pygame.locals import *
from settings import *
from entities.player import *
from worlds.secondfloor import World
from entities.enemy import *
from entities.boss import Boss


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
        self.zombies_killed = 15
        self.boss_spawned = False
        self.spawn_duration = 120  # segundos
        self.spawn_start_time = time.time()
        
        # Boss cutscene variables
        self.showing_boss_cutscene = False
        self.boss_cutscene_start = 0
        self.boss_cutscene_duration = 3.0
        self.boss_flash_on = False
        self.last_flash_time = 0
        self.flash_duration = 0.2
        self.boss_position = None  # Store boss position before cutscene
        self.boss = None  # Reference to the boss enemy

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

    def spawn_boss(self):
        # Store boss position
        self.boss_position = (self.world.width // 2, self.world.height // 2)
        # Start boss cutscene
        self.showing_boss_cutscene = True
        self.boss_cutscene_start = time.time()
        # Play boss sound
        try:
            pygame.mixer.Sound("assets/sounds/boss_appear.wav").play()
        except:
            print("Warning: Could not load boss sound")

    def create_boss(self):
        x, y = self.boss_position
        self.boss = Boss(x, y)
        self.enemies.append(self.boss)
        self.boss_spawned = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.attack(self)
                elif event.button == 3:
                    self.player.throwProjectile(self)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Skip boss cutscene
                    if self.showing_boss_cutscene:
                        self.showing_boss_cutscene = False
                        self.create_boss()

    def update(self):
        # If showing boss cutscene, don't update game
        if self.showing_boss_cutscene:
            current_time = time.time()
            if current_time - self.boss_cutscene_start >= self.boss_cutscene_duration:
                self.showing_boss_cutscene = False
                self.create_boss()
            
            # Update flash effect
            if current_time - self.last_flash_time >= self.flash_duration:
                self.boss_flash_on = not self.boss_flash_on
                self.last_flash_time = current_time
            return

        self.player.update()
        self.player.move(self.world.walls)

        # Track dead enemies
        dead_enemies = [e for e in self.enemies if e.lifePoints <= 0]
        self.zombies_killed += len(dead_enemies)

        # Remove dead enemies
        self.enemies = [e for e in self.enemies if e.lifePoints > 0]

        # Update remaining enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.world.walls, self.enemies, self.world)

        # Spawn boss if all zombies are killed and boss hasn't been spawned
        if self.zombies_killed >= self.max_enemies and not self.boss_spawned:
            self.spawn_boss()
        
        # Check for victory: all enemies dead and player collides with elevator
        if not self.enemies and not self.showing_boss_cutscene:
            for elevator in self.world.elevators:
                if self.player.rect.colliderect(elevator):
                    self.next_scene_name = "VICTORY"
        
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
                # Draw boss health bar if it's the boss
                if hasattr(enemy, 'is_boss') and enemy.is_boss:
                    enemy.draw_health_bar(self.screen, offset)
                
        # Draw boss cutscene overlay
        if self.showing_boss_cutscene:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            self.screen.blit(overlay, (0, 0))
            
            # Draw flashing text
            if self.boss_flash_on:
                font = pygame.font.SysFont(None, 72)
                text = font.render("BOSS INCOMING!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(text, text_rect)
                
                # Draw skip text
                skip_font = pygame.font.SysFont(None, 36)
                skip_text = skip_font.render("Press SPACE to skip", True, (100, 100, 100))
                skip_rect = skip_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
                self.screen.blit(skip_text, skip_rect)
