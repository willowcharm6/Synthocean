import pygame

class Producer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect(center=(x, y))  # Set the position of the producer
