# Importing the necessary module for the game
import pygame

# Initialize the pygame library
pygame.init()

# ==============================================================
#                         IMPORTANT VARIABLES
# ==============================================================

# Game Window Dimensions
WINDOW_WIDTH = 800  # Width of the game window (in pixels)
WINDOW_HEIGHT = 600  # Height of the game window (in pixels)

# Grid Settings
GRID_WIDTH = 4  # Number of columns in the grid
GRID_HEIGHT = 4  # Number of rows in the grid
CELL_SIZE = 50  # Size (width and height) of each cell in the grid (in pixels)

# Player Settings
PLAYER_COUNT = 2  # Number of players in the game

# ==============================================================
#                         GAME STATISTICS
# ==============================================================

# Run Completion Flag
RUN_COMPLETE = False  # Flag to indicate whether the game run is complete (True/False)

# Track Longest and Shortest Runs Without Meeting
LONGEST_RUN_WITHOUT_MEETING = 0  # Longest time (in seconds) without players meeting
LONGEST_RUN = -1  # Longest run time (in seconds) during a simulation
SHORTEST_RUN = -1  # Shortest run time (in seconds) during a simulation

# Average and Current Run Times
AVERAGE_RUN = 0  # Average run time across all runs
CURRENT_RUN = 0  # Current run time (in seconds)

# List to store run times for all runs
AGGREGATE_RUNS = []  # List of all run times to calculate averages and comparisons

# ==============================================================
#                         GAME DESIGN PARAMETERS
# ==============================================================

# Grade Level (1 = K-2 | 2 = 3-5 | 3 = 6-8)
GRADE_LEVEL = 1  # Grade level for which the game is designed (default is K-2)

# Wandering Choice (Player movement behavior)
WANDERING_CHOICE = 'Biased Unexplored'  # Defines how players wander in the game (random or biased)

# ==============================================================
#                         COLOR DEFINITIONS
# ==============================================================

# Color Definitions (RGB format)
WHITE = (255, 255, 255)  # RGB for White
YELLOW = (255, 255, 0)  # RGB for Yellow
GRAY = (200, 200, 200)  # RGB for Gray (used for background and neutral elements)
BLACK = (0, 0, 0)  # RGB for Black (used for borders, text, etc.)
BACKGROUND_COLOR = (200, 200, 200)  # Light gray background color for the game window
TEXT_COLOR = (255, 255, 255)  # White color for text rendering in the game
GROUP_MERGED_COLOR = (128, 0, 128)  # Purple color for merged player groups

# ==============================================================
#                         GAME SETTINGS
# ==============================================================

# Turn Time Settings (Duration of each player's turn)
TURN_TIME = 1  # Time (in seconds) for each player's turn before the game progresses

# ==============================================================
#                         BUTTON SETTINGS
# ==============================================================

# Button Appearance Settings
BUTTON_BG_COLOR = (55, 55, 55)  # Background color of buttons (dark gray)
BUTTON_BG_HOVER_COLOR = (100, 100, 100)  # Background color of buttons when hovered (lighter gray)
BUTTON_TEXT_COLOR = WHITE  # Text color on buttons (white text)

# ==============================================================
#                         PLAYER COLOR SETTINGS
# ==============================================================

# Player Colors (for distinguishing players visually)
PLAYER_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]  # Blue, Red, Green, Yellow

# ==============================================================
#                         FONT SETTINGS
# ==============================================================

# General Font for Text and Titles
font = pygame.font.SysFont('Arial', 24)  # Standard font (size 24) for in-game text
font_title = pygame.font.SysFont('Arial', 60)  # Larger font (size 60) for titles and headers
BUTTON_FONT = pygame.font.SysFont('Arial', 40)  # Font (size 40) for button text
