import os
import sys
import time
import pygame

import group_manager
import simulation
import universal_variables

pygame.init()

# Function to get the correct path for bundled files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if getattr(sys, 'frozen', False):  # Check if running as an exe
        base_path = sys._MEIPASS  # Temporary directory for PyInstaller
    else:
        base_path = os.path.abspath(".")  # Normal script execution

    return os.path.join(base_path, relative_path)

# Load the image with transparency using the resource path
try:
    happy_image_path = resource_path('happy.png')  # Get correct path for bundled image
    happy_image = pygame.image.load(happy_image_path).convert_alpha()  # Ensure alpha channel is used
    happy_image = pygame.transform.scale(happy_image, (100, 100))  # Resize image if needed
    happy_image.set_alpha(150)  # Set transparency (0 = fully transparent, 255 = fully opaque)
except pygame.error as e:
    print(f"Unable to load image: {e}")


class Game:
    """
    A class representing the game logic, including grid setup, movement, and game state management.
    """

    def __init__(self, grid_width, grid_height, num_people):
        """
        Initialize the game with a given grid size and number of people.

        :param grid_width: Width of the grid in cells.
        :param grid_height: Height of the grid in cells.
        :param num_people: Number of people in the simulation.
        """
        self.grid_width = grid_width  # Set grid width
        self.grid_height = grid_height  # Set grid height
        self.num_people = num_people  # Set number of people
        self.people = []  # Initialize list of people

    def all_met(self):
        """
        Check if all people in the simulation have met at the same location.

        :return: True if all people are at the same position, False otherwise.
        """
        if not self.people:
            print("NO CURRENT PEOPLE")
            return False

        first_x, first_y = self.people[0].x, self.people[0].y  # Get position of first person

        # Check if all people are at the same position
        return all(person.x == first_x and person.y == first_y for person in self.people)

    def draw_grid(self, screen):
        """
        Draw the grid, people, and game statistics on the screen.

        :param screen: Pygame display surface.
        """
        screen.fill(universal_variables.BACKGROUND_COLOR)  # Set background color

        # Draw grid cells
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(screen, universal_variables.WHITE, (
                    x * universal_variables.CELL_SIZE, y * universal_variables.CELL_SIZE,
                    universal_variables.CELL_SIZE, universal_variables.CELL_SIZE), 1)

        # Draw people on the grid
        for person in self.people:
            person.draw(screen)

        # Display turn time text
        text_surface = universal_variables.font.render(f'Turn Time: ' + str(universal_variables.TURN_TIME), True,
                                                       universal_variables.WHITE)
        text_rect = text_surface.get_rect(
            topleft=(10, self.grid_height * universal_variables.CELL_SIZE + (universal_variables.CELL_SIZE // 4)))

        # Draw black background for text area
        pygame.draw.rect(screen, universal_variables.BLACK, (
            0, self.grid_height * universal_variables.CELL_SIZE, self.grid_width * universal_variables.CELL_SIZE, 50))

        # Blit text to screen
        screen.blit(text_surface, text_rect)

        pygame.display.update()

    def game_loop(self):
        """
        Main game loop that handles events, updates game state, and manages rendering.
        """
        # Initialize the game window
        screen = pygame.display.set_mode(
            (self.grid_width * universal_variables.CELL_SIZE, self.grid_height * universal_variables.CELL_SIZE + 50))
        pygame.display.set_caption("Wandering in the Woods")

        running = True
        while running:
            game_over = False
            game_move_count = 0  # Track number of moves in the game
            last_time = pygame.time.get_ticks()  # Track elapsed time

            while not game_over:
                # Handle user input events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Quit game
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:  # Increase turn time
                            universal_variables.TURN_TIME += 0.05
                            universal_variables.TURN_TIME = round(universal_variables.TURN_TIME, 2)
                            self.draw_grid(screen)
                        elif event.key == pygame.K_LEFT:  # Decrease turn time
                            universal_variables.TURN_TIME -= 0.05
                            universal_variables.TURN_TIME = round(universal_variables.TURN_TIME, 2)
                            self.draw_grid(screen)

                current_time = pygame.time.get_ticks()  # Get current time

                # Draw initial state
                self.draw_grid(screen)

                if current_time - last_time >= universal_variables.TURN_TIME * 1000:  # Check time elapsed
                    last_time = current_time  # Reset timer
                    self.draw_grid(screen)

                    # Move groups and check for meeting
                    group_manager.move_groups(self.people, self.grid_width, self.grid_height)
                    found_group = group_manager.update_groups(self.people)

                    if found_group:
                        self.draw_grid(screen)
                        screen.blit(happy_image, (self.grid_width * universal_variables.CELL_SIZE // 2 - 50,
                                                  self.grid_height * universal_variables.CELL_SIZE // 2 - 50))  # Show happy image
                        pygame.display.update()
                        time.sleep(3)  # Pause for effect

                    game_move_count += 1  # Increment move count

                    if self.all_met():  # If all people met
                        for person in self.people:
                            person.color = universal_variables.GROUP_MERGED_COLOR  # Change color to indicate merge
                            self.draw_grid(screen)
                        game_over = True  # End game

                pygame.display.update()

            # Collect and update game statistics
            universal_variables.CURRENT_RUN = game_move_count
            universal_variables.AGGREGATE_RUNS.append(game_move_count)

            # Update shortest and longest run stats
            universal_variables.SHORTEST_RUN = min(universal_variables.SHORTEST_RUN,
                                                   game_move_count) if universal_variables.SHORTEST_RUN != -1 else game_move_count
            universal_variables.LONGEST_RUN = max(universal_variables.LONGEST_RUN,
                                                  game_move_count) if universal_variables.LONGEST_RUN != -1 else game_move_count

            # Calculate average run time
            universal_variables.AVERAGE_RUN = round(
                sum(universal_variables.AGGREGATE_RUNS) / len(universal_variables.AGGREGATE_RUNS), 2)

            # Show statistics menu
            universal_variables.RUN_COMPLETE = True
            simulation.main_menu()
