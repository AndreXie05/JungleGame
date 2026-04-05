import pygame
from game_optimized.main_files.config import *

# used to highlight the possible plays 
def darken_color(color, factor=0.7):
    return tuple(max(int(c * factor), 0) for c in color)

# func to determine if a cell is or is not watter
def is_water(x, y):
    # Water region is columns 1-5 and rows 3-5 (0-indexed),
    # except positions D6, D5, D4 (col 3, rows 3,4,5) are exceptions.
    return (1 <= x <= 5 and 3 <= y <= 5) and not (x == 3 and y in [3, 4, 5])

def draw_board(highlighted=[], traps_1=[], traps_2=[], lair_1=(), lair_2=()):
    # Fill the entire screen with GREY -- outside the grid
    SCREEN.fill(GREY)

    # Fill each cell with the correspondent color
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pos = (col, row)
            if is_water(col, row):
                base_color = BLUE
            else:
                base_color = WHITE 

            if pos in traps_1 or pos in traps_2:
                base_color = MAGENTA
            if pos == lair_1 or pos == lair_2:
                base_color = BLACK

            if pos in highlighted and (pos != lair_1 and pos != lair_2): 
                base_color = darken_color(base_color)

            if pos in highlighted and (pos == lair_1 or pos == lair_2):
                base_color = (52,53,60)     # changes the color from the lair when it is a possible move
            
            # drawing the actual grid, cell by cell
            rect = pygame.Rect(MARGIN_LEFT + col * TILE_SIZE, MARGIN_TOP + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, base_color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
    
    # render the text of the grid coordinates -- from 1 to 9 on the lines and from A to G on the collumns
    font = pygame.font.Font(None, 24)
    for i in range(BOARD_ROWS):
        label = font.render(str(BOARD_ROWS - i), True, BLACK)
        SCREEN.blit(label, (MARGIN_LEFT // 2 - label.get_width() // 2,
                            MARGIN_TOP + i * TILE_SIZE + TILE_SIZE // 2 - label.get_height() // 2))
    
    for i, letter in enumerate("ABCDEFG"):
        label = font.render(letter, True, BLACK)
        SCREEN.blit(label, (MARGIN_LEFT + i * TILE_SIZE + TILE_SIZE // 2 - label.get_width() // 2,
                            MARGIN_TOP // 2 - label.get_height() // 2))
