import pygame
import random
import math

from color import darken_color

class Splash:
    def __init__(self, x, y, color, size, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.phase = 0
        self.max_phase = 100
        self.size = size
        self.color = darken_color(color, 0.2)

    def ended(self):
        return self.phase == self.max_phase

    def update(self):
        """Update the phase of the splash effect."""
        if self.phase < self.max_phase:
          self.phase += 1

    def display(self, buffer=None):
        """Draw the splash effect on the screen."""
        if buffer == None:
          buffer = self.screen
        # Draw a circle with increasing size and fading effect
        size = self.size + 30 * smoothstep(self.phase / self.max_phase)  # Example: Increase size as phase progresses
        pygame.draw.circle(buffer, self.color, (self.x, self.y), size)

def smoothstep(x):
    """Smoothly transition input x between 0 and 1."""
    if x < 0:
        return 0
    elif x > 1:
        return 1
    else:
        return x * x * (3 - 2 * x)