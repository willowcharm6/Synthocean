import pygame
import time

class Consumer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.hunger = 100
        self.age = 0
        self.reproductive_urge = 0
        self.last_reproduce_time = time.time()
        self.last_hunger_time = time.time()

    def update(self):
        current_time = time.time()

        # Update hunger
        if current_time - self.last_hunger_time > 1:
            self.hunger -= 1
            self.last_hunger_time = current_time

        # Update age
        self.age += 1 / 60  # Assuming 60 FPS

        # Reproductive urge
        if current_time - self.last_reproduce_time > 5:
            self.reproductive_urge += 1
            self.last_reproduce_time = current_time
            if self.reproductive_urge > 20:
                self.reproductive_urge = 0  # Reset urge
                self.look_for_mate()

        # Check for death
        if self.age > 300:  # 5 minutes = 300 seconds
            self.kill()

    def look_for_mate(self):
        print("Looking for a mate...")
