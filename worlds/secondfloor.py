import pygame

tile_map = [
    "WWWWWWWWWW",
    "W........W",
    "W..P.....W",
    "W........W",
    "WWWWWWWWWW"
]

tile_size = 64

class World:
    def __init__(self):
        self.tiles = []
        self.walls = []
        self.start_pos = pygame.Vector2(0, 0)

        # Carrega as imagens uma vez só
        self.img_floor = pygame.image.load("assets/tileset/chao.png").convert()
        self.img_wall = pygame.image.load("assets/tileset/chao.png").convert()

        for y, row in enumerate(tile_map):
            for x, char in enumerate(row):
                pos = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                
                if char == "W":
                    self.tiles.append((self.img_wall, pos))
                    self.walls.append(pos)
                elif char == ".":
                    self.tiles.append((self.img_floor, pos))
                elif char == "P":
                    self.tiles.append((self.img_floor, pos))
                    self.start_pos = pygame.Vector2(pos.topleft)

    def draw(self, screen, offset):
        screen_rect = screen.get_rect()
        for img, rect in self.tiles:
            # Só desenha se estiver visível
            draw_pos = rect.move(-offset.x, -offset.y)
            if screen_rect.colliderect(draw_pos):
                screen.blit(img, draw_pos)
