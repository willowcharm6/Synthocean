# hello
# poop
import pygame
from producer import Producer
from consumer import Consumer

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Producer and Consumer Simulation')

# Create instances
producer = Producer()
consumer = Consumer()

all_sprites = pygame.sprite.Group()
all_sprites.add(producer)
all_sprites.add(consumer)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill((255, 255, 255))  # White background
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
