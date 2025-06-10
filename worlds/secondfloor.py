import pygame

tile_map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWEEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W............................................................W",
    "W............................................................W",
    "W............................................................W",
    "W..............................P.............................W",
    "W............................................................W",
    "W............................................................W",
    "W............................................................W",
    "W............................................................W",
    "W............................................................W",
    "W............................................................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]



class World:
    def __init__(self):
        self.tiles = []
        self.walls = []
        self.elevators = []  # Store elevator rects
        self.tile_size = 64
        self.start_pos = pygame.Vector2(0, 0)
        
        self.width = len(tile_map[0]) * self.tile_size
        self.height = len(tile_map) * self.tile_size

        self.img_floor = pygame.image.load("assets/tileset/chao.png").convert()
        self.img_wall = pygame.image.load("assets/tileset/wall.png").convert()
        self.img_elevator = pygame.image.load("assets/tileset/elevator.png").convert()

        for y, row in enumerate(tile_map):
            for x, char in enumerate(row):
                pos = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                
                if char == "W":
                    self.tiles.append((self.img_wall, pos))
                    self.walls.append(pos)
                elif char == ".":
                    self.tiles.append((self.img_floor, pos))
                elif char == "E":
                    self.tiles.append((self.img_elevator, pos))
                    self.elevators.append(pos)  # Add elevator rect
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
                
