import pygame
from game_optimized.main_files.config import *
from game_optimized.main_files.board import draw_board, is_water
from game_optimized.main_files.piece import Piece

class Game:
    def __init__(self):
        self.pieces = self.create_pieces()  # Initialize pieces for both players
        self.selected_piece = None          # No piece is selected at the start
        self.turn = 1                       # Player 1 starts the game
        self.traps_1 = [(2, 8), (4, 8), (3, 7)]  # Trap cells for Player 1
        self.traps_2 = [(2, 0), (4, 0), (3, 1)]  # Trap cells for Player 2
        self.lair_1 = (3, 8)                # Lair cell for Player 1
        self.lair_2 = (3, 0)                # Lair cell for Player 2
        self.winner = None                  # No winner at initialization
        self.visualize = True               # Enable board rendering by default

    def create_pieces(self):
        """
        Create and return the initial set of game pieces for both players.

        Returns:
            List[Piece]: List containing all starting pieces for Player 1 and Player 2.
        """
        return [
            # Player 1 pieces with their names, starting positions, and player number.
            Piece("tiger", 0, 8, 1),     # Tiger at (0, 8)
            Piece("lion", 6, 8, 1),      # Lion at (6, 8)
            Piece("elephant", 0, 6, 1),  # Elephant at (0, 6)
            Piece("dog", 5, 7, 1),       # Dog at (5, 7)
            Piece("wolf", 2, 6, 1),      # Wolf at (2, 6)
            Piece("cat", 1, 7, 1),       # Cat at (1, 7)
            Piece("leopard", 4, 6, 1),   # Leopard at (4, 6)
            Piece("mouse", 6, 6, 1),     # Mouse at (6, 6)

            # Player 2 pieces with their names, starting positions, and player number.
            Piece("lion", 0, 0, 2),      # Lion at (0, 0)
            Piece("tiger", 6, 0, 2),     # Tiger at (6, 0)
            Piece("elephant", 6, 2, 2),  # Elephant at (6, 2)
            Piece("dog", 1, 1, 2),       # Dog at (1, 1)
            Piece("wolf", 4, 2, 2),      # Wolf at (4, 2)
            Piece("cat", 5, 1, 2),       # Cat at (5, 1)
            Piece("leopard", 2, 2, 2),   # Leopard at (2, 2)
            Piece("mouse", 0, 2, 2)      # Mouse at (0, 2)
        ]

    def is_valid_move(self, piece, x, y, check_only=False):
        # Ensure the target is within the board boundaries
        if not (0 <= x < BOARD_COLS and 0 <= y < BOARD_ROWS):
            return False

        # Prevent moving into the player's own lair
        if piece.player == 1 and (x, y) == self.lair_1:
            return False
        if piece.player == 2 and (x, y) == self.lair_2:
            return False

        # Non-mouse pieces cannot enter water cells.
        if piece.name != "mouse" and is_water(x, y):
            return False

        # Check if the target cell is an enemy trap.
        enemy_trap = (x, y) in (self.traps_1 if piece.player == 1 else self.traps_2)

        # Evaluate if the target cell is occupied by another piece.
        for p in self.pieces:
            if p.x == x and p.y == y:
                # Cannot move onto a cell with a friendly piece.
                if p.player == piece.player:
                    return False
                # Elephant cannot capture a mouse unless the target cell is an enemy trap.
                if piece.name == "elephant" and p.name == "mouse" and not enemy_trap:
                    return False
                # Mouse in water cannot leave water for land if the target cell is occupied.
                if piece.name == "mouse" and is_water(piece.x, piece.y) and not is_water(x, y):
                    return False
                # If the enemy piece is on an enemy trap, capture is allowed regardless of hierarchy.
                if enemy_trap:
                    return True
                # Otherwise, enforce capture based on hierarchy or allow mouse capturing an elephant.
                return Piece.hierarchy[piece.name] >= Piece.hierarchy[p.name] or \
                       (piece.name == "mouse" and p.name == "elephant")
        return True

    def get_valid_moves(self, piece):
        if piece is None:
            return []
        
        moves = []
        # Check adjacent moves in four cardinal directions.
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            if self.is_valid_move(piece, new_x, new_y):
                moves.append((new_x, new_y))

        # Special moves for lion and tiger: jump over water regions.
        if piece.name in ["lion", "tiger"]:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                jump = 0
                cur_x, cur_y = piece.x, piece.y
                # Continue in the current direction until a non-water cell is encountered.
                while True:
                    next_x = cur_x + dx
                    next_y = cur_y + dy
                    if not (0 <= next_x < BOARD_COLS and 0 <= next_y < BOARD_ROWS):
                        break  # Exit if out-of-bounds.
                    if not is_water(next_x, next_y):
                        break  # Stop if water ends.
                    jump += 1
                    cur_x, cur_y = next_x, next_y
                if jump > 0:
                    # Determine landing square, which is one tile beyond the water region.
                    landing_x = piece.x + dx * (jump + 1)
                    landing_y = piece.y + dy * (jump + 1)
                    if 0 <= landing_x < BOARD_COLS and 0 <= landing_y < BOARD_ROWS:
                        # Check that no mouse obstructs any tile in the water jump path.
                        path_clear = True
                        for i in range(1, jump + 1):
                            check_x = piece.x + dx * i
                            check_y = piece.y + dy * i
                            for p in self.pieces:
                                if p.x == check_x and p.y == check_y and p.name == "mouse":
                                    path_clear = False
                                    break
                            if not path_clear:
                                break
                        # Add the landing square if the jump is valid.
                        if path_clear and self.is_valid_move(piece, landing_x, landing_y):
                            moves.append((landing_x, landing_y))
        return moves

    def move_piece(self, piece, x, y, simulate=False):
        """
        Execute a move for the given piece to the target coordinates (x, y), update the game state,
        handle captures, check for victory conditions, and manage turn switching.
        """
        if (x, y) in self.get_valid_moves(piece):
            # Check victory condition: entering the enemy's lair wins the game
            if piece.player == 1 and (x, y) == self.lair_2:
                piece.move(x, y)
                if not simulate:
                    draw_board([], self.traps_1, self.traps_2, self.lair_1, self.lair_2)
                    for p in self.pieces:
                        p.draw()
                    pygame.display.flip()
                    pygame.time.delay(1000)
                self.winner = 1
                return
            elif piece.player == 2 and (x, y) == self.lair_1:
                piece.move(x, y)
                if not simulate:
                    draw_board([], self.traps_1, self.traps_2, self.lair_1, self.lair_2)
                    for p in self.pieces:
                        p.draw()
                    pygame.display.flip()
                    pygame.time.delay(1000)
                self.winner = 2
                return
            else:
                # Regular move: capture an enemy piece if present
                for p in self.pieces:
                    if p.x == x and p.y == y and p.player != piece.player:
                        self.pieces.remove(p)
                        break
                piece.move(x, y)
                # Switch turn: Toggle between player 1 and player 2
                self.turn = 3 - self.turn
                self.selected_piece = None

            # Check if the opponent has no pieces left, which results in a win
            if not any(p.player == (3 - piece.player) for p in self.pieces):
                self.winner = piece.player
            else:
                # Check if the current player has any legal moves. If not, the opponent wins
                if not any(self.get_valid_moves(p) for p in self.pieces if p.player == self.turn):
                    self.winner = 3 - self.turn

    def draw(self):
        """
        Render the current game state including the board, pieces, and status messages.
        """
        if not self.visualize:
            return
        # Determine valid moves for the selected piece to highlight them
        highlighted = self.get_valid_moves(self.selected_piece) if self.selected_piece else []
        draw_board(highlighted, self.traps_1, self.traps_2, self.lair_1, self.lair_2)
        # Draw all the pieces on the board
        for piece in self.pieces:
            piece.draw()
        # Prepare the font for status messages
        font = pygame.font.Font(None, 36)
        if self.winner in [1, 2]:
            # Display winning message if a player has won
            msg = f"Player {self.winner} wins! Press R to reset."
            text = font.render(msg, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, MARGIN_TOP + BOARD_HEIGHT // 2))
        else:
            # Otherwise, display the current player's turn
            msg = f"Next Player: {self.turn}"
            text = font.render(msg, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, MARGIN_TOP + BOARD_HEIGHT + INFO_HEIGHT // 2))
        SCREEN.blit(text, text_rect)

    # Used by minimax
    def clone_for_minimax(self):
        new_game = Game()

        # Clone all pieces so that moves in the simulation do not affect the original.
        new_game.pieces = [Piece(p.name, p.x, p.y, p.player) for p in self.pieces]
        new_game.winner = self.winner
        new_game.turn = self.turn
        new_game.traps_1 = self.traps_1
        new_game.traps_2 = self.traps_2
        new_game.lair_1 = self.lair_1
        new_game.lair_2 = self.lair_2
        return new_game
