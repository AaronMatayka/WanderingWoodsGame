# -----------------------------------------------------------------------------
# Authors: Andrew Matayka & Aaron Matayka
# Emails: mataykaandrew@gmail.com & aaronjmatayka@gmail.com
# Class: Software Engineering
# Date: 2025-03-14
#
# File Name: player_objects.py
# External Files: None
# Imports Used:
#   - random (for random player movements)
#
# Description:
#   This file defines the `Players` and `Player` classes. The `Players` class manages
#   all players in the game, allowing players to be added, retrieved by their number,
#   and iterated over. The `Player` class represents an individual player, with
#   functionality for moving the player in different directions on the grid,
#   updating the grid accordingly.
# -----------------------------------------------------------------------------

import random

class Players:
    """Manages all players in the game."""

    def __init__(self):
        """Initializes the Players class with an empty player list."""
        self.players = []

    def add_player(self, player):
        """Adds a player to the list."""
        self.players.append(player)

    def get_player(self, number):
        """
        Retrieves a player by their number.

        Parameters:
        number (int): The player's number.

        Returns:
        Player: The player with the given number.

        Raises:
        ValueError: If no player with the given number is found.
        """
        for player in self.players:
            if player.number == number:
                return player
        raise ValueError(f"Player {number} not found.")

    def get_players(self):
        """Returns an iterable object (list of all players)."""
        return iter(self.players)

class Player:
    """
    Represents a player in the grid.

    The player has a number and a position on the grid. The player can move in
    different directions, and the grid will update based on the player's new position.

    Attributes:
    number (int): The player's unique number.
    position (tuple): The current (y, x) position of the player on the grid.
    """

    def __init__(self, number, position):
        """
        Initializes a new player with a given number and position.

        Parameters:
        number (int): The unique number assigned to the player.
        position (tuple): The (y, x) position of the player on the grid.
        """
        self.number = number
        self.position = position

    def move(self, direction, grid):
        """
        Moves the player in the specified direction and updates the grid.

        The player can move in one of the following directions: "up", "down", "left", "right".
        If the direction is "random", the player moves in a random direction. The grid will
        be updated with the player's new position, and their old position will be cleared.

        Parameters:
        direction (str): The direction in which to move the player.
                         Can be one of "up", "down", "left", "right", or "random".
        grid (list of list of Cell objects): The grid where the player is located and moved within.

        Returns:
        None
        """
        # If the direction is "random", choose a random direction
        if direction == "random":
            direction = random.choice(["up", "down", "left", "right"])

        # Define possible movement directions as changes in y and x coordinates
        move_actions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        # Get the delta for the movement in y and x directions
        delta_y, delta_x = move_actions.get(direction, (0, 0))

        # Calculate the new position by adding delta to the current position
        new_y = int(self.position[0]) + delta_y
        new_x = int(self.position[1]) + delta_x

        # Ensure the move is within the grid's bounds
        if 0 <= int(new_y) < len(grid) and 0 <= int(new_x) < len(grid[0]):
            # Remove the player's number (as integer) from the old position
            grid[int(self.position[0])][int(self.position[1])].remove_value(self.number)

            # Update the player's position to the new coordinates
            self.position = (int(new_y), int(new_x))

            # If the new cell is empty, just add the player's number
            if not grid[int(new_y)][int(new_x)].values:
                grid[int(new_y)][int(new_x)].add_value(self.number)
            else:
                # If the cell is occupied, append the player's number
                grid[int(new_y)][int(new_x)].add_value(self.number)
