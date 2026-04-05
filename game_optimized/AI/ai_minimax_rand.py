import random
from game_optimized.main_files.game import Game

game = Game()

def minimax(game, evaluate, depth, player):
    if depth == 0 or game.winner is not None:
        return evaluate(game, player), None

    best_moves = []
    if game.turn == player:  # Maximizing player
        best_eval = float('-inf')
        for piece in game.pieces:
            if piece.player == player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()
                    clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, evaluate, depth - 1, player)
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))
    else:  # Minimizing player
        best_eval = float('inf')
        for piece in game.pieces:
            if piece.player != player:
                for (nx, ny) in game.get_valid_moves(piece):
                    new_game = game.clone_for_minimax()
                    clone_piece = next((p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y and p.player == piece.player), None)
                    if clone_piece is None:
                        continue
                    new_game.move_piece(clone_piece, nx, ny, simulate=True)
                    eval_score, _ = minimax(new_game, evaluate, depth - 1, player)
                    if eval_score < best_eval:
                        best_eval = eval_score
                        best_moves = [(piece, nx, ny)]
                    elif eval_score == best_eval:
                        best_moves.append((piece, nx, ny))

    best_move = random.choice(best_moves) if best_moves else None
    return best_eval, best_move

def get_best_move(game, evaluate, depth=3):
    current_player = game.turn
    score, move = minimax(game, evaluate, depth, current_player)
    return move
