import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, world_width, world_height):
        # self.offset — это прямоугольник, который хранит сдвиг всего мира.
        # Мы используем только его координаты x и y.
        self.offset = pygame.Rect(0, 0, world_width, world_height)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, target):
        """
        Принимает Rect или объект со свойством .rect.
        Возвращает новый Rect, сдвинутый на позицию камеры.
        Именно этот результат нужно передавать в screen.blit()
        """
        if isinstance(target, pygame.Rect):
            return target.move(self.offset.topleft)
        return target.rect.move(self.offset.topleft)

    def update(self, target_rect):
        # Используем 160 (размер virtual_surface), а не SCREEN_WIDTH
        x = -target_rect.centerx + (160 // 2)
        y = -target_rect.centery + (160 // 2)

        x = min(0, x)

        y = min(0, y)

        x = max(-(self.world_width - 160), x)

        y = max(-(self.world_height - 160), y)

        self.offset.topleft = (x, y)