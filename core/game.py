import pygame
from world.world import World
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.player import Player
from world.world import World

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Player(self.world)  # 👈 создаём игрока
        


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((135, 206, 235))
            self.world.draw(self.screen)
            self.player.update(self.world)
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()