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

        self.world = World()
        self.player = Player(self.world)

        self.virtual_surface = pygame.Surface((160, 160))
        self.camera = Camera(self.world.width * TILE_SIZE, self.world.height * TILE_SIZE)

        # 1. Загрузка фона
        self.bg_image = pygame.image.load("assets/tiles/nbg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (160, 160))

        # 2. Настройка Храма
        self.shrine_img = pygame.image.load("assets/tiles/shrine.png").convert_alpha()

        # ВАЖНО: Масштабируем картинку ровно под размер дырки в world.py (10 тайлов в ширину, 6 в высоту)
        shrine_w = TILE_SIZE * 6
        shrine_h = TILE_SIZE * 6
        self.shrine_img = pygame.transform.scale(self.shrine_img, (shrine_w, shrine_h))

        # СИНХРОНИЗАЦИЯ КООРДИНАТ
        sh_tx = self.world.width // 2 - 5
        sh_ty = (self.world.height // 2) + 5

        # Создаем ОДИН Rect с правильными координатами и размером
        self.shrine_rect = pygame.Rect(sh_tx * TILE_SIZE, sh_ty * TILE_SIZE, shrine_w, shrine_h)

        # 3. Спавн игрока (берем готовую точку из world.py)
        self.player.rect.x = self.world.spawn_pos[0]
        self.player.rect.y = self.world.spawn_pos[1]
        self.player.vel_y = 0

        # Сразу наводим камеру на игрока
        self.camera.update(self.player.rect)

        # Инициализируем шрифты
        pygame.font.init()
        self.messages = [
            (0, "Древний Храм пробудился..."),  # Появится сразу (0 сек)
            (7000, "Ты — последнее выжившее насекомое."),  # Через 7 секунд
            (16000, "Найди мутации но пока что просто освой управление .")  # Через 16 секунд (7 + 9)
        ]

        self.current_msg_index = 0
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.text_surface = self.font.render(self.messages[0][1], True, (255, 255, 255))

        self.text_world_x = self.world.width * TILE_SIZE // 2
        self.text_world_y = (self.world.height // 2 + 8) * TILE_SIZE  # Чуть выше Храма

    def run(self):
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # --- 1. ЛОГИКА ---
                self.player.update(self.world)
                self.camera.update(self.player.rect)

                # --- 2. ЛОГИКА ТАЙМЕРА ТЕКСТА ---
                current_time = pygame.time.get_ticks()
                if self.current_msg_index < len(self.messages) - 1:
                    next_msg_time = self.messages[self.current_msg_index + 1][0]
                    if current_time >= next_msg_time:
                        self.current_msg_index += 1
                        # Берем СТРОКУ из списка (теперь в сообщениях должна быть просто строка, не список!)
                        new_text = self.messages[self.current_msg_index][1]
                        self.text_surface = self.font.render(new_text, True, (255, 255, 255))

                # --- 3. ОТРИСОВКА (Мир) ---
                self.virtual_surface.blit(self.bg_image, (0, 0))
                self.world.draw(self.virtual_surface, self.camera, self.player)
                self.virtual_surface.blit(self.shrine_img, self.camera.apply(self.shrine_rect))
                self.virtual_surface.blit(self.player.image, self.camera.apply(self.player.rect))

                # --- 4. МАСШТАБИРОВАНИЕ ---
                scaled = pygame.transform.scale(self.virtual_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(scaled, (0, 0))

                # --- 5. ТЕКСТ (Тот самый простой вариант) ---
                text_x = (SCREEN_WIDTH // 2) - (self.text_surface.get_width() // 2)
                self.screen.blit(self.text_surface, (text_x, 50))

                pygame.display.flip()
                self.clock.tick(60)
        finally:
            pygame.quit()