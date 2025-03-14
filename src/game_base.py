import pygame

from src import simulation, universal_variables
from src.group_manager import GroupManager

pygame.init()


class Game:
    def __init__(self, grid_width, grid_height, num_people):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.num_people = num_people
        self.people = []

    def get_game_settings(self):
        return
        # self.people = []

        # # Randomly Place People Around Grid
        # for i in range(self.num_people):
        #     player_x = random.randint(0, self.grid_width - 1)
        #     player_y = random.randint(0, self.grid_height - 1)
        #
        #     self.people.append(Person(player_x, player_y, PLAYER_COLORS[i]))

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
        self.get_game_settings()

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

                    GroupManager.move_groups(self.people, self.grid_width, self.grid_height)
                    found_group = GroupManager.update_groups(self.people)

                    if found_group:
                        self.draw_grid(screen)

                    game_move_count += 1

                    if self.all_met():
                        for person in self.people:
                            person.color = universal_variables.GROUP_MERGED_COLOR  # Final merged color (purple)

                            # Show winning scenario
                            self.draw_grid(screen)

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

            # Display final message
            # text_surface = universal_variables.font.render(f"All players met ", True, universal_variables.TEXT_COLOR)
            # text_surface_2 = universal_variables.font.render(f"in {game_move_count} moves!", True,
            #                                                  universal_variables.TEXT_COLOR)
            # screen.blit(text_surface, (50, 50))
            # screen.blit(text_surface_2, (50, 100))
            # pygame.display.update()
            #
            # # Wait for user input to restart or quit
            # waiting = True
            # while waiting:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             pygame.quit()
            #             return
            #         if event.type == pygame.KEYDOWN:
            #             if event.key == pygame.K_r:
            #                 simulation.main_menu()
            #             elif event.key == pygame.K_q:
            #                 pygame.quit()
            #                 return
