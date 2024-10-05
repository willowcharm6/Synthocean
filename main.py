import pygame
import random
from producer import Producer
from consumer import Consumer
from fields import Field  # Import the Field class

# Constants
HIGHLIGHT_RADIUS = 100  # Radius to highlight nearby consumers

# Highlight nearby consumers function

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 2000, 2000
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Producer and Consumer Simulation')

# Create groups for consumers, producers, and fields
consumers = pygame.sprite.Group()
producers = pygame.sprite.Group()
fields = pygame.sprite.Group()

# Define carrying capacity for producers
carrying_capacity = 2550  # Set the maximum number of producers allowed

# Create instances of consumers
for _ in range(44):  # Adjust the number of consumers as needed
    consumer = Consumer(WIDTH, HEIGHT)
    consumers.add(consumer)

# Create instances of producers
for _ in range(100):  # Adjust the number of producers as needed
    producer = Producer(WIDTH, HEIGHT)
    producers.add(producer)

# Create instances of fields
for _ in range(44):  # Adjust the number of fields as needed
    field = Field(WIDTH, HEIGHT)
    fields.add(field)

# Add fields and consumers to the all_sprites group
all_sprites = pygame.sprite.Group()
all_sprites.add(consumers)
all_sprites.add(fields)  # Add fields to the all_sprites group

# Main game loop
running = True
clock = pygame.time.Clock()
while running:

    # Update all consumers
    consumers.update(producers, consumers)

    # Update fields to check for producer spawning
    for field in fields:
        field.update(producers, carrying_capacity)  # Pass carrying_capacity to fields

    # Randomly spawn producers across the screen with higher concentration near fields
    if len(producers) < carrying_capacity:  # Only spawn new producers if below carrying capacity
        for _ in range(2):  # Number of additional random producers to spawn
            if random.random() < 0.02:  # Adjust the spawn probability
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                producer = Producer(x, y)
                producers.add(producer)

    # Draw everything
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)  # Draw consumers and fields
    producers.draw(screen)  # Draw producers separately to ensure visibility
    pygame.display.flip()

    if len(consumers) == 0:
        pygame.quit()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
