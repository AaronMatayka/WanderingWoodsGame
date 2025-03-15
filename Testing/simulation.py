import pygame
import pygame_menu
from pygame_menu import themes

from Testing import universal_variables
from Testing.person import Person

# Initialize pygame
pygame.init()


# Settings Menu
def settings_menu(mainmenu, settings):
    mainmenu._open(settings)


def start_the_game(mainmenu, submenu):
    if universal_variables.GRADE_LEVEL == 1:
        simulation_chooser()
    elif universal_variables.GRADE_LEVEL == 2 or universal_variables.GRADE_LEVEL == 3:
        mainmenu._open(submenu)


def final_menu(mainmenu, finalmenu):
    mainmenu._open(finalmenu)


def generate_player_position_inputs(submenu, player_count):
    # Remove any existing player position input boxes
    for widget in submenu.get_widgets():
        submenu.remove_widget(widget)

    # Create new input boxes for each player position
    for i in range(1, player_count + 1):
        submenu.add.text_input(f'Player {i} X Position: ', default='0', maxchar=3)
        submenu.add.text_input(f'Player {i} Y Position: ', default='0', maxchar=3)


def simulation_chooser():
    from Testing.game_base import Game
    test = Game(universal_variables.GRID_WIDTH, universal_variables.GRID_HEIGHT, universal_variables.PLAYER_COUNT)

    if universal_variables.GRADE_LEVEL == 1:
        test.people.append(Person(0, 0, universal_variables.PLAYER_COLORS[0]))
        test.people.append(Person(universal_variables.GRID_WIDTH - 1, universal_variables.GRID_HEIGHT - 1,
                                  universal_variables.PLAYER_COLORS[1]))
    elif universal_variables.GRADE_LEVEL == 2 or universal_variables.GRADE_LEVEL == 3:
        for i in range(universal_variables.PLAYER_COUNT):
            # Use modulo to loop through PLAYER_COLORS in case PLAYER_COUNT exceeds the number of colors available
            color = universal_variables.PLAYER_COLORS[i % len(universal_variables.PLAYER_COLORS)]

            test.people.append(Person(i * (universal_variables.GRID_WIDTH // universal_variables.PLAYER_COUNT),
                                      i * (universal_variables.GRID_HEIGHT // universal_variables.PLAYER_COUNT), color))
    else:
        print("Invalid Grade Level: " + str(universal_variables.GRADE_LEVEL))

    test.game_loop()

def grade_level_changed(self, grade_selector):
    universal_variables.GRADE_LEVEL = grade_selector

# Make sure the input only allows numeric input
def filter_input(text):
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
    screen = pygame.display.set_mode((universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT))

    # MAIN MENU
    mainmenu = pygame_menu.Menu('Wandering In The Woods', universal_variables.WINDOW_WIDTH,
                                universal_variables.WINDOW_HEIGHT, theme=themes.THEME_GREEN)
    mainmenu.add.button('Run Simulation', lambda: start_the_game(mainmenu, submenu))
    mainmenu.add.button('Settings', lambda: settings_menu(mainmenu, settings))
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    # SETTINGS MENU
    settings = pygame_menu.Menu('Settings', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                                theme=themes.THEME_GREEN)
    settings.add.selector('Grade Level :', [('K-2', 1), ('3-5', 2), ('6-8', 3)],
                          default=universal_variables.GRADE_LEVEL - 1, onchange=grade_level_changed)
    time_selector = settings.add.text_input('Simulation Turn Time: ', default=str(universal_variables.TURN_TIME))
    cell_size_selector = settings.add.text_input('Cell Size: ', default=str(universal_variables.CELL_SIZE))

    # PARAMETER MENU
    submenu = pygame_menu.Menu('Game Parameters', universal_variables.WINDOW_WIDTH, universal_variables.WINDOW_HEIGHT,
                               theme=themes.THEME_GREEN)
    grid_width_input = submenu.add.text_input('Grid Width: ', default='5', maxchar=2)
    grid_height_input = submenu.add.text_input('Grid Height: ', default='5', maxchar=2)
    player_count_input = submenu.add.text_input('Player Count: ', default='3', maxchar=2)
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
        # TODO: CHECK VALUES FOR CORRECTNESS
        universal_variables.GRID_WIDTH = int(grid_width_input.get_value())
        universal_variables.GRID_HEIGHT = int(grid_height_input.get_value())

        # Get the value from the input field
        player_count_str = player_count_input.get_value()

        # Check if the input is a valid number
        if player_count_str.isdigit():
            universal_variables.PLAYER_COUNT = int(player_count_str)
            generate_player_position_inputs(finalmenu, universal_variables.PLAYER_COUNT)

        final_menu(mainmenu, finalmenu)

        start_game_button = finalmenu.add.button('Start Game', lambda: simulation_chooser())

        start_game_button.set_col_row_index(0, universal_variables.PLAYER_COUNT * 2,
                                            universal_variables.PLAYER_COUNT * 2)

    def return_to_main_menu(menu):
        universal_variables.RUN_COMPLETE = False
        menu.enable()

    while True:
        events = pygame.event.get()
        for event in events:
            universal_variables.TURN_TIME = filter_input(time_selector.get_value())
            universal_variables.CELL_SIZE = filter_input(cell_size_selector.get_value())

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
