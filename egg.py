import pygame
from color import PALLETTE

class Egg:
    def __init__(self, x, y, type, screen):
        """
        Initialize the Egg instance.

        Args:
            x (int): X-coordinate of the egg's position.
            y (int): Y-coordinate of the egg's position.
            time_to_hatch (float): Time in seconds before the egg hatches.
            screen (pygame.Surface): The Pygame surface where the egg will be drawn.
        """
        self.x = x
        self.y = y
        self.time_to_hatch = 500
        self.screen = screen
        self.hatched = False
        self.type = type
        self.egg_color = PALLETTE[self.type]
        self.size = 5  # Size of the egg

    def update(self):
        if not self.hatched:
            self.time_to_hatch -= 1
            if self.time_to_hatch == 0:
                self.hatched = True

    def display(self):
        # Draw the main circle
        pygame.draw.circle(self.screen, self.egg_color, (self.x, self.y), self.size)

        # Draw the white border
        border_color = (255, 255, 255)  # White color
        border_width = 2  # Width of the border
        pygame.draw.circle(self.screen, border_color, (self.x, self.y), self.size + border_width, border_width)
