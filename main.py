import math
import random
import pygame
import sys

from creature import Creature, check_collision, handle_collision
from presets import *
from splash import Splash

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound effect
soundfxs = {
    "pop": pygame.mixer.Sound('sfx/pop.wav'),
    "crush": pygame.mixer.Sound('sfx/crush.wav'),
    "crush_big": pygame.mixer.Sound('sfx/crush_big.wav'),
    "crush_huge": pygame.mixer.Sound('sfx/crush_huge.wav'),
}
soundfxs["pop"].set_volume(0.8)

NUM_CREATURES = 200
BACKGROUND_COLOR = (110, 100, 50)
CREATURES_PER_EGG = 10
HATCH_SIZE = 10

# Initialize Pygame
pygame.init()

# Get the display info
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Create a fullscreen window
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Create a canvas buffer
buffer = pygame.Surface((width, height))
buffer.fill(BACKGROUND_COLOR)  # Fill the buffer with a gray background

# Create a clock object to manage frame rate
clock = pygame.time.Clock()

creatures = preset_random(num_creatures=NUM_CREATURES, screen=screen)
# creatures = preset_one_vs_one(num_creatures=NUM_CREATURES, screen=screen)
creatures = preset_hurdles(4, 60, screen)
eggs = []
splashes = []

def system_update():
    # Update creatures
    for i, creature in enumerate(creatures):
        creature.think_and_crawl()
        creature.update()
        creature.wipe(buffer=buffer, color=BACKGROUND_COLOR)
        # Check for collisions with other creatures
        for j in range(i + 1, len(creatures)):
            if check_collision(creature, creatures[j]):
                handle_collision(creature, creatures[j])
        if creature.egg_laid is not None:
            eggs.append(creature.egg_laid)
            creature.egg_laid = None
    # Resolve dead creatures
    for creature in creatures:
        if creature.dead:
            if creature.size < 15:
                soundfxs["crush"].play()
            elif creature.size < 25:
                soundfxs["crush_big"].play()
            else:
                soundfxs["crush_huge"].play()
            splashes.append(Splash(creature.x, creature.y, creature.color, creature.size, screen))
            pass
    creatures[:] = [creature for creature in creatures if not creature.dead]

    # Update eggs
    for egg in eggs:
        egg.update()
        if egg.hatched:
            # Hatched
            soundfxs["pop"].play()
            for _ in range(CREATURES_PER_EGG):
                new_creature = Creature(egg.x, egg.y, HATCH_SIZE, screen, egg.type)
                new_creature.random_crawl()
                creatures.append(new_creature)
    eggs[:] = [egg for egg in eggs if not egg.hatched]

    # Update splashes
    for splash in splashes:
        splash.update()
        if splash.ended():
            splash.display(buffer)
    splashes[:] = [s for s in splashes if not s.ended()]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if a key is pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:  # Escape key
            pygame.quit()
            sys.exit()

    system_update()

    # Fill the background with white
    screen.blit(buffer, (0, 0))  # Draw the buffer onto the screen

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Display
    for splash in splashes:
        splash.display()
    for egg in eggs:
        egg.display()
    for creature in creatures:
        creature.display()

    # Update the display
    pygame.display.flip()
    # Limit the frame rate to 60 FPS
    dt = clock.tick(100) / 1000  # Time in seconds since the last frame
    # Calculate and print FPS
    fps = clock.get_fps()
    # print(f"FPS: {fps:.2f}")
