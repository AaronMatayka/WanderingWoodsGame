"""
Player module defining the Person class.

This module contains the Person class, which represents a player or entity
that can move randomly within a grid and form groups with other entities.
"""

import random
import pygame
import universal_variables
import utilities

# Initialize pygame
pygame.init()


class Person:
    """
    A class representing a player or entity that moves within a grid.

    Attributes:
        x (int): The x-coordinate of the entity on the grid.
        y (int): The y-coordinate of the entity on the grid.
        color (tuple): The RGB color of the entity.
        move_count (int): The number of moves the entity has made.
        player_number (int): The unique identifier for the player.
        group (list): A list containing the entity and any group members.
        history (list): A list to track the past visited locations.
    """

    def __init__(self, x, y, color, player_number):
        """
        Initializes a Person instance.

        Args:
            x (int): The starting x-coordinate.
            y (int): The starting y-coordinate.
            color (tuple): The RGB color of the entity.
            player_number (int): The unique player identifier.
        """
        self.x = x  # Set the starting x-coordinate
        self.y = y  # Set the starting y-coordinate
        self.color = color  # Set the color of the entity
        self.move_count = 0  # Initialize move count
        self.player_number = player_number  # Assign the unique player number
        self.group = [self]  # Initially, the group consists only of the entity itself
        self.history = []  # List to track past visited locations
        self.history.append((self.x, self.y))  # Add the initial position to history

    def move(self, grid_width, grid_height):
        """
        Moves the entity randomly within the grid unless it is part of a group.

        If the entity is part of a group, it doesn't move independently.

        Args:
            grid_width (int): The width of the grid.
            grid_height (int): The height of the grid.
        """
        # If the entity is part of a group, it does not move independently
        if len(self.group) > 1:
            return  # Groups move together, no individual movement

        # Randomly choose a direction to move
        direction = random.choice(['up', 'down', 'left', 'right'])

        # Check the boundaries to ensure the entity stays within the grid
        if direction == 'up' and self.y > 0:
            self.y -= 1  # Move up if possible
        elif direction == 'down' and self.y < grid_height - 1:
            self.y += 1  # Move down if possible
        elif direction == 'left' and self.x > 0:
            self.x -= 1  # Move left if possible
        elif direction == 'right' and self.x < grid_width - 1:
            self.x += 1  # Move right if possible

        self.move_count += 1  # Increment the move count after each move

    def draw(self, screen):
        """
        Draws the entity on the screen. If part of a group, it blends the colors.

        The entity is drawn as a circle, and its color is determined by whether it
        is alone or part of a group. If part of a group, the colors are blended.

        Args:
            screen (pygame.Surface): The screen surface to draw the entity on.
        """
        # If the entity is part of a group, blend the colors of all members
        if len(self.group) > 1:
            group_colors = [p.color for p in self.group]  # Gather colors from group members
            color = utilities.blend_colors(group_colors)  # Blend the colors using the utility function
        else:
            color = self.color  # Use the entity's color if not part of a group

        # Draw the entity on the screen as a circle
        pygame.draw.circle(
            screen,
            color,
            (self.x * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2,
             self.y * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2),
            universal_variables.CELL_SIZE // 3  # Size of the circle
        )

    def __str__(self):
        """
        Returns a string representation of the entity's position.

        This method is useful for debugging and logging the entity's current location.

        Returns:
            str: The x and y coordinates as a comma-separated string.
        """
        return str(self.x) + ', ' + str(self.y)  # Return a string of the entity's current position
