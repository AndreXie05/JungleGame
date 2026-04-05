import pygame
from game_optimized.main_files.config import *
from game_optimized.main_files.game import Game

def main(eval_function, get_best_move):
    pygame.init()
    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        # Process all events at the start of each frame
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                 # Stop the game if the window is closed

            elif event.type == pygame.KEYDOWN:
                # Reset the game if the 'r' key is pressed
                if event.key == pygame.K_r:
                    game = Game()

            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == 1 and game.winner is None:
                # Get the x and y coordinates of the mouse click
                mx, my = event.pos
                # Check if the click is within the board boundaries using margins and board dimensions
                if MARGIN_LEFT <= mx < MARGIN_LEFT + BOARD_WIDTH and MARGIN_TOP <= my < MARGIN_TOP + BOARD_HEIGHT:
                    # Convert screen coordinates to board coordinates
                    board_x = (mx - MARGIN_LEFT) // TILE_SIZE
                    board_y = (my - MARGIN_TOP) // TILE_SIZE
                    clicked_piece = None
                    # Iterate over all pieces to check if a piece belonging to player 1 is at the clicked board cell
                    for piece in game.pieces:
                        # If a piece is found at the clicked location, select it
                        if piece.x == board_x and piece.y == board_y and piece.player == game.turn:
                            clicked_piece = piece
                            break
                    if clicked_piece is not None:
                        game.selected_piece = clicked_piece

                    # If no new piece is clicked but a piece is already selected, attempt to move it to the clicked cell
                    elif game.selected_piece:
                        game.move_piece(game.selected_piece, board_x, board_y)
        
        # AI turn: only run when no events need handling and the game isn't over
        if game.winner is None and game.turn == 2:
            pygame.time.delay(50)  # Optional delay for visualization
            move = get_best_move(game, eval_function, depth=3)
            if move is None:
                print("No valid moves available. Ending game.")
                running = False
            else:
                piece, nx, ny = move
                # Find the matching piece in the current game state.
                for p in game.pieces:
                    if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player:
                        game.move_piece(p, nx, ny)
                        break

        game.draw()
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()

if __name__ == "__main__":
    main()
