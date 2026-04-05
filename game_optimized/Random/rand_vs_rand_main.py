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

            if game.winner is None:
                pygame.time.delay(200)  # small delay to simulate thinking
                move = get_random_move(game, game.turn)
                if move:
                    piece, move = move
                    game.move_piece(piece, move[0], move[1])
                pygame.time.delay(200)

            game.draw()
            pygame.display.flip()
            clock.tick(30)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
