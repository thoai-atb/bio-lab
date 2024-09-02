
import math
import random
from creature import PALLETTE, Creature

STARTING_SIZE = 10

def preset_random(num_creatures, screen):
    size = STARTING_SIZE
    creatures = []
    for _ in range(num_creatures):
        x = random.randint(size, screen.get_width() - size)  # X-coordinate
        y = random.randint(size, screen.get_height() - size)  # Y-coordinate
        creature = Creature(x, y, size, screen)
        creatures.append(creature)
    return creatures

def preset_one_vs_one(num_creatures, screen):
    size = STARTING_SIZE
    random_type_a = random.choice(list(PALLETTE.keys()))
    random_type_b = random.choice(list(PALLETTE.keys()))
    creatures = []
    for _ in range(num_creatures):
        x = random.randint(size, screen.get_width() - size)  # X-coordinate
        y = random.randint(size, screen.get_height() - size)  # Y-coordinate
        creature = Creature(x, y, size, screen)
        if creature.x < screen.get_width() / 2:
            creature.change_type(random_type_a)
        else:
            creature.change_type(random_type_b)
        creatures.append(creature)
    return creatures

def preset_hurdles(screen, num_hurdles=8, hurdle_size=60):
    size = STARTING_SIZE
    creatures = []
    remaining_types = list(PALLETTE.keys())

    def distribute_points_evenly():
        points = []
        # Calculate horizontal and vertical spacing
        horizontal_spacing = screen.get_width() // (num_hurdles / 2)
        vertical_spacing = screen.get_height() // 2
        # Generate 6 points
        for i in range(num_hurdles // 2):
            for j in range(2):
                x = (i + 0.5) * horizontal_spacing
                y = (j + 0.5) * vertical_spacing
                points.append((int(x), int(y)))
        return points
    points = distribute_points_evenly()

    for i in range(num_hurdles):
        # Select a random point on the screen
        point_x = points[i][0]
        point_y = points[i][1]
        
        # Select a random type for this group of creatures
        group_type = random.choice(remaining_types)
        remaining_types.remove(group_type)
        
        # Create m creatures nearby the selected point with the same type
        for _ in range(hurdle_size):
            # Generate a random angle and distance within a small radius
            radius = 100  # Define the radius within which creatures are placed
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)
            
            # Calculate the new position
            x = point_x + int(distance * math.cos(angle))
            y = point_y + int(distance * math.sin(angle))
            
            # Ensure the creature stays within the screen bounds
            x = max(size, min(x, screen.get_width() - size))
            y = max(size, min(y, screen.get_height() - size))
            
            # Create a new creature at the calculated position
            creature = Creature(x, y, size, screen)
            
            # Assign the selected group type to the creature
            creature.change_type(group_type)
            
            creatures.append(creature)
    
    return creatures
