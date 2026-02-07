import random

import pygame

from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class World:
    def __init__(self):
        self.height = SCREEN_HEIGHT // TILE_SIZE
        self.width = SCREEN_WIDTH // TILE_SIZE

        self.map = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if y < self.height // 2:
                    row.append(0)
                else:
                    row.append(random.choice([1, 2, 1, 1, 1, 1 ]))

            self.map.append(row)

        # self.map = [
        #     [
        #         0 if y < self.height // 2 else random.choice([1, 2, 1, 1, 1])
        #         for x in range(self.width)
        #     ]
        #     for y in range(self.height)
        # ]

        # 👇 СПАВН ИГРОКА (фиксированное место)
        spawn_x = self.width // 2
        spawn_y = self.height // 2 - 1  # прямо над песком
        self.map[spawn_y][spawn_x] = 3

        # for y in range(self.height):
        #     for x in range(self.width):
        #         if y <= self.height // 2:
        #             self.map[y][x] = 0  # 0 — воздух
        #
        #         elif x % 2 == 0:
        #             self.map[y][x] = 1  # 1 — песок (вариант 1)
        #
        #         else:
        #             self.map[y][x] = 2  # 2 — песок (вариант 2)

        # for y in range(self.height // 2, self.height):
        #     row = []
        #     for x in range(self.width):
        #         if y <= self.height // 2:
        #             row.append(0)  # 0 — воздух
        #
        #         elif x % 2 == 0:
        #             row.append(1)  # 1 — песок (вариант 1)
        #
        #         else:
        #             row.append(2)  # 2 — песок (вариант 2)
        #         self.map.append(row)
        #
        #     self.air_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        #     self.air_tile.fill((135, 206, 235))  # светло-голубой цвет (небо)

        self.air_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.air_tile.fill((135, 206, 235))  # светло-голубой цвет (небо)

        # self.sand_tiles = [
        #     pygame.image.load("assets/tiles/sand.png").convert_alpha(),
        #     pygame.image.load("assets/tiles/sand_with_stones.png").convert_alpha(),
        # ]

        self.tiles = {
            0: pygame.image.load("assets/tiles/Clouds V2-2.png").convert_alpha(),
            1: pygame.image.load("assets/tiles/sand.png").convert_alpha(),
            2: pygame.image.load("assets/tiles/sand_with_stones.png").convert_alpha(),
            3: pygame.image.load("assets/tiles/spawnpoint.png").convert_alpha(),
        }

        self.tile_health = {}  # Словарь для хранения HP сломанных блоков
        self.max_hp = {1: 10, 2: 20}  # Прочность: ID 1 (10 ударов), ID 2 (20 ударов)

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.map[y][x]
                # if tile_id != 0:
                tile = self.tiles[tile_id]
                screen.blit(
                    tile,
                    (x * TILE_SIZE, y * TILE_SIZE)
                )

    def get_ground_y(self, tile_x):
        """
        Возвращает Y (в пикселях), где начинается земля
        """
        for tile_y in range(self.height):
            tile_id = self.map[tile_y][tile_x]
            if tile_id in (1, 2):  # не воздух
                return tile_y * TILE_SIZE

        return self.height * TILE_SIZE  # если земли нет
#hello
