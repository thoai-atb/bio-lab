import pygame
import sys

from box import Box
from creature import Creature, check_collision, handle_collision
from events import BOX_DROPPED_EVENT
from presets import *
from splash import Splash
from color import *

CREATURES_PER_EGG = 10
HATCH_SIZE = 10

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize Pygame
pygame.init()

# Get the display info
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Load sound effect
soundfxs = {
    "pop": pygame.mixer.Sound('sfx/pop.wav'),
    "crack": pygame.mixer.Sound('sfx/crack.wav'),
    "crush": pygame.mixer.Sound('sfx/crush.wav'),
    "crush_big": pygame.mixer.Sound('sfx/crush_big.wav'),
    "crush_huge": pygame.mixer.Sound('sfx/crush_huge.wav'),
    "drop": pygame.mixer.Sound('sfx/drop.wav'),
}
soundfxs["pop"].set_volume(0.8)

# Load the texture
bg_texture = pygame.image.load('texture/argyle.png')

# Create a fullscreen window
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Background
background = pygame.Surface((width, height))
background.fill(BACKGROUND_COLOR)
tile_texture(background, bg_texture)

# Create a canvas buffer
buffer = pygame.Surface((width, height), pygame.SRCALPHA)

# Create a clock object to manage frame rate
clock = pygame.time.Clock()

# Simulation objects
creatures = preset_herds(screen, num_herds=8, herd_size=30)
eggs = []
splashes = []
boxes = [Box(screen)]

def system_update():
    # Update creatures
    for i, creature in enumerate(creatures):
        creature.think_and_crawl()
        creature.update()
        creature.wipe(buffer=buffer, color=(0,0, 0, 0))
        # Check for collisions with other creatures
        for j in range(i + 1, len(creatures)):
            if check_collision(creature, creatures[j]):
                handle_collision(creature, creatures[j])
        if creature.egg_laid is not None:
            eggs.append(creature.egg_laid)
            creature.egg_laid = None
        # Resolve dead creatures
        if creature.dead:
            if creature.size < 15:
                soundfxs["crush"].play()
            elif creature.size < 25:
                soundfxs["crush_big"].play()
            else:
                soundfxs["crush_huge"].play()
            splashes.append(Splash(creature.x, creature.y, creature.color, creature.size, screen))
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

    # Update boxes
    for box in boxes:
        box.update()
        for c in creatures:
            box.check_collision(c)
        if box.opened:
            # Cracked
            soundfxs["crack"].play()
            type = random_type()
            for _ in range(10):
                x, y = box.get_center()
                new_creature = Creature(x, y, HATCH_SIZE, screen, type)
                new_creature.random_crawl()
                creatures.append(new_creature)
    boxes[:] = [b for b in boxes if not b.opened]
    if len(boxes) == 0:
        boxes.append(Box(screen))

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

        # Handle mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                boxes.append(Box(screen))

        # Box dropped
        if event.type == BOX_DROPPED_EVENT:
            soundfxs["drop"].play()

    # UPDATE OBJECTS
    system_update()

    # Fill the background
    screen.blit(background, (0, 0))  # Draw the buffer onto the screen
    screen.blit(buffer, (0, 0))  # Draw the buffer onto the screen

    # Display
    for splash in splashes:
        splash.display()
    for egg in eggs:
        egg.display()
    for creature in creatures:
        creature.display()

    # Draw the box
    for box in boxes:
        box.draw()

    # UI display
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for creature in creatures:
        if creature.contains(mouse_x, mouse_y):
            creature.draw_info_above()

    # Update the display
    pygame.display.flip()
    # Limit the frame rate to 60 FPS
    dt = clock.tick(100) / 1000  # Time in seconds since the last frame
    fps = clock.get_fps()
    # print(f"FPS: {fps:.2f}")
