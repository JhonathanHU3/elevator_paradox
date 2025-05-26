import pygame, sys
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
        self.enemy = Enemy(400, 200);
        
    def handle_events(self, events):
        
        pass

    def update(self):
        self.player.update()
        self.player.move(self.world.walls)
        self.enemy.update(self.player, self.world.walls)
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
        self.enemy.draw(self.game.screen, offset)
        pass
        
        