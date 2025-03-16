"""
Utilities module containing helper functions.

This module provides utility functions for handling color blending and other
miscellaneous tasks such as limiting input values within specified ranges.
"""

def blend_colors(colors):
    """
    Blends a list of RGB colors by averaging their respective components.

    Args:
        colors (list of tuple): A list of RGB color tuples (each tuple is of the form (r, g, b)).

    Returns:
        tuple: The blended RGB color as a tuple (r, g, b), where each component is an average
               of the corresponding components from the input colors.
    """
    # Calculate the average of the red, green, and blue components
    r = sum(c[0] for c in colors) // len(colors)  # Average red value
    g = sum(c[1] for c in colors) // len(colors)  # Average green value
    b = sum(c[2] for c in colors) // len(colors)  # Average blue value

    return r, g, b  # Return the blended color as a tuple


def limit_input_value(value, input_field, min, max):
    """
    Limits the input value to be within a specified range.

    Args:
        value (str): The input value to be validated (should be convertible to an integer).
        input_field (pygame_menu.widgets.TextInput): The input field to set the value.
        min (int): The minimum allowable value.
        max (int): The maximum allowable value.

    This function updates the input field to ensure the value stays within the specified range.
    """
    value = int(value)  # Convert the input to an integer

    # Check if the value is within the valid range, and adjust if necessary
    if value < min:
        input_field.set_value(str(min))  # Set to minimum if the value is too low
    elif value > max:
        input_field.set_value(str(max))  # Set to maximum if the value is too high
    else:
        input_field.set_value(str(value))  # Otherwise, keep the value unchanged


def limit_input_value_selected(input_field, menu, min, max):
    """
    Limits the input value based on the selection in the input field.

    This function specifically handles scenarios where the value is being selected
    (e.g., by using up/down arrows) and ensures it remains within the specified bounds.

    Args:
        input_field (pygame_menu.widgets.TextInput): The input field to get and set the value.
        menu (pygame_menu.Menu): The menu containing the input field.
        min (int): The minimum allowable value.
        max (int): The maximum allowable value.

    This function updates the value in the input field if it exceeds the specified limits.
    """
    value = int(input_field.get_value())  # Convert the current input field value to integer

    # Check if the selected value is within the valid range
    if input_field.get_selected_time() == 0:  # If this is the initial selection
        # Adjust the value if it falls outside the allowed range
        if value < min:
            input_field.set_value(str(min))  # Set to minimum value if it's too low
        elif value > max:
            input_field.set_value(str(max))  # Set to maximum value if it's too high
        else:
            input_field.set_value(str(value))  # Otherwise, retain the current value
