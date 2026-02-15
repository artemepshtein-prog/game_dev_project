import random
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class World:
    def __init__(self):
        # 1. Базовые настройки
        self.height = SCREEN_HEIGHT // TILE_SIZE * 2
        self.width = SCREEN_WIDTH // TILE_SIZE * 2
        self.map = []

        # 2. Загрузка ресурсов
        self.tiles = {
            0: pygame.image.load("assets/tiles/c.png").convert_alpha(),
            1: pygame.image.load("assets/tiles/sand.png").convert_alpha(),
            2: pygame.image.load("assets/tiles/sand_with_stones.png").convert_alpha(),
            3: pygame.image.load("assets/tiles/air.png").convert_alpha(),
        }

        self.tile_health = {}
        self.max_hp = {1: 10, 2: 20}

        # 3. ЗАПУСКАЕМ генерацию (только один раз!)
        self.generate_world()

    def generate_world(self):
        # 1. ОБНУЛЯЕМ КАРТУ
        self.map = []

        # 2. СНАЧАЛА ЗАПОЛНЯЕМ ВЕСЬ МИР (Песок, небо, рандом)
        # Этот блок должен идти ПЕРВЫМ
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if y < self.height // 2:
                    row.append(0)  # Небо
                else:
                    row.append(random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2]))
            self.map.append(row)

        # 3. А ВОТ ТЕПЕРЬ "ВЫРУБАЕМ" ХРАМ (Последнее слово за ним!)
        # Поднимем координаты еще выше для верности
        shrine_x = self.width // 2 - 5
        shrine_y = (self.height // 2) + 5  # Подняли к самому небу

        for dy in range(6):
            for dx in range(10):
                ty = shrine_y + dy
                tx = shrine_x + dx

                if 0 <= ty < self.height and 0 <= tx < self.width:
                    if dy == 5:
                        # Пол храма — заменяем песок на спецблок
                        self.map[ty][tx] = 3
                    else:
                        # Внутренность храма — стираем песок в 0 (воздух)
                        self.map[ty][tx] = 0

                        # 4. ОБНОВЛЯЕМ ТОЧКУ СПАВНА
        self.spawn_pos = ((shrine_x + 5) * TILE_SIZE, (shrine_y + 3) * TILE_SIZE)
    def draw(self, screen, camera, player):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.map[y][x]
                if tile_id != 0:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    screen.blit(self.tiles[tile_id], camera.apply(tile_rect))

    def get_ground_y(self, tile_x):
        for tile_y in range(self.height):
            tile_id = self.map[tile_y][tile_x]
            if tile_id in (1, 2, 3):
                return tile_y * TILE_SIZE
        return self.height * TILE_SIZE