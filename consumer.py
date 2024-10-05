import pygame
import time
import random
import math

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

        # Movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 2  # Speed of the consumer
        self.last_direction_change_time = time.time()  # Track time for direction change

    def update(self, producers):
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

        # Move the consumer
        self.move()

        # Check distance to producers and move towards them if within 8 pixels
        for producer in producers:
            if self.rect.colliderect(producer.rect.inflate(8, 8)):
                self.move_towards(producer)
                if self.rect.colliderect(producer.rect):
                    producer.kill()

    def move(self):
        current_time = time.time()
        
        # Change direction every 4 seconds
        if current_time - self.last_direction_change_time > 4 or self.direction.length() == 0:
            self.direction.x = random.choice([-1, 1])
            self.direction.y = random.choice([-1, 1])
            self.last_direction_change_time = current_time

        # Check if the direction vector is non-zero before normalizing
        if self.direction.length() > 0:
            self.direction = self.direction.normalize() * self.speed

        # Update position
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        # Screen boundaries check
        if self.rect.left < 0 or self.rect.right > 800:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > 600:
            self.direction.y *= -1


    def move_towards(self, producer):
        # Calculate direction towards the producer
        dx = producer.rect.centerx - self.rect.centerx
        dy = producer.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def look_for_mate(self):
        print("Looking for a mate...")
