from game_utilities import *
from player_objects import *


# TODO: move test code at bottom to main
# TODO: Make 3 different py files, one for each scenario we have to implement: K-2, 3-5, and 6-8
# TODO: For each scenario, music needs to play during gameplay.
# TODO: For each scenario, when all players are in a group display a graphic and statistics from wandering, and announe them audibly. Game resets.
# TODO: For K-2, implement 2 people in opposite corners, who wander randomly. Count each move for each person. Basically the default scenario for functions.
# TODO: For 3-5, grid size can be set manually, which can now be rectangular. 2, 3 or 4 people, can be placed anywhere. Can play and replay multiple times, and display stats like longest run, shortest, average etc.
# TODO: For 6-8, Students are meant to run experiments to find how average runs vary with different sizes and shapes of grids, will need run-to-run tracking like 3-5. Also need different wandering protocols to use besides random.
# TODO: Change the appearance of two collided players to better represent they are both there, currently just 1 or 2 appears.
# TODO: Implement main to run in a loop for testing multiple times and multiple levels of complexity, needs to run until user ends it.
# TODO: Design document: Needs both specifications and software design, sample document is posted. Can be combined with user's guide.
# TODO: User's guide, simple instructions to tell users how to install and use the program.
# TODO: Finished code needs to be in exe file or binary, click to execute.
# TODO: Demo of code, given 20 minutes to demo our code.

class Main:
    def __init__(self):
        self.test_grid = make_grid(5, 3)
        self.players_list = Players()

    def run(self):
        """
        Run the game simulation, including setting up the grid,
        placing players, and making players move.
        """
        # Setup grid and players
        print("Initial Grid:")
        print_grid(self.test_grid)

        self.players_list = place_players(self.test_grid, 3)
        print("Players placed:")
        print_grid(self.test_grid)

        # Run player movement and print grid after each move
        if self.players_list:
            self.move_players()

    def move_players(self):
        """Move players around the grid and print grid after each move."""
        # Move Player 1 (number 1) around the grid
        self.players_list.get_player(1).move("right", self.test_grid)
        print_grid(self.test_grid)

        self.players_list.get_player(1).move("right", self.test_grid)
        print_grid(self.test_grid)

        self.players_list.get_player(1).move("down", self.test_grid)
        print_grid(self.test_grid)

        # Move Player 2 (number 2) around the grid
        self.players_list.get_player(2).move("left", self.test_grid)
        print_grid(self.test_grid)

        self.players_list.get_player(2).move("left", self.test_grid)
        print_grid(self.test_grid)

        self.players_list.get_player(2).move("up", self.test_grid)
        print_grid(self.test_grid)


if __name__ == "__main__":
    main_program = Main()
    main_program.run()
