# Constants

import pygame

# Initialize pygame
pygame.init()

# Important Variables
WINDOW_WIDTH = 800  # Width of the game window
WINDOW_HEIGHT = 600  # Height of the game window

GRID_WIDTH = 4  # Number of columns in the grid
GRID_HEIGHT = 4  # Number of rows in the grid
CELL_SIZE = 50  # Size of each cell in the grid
PLAYER_COUNT = 2  # Number of players in the game

# Statistics
RUN_COMPLETE = False  # Flag to indicate whether the game run is complete
LONGEST_RUN_WITHOUT_MEETING = 0  # Track the longest run without meeting between players
LONGEST_RUN = -1  # Track the longest run in total
SHORTEST_RUN = -1  # Track the shortest run in total
AVERAGE_RUN = 0  # Average run time
CURRENT_RUN = 0  # Current run time
AGGREGATE_RUNS = []  # List to store all run times

# Grade Level (1 = K-2 | 2 = 3-5 | 3 = 6-8)
GRADE_LEVEL = 3  # Grade level for which the game is designed

WANDERING_CHOICE = 'Biased Unexplored'

# Colors
WHITE = (255, 255, 255)  # RGB color code for white
GRAY = (200, 200, 200)  # RGB color code for gray
BLACK = (0, 0, 0)  # RGB color code for black
BACKGROUND_COLOR = (200, 200, 200)  # Background color of the game window (light gray)
TEXT_COLOR = (255, 255, 255)  # Color of the text (white)
GROUP_MERGED_COLOR = (128, 0, 128)  # Color for merged groups (purple)

# Game settings
TURN_TIME = 3  # Time (in seconds) per turn for each player

# Button settings
BUTTON_BG_COLOR = (55, 55, 55)  # Background color of buttons (dark gray)
BUTTON_BG_HOVER_COLOR = (100, 100, 100)  # Background color of buttons when hovered (lighter gray)
BUTTON_TEXT_COLOR = WHITE  # Text color on buttons (white)

# Player colors
PLAYER_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]  # Player colors for Blue, Red, Green, Yellow

# Fonts
font = pygame.font.SysFont('Arial', 24)  # Font for general text (size 24)
font_title = pygame.font.SysFont('Arial', 60)  # Font for titles (size 60)
BUTTON_FONT = pygame.font.SysFont('Arial', 40)  # Font for button text (size 40)
