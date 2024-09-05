import pygame
import time
import random
import math

class Consumer(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        self.hunger = 100
        self.age = 0
        self.reproductive_urge = 0
        self.last_reproduce_time = time.time()
        self.last_hunger_time = time.time()
        self.last_move_time = time.time()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.base_speed = 2  # Base speed value
        self.speed = self.base_speed
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def update(self, producers, all_consumers):
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
        if self.age > 300 or self.hunger <= 0:  # 5 minutes = 300 seconds or starved
            self.kill()

          # Movement logic
        #self.adjust_speed_based_on_hunger()
        self.move_towards_producer(producers)  # Move towards producers if any nearby
        self.random_move()
        self.apply_periodic_boundary()

        # Check distance to producers and move towards them if within 100 pixels
        for producer in producers:
            if self.rect.colliderect(producer.rect.inflate(100, 100)):
                self.move_towards_producer(producers)
                if self.rect.colliderect(producer.rect):
                    self.compete_for_producer(producer, all_consumers)
        
        # Check collision with producers
        collided_producers = pygame.sprite.spritecollide(self, producers, True)
        for producer in collided_producers:
            self.eat_producer()

    #def adjust_speed_based_on_hunger(self):
    #    # Speed increases as hunger decreases
    #    hunger_percentage = self.hunger / 100  # Assuming hunger is a value from 0 to 100
    #    self.speed = self.base_speed * (2 - hunger_percentage)  # Adjust multiplier for desired effect

    
    def apply_periodic_boundary(self):
        # Wrap the Consumer around if it moves out of screen boundaries
        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.screen_height
        elif self.rect.top > self.screen_height:
            self.rect.bottom = 0

    def random_move(self):
        # Introduce random changes in direction
        if random.random() < 0.05:  # 5% chance to change direction each frame
            self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

        # Normalize the direction vector and apply speed
        if self.direction.length() > 0:
            self.direction = self.direction.normalize() * self.speed

        # Update position
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        # Reverse direction if hitting boundaries
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.direction.y *= -1

    def move_towards_producer(self, producers):
        # Check distance to producers and move towards them
        closest_producer = None
        min_distance = float('inf')

        for producer in producers:
            distance = math.hypot(producer.rect.centerx - self.rect.centerx, producer.rect.centery - self.rect.centery)
            if distance < min_distance:
                min_distance = distance
                closest_producer = producer

        if closest_producer and min_distance < 200:  # Only move towards producers within a certain distance
            # Calculate direction towards the producer
            dx = closest_producer.rect.centerx - self.rect.centerx
            dy = closest_producer.rect.centery - self.rect.centery

            if min_distance > 0:
                dx /= min_distance
                dy /= min_distance

                self.rect.x += dx * (self.speed + 2)  # Increase speed by 2 when moving towards a producer
                self.rect.y += dy * (self.speed + 2)

            # Eat the producer if collided
            if self.rect.colliderect(closest_producer.rect):
                closest_producer.kill()
                self.eat_producer()
    
    def eat_producer(self):
        # Eat the producer and increase hunger
        self.hunger += 20  # Adjust as needed

    def compete_for_producer(self, producer, all_consumers):
        # Find the closest competing consumer
        for other in all_consumers:
            if other != self and self.rect.colliderect(other.rect.inflate(50, 50)):
                # Simulate a fight: the consumer with higher hunger wins
                if self.hunger > other.hunger:
                    other.kill()  # The other consumer "dies" in the competition
                elif self.hunger < other.hunger:
                    self.kill()   # This consumer "dies" in the competition
                else:
                     # 50/50 chance if both have the same hunger level
                    if random.choice([True, False]):
                        other.kill()  # Randomly kill the other consumer
                    else:
                        self.kill()   # Randomly kill this consumer

    def look_for_mate(self):
        print("Looking for a mate...")