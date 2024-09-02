import pygame
import random
import math

from egg import Egg
from color import PALLETTE

CREATURE_FRICTION = 0.99
CREATURE_IMPULSE = 1
CREATURE_CRAWL_PROB = 0.005
CREATURE_LAY_EGGS_PROB = 0.002
CREATURE_LAY_EGGS_SIZE = 20

class Creature:
    def __init__(self, x, y, size, screen, type=None):
        if type == None: type = random.choice(list(PALLETTE.keys()))
        self.x = x
        self.y = y
        self.type = type
        self.vx = 0
        self.vy = 0
        self.screen = screen
        self.size = size  # Size of the creature
        self.color = PALLETTE[self.type]
        self.length = 10
        self.history = []
        self.impulse = CREATURE_IMPULSE
        self.dead = False
        self.level = 1
        self.egg_laid = None
        self.selected = False

    def change_type(self, type):
        self.type = type
        self.color = PALLETTE[self.type]

    def die(self):
        self.dead = True

    def upgrade(self):
        self.level = max(10, self.level + 1)
        self.impulse = (self.level / 10) * 3 * CREATURE_IMPULSE
        self.size += 1

    def crawl(self, dx, dy):
        """Apply impulse to the creature."""
        if self.dead:
            return
        self.vx += dx
        self.vy += dy

    def random_crawl(self):
        distance = self.impulse # Fixed distance
        angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)
        self.crawl(dx, dy)

    def update(self, friction=CREATURE_FRICTION):
        # Apply friction to velocity
        self.vx *= friction
        self.vy *= friction
        # Update position
        self.history.append((self.x, self.y))
        if len(self.history) > self.length:
            self.history = self.history[-self.length:]
        self.x += self.vx
        self.y += self.vy
        # Apply boundary checks
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        # Check horizontal boundaries
        if self.x < self.size:
            self.x = self.size
            self.vx = -self.vx  # Reverse direction
        elif self.x > screen_width - self.size:
            self.x = screen_width - self.size
            self.vx = -self.vx  # Reverse direction
        # Check vertical boundaries
        if self.y < self.size:
            self.y = self.size
            self.vy = -self.vy  # Reverse direction
        elif self.y > screen_height - self.size:
            self.y = screen_height - self.size
            self.vy = -self.vy  # Reverse direction
        if self.size >= CREATURE_LAY_EGGS_SIZE:
            if random.random() < CREATURE_LAY_EGGS_PROB:
                self.egg_laid = Egg(self.x, self.y, self.type, screen=self.screen)

    def think_and_crawl(self):
        """Occasionally makes the creature move by randomly deciding to crawl."""
        if random.random() < CREATURE_CRAWL_PROB:
            self.random_crawl()

    def display(self, buffer=None):
        if buffer == None: buffer = self.screen
        velocity_length = math.sqrt(self.vx ** 2 + self.vy ** 2)
        display_size = max(self.size / 3, self.size / (1 + velocity_length))
        border_color = (0, 0, 0) # (255, 255, 255)
        if not self.dead:
            pygame.draw.circle(buffer, border_color, (self.x, self.y), self.size + 2, 2)
            if len(self.history):
                pygame.draw.circle(buffer, border_color, (self.history[0][0], self.history[0][1]), display_size + 2, 2)
        for i, (x, y) in enumerate(self.history):
            pygame.draw.circle(buffer, self.color, (x, y), display_size)
            if i == len(self.history) - 1:
                pygame.draw.circle(buffer, self.color, (x, y), self.size)

    def draw_info_above(self):
        info_size = 5

        # Define the triangle's size and color
        triangle_size = info_size
        triangle_color = (0, 0, 255)  # Red color for the triangle
        
        # Calculate the points of the triangle
        point1 = (self.x, self.y - self.size - triangle_size)
        point2 = (self.x - triangle_size, self.y - self.size - triangle_size * 2)
        point3 = (self.x + triangle_size, self.y - self.size - triangle_size * 2)
        
        # Draw the triangle
        pygame.draw.polygon(self.screen, triangle_color, [point1, point2, point3])

        # Define the rectangle's size and color
        rect_width = 120
        rect_height = 50
        rect_color = (0, 0, 255)  # Blue color for the rectangle
        text_color = (255, 255, 255)  # White color for the text
        
        # Calculate the position for the rectangle
        rect_x = self.x - rect_width // 2
        rect_y = self.y - self.size - rect_height - 10  # Adjust position above the creature
        
        # Draw the rectangle
        pygame.draw.rect(self.screen, rect_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))
        
        # Prepare and render the text
        font = pygame.font.SysFont(None, 24)
        size_text = font.render(f"Size: {self.size}", True, text_color)
        impulse_text = font.render(f"Impulse: {round(self.impulse, 2)}", True, text_color)
        
        # Draw the text onto the screen
        self.screen.blit(size_text, (rect_x + 10, rect_y + 10))
        self.screen.blit(impulse_text, (rect_x + 10, rect_y + 30))

    def wipe(self, buffer, color):
        pygame.draw.circle(buffer, color, (self.x, self.y), self.size)

    def is_clicked(self, mouse_x, mouse_y):
        # Calculate the distance from the mouse click to the creature's center
        distance = ((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2) ** 0.5
        # If the distance is less than the radius of the creature, it's considered clicked
        return distance <= self.size

    def get_position(self):
        """Return the position as a tuple."""
        return self.x, self.y

    def set_position(self, x, y):
        """Set a new position for the creature."""
        self.x = x
        self.y = y

    def set_size(self, new_size):
        """Set a new size for the creature."""
        self.size = new_size

### INTERACTION ###

def check_collision(creature1, creature2):
    """Check if two creatures collide."""
    dx = creature1.x - creature2.x
    dy = creature1.y - creature2.y
    combined_radius = (creature1.size + creature2.size)
    if abs(dx) > combined_radius or abs(dy) > combined_radius:
        return False
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance < combined_radius

def handle_collision(creature1, creature2):
    """Handle collision between two creatures based on their type."""
    if creature1.dead or creature2.dead:
        return
    if creature1.type == creature2.type:
        # Change velocity if types are the same
        pass
        factor = 1
        creature1.vx *= factor
        creature1.vy *= factor
        creature2.vx *= factor
        creature2.vy *= factor
    else:
        # Mark the creature with lower velocity as dead
        velocity1 = math.sqrt(creature1.vx ** 2 + creature1.vy ** 2)
        velocity2 = math.sqrt(creature2.vx ** 2 + creature2.vy ** 2)
        if velocity1 < velocity2:
            creature1.die()
            creature2.upgrade()
        else:
            creature2.die()
            creature1.upgrade()