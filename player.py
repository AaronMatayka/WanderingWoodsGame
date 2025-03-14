# player.py
import random

class Player:
    def __init__(self, number, position):
        self.number = number
        self.position = position

    def move(self, direction, grid):
        if direction == "random":
            direction = random.choice(["up", "down", "left", "right"])

        move_actions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        delta_y, delta_x = move_actions.get(direction, (0, 0))
        new_y = self.position[0] + delta_y
        new_x = self.position[1] + delta_x

        # Ensure the move is within grid bounds
        if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
            grid[self.position[0]][self.position[1]] = 0  # Clear old position
            self.position = (new_y, new_x)
            grid[new_y][new_x] = self.number  # Place player in new position
