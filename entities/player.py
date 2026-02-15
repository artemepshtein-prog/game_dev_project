import pygame
from core.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT



class Player:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
        # Загружаем спрайт
        self.original_image = pygame.image.load("assets/tiles/hero.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Переменная направления (True - вправо, False - влево)
        self.facing_right = True

        self.rect.x = 5 * TILE_SIZE
        self.rect.y = 5 * TILE_SIZE
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


        self.vel_x = 0
        self.vel_y = 0
        self.speed = 2
        self.gravity = 0.8
        self.jump_power = -12
        # self.on_ground = False
        #прочност2
        # 👇 ДОБАВЬ ЭТИ СТРОКИ В КОНЕЦ __init__
        self.tile_health = {}  # Словарь для хранения HP сломанных блоков
        self.max_hp = {1: 10, 2: 20}  # Прочность: ID 1 (10 ударов), ID 2 (20 ударов)
        self.dig_cooldown = 0

    def update(self, world):
        self.handle_input()
        self.dig(world)

        # 1. Движение по X и коллизии со стенами
        self.rect.x += self.vel_x
        self.check_wall_collisions(world, self.vel_x)

        # 2. Движение по Y (Гравитация) и коллизии с полом/потолком
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.check_floor_collisions(world)

        # 3. Границы мира (чтобы не уйти за край)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > world.width * TILE_SIZE:
            self.rect.right = world.width * TILE_SIZE
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > world.height * TILE_SIZE:
            self.rect.bottom = world.height * TILE_SIZE
            self.vel_y = 0
            self.on_ground = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0  # Сбрасываем скорость каждый кадр

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True

        # Обновляем картинку (flip)
        if not self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def check_wall_collisions(self, world, direction):
        # Находим границы игрока в тайлах
        tile_x_left = self.rect.left // TILE_SIZE
        tile_x_right = (self.rect.right - 1) // TILE_SIZE
        tile_y_top = self.rect.top // TILE_SIZE
        tile_y_bottom = (self.rect.bottom - 1) // TILE_SIZE

        # Проверяем все тайлы, которых касается игрок по высоте
        for ty in range(tile_y_top, tile_y_bottom + 1):
            for tx in range(tile_x_left, tile_x_right + 1):
                if 0 <= tx < world.width and 0 <= ty < world.height:
                    if world.map[ty][tx] in (1, 2):  # Если там блок
                        if direction > 0:  # Шли вправо
                            self.rect.right = tx * TILE_SIZE
                        elif direction < 0:  # Шли влево
                            self.rect.left = (tx + 1) * TILE_SIZE

    def check_floor_collisions(self, world):
        tile_x_left = self.rect.left // TILE_SIZE
        tile_x_right = (self.rect.right - 1) // TILE_SIZE
        tile_y_bottom = (self.rect.bottom - 1) // TILE_SIZE
        tile_y_top = self.rect.top // TILE_SIZE

        # Проверяем тайлы под игроком (и над ним для потолка)
        for tx in range(tile_x_left, tile_x_right + 1):
            for ty in range(tile_y_top, tile_y_bottom + 1):
                if 0 <= tx < world.width and 0 <= ty < world.height:
                    if world.map[ty][tx] in (1, 2):
                        if self.vel_y > 0:  # Падаем вниз
                            self.rect.bottom = ty * TILE_SIZE
                            self.vel_y = 0
                            self.on_ground = True
                        elif self.vel_y < 0:  # Бьемся головой
                            self.rect.top = (ty + 1) * TILE_SIZE
                            self.vel_y = 0



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

    def dig(self, world):
            keys = pygame.key.get_pressed()

            if self.dig_cooldown > 0:
                self.dig_cooldown -= 1
                return

            # 1. Сначала определяем, КУДА мы хотим копать
            target_tile = None

            if keys[pygame.K_s]:  # ВНИЗ
                tx = self.rect.centerx // TILE_SIZE
                ty = (self.rect.bottom + 5) // TILE_SIZE  # +5 пикселей вниз от ног
                target_tile = (tx, ty)
            if keys[pygame.K_w]:  # ВВЕРХ
                tx = self.rect.centerx // TILE_SIZE
                ty = (self.rect.top - 5) // TILE_SIZE  # -5 пикселей вверх от головы
                target_tile = (tx, ty)

            if keys[pygame.K_e]:  # ВПРАВО (Проверь, что кнопка именно E)
                tx = (self.rect.right + 5) // TILE_SIZE  # +5 пикселей вправо от края
                ty = self.rect.centery // TILE_SIZE
                target_tile = (tx, ty)

            if keys[pygame.K_q]:  # ВЛЕВО
                tx = (self.rect.left - 5) // TILE_SIZE  # -5 пикселей влево от края
                ty = self.rect.centery // TILE_SIZE
                target_tile = (tx, ty)
                pygame.transform.flip(self.image, True, False)

            # 2. Если кнопка нажата и цель определена
            if target_tile:
                target_x, target_y = target_tile

                # Проверка границ карты
                if 0 <= target_x < world.width and 0 <= target_y < world.height:
                    tile_id = world.map[target_y][target_x]

                    # Тот самый отладочный принт (если его нет, значит мы не тут)
                    print(f"Пытаюсь копать: {target_x}:{target_y}, Блок ID: {tile_id}")

                    if tile_id in (1, 2):
                        pos = (target_x, target_y)

                        if pos not in world.tile_health:
                            world.tile_health[pos] = world.max_hp.get(tile_id, 10)

                        world.tile_health[pos] -= 1
                        self.dig_cooldown = 12

                        if world.tile_health[pos] <= 0:
                            world.map[target_y][target_x] = 0
                            if pos in world.tile_health:
                                del world.tile_health[pos]
                            print("УНИЧТОЖЕНО!")
                    else:
                        print(f"Пытаюсь копать воздух в {target_tile}")

    def draw(self, screen):
        screen.blit(self.image,  self.rect)
#hello