from simulation_base import SimulationBase
from game_utilities import *
import time
import random
class IntermediateSimulation(SimulationBase):
    """Runs the 3-5 version of Wandering in the Woods."""

    def __init__(self):
        """
        Initializes the simulation with user-defined grid size and player count.
        """
        grid_size_y = int(input("Please enter the grid height: "))
        grid_size_x = int(input("Please enter the grid width: "))
        player_count = int(input("Please enter the number of players: "))
        super().__init__(grid_size_y, grid_size_x, player_count)

    def place_players(self):
        """Places players based on user input for positions (3-5 version)."""
        players_object = place_players_with_input(self.grid, self.player_count)
        return players_object
