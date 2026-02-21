import pygame
from core.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/tiles/hero.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 5 * TILE_SIZE
        self.rect.y = 5 * TILE_SIZE
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 2
        self.gravity = 0.8
        self.jump_power = -12
        self.on_ground = False
        self.facing_right = True
        self.inventory = 0
        self.tile_health = {}

    def interact(self, world):
        # Метод для взаимодействия с Храмом
        if self.inventory > 0:
            return "Вы поднесли красный камень к алтарю... Храм начинает дрожать!"
        return "Древний алтарь молчит. Нужно что-то особенное..."

    def update(self, world):
        self.handle_input()
        self.rect.x += self.vel_x
        self.check_collisions(world, self.vel_x, 0)
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.check_collisions(world, 0, self.vel_y)
        self.check_bounds(world)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = -self.speed if keys[pygame.K_a] else (self.speed if keys[pygame.K_d] else 0)
        if keys[pygame.K_a]: self.facing_right = False
        if keys[pygame.K_d]: self.facing_right = True
        self.image = self.original_image if self.facing_right else pygame.transform.flip(self.original_image, True,
                                                                                         False)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def check_collisions(self, world, dx, dy):
        for y in range(self.rect.top // TILE_SIZE, self.rect.bottom // TILE_SIZE + 1):
            for x in range(self.rect.left // TILE_SIZE, self.rect.right // TILE_SIZE + 1):
                if 0 <= x < world.width and 0 <= y < world.height:
                    if world.map[y][x] in (1, 2, 5):
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if self.rect.colliderect(tile_rect):
                            if dx > 0:
                                self.rect.right = tile_rect.left
                            elif dx < 0:
                                self.rect.left = tile_rect.right
                            if dy > 0:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.on_ground = True
                            elif dy < 0:
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0

    def check_bounds(self, world):
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > world.width * TILE_SIZE: self.rect.right = world.width * TILE_SIZE
        if self.rect.bottom > world.height * TILE_SIZE:
            self.rect.bottom = world.height * TILE_SIZE
            self.vel_y = 0
            self.on_ground = True

    def dig(self, world):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            target_x, target_y = self.rect.centerx // TILE_SIZE, (self.rect.top - 5) // TILE_SIZE
        elif keys[pygame.K_s]:
            target_x, target_y = self.rect.centerx // TILE_SIZE, (self.rect.bottom + 5) // TILE_SIZE
        elif keys[pygame.K_e]:
            target_x, target_y = (self.rect.right + 5) // TILE_SIZE, self.rect.centery // TILE_SIZE
        elif keys[pygame.K_q]:
            target_x, target_y = (self.rect.left - 5) // TILE_SIZE, self.rect.centery // TILE_SIZE
        else:
            return None

        if 0 <= target_x < world.width and 0 <= target_y < world.height:
            tile_id = world.map[target_y][target_x]
            pos = (target_x, target_y)
            if tile_id in [1, 2, 5]:
                if pos not in self.tile_health:
                    self.tile_health[pos] = 200.0 if tile_id == 5 else (100.0 if tile_id == 2 else 40.0)

                m_hp = 200.0 if tile_id == 5 else (100.0 if tile_id == 2 else 40.0)
                self.tile_health[pos] -= (0.3 if tile_id == 5 else 0.8)
                prog = int((1 - self.tile_health[pos] / m_hp) * 100)

                if self.tile_health[pos] <= 0:
                    world.map[target_y][target_x] = 0
                    del self.tile_health[pos]
                    if tile_id == 5:
                        self.inventory += 1
                        return "Что это за красный камень? Кажется, им можно что-то активировать..."
                    return "РАЗРУШЕНО!"
                return f"ПРОЦЕСС: {max(0, prog)}%"
        return None