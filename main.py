import pygame
from producer import Producer
from consumer import Consumer

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Producer and Consumer Simulation')

# Create a Consumer instance with screen dimensions
consumer = Consumer(WIDTH, HEIGHT)

# Create a group for producers
producers = pygame.sprite.Group()
for _ in range(20):  # Adjust the number of producers as needed
    producer = Producer()
    producers.add(producer)

all_sprites = pygame.sprite.Group()
all_sprites.add(consumer)
all_sprites.add(producers)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    consumer.update(producers)
    producers.update()  # Assuming Producers have an update method (not necessary if static)

    # Draw everything
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(120)

pygame.quit()
