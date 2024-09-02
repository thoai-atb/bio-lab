import random
import pygame

from events import BOX_DROPPED_EVENT

BOX_SIZE = 50

class Box:
    def __init__(self, screen):
        self.size = BOX_SIZE  # Fixed size for the square
        screen_width, screen_height = screen.get_size()
        # Randomly position the center of the box within the screen boundaries
        center_x = random.randint(self.size // 2, screen_width - self.size // 2)
        center_y = random.randint(self.size // 2, screen_height - self.size // 2)
        self.x = center_x - self.size // 2
        self.y = center_y - self.size // 2
        self.z = screen.get_height()
        self.vz = 0
        self.screen = screen
        self.color = (139, 69, 19)  # Wood color (brown)
        self.border_color = (105, 56, 15)  # Darker shade for the border
        self.opened = False
        self.font = pygame.font.SysFont(None, int(BOX_SIZE * 0.6))  # Adjust size to fit the box

    def get_center(self):
        return self.x + self.size / 2, self.y + self.size / 2

    def update(self):
        if self.z == 0:
            return
        self.vz -= 0.3
        if self.z > 0:
            self.z += self.vz
        if self.z <= 0:
            event = pygame.event.Event(BOX_DROPPED_EVENT)
            pygame.event.post(event)
            self.z = 0

    def draw(self):
        display_y = self.y - self.z

        # Create a surface for the shadow with an alpha channel
        shadow_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Fill the shadow surface with black color and desired alpha (opacity)
        shadow_surface.fill((0, 0, 0, 128))  # 128 is the alpha value for 50% opacity

        # Draw the shadow by blitting the shadow surface onto the main screen
        self.screen.blit(shadow_surface, (self.x, self.y))

        # Draw the box with a border
        pygame.draw.rect(self.screen, self.border_color, (self.x, display_y, self.size, self.size))
        pygame.draw.rect(self.screen, self.color, (self.x + 5, display_y + 5, self.size - 10, self.size - 10))

        # Set up the font and draw a question mark
        question_mark = self.font.render("?", True, (255, 255, 255))  # White color for the question mark

        # Calculate position to center the question mark
        text_rect = question_mark.get_rect(center=(self.x + self.size // 2, display_y + self.size // 2))

        # Draw the question mark onto the screen
        self.screen.blit(question_mark, text_rect)

    def check_collision(self, creature):
        # Don't check if it is hovering
        if self.z > 0: return

        # Find the closest point on the rectangle to the creature's center
        closest_x = max(self.x, min(creature.x, self.x + self.size))
        closest_y = max(self.y, min(creature.y, self.y + self.size))

        # Calculate the distance between the closest point and the creature's center
        distance_x = creature.x - closest_x
        distance_y = creature.y - closest_y
        distance_squared = distance_x**2 + distance_y**2

        # Check if the distance is less than or equal to the radius squared
        if distance_squared <= creature.size**2:
            self.opened = True
            creature.die()
