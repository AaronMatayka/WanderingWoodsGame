import os
import sys
from functools import partial

import pygame
import pygame_menu
from pygame_menu import themes

import universal_variables
import utilities
from person import Person

# Initialize pygame
pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()

# Function to get the correct path for bundled files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if getattr(sys, 'frozen', False):  # Check if running as an exe
        base_path = sys._MEIPASS  # Temporary directory for PyInstaller
    else:
        base_path = os.path.abspath(".")  # Normal script execution

    return os.path.join(base_path, relative_path)

# Load the background music
background_music_path = resource_path('music.wav')
background_music = pygame.mixer.Sound(background_music_path)

def start_the_game(mainmenu, submenu):
    """
    Starts the game based on the grade level.
    Opens the simulation chooser or the main menu with a parameter submenu.

    Args:
        mainmenu: The main menu to be displayed.
        submenu: The submenu for game parameters.
    """
    if universal_variables.GRADE_LEVEL == 1:
        simulation_chooser(mainmenu)
    elif universal_variables.GRADE_LEVEL == 2 or universal_variables.GRADE_LEVEL == 3:
        mainmenu._open(submenu)


def generate_player_position_inputs(submenu, player_count):
    """
    Generates input fields for player positions (X, Y) in the game.
    Clears any existing input fields and creates new ones.

    Args:
        submenu: The submenu where input fields will be added.
        player_count: The number of players for whom inputs are generated.
    """
    # Remove any existing player position input boxes
    for widget in submenu.get_widgets():
        submenu.remove_widget(widget)

    # Create a parent frame to hold columns of input frames
    parent_frame = submenu.add.frame_h(220 * 2 + 80, universal_variables.PLAYER_COUNT * 49 + 20)

    # Create two vertical frames for each text input (X and Y coordinates)
    frame1 = submenu.add.frame_v(220 + 20, universal_variables.PLAYER_COUNT * 49 + 10)
    frame2 = submenu.add.frame_v(220 + 20, universal_variables.PLAYER_COUNT * 49 + 10)

    # Create new input boxes for each player position
    for i in range(1, player_count + 1):
        # Player X position input
        input1 = submenu.add.text_input(f'Player {i} X: ', default='0', maxchar=3,
                                        input_type=pygame_menu.locals.INPUT_INT)
        frame1.pack(input1)  # Pack X input into first vertical frame

        # Player Y position input
        input2 = submenu.add.text_input(f'Player {i} Y: ', default='0', maxchar=3,
                                        input_type=pygame_menu.locals.INPUT_INT)
        frame2.pack(input2)  # Pack Y input into second vertical frame

        # Apply the limit function to both input fields with partial function
        input1.add_draw_callback(
            partial(utilities.limit_input_value_selected, min=0, max=universal_variables.GRID_WIDTH - 1))
        input2.add_draw_callback(
            partial(utilities.limit_input_value_selected, min=0, max=universal_variables.GRID_HEIGHT - 1))

    # Pack both frames into the parent frame for display
    parent_frame.pack(frame1)
    parent_frame.pack(frame2)


def simulation_chooser(finalmenu):
    """
    Chooses and initializes the simulation based on the grade level.
    Creates the player objects and sets their positions accordingly.

    Args:
        finalmenu: The final menu to open after the simulation setup.
    """
    # Import the Game class from the game_base module
    from game_base import Game

    # Initialize the main game with grid dimensions and the number of players
    main_game = Game(universal_variables.GRID_WIDTH, universal_variables.GRID_HEIGHT, universal_variables.PLAYER_COUNT)

    # Based on the grade level, initialize the players with specific positions and colors
    if universal_variables.GRADE_LEVEL == 1:
        # For grade level 1, place two players at opposite corners of the grid
        main_game.people.append(Person(0, 0, universal_variables.PLAYER_COLORS[0], 1))  # First player at top-left
        main_game.people.append(Person(universal_variables.GRID_WIDTH - 1, universal_variables.GRID_HEIGHT - 1,
                                       universal_variables.PLAYER_COLORS[1], 2))  # Second player at bottom-right
    elif universal_variables.GRADE_LEVEL == 2 or universal_variables.GRADE_LEVEL == 3:
        # For grade levels 2 and 3, distribute players evenly across the grid
        for i in range(universal_variables.PLAYER_COUNT):
            # Use modulo to cycle through the PLAYER_COLORS list if the player count exceeds available colors
            color = universal_variables.PLAYER_COLORS[i % len(universal_variables.PLAYER_COLORS)]

            # Assign each player a unique position in the grid based on their index
            main_game.people.append(Person(i * (universal_variables.GRID_WIDTH // universal_variables.PLAYER_COUNT),
                                           i * (universal_variables.GRID_HEIGHT // universal_variables.PLAYER_COUNT),
                                           color, i + 1))
    else:
        # If an invalid grade level is provided, print an error message
        print("Invalid Grade Level: " + str(universal_variables.GRADE_LEVEL))

    # Now assign player positions based on the input values from the final menu
    for widget in finalmenu.get_widgets():
        # Check if the widget is a TextInput (i.e., the input fields for X and Y positions)
        if isinstance(widget, pygame_menu.widgets.TextInput):
            value = widget.get_value()  # Get the value entered for the position
            x, y = -1, -1  # Initialize x and y coordinates to -1

            # If the input widget is for X position, assign the X value
            if 'X' in widget.get_title():
                x = int(value)
            # If the input widget is for Y position, assign the Y value
            elif 'Y' in widget.get_title():
                y = int(value)

            # Extract the player number from the widget title (assumes player numbers are in the title)
            player_number = ''.join(c for c in widget.get_title() if c.isdigit())

            # Find the corresponding player and set their position based on the input
            for person in main_game.people:
                if person.player_number == int(player_number):
                    if x != -1:
                        person.x = x  # Update the player's X coordinate if it was provided
                    elif y != -1:
                        person.y = y  # Update the player's Y coordinate if it was provided

    # Start the game loop, which runs the main game logic
    main_game.game_loop()

def main_menu():
    """
    Initializes and runs the main menu loop, allowing navigation through menus and handling input.
    The main loop manages the state of the menus and the flow of the simulation.
    """
    # Set up the screen for the game window using the dimensions from universal_variables
    screen = pygame.display.set_mode((universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT))

    # MAIN MENU
    # Create the main menu using pygame_menu, setting the window dimensions and theme
    mainmenu = pygame_menu.Menu('Wandering In The Woods', universal_variables.WINDOW_WIDTH,
                                universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)

    # Add a button to run the simulation; when clicked, it triggers the start_the_game function
    mainmenu.add.button('Run Simulation', lambda: start_the_game(mainmenu, submenu))

    # Add a button to open the settings menu, which allows the user to modify game settings
    mainmenu.add.button('Settings', lambda: mainmenu._open(settings))

    # Add a button to quit the game and exit the application
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    # SETTINGS MENU
    # Create the settings menu where the user can modify the grade level, simulation time, and cell size
    settings = pygame_menu.Menu('Settings', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                                theme=themes.THEME_GREEN)

    # Add a selector for grade level, allowing the user to choose between K-2, 3-5, and 6-8
    # The default value is set based on the current grade level in universal_variables
    grade_selector = settings.add.selector('Grade Level :', [('K-2', 1), ('3-5', 2), ('6-8', 3)],
                                           default=universal_variables.GRADE_LEVEL - 1)

    # Add a text input for the simulation turn time, allowing the user to set how long each simulation turn lasts
    # The default value is based on the TURN_TIME variable in universal_variables
    time_selector = settings.add.text_input('Simulation Turn Time: ', default=str(universal_variables.TURN_TIME),
                                            input_type=pygame_menu.locals.INPUT_FLOAT)

    # Add a text input for the cell size, allowing the user to modify the size of each grid cell in the simulation
    # The default value is set based on the CELL_SIZE variable in universal_variables
    cell_size_selector = settings.add.text_input('Cell Size: ', default=str(universal_variables.CELL_SIZE),
                                                 input_type=pygame_menu.locals.INPUT_INT)

    # PARAMETER MENU
    # Create the game parameters menu for inputting game settings like grid size and player count
    submenu = pygame_menu.Menu('Game Parameters', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                               theme=themes.THEME_GREEN)

    # Add text input for grid width, with a default value of '5' and a maximum of 2 characters
    grid_width_input = submenu.add.text_input('Grid Width: ', default='5', maxchar=2,
                                              input_type=pygame_menu.locals.INPUT_INT)

    # Add text input for grid height, with a default value of '5' and a maximum of 2 characters
    grid_height_input = submenu.add.text_input('Grid Height: ', default='5', maxchar=2,
                                               input_type=pygame_menu.locals.INPUT_INT)

    # Add text input for player count, with a default value of '2' and a maximum of 2 characters
    player_count_input = submenu.add.text_input('Player Count: ', default='2', maxchar=2,
                                                input_type=pygame_menu.locals.INPUT_INT)

    # Add a selector for wandering choice, allowing selection between three options
    wandering_choice = submenu.add.selector('Wandering Choice: ',
                                            [('Random', 1), ('Random Valid', 2), ('Biased Unexplored', 3)], default=0)

    # Initially hide the wandering choice selector, as it's not needed for all grade levels
    wandering_choice.hide()

    # Add a button to continue to the final menu, which will process the inputs and start the game
    submenu.add.button('Continue', lambda: final_menu_handler())

    # STATS MENU
    # Create a separate stats menu to show simulation results like the current run and longest run
    statsmenu = pygame_menu.Menu('Wandering In The Woods', universal_variables.WINDOW_WIDTH,
                                 universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)

    # Display the current run number
    statsmenu.add.label('Current Run: ' + str(universal_variables.CURRENT_RUN))

    # Display the longest run without any player meeting
    statsmenu.add.label('Longest Run Without Meeting: ' + str(universal_variables.LONGEST_RUN_WITHOUT_MEETING))

    # Display the longest run time (e.g., how long the simulation lasted)
    statsmenu.add.label('Longest Run: ' + str(universal_variables.LONGEST_RUN))

    # Display the shortest run time (e.g., how quickly the simulation completed)
    statsmenu.add.label('Shortest Run: ' + str(universal_variables.SHORTEST_RUN))

    # Display the average run time of all simulations
    statsmenu.add.label('Average Run: ' + str(universal_variables.AVERAGE_RUN))

    # Display the total number of runs completed
    statsmenu.add.label('Aggregate Runs: ' + str(universal_variables.AGGREGATE_RUNS))

    # Add a button to return to the main menu after the user views stats
    statsmenu.add.button('Return To Main Menu', lambda: return_to_main_menu(mainmenu))

    # Add a button to quit the application
    statsmenu.add.button('Quit', pygame_menu.events.EXIT)

    # FINAL MENU
    finalmenu = pygame_menu.Menu('Final Game Parameters', universal_variables.WINDOW_WIDTH,
                                 universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)

    def final_menu_handler():
        """
        Handles the final game parameter inputs, sets the game parameters, and opens the final menu.
        """
        universal_variables.GRID_WIDTH = int(grid_width_input.get_value())
        universal_variables.GRID_HEIGHT = int(grid_height_input.get_value())
        universal_variables.PLAYER_COUNT = int(player_count_input.get_value())

        generate_player_position_inputs(finalmenu, universal_variables.PLAYER_COUNT)

        mainmenu._open(finalmenu)

        start_game_button = finalmenu.add.button('Start Game', lambda: simulation_chooser(finalmenu))

        start_game_button.set_col_row_index(0, universal_variables.PLAYER_COUNT * 2,
                                            universal_variables.PLAYER_COUNT * 2)

    def return_to_main_menu(menu):
        """
        Resets the game and returns to the main menu.

        Args:
            menu: The main menu to return to.
        """
        universal_variables.RUN_COMPLETE = False
        menu.enable()

    while True:
        events = pygame.event.get()  # Get all the events in the event queue

        # Limit the values of the input fields to ensure they stay within acceptable ranges.
        # These checks are done each time the user interacts with the fields.
        if time_selector.get_selected_time() == 0:
            # Ensures the time input stays within the range 0 to 10
            utilities.limit_input_value(time_selector.get_value(), time_selector, 0, 10)
        if cell_size_selector.get_selected_time() == 0:
            # Ensures the cell size input stays within the range 10 to 100
            utilities.limit_input_value(cell_size_selector.get_value(), cell_size_selector, 10, 100)
        if grid_width_input.get_selected_time() == 0:
            # Ensures the grid width input stays within the range 2 to 25
            utilities.limit_input_value(grid_width_input.get_value(), grid_width_input, 2, 25)
        if grid_height_input.get_selected_time() == 0:
            # Ensures the grid height input stays within the range 2 to 25
            utilities.limit_input_value(grid_height_input.get_value(), grid_height_input, 2, 25)
        if player_count_input.get_selected_time() == 0:
            # Ensures the player count input stays within the range 2 to 16
            utilities.limit_input_value(player_count_input.get_value(), player_count_input, 2, 16)

        for event in events:  # Process each event in the event queue
            # Update the global variables based on the user's input in the settings menu
            universal_variables.GRADE_LEVEL = grade_selector.get_value()[1] + 1  # Update the grade level
            universal_variables.TURN_TIME = time_selector.get_value()  # Update the turn time
            universal_variables.CELL_SIZE = cell_size_selector.get_value()  # Update the cell size
            universal_variables.WANDERING_CHOICE = wandering_choice.get_value()[0][0]  # Update the wandering choice

            # Display or hide the wandering choice based on the selected grade level
            if universal_variables.GRADE_LEVEL == 3:
                wandering_choice.show()  # Show wandering choice for grade 3
            else:
                wandering_choice.hide()  # Hide wandering choice for other grades

            if event.type == pygame.QUIT:  # Check if the user has closed the window
                exit()  # Exit the game if the window is closed

        # Update the menu based on the current state
        if universal_variables.RUN_COMPLETE:  # If a simulation run was completed, show stats
            statsmenu.update(events)  # Update the stats menu
            statsmenu.draw(screen)  # Draw the stats menu on the screen
        else:  # Otherwise, show the main menu
            if mainmenu.is_enabled():
                mainmenu.update(events)  # Update the main menu with current events
                mainmenu.draw(screen)  # Draw the main menu on the screen

        pygame.display.update()  # Update the display to show any changes made in the loop


# Run the main menu
if __name__ == "__main__":
    background_music.play(-1)  # -1 means loop the music indefinitely
    main_menu()
