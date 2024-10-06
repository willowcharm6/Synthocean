import pygame
import random

class Producer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect(center=(x, y))  # Set the position of the producer
        self.max_age = random.randint(250, 350)  # Vary lifetime between 250 and 350 frames
        self.age = 0  # Current age

    def update(self):
        # Increment age
        self.age += 1 / 60  # Assuming 60 FPS

        # Check for death due to age
        if self.age > self.max_age:
            self.kill()  # Remove the producer from the game
