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
