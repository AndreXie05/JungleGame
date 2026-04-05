from game_optimized.main_files.config import *
import random

def get_random_move(game, player):

    if player == 1:
        all_moves = []
        for piece in game.pieces:
            if piece.player == 1:
                valid_moves = game.get_valid_moves(piece) # as game is already the func argument, don't need to import the module game.py, as it is already imported in the main random modules
                for move in valid_moves:
                    all_moves.append((piece, move))
    if player == 2:
        all_moves = []
        for piece in game.pieces:
            if piece.player == 2:
                valid_moves = game.get_valid_moves(piece)
                for move in valid_moves:
                    all_moves.append((piece, move))

    if all_moves:
        return random.choice(all_moves)
    return None
