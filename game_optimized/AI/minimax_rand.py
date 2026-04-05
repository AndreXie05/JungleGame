import random
from game_optimized.main_files.game import Game

def minimax(game, depth, player, eval_function):
    # Base case: if we have reached the maximum search depth or the game is over
    if depth == 0 or game.winner is not None:
        return eval_function(game, player), None

    best_moves = []

    # Maximizing player
    if game.turn == player:  
        best_eval = float('-inf')
        # Iterate over each piece belonging to the current player.
        for piece in game.pieces:
            if piece.player == player:
                for (nx, ny) in game.get_valid_moves(piece):
                    # Clone the current state to simulate the move
                    new_game = game.clone_for_minimax()
                    # Find the corresponding piece in the cloned game.
                    clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    # Apply the move to the cloned game.
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    # Recursively call minimax on the new game state with reduced depth.
                    eval_score, _ = minimax(new_game, depth - 1, player, eval_function)

                    # If the new evaluation score is better than the best found so far,
                    # update the best evaluation and reset the best_moves list.
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    # If the score is equal to the best found, add the move to the list.
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))

    else:  # Minimizing player - same but for the enemy player.
        best_eval = float('inf')
        for piece in game.pieces:
            if piece.player != player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()
                    clone_piece = next((p for p in new_game.pieces 
                                        if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, depth - 1, player, eval_function)
                    if eval_score < best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))

    # Choose one move randomly from the list of best moves
    best_move = random.choice(best_moves) if best_moves else None
    return best_eval, best_move

def get_best_move(game, eval_function=None, depth=3):
    current_player = game.turn
    score, move = minimax(game, depth, current_player, eval_function)
    return move
