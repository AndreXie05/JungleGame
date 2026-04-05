from game_optimized.main_files.images import images
from game_optimized.main_files.config import *

class Piece:
    hierarchy = {"mouse": 1, "cat": 2, "dog": 3, "wolf": 4, "leopard": 5, "tiger": 6, "lion": 7, "elephant": 8}
    def __init__(self, name, x, y, player):
        self.name = name
        self.x = x
        self.y = y
        self.player = player
        self.image = images[self.name + f"_{player}"]
    def draw(self):
        SCREEN.blit(self.image, (MARGIN_LEFT + self.x * TILE_SIZE, MARGIN_TOP + self.y * TILE_SIZE))
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def update_image(self):
        """Call this method to refresh this piece's image after the global images dictionary is updated."""
        from game_optimized.main_files.images import images
        self.image = images[self.name + f"_{self.player}"]
