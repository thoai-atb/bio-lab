BACKGROUND_COLOR = (50, 80, 80)

PALLETTE = {
    "A": (255, 0, 0),        # Red
    "B": (255, 165, 0),      # Orange
    "C": (255, 255, 0),      # Yellow
    "D": (0, 255, 0),        # Lime
    "E": (0, 255, 255),      # Cyan
    "F": (0, 0, 255),        # Blue
    "H": (255, 255, 255),    # White
    "J": (255, 0, 203),      # Magenta
    "K": (0, 10, 10),          # Black
    "L": (120, 100, 80)      # Brown
}

def tile_texture(screen, texture):
    """
    Tile the given texture across the screen while maintaining the original size.

    Args:
        screen (pygame.Surface): The surface on which to draw the tiled texture.
        texture (pygame.Surface): The texture to tile across the screen.
    """
    # Get the dimensions of the screen
    screen_width, screen_height = screen.get_size()

    # Get the dimensions of the texture
    texture_width = texture.get_width()
    texture_height = texture.get_height()

    # Tile the texture across the screen
    for x in range(0, screen_width, texture_width):
        for y in range(0, screen_height, texture_height):
            screen.blit(texture, (x, y))

def darken_color(color, factor=0.5):
    """
    Darken the input color by reducing its brightness.
    
    Args:
        color (tuple): The RGB color as a tuple (R, G, B) with values between 0 and 255.
        factor (float): The factor by which to darken the color (0.0 to 1.0). Default is 0.5.
    
    Returns:
        tuple: The darker RGB color as a tuple (R, G, B).
    """
    # Ensure the factor is within the valid range
    factor = max(0.0, min(factor, 1.0))
    
    r, g, b = color
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    
    return (r, g, b)

def lighten_color(color, factor=0.5):
    """
    Lighten the input color by blending it with white.
    
    Args:
        color (tuple): The RGB color as a tuple (R, G, B) with values between 0 and 255.
        factor (float): The factor by which to lighten the color (0.0 to 1.0). Default is 0.5.
    
    Returns:
        tuple: The lighter RGB color as a tuple (R, G, B).
    """
    # Ensure the factor is within the valid range
    factor = max(0.0, min(factor, 1.0))
    
    r, g, b = color
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    
    # Ensure RGB values are within the valid range (0-255)
    r = min(255, r)
    g = min(255, g)
    b = min(255, b)
    
    return (r, g, b)
