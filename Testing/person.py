# Player class
import random
import pygame

from Testing import utilities, universal_variables

# Initialize pygame
pygame.init()


class Person:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.move_count = 0
        self.group = [self]  # A list to store group members, initially just the person

    def move(self, grid_width, grid_height):
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
        if len(self.group) > 1:
            group_colors = [p.color for p in self.group]
            color = utilities.blend_colors(group_colors)  # Blend all colors in the group
        else:
            color = self.color

        pygame.draw.circle(screen, color, (self.x * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2,
                                           self.y * universal_variables.CELL_SIZE + universal_variables.CELL_SIZE // 2),
                           universal_variables.CELL_SIZE // 3)

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)
