"""
Utilities module containing helper functions.

This module provides utility functions for handling color blending and other
miscellaneous tasks.
"""


def blend_colors(colors):
    """
    Blends a list of RGB colors by averaging their respective components.

    Args:
        colors (list of tuple): A list of RGB color tuples.

    Returns:
        tuple: The blended RGB color as a tuple (r, g, b).
    """
    r = sum(c[0] for c in colors) // len(colors)
    g = sum(c[1] for c in colors) // len(colors)
    b = sum(c[2] for c in colors) // len(colors)
    return r, g, b

def limit_input_value(value, input_field, min, max):
    if not value.strip():  # Check if the input is blank
        return
    elif value.isdigit():
        value = int(value)
        print(input_field.get_title())
        if value < min:
            input_field.set_value(str(min))
        elif value > max:
            input_field.set_value(str(max))
        else:
            input_field.set_value(str(value))
    else:
        input_field.set_value(str(min))  # Set value to 0 if the input is not a valid number