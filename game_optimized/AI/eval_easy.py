from game_optimized.main_files.piece import Piece

#High/low values representimg the win, could be any high/low value
WIN_SCORE = 100000
LOSS_SCORE = -100000

def evaluate_easy(game, player):
    # Checks if the current player won or lost
    if game.winner is not None:
        return WIN_SCORE if game.winner == player else LOSS_SCORE

    score = 0
    if player == 1:
        opp_traps = game.traps_2
        opp_den = game.lair_2
        own_den = game.lair_1
    else:
        opp_traps = game.traps_1
        opp_den = game.lair_1
        own_den = game.lair_2

    # These parameters control the contribution of distance and mobility to the score.

    max_distance = 11
    factor_distance = 0.5 #weight for the distance
    factor_mobility = 0.3 # Weight for the number of valid moves

    # Loop over every piece, to evaluate the two parameters
    for piece in game.pieces:
        # Determine the effective value of the piece
        # If the piece is on an opponent's trap, its value is reduced to 0
        if (piece.x, piece.y) in opp_traps:
            effective_value = 0
        elif piece.name == "mouse": effective_value = 5
        else:
            effective_value = Piece.hierarchy[piece.name]

        # Calculate a bonus (if) or penalty (else) based on the Manhattan distance to the enemy lair (or own lair for opponent)
        if piece.player == player:
            # For the current player's pieces, a closer distance to the opponent's lair is better
            distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1])
    
            # The bonus is higher when the piece is closer (i.e. when distance is smaller)
            bonus_distance = (max_distance - distance) * factor_distance
        else:

            # For the opponent's pieces, we want them to be farther from our own lair
            distance = abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])

            # The bonus is negative since the closer the opponent is, the worse it is
            bonus_distance = -(max_distance - distance) * factor_distance

        # Calculate a bonus based on the mobility (number of valid moves) for the piece
        mobility = len(game.get_valid_moves(piece))
        bonus_mobility = mobility * factor_mobility

        # Sums the three paramters into the score
        if piece.player == player:
            score += effective_value + bonus_distance + bonus_mobility
        else:
            score -= effective_value + bonus_distance + bonus_mobility

    return score
