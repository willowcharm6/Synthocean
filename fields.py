import pygame
import random
from producer import Producer  # Import the Producer class

class Field(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)  # Transparent surface
        self.color = (0, 255, 0, 100)  # Semi-transparent green
        pygame.draw.circle(self.image, self.color, (50, 50), 50)  # Draw a circle in the center
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.spawn_probability = 0.01  # Adjust the probability as needed

    def update(self, producers, carrying_capacity):
        # Randomly decide to spawn a new producer if below carrying capacity
        if len(producers) < carrying_capacity and random.random() < self.spawn_probability:
            producer = Producer(self.rect.centerx + random.randint(-10, 10), 
                                self.rect.centery + random.randint(-10, 10))  # Spawn close to the field
            producers.add(producer)  # Add producer to the producers group
