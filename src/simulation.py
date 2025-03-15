import pygame
import pygame_menu
from pygame_menu import themes

from src import universal_variables
from src.person import Person

# Initialize pygame
pygame.init()


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

    # Create a parent frame to hold columns
    parent_frame = submenu.add.frame_h(220 * 2 + 80, universal_variables.PLAYER_COUNT * 49 + 20)

    # Create two vertical frames for each text input
    frame1 = submenu.add.frame_v(220 + 20, universal_variables.PLAYER_COUNT * 49 + 10)
    frame2 = submenu.add.frame_v(220 + 20, universal_variables.PLAYER_COUNT * 49 + 10)

    # Create new input boxes for each player position
    for i in range(1, player_count + 1):
        input1 = submenu.add.text_input(f'Player {i} X: ', default='0', maxchar=3)
        frame1.pack(input1)
        input2 = submenu.add.text_input(f'Player {i} Y: ', default='0', maxchar=3)
        frame2.pack(input2)

    parent_frame.pack(frame1)
    parent_frame.pack(frame2)


def simulation_chooser(finalmenu):
    """
    Chooses and initializes the simulation based on the grade level.
    Creates the player objects and sets their positions accordingly.

    Args:
        finalmenu: The final menu to open after the simulation setup.
    """
    from src.game_base import Game
    test = Game(universal_variables.GRID_WIDTH, universal_variables.GRID_HEIGHT, universal_variables.PLAYER_COUNT)

    if universal_variables.GRADE_LEVEL == 1:
        test.people.append(Person(0, 0, universal_variables.PLAYER_COLORS[0], 1))
        test.people.append(Person(universal_variables.GRID_WIDTH - 1, universal_variables.GRID_HEIGHT - 1,
                                  universal_variables.PLAYER_COLORS[1], 2))
    elif universal_variables.GRADE_LEVEL == 2 or universal_variables.GRADE_LEVEL == 3:
        for i in range(universal_variables.PLAYER_COUNT):
            # Use modulo to loop through PLAYER_COLORS in case PLAYER_COUNT exceeds the number of colors available
            color = universal_variables.PLAYER_COLORS[i % len(universal_variables.PLAYER_COLORS)]

            test.people.append(Person(i * (universal_variables.GRID_WIDTH // universal_variables.PLAYER_COUNT),
                                      i * (universal_variables.GRID_HEIGHT // universal_variables.PLAYER_COUNT), color,
                                      i + 1))
    else:
        print("Invalid Grade Level: " + str(universal_variables.GRADE_LEVEL))

    for widget in finalmenu.get_widgets():
        if isinstance(widget, pygame_menu.widgets.TextInput):
            value = widget.get_value()
            x, y = -1, -1
            if 'X' in widget.get_title():
                x = int(value)
            elif 'Y' in widget.get_title():
                y = int(value)

            player_number = ''.join(c for c in widget.get_title() if c.isdigit())

            for person in test.people:
                if person.player_number == int(player_number):
                    if x != -1:
                        person.x = x
                    elif y != -1:
                        person.y = y

    test.game_loop()


def filter_input(text):
    """
    Filters the input to ensure it only allows numeric values, returning a float.

    Args:
        text: The input string to be filtered.

    Returns:
        float: The numeric value of the input, or 1.0 if the input is invalid.
    """
    if not text:
        return 1.0  # Return 1 if input is empty
    # Check if the text starts with a dot and prepend 0
    if text.startswith('.'):
        text = '0' + text
    # Try to convert the text to float and return the result
    try:
        return float(''.join([char for char in text if char.isdigit() or char == '.']))
    except ValueError:
        return 1.0  # Return 0 if the input is invalid


def main_menu():
    """
    Initializes and runs the main menu loop, allowing navigation through menus and handling input.
    """
    screen = pygame.display.set_mode((universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT))

    # MAIN MENU
    mainmenu = pygame_menu.Menu('Wandering In The Woods', universal_variables.WINDOW_WIDTH,
                                universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)
    mainmenu.add.button('Run Simulation', lambda: start_the_game(mainmenu, submenu))
    mainmenu.add.button('Settings', lambda: mainmenu._open(settings))
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    # SETTINGS MENU
    settings = pygame_menu.Menu('Settings', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                                theme=themes.THEME_GREEN)
    grade_selector = settings.add.selector('Grade Level :', [('K-2', 1), ('3-5', 2), ('6-8', 3)],
                                           default=universal_variables.GRADE_LEVEL - 1)
    time_selector = settings.add.text_input('Simulation Turn Time: ', default=str(universal_variables.TURN_TIME))
    cell_size_selector = settings.add.text_input('Cell Size: ', default=str(universal_variables.CELL_SIZE))

    # PARAMETER MENU
    submenu = pygame_menu.Menu('Game Parameters', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                               theme=themes.THEME_GREEN)
    grid_width_input = submenu.add.text_input('Grid Width: ', default='5', maxchar=2)
    grid_height_input = submenu.add.text_input('Grid Height: ', default='5', maxchar=2)
    player_count_input = submenu.add.text_input('Player Count: ', default='3', maxchar=2)
    wandering_choice = submenu.add.selector('Wandering Choice: ', [('Random', 1), ('src', 2)], default=0)
    wandering_choice.hide()
    submenu.add.button('Continue', lambda: final_menu_handler())

    # STATS MENU
    statsmenu = pygame_menu.Menu('Wandering In The Woods', universal_variables.WINDOW_WIDTH,
                                 universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)
    statsmenu.add.label('Current Run: ' + str(universal_variables.CURRENT_RUN))
    statsmenu.add.label('Longest Run Without Meeting: ' + str(universal_variables.LONGEST_RUN_WITHOUT_MEETING))
    statsmenu.add.label('Longest Run: ' + str(universal_variables.LONGEST_RUN))
    statsmenu.add.label('Shortest Run: ' + str(universal_variables.SHORTEST_RUN))
    statsmenu.add.label('Average Run: ' + str(universal_variables.AVERAGE_RUN))
    statsmenu.add.label('Aggregate Runs: ' + str(universal_variables.AGGREGATE_RUNS))
    statsmenu.add.button('Return To Main Menu', lambda: return_to_main_menu(mainmenu))
    statsmenu.add.button('Quit', pygame_menu.events.EXIT)

    # FINAL MENU
    finalmenu = pygame_menu.Menu('Final Game Parameters', universal_variables.WINDOW_WIDTH,
                                 universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)

    def final_menu_handler():
        """
        Handles the final game parameter inputs, sets the game parameters, and opens the final menu.
        """
        # TODO: CHECK VALUES FOR CORRECTNESS
        universal_variables.GRID_WIDTH = int(grid_width_input.get_value())
        universal_variables.GRID_HEIGHT = int(grid_height_input.get_value())

        # Get the value from the input field
        player_count_str = player_count_input.get_value()

        # Check if the input is a valid number
        if player_count_str.isdigit():
            universal_variables.PLAYER_COUNT = int(player_count_str)
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
        events = pygame.event.get()
        for event in events:
            universal_variables.GRADE_LEVEL = grade_selector.get_value()[1] + 1
            universal_variables.TURN_TIME = filter_input(time_selector.get_value())
            universal_variables.CELL_SIZE = filter_input(cell_size_selector.get_value())

            if universal_variables.GRADE_LEVEL == 3:
                wandering_choice.show()
            else:
                wandering_choice.hide()

            if event.type == pygame.QUIT:
                exit()

        if universal_variables.RUN_COMPLETE:
            # If a run was completed, show the stats menu
            statsmenu.update(events)
            statsmenu.draw(screen)
        else:
            # Otherwise, show the main menu
            if mainmenu.is_enabled():
                mainmenu.update(events)
                mainmenu.draw(screen)

        pygame.display.update()


# Run the main menu
if __name__ == "__main__":
    main_menu()
