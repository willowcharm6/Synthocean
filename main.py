import pygame
from producer import Producer
from consumer import Consumer

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Producer and Consumer Simulation')

# Create groups for consumers and producers
consumers = pygame.sprite.Group()
producers = pygame.sprite.Group()

# Create instances of consumers
for _ in range(10):  # Adjust the number of consumers as needed
    consumer = Consumer(WIDTH, HEIGHT)
    consumers.add(consumer)

# Create instances of producers
for _ in range(100):  # Adjust the number of producers as needed
    producer = Producer(WIDTH, HEIGHT)
    producers.add(producer)

all_sprites = pygame.sprite.Group()
all_sprites.add(consumers)
all_sprites.add(producers)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all consumers and check for fights over producers
    consumers.update(producers, consumers)

    # Draw everything
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()