import random
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class World:
    def __init__(self):
        self.height = (SCREEN_HEIGHT // TILE_SIZE) * 2
        self.width = (SCREEN_WIDTH // TILE_SIZE) * 2
        self.map = []

        # Загрузка ресурсов
        self.tiles = {
            0: pygame.image.load("assets/tiles/c.png").convert_alpha(),
            1: pygame.image.load("assets/tiles/sand.png").convert_alpha(),
            2: pygame.image.load("assets/tiles/sand_with_stones.png").convert_alpha(),
            3: pygame.image.load("assets/tiles/air.png").convert_alpha(),
            4: pygame.image.load("assets/tiles/c.png").convert_alpha(),  # Еда
            5: pygame.image.load("assets/tiles/ore.png").convert_alpha()  # Мутация
        }

        self.tile_health = {}
        self.max_hp = {1: 10, 2: 20, 5: 100}
        self.generate_world()

    def generate_world(self):
        self.map = []
        # Заполнение: небо (0) и песок (1/2)
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if y < self.height // 2:
                    row.append(0)
                else:
                    row.append(random.choice([1] * 9 + [2]))
            self.map.append(row)

        # Храм
        shrine_x, shrine_y = self.width // 2 - 5, (self.height // 2) + 5
        for dy in range(6):
            for dx in range(6):
                ty, tx = shrine_y + dy, shrine_x + dx
                if 0 <= ty < self.height and 0 <= tx < self.width:
                    self.map[ty][tx] = 3 if dy == 5 else 0

        # Пещера (Нора)
        cave_x, cave_y = self.width // 2 - 8, (self.height // 2) + 15
        for dy in range(3):
            for dx in range(4):
                if 0 <= cave_y + dy < self.height and 0 <= cave_x + dx < self.width:
                    self.map[cave_y + dy][cave_x + dx] = 0

        # Столбик с рудой
        if 0 <= cave_x + 3 < self.width:
            self.map[cave_y][cave_x] = 0
            self.map[cave_y][cave_x + 3] = 2
            self.map[cave_y + 1][cave_x + 3] = 2
            self.map[cave_y + 2][cave_x + 3] = 5

    def draw(self, screen, camera, player):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.map[y][x]

                # РИСУЕМ ТОЛЬКО ЕСЛИ:
                # 1. Это не воздух (0)
                # 2. Картинка для этого ID существует в словаре
                if tile_id != 0 and self.tiles.get(tile_id):
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    image = self.tiles[tile_id]

                    # Масштабируем до 16x16, если нужно
                    if image.get_width() != TILE_SIZE:
                        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

                    # Рисуем блок поверх неба
                    screen.blit(image, camera.apply(tile_rect))

                    # Эффект копания (проценты или искры)
                    if (x, y) in self.tile_health:
                        # Твой код эффектов...
                        pass