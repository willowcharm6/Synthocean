import pygame
import random

class Producer(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 780)
        self.rect.y = random.randint(0, 580)
