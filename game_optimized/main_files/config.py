import pygame

# Initialize Pygame
pygame.init()
# screen dimensions and margins
BOARD_COLS, BOARD_ROWS = 7, 9
TILE_SIZE = 700 // BOARD_COLS  # Board area is 700x700
MARGIN_LEFT = 50
MARGIN_TOP = 50
BOARD_WIDTH = TILE_SIZE * BOARD_COLS
BOARD_HEIGHT = TILE_SIZE * BOARD_ROWS
INFO_HEIGHT = 50  # Bottom info area height

#set the display
WIDTH, HEIGHT = MARGIN_LEFT * 2 + BOARD_WIDTH, MARGIN_TOP * 2 + BOARD_HEIGHT + INFO_HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Chess")

# Colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
BLUE    = (100, 100, 255)
MAGENTA = (255, 0, 255)
GREY    = (244, 244, 244)  # Background outside the grid
