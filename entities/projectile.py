import pygame

class Projectile:
    def __init__(self, x, y, direction, speed=7, damage=5):
        self.image = pygame.transform.scale(pygame.image.load("assets/sprites/projectile.png").convert_alpha(), (20, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.Vector2(direction)
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)
        self.speed = speed
        self.damage = damage
        self.alive = True

    def update(self, game):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Colisão com inimigos
        for enemy in game.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.lifePoints -= self.damage
                print("🔥 Projétil acertou inimigo!")
                self.alive = False
                break

        # Fora dos limites do mundo
        if not (0 <= self.rect.centerx <= game.world.width and
                0 <= self.rect.centery <= game.world.height):
            self.alive = False

    def draw(self, screen, offset):
        screen.blit(self.image, self.rect.topleft - offset)
