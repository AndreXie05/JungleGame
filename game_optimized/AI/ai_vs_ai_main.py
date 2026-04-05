import pygame
import random
from game_optimized.main_files.config import *
from game_optimized.main_files.game import Game
from game_optimized.AI.ai_minimax_rand import get_best_move
from game_optimized.AI.eval_easy import evaluate_easy
from game_optimized.AI.eval_medium import evaluate_medium
from game_optimized.AI.eval_hard import evaluate_hard
from game_optimized.AI.eval_impossible import evaluate_impossible

choose = [evaluate_easy, evaluate_medium, evaluate_hard, evaluate_impossible]

evaluate1 = random.choice(choose)
evaluate2 = random.choice(choose)

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game()

        if game.winner is None:
            pygame.time.delay(500)  # delay for visualization
            if game.turn == 1:
                move = get_best_move(game, evaluate1)
            elif game.turn == 2:
                move = get_best_move(game, evaluate2)
            if move is None:
                print("No valid moves available. Ending game.")
                running = False
            else:
                # Unpack the best move: the piece to move and its target coordinates
                piece, nx, ny = move
                # Find the matching piece in the current game state.
                for p in game.pieces:
                    if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player:
                        game.move_piece(p, nx, ny)
                        break

        game.draw()
        pygame.display.flip()
        clock.tick(30) # Frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
