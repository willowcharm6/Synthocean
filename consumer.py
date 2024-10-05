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
        self.hunger = 10
        self.age = 0
        self.reproductive_urge = 0
        self.last_reproduce_time = time.time()
        self.last_hunger_time = time.time()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.a = 0.4  # Logistic function sharpness, adjust as needed
        self.speed = self.calculate_speed()  # Initial speed based on hunger
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
        self.reproduction_delay = random.uniform(3, 8)  # Each consumer waits 3-8 seconds before trying to reproduce
        self.max_age = random.randint(250, 350)  # Set a random max age for each consumer
        self.velocity_threshold = 0.1  # Set a lower velocity threshold for dying

    def calculate_speed(self):
        """Calculate speed based on hunger."""
        return max(0, 1 / (1 + math.exp(self.a * ((-self.hunger + 10 * self.a) + 1))))  # Ensure non-negative speed

    def update(self, producers, all_consumers):
        current_time = time.time()

        # Check if hunger reaches 0 or below
        if self.hunger <= 0:
            self.kill()  # Kill the consumer if hunger reaches 0
            return  # Exit the method if the consumer is dead

        # Decrease hunger over time
        if current_time - self.last_hunger_time > 5:  # Decrease hunger every 5 seconds
            self.hunger -= 1  # Decrease hunger by 1 unit
            self.last_hunger_time = current_time  # Reset the hunger timer

        # Update age
        self.age += 1 / 60  # Assuming 60 FPS

        # Check for death due to age
        if self.age > self.max_age:  # Compare age with max_age
            self.kill()

        # Check for death due to low velocity
        if self.speed < self.velocity_threshold:  # Check against the velocity threshold
            self.kill()  # Kill the consumer if speed is below the threshold

        # Reproduce if conditions are met
        if self.age > 100 and self.reproductive_urge > 20:  # Example conditions for reproduction
            new_consumer = self.reproduce(all_consumers)  # Pass all_consumers as argument
            if new_consumer:  # Check if a new consumer was created
                return new_consumer  # Return the new consumer object

        # Recalculate speed based on updated hunger
        self.speed = self.calculate_speed()

        # Reproductive urge - Random delay between reproductions
        if current_time - self.last_reproduce_time > self.reproduction_delay:  # Random time for each consumer
            self.reproductive_urge += 1
            self.last_reproduce_time = current_time
            self.reproduction_delay = random.uniform(3, 8)  # Reset random reproduction delay

            # Only allow reproduction if there's enough hunger
            if self.reproductive_urge > 20 and self.hunger > 5:  # Ensure enough hunger for reproduction
                self.reproductive_urge = 0  # Reset urge
                return self.reproduce(all_consumers)  # Return new consumer object

        # Always allow random movement
        self.random_move()

        # Find the closest producer
        closest_producer = None
        min_distance = float('inf')

        for producer in producers:
            distance = math.hypot(producer.rect.centerx - self.rect.centerx, producer.rect.centery - self.rect.centery)
            if distance < min_distance:
                min_distance = distance
                closest_producer = producer

        # If there's a nearby producer, move towards it
        if closest_producer and min_distance < 200:  # Only move towards producers within 200 pixels
            self.move_towards_producer(closest_producer)  # Move towards the closest producer

        # Apply periodic boundary to keep the consumer within screen limits
        self.apply_periodic_boundary()

        # Check collision with producers
        collided_producers = pygame.sprite.spritecollide(self, producers, True)
        for producer in collided_producers:
            self.eat_producer()

    def reproduce(self, all_consumers):
        """Reproduce a new consumer."""
        # Find a nearby consumer to reproduce with
        for other in all_consumers:
            if other != self and self.rect.colliderect(other.rect.inflate(50, 50)):  # Nearby consumers
                # Create a new consumer and add it to the group
                new_consumer = Consumer(self.screen_width, self.screen_height)
                new_consumer.rect.center = self.rect.center  # Position the new consumer at the parent’s location
                all_consumers.add(new_consumer)  # Add the new consumer to the consumers group

                # Reset the reproductive urge
                self.reproductive_urge = 0
                other.reproductive_urge = 0  # Reset for the other consumer as well
                return new_consumer  # Return the newly created consumer

        # Increase the reproductive urge if reproduction doesn't happen
        self.reproductive_urge += 1  # Increase urge over time
        return None  # Return None if no reproduction occurred

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

    def move_towards_producer(self, producer):
        # Calculate the distance to the producer
        distance = math.hypot(producer.rect.centerx - self.rect.centerx, producer.rect.centery - self.rect.centery)

        if distance < 200:  # Only move towards producers within a certain distance
            # Calculate direction towards the producer
            dx = producer.rect.centerx - self.rect.centerx
            dy = producer.rect.centery - self.rect.centery

            if distance > 0:
                dx /= distance
                dy /= distance

                # Move at the current speed without increasing it
                self.rect.x += dx * self.speed  # Maintain current speed
                self.rect.y += dy * self.speed  # Maintain current speed

            # Eat the producer if collided
            if self.rect.colliderect(producer.rect):
                producer.kill()
                self.eat_producer()

    def eat_producer(self):
        # Eat the producer and increase hunger
        self.hunger += 2  # Adjust as needed

    def compete_for_producer(self, producer, all_consumers):
        # Find the closest competing consumer
        for other in all_consumers:
            if other != self and self.rect.colliderect(other.rect.inflate(50, 50)):
                # Simulate a fight: the consumer with higher hunger wins
                if self.hunger > other.hunger:
                    other.kill()  # The other consumer "dies" in the competition
                elif self.hunger < other.hunger:
                    self.kill()  # This consumer "dies" in the competition
                else:
                    # 50/50 chance if both have the same hunger level
                    if random.choice([True, False]):
                        other.kill()  # Randomly kill the other consumer
                    else:
                        self.kill()  # Randomly kill this consumer
