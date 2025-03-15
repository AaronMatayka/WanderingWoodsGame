from game_utilities import *
import time
import random

class IntermediateSimulation:
    """Runs the 3-5 version of Wandering in the Woods."""

    def __init__(self):
        self.grid_size_y = int(input("Please enter the grid height: "))
        self.grid_size_x = int(input("Please enter the grid width: "))
        self.grid = make_grid(self.grid_size_y, self.grid_size_x)

        self.player_count = int(input("Please enter the number of players: "))
        self.players = place_players_with_input(self.grid, self.player_count)
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
        for player in self.players.get_players():
            print(f"📍 Player {player.number} moved {self.move_counts[player.number]} times.")

    def wait_for_restart(self):
        """Pauses until the user presses Enter before restarting the game."""
        input("\nPress Enter to restart the game...")
        self.reset_game()

    def reset_game(self):
        """Resets the game by re-initializing the grid and players."""
        print("\n🔄 Resetting the game...\n")
        self.grid = make_grid(self.grid_size_y, self.grid_size_x)
        self.players = place_players_with_input(self.grid, self.player_count)
        self.move_counts = {player.number: 0 for player in self.players.get_players()}