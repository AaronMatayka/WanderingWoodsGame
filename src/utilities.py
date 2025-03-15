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
