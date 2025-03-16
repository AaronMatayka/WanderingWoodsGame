import time

import pygame
import group_manager

from src import simulation, universal_variables

pygame.init()

# Try to load the image
try:
    happy_image = pygame.image.load('src/happy.png')
    happy_image = pygame.transform.scale(happy_image, (100, 100))  # Resize image if needed
except pygame.error as e:
    print(f"Unable to load image: {e}")

class Game:
    def __init__(self, grid_width, grid_height, num_people):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.num_people = num_people
        self.people = []

    def all_met(self):
        if not self.people:
            print("NO CURRENT PEOPLE")
            return False

        first_x, first_y = self.people[0].x, self.people[0].y

        return all(person.x == first_x and person.y == first_y for person in self.people)

    def draw_grid(self, screen):
        screen.fill(universal_variables.BACKGROUND_COLOR)

        # Draw grid
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(screen, universal_variables.WHITE, (
                    x * universal_variables.CELL_SIZE, y * universal_variables.CELL_SIZE, universal_variables.CELL_SIZE,
                    universal_variables.CELL_SIZE), 1)

        # Draw the people
        for person in self.people:
            person.draw(screen)

        text_surface = universal_variables.font.render(f'Turn Time: ' + str(universal_variables.TURN_TIME), True,
                                                       universal_variables.WHITE)
        text_rect = text_surface.get_rect(
            topleft=(10, self.grid_height * universal_variables.CELL_SIZE + (universal_variables.CELL_SIZE // 4)))

        pygame.draw.rect(screen, universal_variables.BLACK, (
            0, self.grid_height * universal_variables.CELL_SIZE, self.grid_width * universal_variables.CELL_SIZE, 50))

        screen.blit(text_surface, text_rect)

        pygame.display.update()

    def game_loop(self):
        # Set the window to the grid size
        screen = pygame.display.set_mode(
            (self.grid_width * universal_variables.CELL_SIZE, self.grid_height * universal_variables.CELL_SIZE + 50))
        pygame.display.set_caption("Wandering in the Woods")

        running = True
        while running:
            game_over = False
            game_move_count = 0
            last_time = pygame.time.get_ticks()  # Initialize the last_time for tracking elapsed time

            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        # Check if the right arrow key is pressed
                        if event.key == pygame.K_RIGHT:
                            universal_variables.TURN_TIME += 0.05  # Increment TURN_TIME by 0.1
                            universal_variables.TURN_TIME = round(universal_variables.TURN_TIME, 2)
                            self.draw_grid(screen)
                        # Check if the left arrow key is pressed
                        elif event.key == pygame.K_LEFT:
                            universal_variables.TURN_TIME -= 0.05  # Decrement TURN_TIME by 0.1
                            universal_variables.TURN_TIME = round(universal_variables.TURN_TIME, 2)
                            self.draw_grid(screen)

                current_time = pygame.time.get_ticks()  # Get the current time

                # Initial Draw
                self.draw_grid(screen)
                if current_time - last_time >= universal_variables.TURN_TIME * 1000:  # Convert TURN_TIME to milliseconds
                    last_time = current_time  # Reset the last_time
                    self.draw_grid(screen)

                    group_manager.move_groups(self.people, self.grid_width, self.grid_height)
                    found_group = group_manager.update_groups(self.people)

                    if found_group:
                        self.draw_grid(screen)
                        screen.blit(happy_image, (self.grid_width * universal_variables.CELL_SIZE // 2 - 50,
                                                  self.grid_height * universal_variables.CELL_SIZE // 2 - 50))  # Draw the image at position (250, 200)
                        pygame.display.update()
                        time.sleep(3)

                    game_move_count += 1

                    if self.all_met():
                        for person in self.people:
                            person.color = universal_variables.GROUP_MERGED_COLOR  # Final merged color (purple)

                            # Show winning scenario
                            self.draw_grid(screen)

                        #screen.blit(happy_image, (self.grid_width * universal_variables.CELL_SIZE // 2 - 50, self.grid_height * universal_variables.CELL_SIZE // 2 - 50))  # Draw the image at position (250, 200)
                        #pygame.display.update()
                        #time.sleep(3)
                        game_over = True

                pygame.display.update()

            # Game Ended Collect Statistics
            if universal_variables.SHORTEST_RUN == -1 or game_move_count < universal_variables.SHORTEST_RUN:
                universal_variables.SHORTEST_RUN = game_move_count

            if universal_variables.LONGEST_RUN == -1 or game_move_count > universal_variables.LONGEST_RUN:
                universal_variables.LONGEST_RUN = game_move_count

            universal_variables.AGGREGATE_RUNS.append(game_move_count)

            universal_variables.AVERAGE_RUN = 0
            for run in universal_variables.AGGREGATE_RUNS:
                universal_variables.AVERAGE_RUN += run

            universal_variables.AVERAGE_RUN = round(universal_variables.AVERAGE_RUN / len(universal_variables.AGGREGATE_RUNS), 2)

            universal_variables.CURRENT_RUN = game_move_count

            # Show Statistics Menu
            universal_variables.RUN_COMPLETE = True
            simulation.main_menu()