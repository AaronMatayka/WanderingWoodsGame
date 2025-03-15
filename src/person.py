"""
Player module defining the Person class.

This module contains the Person class, which represents a player or entity
that can move randomly within a grid and form groups with other entities.
"""
import random
import pygame

from src import utilities, universal_variables

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
        self.x = x
        self.y = y
        self.color = color
        self.move_count = 0
        self.player_number = player_number
        self.group = [self]  # A list to store group members, initially just the person

    def move(self, grid_width, grid_height):
        """
        Moves the entity randomly within the grid unless it is part of a group.

        Args:
            grid_width (int): The width of the grid.
            grid_height (int): The height of the grid.
        """
        if len(self.group) > 1:
            return  # Groups move together

        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and self.y > 0:
            self.y -= 1
        elif direction == 'down' and self.y < grid_height - 1:
            self.y += 1
        elif direction == 'left' and self.x > 0:
            self.x -= 1
        elif direction == 'right' and self.x < grid_width - 1:
            self.x += 1

        self.move_count += 1

    def draw(self, screen):
        """
        Draws the entity on the screen. If part of a group, blends colors.

        Args:
            screen (pygame.Surface): The screen surface to draw the entity on.
        """
        if len(self.group) > 1:
            group_colors = [p.color for p in self.group]
            color = utilities.blend_colors(group_colors)  # Blend all colors in the group
        else:
            color = self.color

        pygame.draw.circle(screen, color, (self.x * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2,
                                           self.y * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2),
                           universal_variables.CELL_SIZE // 3)

    def __str__(self):
        """
        Returns a string representation of the entity's position.

        Returns:
            str: The x and y coordinates as a comma-separated string.
        """
        return str(self.x) + ', ' + str(self.y)
