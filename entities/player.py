import pygame
from core.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT



class Player:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
        # Загружаем спрайт
        self.image = (pygame.image.load("assets/tiles/main_hero (2).png")
                      .convert_alpha())
        # Опционально масштабируем, чтобы точно 16×16
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)
                                            )
        self.rect = self.image.get_rect()
        self.rect.x = 64
        self.rect.y = 0
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.bottom // TILE_SIZE
        # self.velocity_y = 0  # скорость падения
        #self.gravity = 0.5  # сила гравитации
        self.on_ground = True  # стоит ли на земле
        self.jump_power = 0
        self.current_x = 0
        self.current_y = 0

        # Рект для коллизий и позиции
        #self.rect = self.image.get_rect()
        #spawn_x = self.world.width // 2#

        for y in range(world.height):
            if world.map[y][tile_x] != 0:
                self.rect.x = tile_x * TILE_SIZE
                self.rect.bottom = y * TILE_SIZE
                break

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 2
        self.gravity = 0.8
        self.jump_power = -12
        # self.on_ground = False


    def update(self, world):
        self.handle_input()

        # Горизонтальное движение
        self.rect.x += self.vel_x

        # Вертикальное движение
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Проверяем землю (коллизии)
        tile_x = self.rect.centerx // TILE_SIZE
        tile_y = self.rect.bottom // TILE_SIZE

        if tile_y < world.height:
            tile_id = world.map[tile_y][tile_x]
            if tile_id in (1, 2):  # песок
                self.rect.bottom = tile_y * TILE_SIZE
                self.vel_y = 0
                self.on_ground = True
            else:
                self.on_ground = False


        if self.x >= SCREEN_WIDTH and self.y >= SCREEN_HEIGHT:
            self.x = 0
            self.y = 0
            self.rect.x = 0


        if tile_y < self.world.height and tile_x < world.width:
            tile_id = self.world.map[tile_y][tile_x]
            if tile_id in (1, 2):  # если есть песок
                self.rect.bottom = tile_y * TILE_SIZE
                self.vel_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
        #print(self.x, self.y)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_d]:
            self.vel_x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False



    def check_collision(self, world, dx, dy):
        for y in range(world.height):
            for x in range(world.width):
                tile_x = self.world.width // 2  # теперь ВСЕГДА в пределах карты
                tile_y = self.rect.bottom // TILE_SIZE

                tile_id = world.map[y][x]
                if self.world.map[y][tile_x] != 0:  # 1 или 2 = песокif self.world.map[y][tile_x] != 0:  # 1 или 2 = песок
                    self.rect.x = tile_x * TILE_SIZE
                    self.rect.bottom = y * TILE_SIZE
                    break
                if tile_y < self.world.height:
                    tile_id = self.world.map[tile_y][tile_x]

                    if tile_id != 0:  # НЕ воздух
                        self.rect.bottom = tile_y * TILE_SIZE
                        self.velocity_y = 0
                        self.on_ground = True
                    else:
                        self.on_ground = False

    def draw(self, screen):
        screen.blit(self.image,  self.rect)