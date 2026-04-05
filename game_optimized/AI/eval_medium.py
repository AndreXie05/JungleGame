from game_optimized.main_files.piece import Piece

WIN_SCORE = 100000
LOSS_SCORE = -100000

def evaluate_medium(game, player):
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

    max_distance = 11
    factor_distance = 0.4
    factor_mobility = 0.3
    factor_safety = 0.6
    factor_trap_control = 0.5

    for piece in game.pieces:
        if (piece.x, piece.y) in opp_traps:
            effective_value = 0
        elif piece.name == "mouse":
            effective_value = 5
        else:
            effective_value = Piece.hierarchy[piece.name]

        if piece.player == player:
            distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1])
            bonus_distance = (max_distance - distance) * factor_distance
        else:
            distance = abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])
            bonus_distance = -(max_distance - distance) * factor_distance

        mobility = len(game.get_valid_moves(piece))
        bonus_mobility = mobility * factor_mobility

        # Safety: If an enemy can capture this piece next turn
        danger = False
        if piece.player != player:
            for enemy in game.pieces:
                if enemy.player == player:
                    moves = game.get_valid_moves(enemy)
                    if (piece.x, piece.y) in moves:
                        danger = True
                        break
        else:
            for enemy in game.pieces:
                if enemy.player != player:
                    moves = game.get_valid_moves(enemy)
                    if (piece.x, piece.y) in moves:
                        danger = True
                        break
        bonus_safety = -effective_value * factor_safety if danger else 0

        # Trap control: If own piece is near (or on) opponent’s trap
        trap_bonus = 0
        if piece.player == player:
            for trap in opp_traps:
                dist_to_trap = abs(piece.x - trap[0]) + abs(piece.y - trap[1])
                if dist_to_trap <= 1:
                    trap_bonus += factor_trap_control

        total_bonus = bonus_distance + bonus_mobility + bonus_safety + trap_bonus

        if piece.player == player:
            score += effective_value + total_bonus
        else:
            score -= effective_value + total_bonus

    return score
