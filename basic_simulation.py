from game_utilities import *
import time
import random

class BasicSimulation:
    """Runs the K-2 version of Wandering in the Woods."""

    def __init__(self, grid_size=2):
        """
        Initializes the simulation with a square grid and two players.

        Parameters:
        grid_size (int): The size of the grid (default is 2x2).
        """
        self.grid_size = grid_size
        self.grid = make_grid(grid_size, grid_size)
        self.players = place_players(self.grid, player_count=2)
        self.move_counts = {player.number: 0 for player in self.players.get_players()}

    def run_simulation(self):
        """Runs the simulation, moving players randomly until they collide."""
        while True:
            print_grid(self.grid)
            time.sleep(1)  # Pause to simulate movement

            for player in self.players.get_players():
                player.move("random", self.grid)
                self.move_counts[player.number] += 1

            if check_collision(self.players):
                self.display_results()
                self.wait_for_restart()

    def display_results(self):
        """Displays results when players collide."""
        print("\n🎉 The players have found each other! 🎉")
        print(f"📍 Player 1 moved {self.move_counts[1]} times.")
        print(f"📍 Player 2 moved {self.move_counts[2]} times.")

    def wait_for_restart(self):
        """Pauses until the user presses Enter before restarting the game."""
        input("\nPress Enter to restart the game...")
        self.reset_game()

    def reset_game(self):
        """Resets the game by re-initializing the grid and players."""
        print("\n🔄 Resetting the game...\n")
        self.grid = make_grid(self.grid_size, self.grid_size)
        self.players = place_players(self.grid, player_count=2)
        self.move_counts = {player.number: 0 for player in self.players.get_players()}
