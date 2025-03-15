# Constants
import pygame

# Initialize pygame
pygame.init()

# Important Variables
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GRID_WIDTH = 4
GRID_HEIGHT = 4
CELL_SIZE = 50
PLAYER_COUNT = 2

# 1 = K-2 | 2 = 3-5 | 3 = 6-8
GRADE_LEVEL = 2

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)  # Light gray
TEXT_COLOR = (255, 255, 255)  # White Text
GROUP_MERGED_COLOR = (128, 0, 128)  # Purple

TURN_TIME = 0.7

BUTTON_BG_COLOR = (55, 55, 55)
BUTTON_BG_HOVER_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = WHITE

# Player colors
PLAYER_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]  # Blue, Red, Green, Yellow

# Fonts
font = pygame.font.SysFont('Arial', 24)
font_title = pygame.font.SysFont('Arial', 60)
BUTTON_FONT = pygame.font.SysFont('Arial', 40)
