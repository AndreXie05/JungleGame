import random
from game_optimized.main_files.game import Game
from game_optimized.AI.eval_easy import evaluate_easy
from game_optimized.AI.eval_medium import evaluate_medium
from game_optimized.AI.eval_hard import evaluate_hard
from game_optimized.AI.eval_impossible import evaluate_impossible

game = Game()

# Assign evaluation functions for two players - CHANGE HERE FOR DIFFERENT DIFICULTY
evaluate1 = evaluate_impossible  # For player 1
evaluate2 = evaluate_medium    # For player 2

def minimax(game, depth, player):
    """
    Use minimax algorithm to choose the best move.
    
    game: current game state
    depth: how many moves ahead to simulate
    player: the player we're finding the move for
    """
    # Stop if no more depth or game is over, then evaluate
    if depth == 0 or game.winner is not None:
        evaluate = evaluate1 if player == 1 else evaluate2
        return evaluate(game, player), None

    best_moves = []

    # Maximizing player: try to get the highest score
    if game.turn == player:
        best_eval = float('-inf')
        for piece in game.pieces:
            if piece.player == player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()  # Clone game to simulate move
                    clone_piece = next((p for p in new_game.pieces 
                                        if p.name == piece.name and p.x == piece.x and p.y == piece.y 
                                        and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, depth - 1, player)
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))
    # Minimizing player: simulate the opponent's turn, try to lower the score
    else:
        best_eval = float('inf')
        for piece in game.pieces:
            if piece.player != player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()  # Clone game to simulate move
                    clone_piece = next((p for p in new_game.pieces 
                                        if p.name == piece.name and p.x == piece.x and p.y == piece.y 
                                        and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, depth - 1, player)
                    if eval_score < best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))

    # Choose a random move among the best options
    best_move = random.choice(best_moves) if best_moves else None
    return best_eval, best_move

def get_best_move(game, depth=3):
    """
    Find the best move for the current game state.
    
    game: current game state
    depth: how many moves ahead to look (default is 3)
    """
    current_player = game.turn
    score, move = minimax(game, depth, current_player)
    return move
