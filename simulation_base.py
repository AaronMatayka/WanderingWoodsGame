# -----------------------------------------------------------------------------
# Authors: Andrew Matayka & Aaron Matayka
# Emails: mataykaandrew@gmail.com & aaronjmatayka@gmail.com
# Class: Software Engineering
# Date: 2025-03-14
#
# File Name: simulation_base.py
# External Files: player_objects.py TODO:
# Imports Used:
#   - None
#
# Description:
#   This file defines the basic functions used in all simulation classes to implement the simulations, such as run_simulation, reset_game, etc.
# -----------------------------------------------------------------------------
import time
import winsound
from game_utilities import *

class SimulationBase:
    """Base class for running a grid-based simulation."""

    def __init__(self, grid_size_y=None, grid_size_x=None, player_count=None, music_file="music.wav"):
        """
        Initializes the simulation with a grid and players.
        Derived classes should provide specific details for grid size and player count.
        """
        self.grid_size_y = grid_size_y
        self.grid_size_x = grid_size_x
        self.player_count = player_count

        # Initialize the grid
        self.grid = make_grid(self.grid_size_y, self.grid_size_x)

        # Initialize players (this will be handled by the derived class)
        self.players = self.place_players()

        # Initialize movement counts
        self.move_counts = {player.number: 0 for player in self.players.get_players()}

        #Checks for music file, and runs audio if present TODO: Fix to work without music file
        if music_file:
            self.play_background_music(music_file)

    def play_background_music(self, music_file):
        """Plays background music while the simulation is running."""
        winsound.PlaySound(music_file, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def stop_background_music(self):
        """Stops the background music."""
        winsound.PlaySound(None, winsound.SND_PURGE)


    def place_players(self):
        """Placeholder method for placing players in derived classes."""
        raise NotImplementedError("place_players method should be implemented in the derived class.")

    def run_simulation(self):
        """Runs the simulation, moving players randomly until they collide."""
        while True:
            print_grid(self.grid)
            time.sleep(1)  # Pause to simulate movement

            for player in self.players.get_players():  # Assuming this returns a list of players
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

        #TODO: MOVE THIS ENTIRE METHOD TO MAIN, MAKE MAIN LOOP IN MAIN AND ASK USER WHICH MODE TO PLAY. MUST CHANGE BEHAVIOR BASED ON MODE.
        self.grid = make_grid(self.grid_size_y, self.grid_size_x)
        self.players = self.place_players()
        self.move_counts = {player.number: 0 for player in self.players.get_players()}