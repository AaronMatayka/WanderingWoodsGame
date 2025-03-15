from SimulationBase import SimulationBase
from game_utilities import *
import time
import random

class BasicSimulation(SimulationBase):
    """Runs the K-2 version of Wandering in the Woods."""

    def __init__(self, grid_size=2):
        """
        Initializes the simulation with a 2x2 grid and two players.
        """
        self.grid_size_y = grid_size
        self.grid_size_x = grid_size
        super().__init__(self.grid_size_y, self.grid_size_x, player_count=2)

    def place_players(self):
        """Places two players at opposite corners of the grid (K-2 version)."""
        players_object = place_players(self.grid, player_count=2)
        return players_object
