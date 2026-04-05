import pygame
import sys
from game_optimized.main_files.config import *
from game_optimized.main_files.game import Game
from game_optimized.Random.random_game import get_random_move

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and game.winner is None:
                    mx, my = event.pos
                    if MARGIN_LEFT <= mx < MARGIN_LEFT + BOARD_WIDTH and MARGIN_TOP <= my < MARGIN_TOP + BOARD_HEIGHT:
                        board_x = (mx - MARGIN_LEFT) // TILE_SIZE
                        board_y = (my - MARGIN_TOP) // TILE_SIZE
                        clicked_piece = None
                        for piece in game.pieces:
                            if piece.x == board_x and piece.y == board_y and piece.player == game.turn:
                                clicked_piece = piece
                                break
                        if clicked_piece is not None:
                            game.selected_piece = clicked_piece
                        elif game.selected_piece:
                           game.move_piece(game.selected_piece, board_x, board_y)


                elif game.turn == 2 and game.winner is None:
                    pygame.time.delay(200)  # Pequena pausa para simular pensamento
                    best_move = get_random_move(game, 2)
                    if best_move:
                        piece, move = best_move
                        game.move_piece(piece, move[0], move[1])
                    pygame.time.delay(200)

                # NEW: When the game is over, allow reset by pressing R.
                elif event.type == pygame.KEYDOWN and game.winner is not None:
                    if event.key == pygame.K_r:
                        game = Game()


            game.draw()
            pygame.display.flip()
            clock.tick(30)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
