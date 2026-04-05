from game_optimized.main_files.piece import Piece
from game_optimized.main_files.board import is_water

# Constants for win/loss scores
WIN_SCORE = 10000
LOSS_SCORE = -10000
MAX_DISTANCE = 11  # Maximum Manhattan distance on the 7x9 board
BOARD_COLS, BOARD_ROWS = 7, 9

# Parameters used with new factor names
factor_piece_value = 10.0      # High value to prioritize material
factor_distance = 2.0          # Strong incentive to approach opponent's den
factor_mobility = 1.5          # Emphasize move options, especially for key pieces
factor_trap_control = 5.0      # Traps are critical for captures
factor_lair_defense = 20.0     # Severe penalty for threats to own den
factor_mouse_position = 3.0      # Mouse's are strategically vital
factor_piece_protection = 2.0  # Encourage piece support
factor_central_control = 1.0   # Control key areas near water
factor_threats = 15.0          # Heavy weight on immediate capture opportunities
factor_jump_position = 4.0     # Bonus for Lions/Tigers in jump positions

def get_adjacent_positions(x, y):
    """Return list of adjacent positions within board boundaries."""
    return [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if 0 <= x + dx < BOARD_COLS and 0 <= y + dy < BOARD_ROWS]

def can_capture(attacker, defender, game):
    """Determine if attacker can capture defender based on Jungle rules."""
    # Check if defender is in attacker's trap
    own_traps = game.traps_1 if attacker.player == 1 else game.traps_2
    if (defender.x, defender.y) in own_traps:
        return True  # Any piece can capture a piece on its own trap
    
    # Check water rule: only rats can capture in water
    if is_water(defender.x, defender.y):
        return attacker.name == "rat"
    
    # Special case: rat can capture elephant
    if attacker.name == "mouse" and defender.name == "elephant":
        return True
    
    # Special case: elephant cannot capture rat
    if attacker.name == "elephant" and defender.name == "mouse":
        return False
    
    # General case: compare ranks using the hierarchy dictionary
    return Piece.hierarchy[attacker.name] >= Piece.hierarchy[defender.name]

def is_jump_position(piece, game):
    """Check if a Lion or Tiger is in position to jump over the river."""
    if piece.name not in ["lion", "tiger"]:
        return False
    x, y = piece.x, piece.y
    # Assuming river is roughly rows 3-5; adjust based on exact board layout
    # Player 1: jump from row 3 to 6, Player 2: jump from row 6 to 3
    jump_rows = {1: 3, 2: 6}
    target_row = 6 if piece.player == 1 else 3
    return y == jump_rows[piece.player] and not any(
        p.x == x and p.y in range(min(y, target_row), max(y, target_row) + 1)
        for p in game.pieces if p != piece
    ) and all(is_water(x, ny) for ny in range(4, 6))

def evaluate_impossible(game, player):
    """
    Evaluate the game state from the player's perspective.
    Higher scores are better for the player, making the AI nearly unbeatable.
    """
    if game.winner is not None:
        return WIN_SCORE if game.winner == player else LOSS_SCORE

    score = 0
    opp_traps = game.traps_2 if player == 1 else game.traps_1
    own_traps = game.traps_1 if player == 1 else game.traps_2
    opp_den = game.lair_2 if player == 1 else game.lair_1  # (3, 0) or (3, 8)
    own_den = game.lair_1 if player == 1 else game.lair_2  # (3, 8) or (3, 0)

    # 1. Piece Values and Distance to Opponent's Den
    for piece in game.pieces:
        is_on_opp_trap = (piece.x, piece.y) in (opp_traps if piece.player == player else own_traps)
        effective_value = 0 if is_on_opp_trap else Piece.hierarchy[piece.name]
        distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1]) if piece.player == player else \
                   abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])
        bonus_distance = (MAX_DISTANCE - distance) * factor_distance
        if piece.player == player:
            score += effective_value * factor_piece_value + bonus_distance
        else:
            score -= effective_value * factor_piece_value + bonus_distance

    # 2. Mobility
    for piece in game.pieces:
        mobility = len(game.get_valid_moves(piece))
        if piece.player == player:
            score += mobility * factor_mobility
        else:
            score -= mobility * factor_mobility

    # 3. Trap Control
    for trap in opp_traps:
        adjacent = get_adjacent_positions(trap[0], trap[1])
        control = sum(1 for pos in adjacent for p in game.pieces if p.player == player and (p.x, p.y) == pos)
        score += control * factor_trap_control
    for trap in own_traps:
        adjacent = get_adjacent_positions(trap[0], trap[1])
        control = sum(1 for pos in adjacent for p in game.pieces if p.player != player and (p.x, p.y) == pos)
        score -= control * factor_trap_control

    # 4. Lair Defense Penalty (Exponential for proximity)
    opp_pieces = [p for p in game.pieces if p.player != player]
    if opp_pieces:
        min_dist = min(abs(p.x - own_den[0]) + abs(p.y - own_den[1]) for p in opp_pieces)
        penalty = factor_lair_defense * (MAX_DISTANCE - min_dist) ** 1.5  # Non-linear penalty
        score -= penalty

    # 5. Rat Positioning
    player_rat = next((p for p in game.pieces if p.player == player and p.name == "rat"), None)
    if player_rat:
        if is_water(player_rat.x, player_rat.y):
            score += factor_mouse_position  # Control river
        for p in game.pieces:
            if p.player != player and p.name == "elephant" and \
               abs(p.x - player_rat.x) + abs(p.y - player_rat.y) == 1:
                score += factor_mouse_position  # Threaten elephant
    opp_rat = next((p for p in game.pieces if p.player != player and p.name == "rat"), None)
    if opp_rat:
        if is_water(opp_rat.x, opp_rat.y):
            score -= factor_mouse_position
        for p in game.pieces:
            if p.player == player and p.name == "elephant" and \
               abs(p.x - opp_rat.x) + abs(p.y - opp_rat.y) == 1:
                score -= factor_mouse_position

    # 6. Piece Protection
    for piece in game.pieces:
        adjacent = get_adjacent_positions(piece.x, piece.y)
        protectors = sum(1 for pos in adjacent for p in game.pieces if p.player == piece.player and (p.x, p.y) == pos)
        if piece.player == player:
            score += protectors * factor_piece_protection * (Piece.hierarchy[piece.name] / 8)  # Scale by rank
        else:
            score -= protectors * factor_piece_protection * (Piece.hierarchy[piece.name] / 8)

    # 7. Central Control
    central_squares = [(x, y) for x in range(BOARD_COLS) for y in range(BOARD_ROWS)
                       if not is_water(x, y) and any(is_water(nx, ny) for nx, ny in get_adjacent_positions(x, y))]
    for pos in central_squares:
        for p in game.pieces:
            if (p.x, p.y) == pos:
                score += factor_central_control if p.player == player else -factor_central_control

    # 8. Threat Calculation
    player_threats = 0
    opp_threats = 0
    for piece in game.pieces:
        if piece.player == player:
            for adj_pos in get_adjacent_positions(piece.x, piece.y):
                for opp_piece in game.pieces:
                    if opp_piece.player != player and (opp_piece.x, opp_piece.y) == adj_pos and \
                       can_capture(piece, opp_piece, game):
                        player_threats += Piece.hierarchy[opp_piece.name]
        else:
            for adj_pos in get_adjacent_positions(piece.x, piece.y):
                for own_piece in game.pieces:
                    if own_piece.player == player and (own_piece.x, own_piece.y) == adj_pos and \
                       can_capture(piece, own_piece, game):
                        opp_threats += Piece.hierarchy[own_piece.name]
    score += factor_threats * player_threats - factor_threats * opp_threats

    # 9. Lion/Tiger Jump Positioning
    for piece in game.pieces:
        if is_jump_position(piece, game):
            if piece.player == player:
                score += factor_jump_position
            else:
                score -= factor_jump_position

    return score
