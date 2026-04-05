import time
from game_optimized.main_files.config import *
from game_optimized.main_files.game import Game
from game_optimized.AI.minimax_stats import get_best_move

def run_games(num_games, depth=3):
    """
    Run AI vs AI games and collect statistics without visualization.
    
    In these games, AI1 (player 1) always uses evaluate1 and AI2 (player 2) uses evaluate2.
    
    Args:
        num_games (int): Number of games to simulate.
        depth (int): Search depth for minimax algorithm.
    
    Returns:
        dict: Statistics including wins, draws, moves, and times.
    """
    # Statistics tracking
    results = {'AI1_wins': 0, 'AI2_wins': 0, 'draws': 0, 'inconclusive': 0}
    total_moves = 0
    total_time_ai1 = 0
    total_time_ai2 = 0
    ai1_move_count = 0
    ai2_move_count = 0

    for game_num in range(num_games):
        game = Game()
        move_count = 0
        running = True

        # Always assign player 1 to AI1 (evaluate1) and player 2 to AI2 (evaluate2)
        ai1_player = 1
        ai2_player = 2

        while running:
            # Check for move limit
            if move_count > 100:
                results['inconclusive'] += 1
                print(f"Game {game_num + 1}: Exceeded 100 moves. Marked as inconclusive.")
                running = False
                break

            # Check for game end
            if game.winner is not None:
                if game.winner == ai1_player:
                    results['AI1_wins'] += 1
                elif game.winner == ai2_player:
                    results['AI2_wins'] += 1
                running = False
            elif not any(game.get_valid_moves(p) for p in game.pieces if p.player == game.turn):
                # No valid moves for current player: draw or opponent wins
                if not any(game.get_valid_moves(p) for p in game.pieces if p.player != game.turn):
                    results['draws'] += 1  # Both players have no moves: draw
                else:
                    results['AI1_wins' if game.turn == ai2_player else 'AI2_wins'] += 1  # Opponent wins
                running = False
            else:
                # AI move selection
                start_time = time.time()
                move = get_best_move(game, depth=depth)  # call without extra player parameter
                end_time = time.time()

                # Update timing stats
                if game.turn == ai1_player:
                    total_time_ai1 += end_time - start_time
                    ai1_move_count += 1
                else:
                    total_time_ai2 += end_time - start_time
                    ai2_move_count += 1

                if move is None:
                    print(f"Game {game_num + 1}: No move returned for Player {game.turn}. Treating as loss.")
                    results['AI1_wins' if game.turn == ai2_player else 'AI2_wins'] += 1
                    running = False
                else:
                    try:
                        piece, nx, ny = move
                        game.move_piece(piece, nx, ny)
                        move_count += 1
                    except (ValueError, TypeError) as e:
                        print(f"Game {game_num + 1}: Invalid move format {move}. Error: {e}")
                        running = False

        total_moves += move_count
        print(f"Game {game_num + 1} completed with {move_count} moves.")

    # Calculate statistics
    stats = {
        'results': results,
        'avg_moves': total_moves / num_games if num_games > 0 else 0,
        'avg_time_ai1': total_time_ai1 / ai1_move_count if ai1_move_count > 0 else 0,
        'avg_time_ai2': total_time_ai2 / ai2_move_count if ai2_move_count > 0 else 0,
        'ai1_win_rate': results['AI1_wins'] / num_games * 100 if num_games > 0 else 0,
        'ai2_win_rate': results['AI2_wins'] / num_games * 100 if num_games > 0 else 0,
        'draw_rate': results['draws'] / num_games * 100 if num_games > 0 else 0,
        'inconclusive_rate': results['inconclusive'] / num_games * 100 if num_games > 0 else 0
    }

    # Print results
    print("\n=== Final Statistics ===")
    print(f"Results after {num_games} games:")
    print(f"AI1 (evaluate1) wins: {results['AI1_wins']} ({stats['ai1_win_rate']:.2f}%)")
    print(f"AI2 (evaluate2) wins: {results['AI2_wins']} ({stats['ai2_win_rate']:.2f}%)")
    print(f"Draws: {results['draws']} ({stats['draw_rate']:.2f}%)")
    print(f"Inconclusive: {results['inconclusive']} ({stats['inconclusive_rate']:.2f}%)")
    print(f"Average moves per game: {stats['avg_moves']:.2f}")
    print(f"Average time per move for AI1: {stats['avg_time_ai1']:.4f} seconds")
    print(f"Average time per move for AI2: {stats['avg_time_ai2']:.4f} seconds")

    return stats

if __name__ == "__main__":
    run_games(num_games=10, depth=3)
