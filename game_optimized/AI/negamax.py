from game_optimized.main_files.game import Game

def negamax(initial_game, evaluate, max_depth, player):
    stack = [(initial_game, max_depth, 1, None)]  # Cada entrada: (estado do jogo, profundidade, color, movimento)
    best_move = None
    best_value = float('-inf')
    
    while stack:
        game, depth, color, move = stack.pop()
        if depth == 0 or game.winner is not None:
            value = color * evaluate(game, player)
            if value > best_value:
                best_value = value
                best_move = move
        else:
            for piece in game.pieces:
                if piece.player == game.turn:
                    for (nx, ny) in game.get_valid_moves(piece):
                        new_game = game.clone_for_minimax()
                        clone_piece = next(
                            (p for p in new_game.pieces if p.name == piece.name and p.x == piece.x and p.y == piece.y),
                            None
                        )
                        if clone_piece is None:
                            continue
                        new_game.move_piece(clone_piece, nx, ny, simulate=True)
                        # Empilha o novo estado com profundidade decrescente; o movimento atual pode ser repassado se for o primeiro nível
                        new_move = (piece, nx, ny) if depth == max_depth else move
                        stack.append((new_game, depth - 1, -color, new_move))
    return best_value, best_move

# Wrapper function to get the best move for the current player
def get_best_move(game, evaluate, depth=3):
    current_player = game.turn
    _, move = negamax(game, evaluate, depth, current_player)
    return move
