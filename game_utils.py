# Aaron Matayka
# Andrew Matayka
# 03/13/25
# Main Utility File for holding shared functions such as
# generating the grid, moving players, checking meet conditions, displaying statistics, etc

from player import *
from time import *

class Cell:
    """Represents a single cell in the grid that can hold multiple integer values."""
    def __init__(self, *values):
        for value in values:
            if any(type(value) is not int):
                raise ValueError("All values must be integers.")

        self.values = list(values)
        self.add_value(0)

    def add_value(self, value):
        """Adds an integer value to the cell."""
        if type(value) is not int:
            raise ValueError("Only integers can be added.")

        if value != 0 and 0 in self.values:
            self.values.remove(0)  # Remove 0 if adding a non-zero value

        self.values.append(value)

    def remove_value(self, value):
        """Removes an integer value from the cell."""
        if type(value) is not int:
            raise ValueError("Only integers can be removed.")

        if value not in self.values:
            raise ValueError("Value not found in the cell.")

        # If the cell is empty, add zero back
        self.values.remove(value)

        if not self.values:
            self.add_value(0)

    def __repr__(self):
        # Return the values inside square brackets, with values separated by commas
        return f"[{', '.join(map(str, self.values))}]"

def make_grid(x_size=2, y_size=2):
    """
    Creates a grid (list of lists) with specified dimensions.

    Parameters:
    x_size (int): The width of the grid (number of columns). Default is 2.
    y_size (int): The height of the grid (number of rows). Default is 2.

    Returns:
    list: A two-dimensional grid filled with Cell objects.
    """

    if type(x_size) is not int or type(y_size) is not int:
        raise ValueError("x_size and y_size must be integers.")
    if x_size <= 0 or y_size <= 0:
        raise ValueError("x_size and y_size must be positive integers.")

    return [[Cell() for _ in range(x_size)] for _ in range(y_size)]

def print_grid(grid):
    """
    Prints a 2D grid where each cell contains a list of integers.

    The grid is formatted such that each cell's integer values are centered within
    columns, with 3 spaces between each cell. The width of each column is determined
    by the longest string representation of the values in that column.

    Parameters:
    grid (list of list of Cell objects): A 2D list representing the grid, where
                                         each cell is an instance of the Cell class.

    Returns:
    None: The function prints the grid to the console.
    """

    # Find the maximum width needed for each column (based on the length of the string representation)
    col_widths = [max(len(str(row[col])) for row in grid) for col in range(len(grid[0]))]

    for row in grid:
        # Center-align each cell based on its column width
        formatted_row = [f"{str(cell):^{col_widths[col]}}" for col, cell in enumerate(row)]
        # Print the row with 3 spaces between each cell
        print("   ".join(formatted_row))
    print()

# Function used to place players on the grid, defaulting to 2 players and the
# top left and bottom right corner of the grid. Can also input direct positions
# on the grid instead to position each character
def place_players(grid, player_count = 2, positions = None):
    """
    Places players on the grid at the specified positions.

    Parameters:
    grid (list of list of Cell objects): The grid where players will be placed.
    players (int): The number of players to place on the grid. Default is 2.
    positions (list of tuples): A list of (y, x) positions to place the players. Default is None.

    Returns:
    list: A list of Player objects representing the players placed on the grid.
    """
    x_size = len(grid[0])
    y_size = len(grid)
    players_object = Players()

    # Set default positions if not provided
    if positions is None:
        if player_count == 2:
            positions = [(0, 0), (y_size - 1, x_size - 1)]  # Top-left and bottom-right for two players
        elif player_count == 3:
            # Two players in corners, third player in the center
            center_y = y_size // 2
            center_x = x_size // 2
            positions = [(0, 0), (y_size - 1, x_size - 1), (center_y, center_x)]
        else:
            positions = []  # Default for player_count other than 2 or 3

    # Loop to place players at specified positions
    for i in range(player_count):
        if i < len(positions):
            y, x = positions[i]
            if 0 <= y < y_size and 0 <= x < x_size:
                player = Player(i + 1, (y, x))  # Player number is an integer, position is tuple of ints
                grid[y][x].add_value(player.number)  # Store player's number in the cell
                players_object.add_player(player)
            else:
                print(f"Invalid position for player {i + 1}: {(y, x)}")
        else:
            raise ValueError(f"Not enough positions for {player_count} players.")


    return players_object

#Function used to check if two players are on the same spot, and if so print this and return true.
# def check_collision(player):
#     player_positions = set()
#     for player in players:
#         if player.position in player_positions:
#             print("Collision detected!")
#             return True #Collision detected
#         player_positions.add(player.position)
#     print("No collision detected!")
#     return False #No collision


# Testing code
test_grid = make_grid(5, 3)
print_grid(test_grid)

players_list = place_players(test_grid, 3)
print_grid(test_grid)

# Run a loop to move the player randomly multiple times
# for _ in range(25):  # Move 10 times
#     if players:
#         players[0].move("random", test_grid)
#         players[1].move("random", test_grid)
#     print_grid(test_grid)
#
#     if check_collision(players):
#         print("Players have met! Stopping simulation.")
#         break
#     time.sleep(0.5)  # Pause for half a second to visualize changes

if players_list:
    print("Test")
    # Move Player 1 (number 1) around the grid
    players_list.get_player(1).move("right", test_grid)
    print_grid(test_grid)

    players_list.get_player(1).move("right", test_grid)
    print_grid(test_grid)

    players_list.get_player(1).move("down", test_grid)
    print_grid(test_grid)

    # Move Player 2 (number 2) around the grid
    players_list.get_player(2).move("left", test_grid)
    print_grid(test_grid)

    players_list.get_player(2).move("left", test_grid)
    print_grid(test_grid)

    players_list.get_player(2).move("up", test_grid)
    print_grid(test_grid)

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