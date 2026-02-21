import pygame
from world.world import World
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from entities.player import Player
from camera.camera import Camera


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.virtual_surface = pygame.Surface((160, 160))

        self.world = World()
        self.player = Player()
        self.camera = Camera(self.world.width * TILE_SIZE, self.world.height * TILE_SIZE)

        # Центрирование игрока
        self.player.rect.x = (self.world.width // 2) * TILE_SIZE
        self.player.rect.y = ((self.world.height // 2) + 5) * TILE_SIZE

        # Ассеты
        try:
            self.sky_image = pygame.transform.scale(pygame.image.load("assets/tiles/c.png").convert(), (160, 160))
            self.inv_icon = pygame.transform.scale(pygame.image.load("assets/tiles/ore.png").convert_alpha(), (40, 40))
            raw_shrine = pygame.image.load("assets/tiles/shrine.png").convert_alpha()
            self.shrine_img = pygame.transform.scale(raw_shrine, (TILE_SIZE * 6, TILE_SIZE * 6))
            raw_cave = pygame.image.load("assets/tiles/caveb.png").convert_alpha()
            self.cave_bg_image = pygame.transform.scale(raw_cave, (4 * TILE_SIZE, 3 * TILE_SIZE))
        except:
            self.inv_icon = pygame.Surface((40, 40));
            self.inv_icon.fill((255, 215, 0))

        self.shrine_rect = pygame.Rect((self.world.width // 2 - 3) * 15.3, ((self.world.height // 2) + 5) * TILE_SIZE,
                                       TILE_SIZE * 6, TILE_SIZE * 6)

        # Шрифты и сообщения
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.messages = [(0, "Древний Храм пробудился..."), (7000, "Ты — Кротазавр. Слабый, но с козырями."),
                         (14000, "Найди мутации, чтобы выжить.")]
        self.current_msg_index = 0
        self.msg_text = self.messages[0][1]
        self.last_msg_time = pygame.time.get_ticks()

    def run(self):
        while True:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    res = self.player.interact(self.world)
                    if res:
                        self.msg_text = res
                        self.last_msg_time = now

            # Таймер сообщений
            if self.current_msg_index < len(self.messages) - 1:
                if now >= self.messages[self.current_msg_index + 1][0]:
                    self.current_msg_index += 1
                    self.msg_text = self.messages[self.current_msg_index][1]
                    self.last_msg_time = now

            # Очистка через 10 сек (если не процесс копания)
            if self.msg_text and "ПРОЦЕСС" not in self.msg_text and now - self.last_msg_time > 10000:
                self.msg_text = ""

            # Копание
            keys = pygame.key.get_pressed()
            if any([keys[pygame.K_e], keys[pygame.K_q], keys[pygame.K_w], keys[pygame.K_s]]):
                res = self.player.dig(self.world)
                if res:
                    self.msg_text = res
                    self.last_msg_time = now

            self.player.update(self.world)
            self.camera.update(self.player.rect)

            # --- ОТРИСОВКА ---

            # 1. Сначала заполняем всё небом (самый нижний слой)
            for x in range(2):
                for y in range(2):
                    self.virtual_surface.blit(self.sky_image, (x * 160, y * 160))

            # 2. Рисуем ФОН ПЕЩЕРЫ (он будет виден там, где выкопаны блоки)
            # Координаты должны точно совпадать с теми, что в генерации мира
            cx, cy = self.world.width // 2 - 8, (self.world.height // 2) + 15
            # Превращаем координаты тайлов в пиксели
            c_rect = pygame.Rect(cx * TILE_SIZE, cy * TILE_SIZE, 4 * TILE_SIZE, 3 * TILE_SIZE)

            # Рисуем caveb.png поверх неба, но ПОД блоками мира
            self.virtual_surface.blit(self.cave_bg_image, self.camera.apply(c_rect))

            # 3. Рисуем МИР (блоки песка, камня и руды)
            # Если в world.map стоит 0, world.draw ничего не нарисует,
            # и мы увидим нашу пещеру или небо.
            self.world.draw(self.virtual_surface, self.camera, self.player)

            # 4. Рисуем ХРАМ и ИГРОКА (самый верхний слой в мире)
            self.virtual_surface.blit(self.shrine_img, self.camera.apply(self.shrine_rect))
            self.virtual_surface.blit(self.player.image, self.camera.apply(self.player.rect))

            # 5. Масштабируем всё это на большой экран
            final_frame = pygame.transform.scale(self.virtual_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(final_frame, (0, 0))

            # HUD: Две строки текста
            if self.msg_text:
                if "?" in self.msg_text:
                    parts = self.msg_text.split("? ")
                    line1 = self.font.render(parts[0] + "?", True, (255, 255, 255))
                    line2 = self.font.render(parts[1], True, (255, 255, 255))
                    self.screen.blit(line1, (SCREEN_WIDTH // 2 - line1.get_width() // 2, 70))
                    self.screen.blit(line2, (SCREEN_WIDTH // 2 - line2.get_width() // 2, 105))
                else:
                    m_r = self.font.render(self.msg_text, True, (255, 255, 255))
                    self.screen.blit(m_r, (SCREEN_WIDTH // 2 - m_r.get_width() // 2, 70))

            # Инвентарь
            slot_rect = pygame.Rect(SCREEN_WIDTH - 90, 20, 70, 70)
            pygame.draw.rect(self.screen, (40, 40, 40), slot_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), slot_rect, 3)
            if self.player.inventory > 0:
                self.screen.blit(self.inv_icon, (SCREEN_WIDTH - 75, 30))
                c_t = self.small_font.render(str(self.player.inventory), True, (255, 215, 0))
                self.screen.blit(c_t, (SCREEN_WIDTH - 40, 65))

            pygame.display.flip()
            self.clock.tick(60)