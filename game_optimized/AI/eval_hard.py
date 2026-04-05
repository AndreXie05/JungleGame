from game_optimized.main_files.piece import Piece
from game_optimized.main_files.board import is_water

# Score constants for win and loss outcomes
WIN_SCORE = 10000
LOSS_SCORE = -10000
MAX_DISTANCE = 11  # Maximum Manhattan distance possible on the 7x9 board
BOARD_COLS, BOARD_ROWS = 7, 9

# Factors used to weight various strategic elements.
factor_distance = 0.5         # Weight for the bonus based on proximity to opponent's den
factor_mobility = 0.3         # Weight for the number of valid moves (mobility)
factor_trap_control = 0.2     # Weight for controlling squares adjacent to traps
factor_lair_defense = 1.0     # Penalty for enemy pieces approaching own den
factor_mouse_position = 0.1   # Bonus/Penalty for mouse positioning, particularly with water and elephant proximity
factor_piece_protection = 0.1 # Bonus for having adjacent friendly pieces
factor_central_control = 0.05 # Bonus for occupying central positions near water edges

def get_adjacent_positions(x, y):
    """
    Returns adjacent positions (up, down, left, right) that lie within the board boundaries.
    """
    return [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if 0 <= x + dx < BOARD_COLS and 0 <= y + dy < BOARD_ROWS]

def evaluate_hard(game, player):
    """
    Compute a score for the current game state from the perspective of 'player'.
    A higher score indicates a more favorable position for the player.
    """
    # If game has ended, return the win or loss score immediately
    if game.winner is not None:
        return WIN_SCORE if game.winner == player else LOSS_SCORE

    score = 0

    # Define key board elements (traps and dens) based on which player is evaluating
    if player == 1:
        opp_traps = game.traps_2
        own_traps = game.traps_1
        opp_den = game.lair_2  # Opponent's den location (target for pieces)
        own_den = game.lair_1  # Own den location (to defend)
    else:
        opp_traps = game.traps_1
        own_traps = game.traps_2
        opp_den = game.lair_1
        own_den = game.lair_2

    # 1. Evaluate Piece Values and their distances from the opponent's den (or own den for enemy pieces)
    for piece in game.pieces:
        # Pieces on opponent traps have no effective value
        is_on_opp_trap = (piece.x, piece.y) in (opp_traps if piece.player == player else own_traps)
        effective_value = 0 if is_on_opp_trap else Piece.hierarchy[piece.name]

        if piece.player == player:
            # Closer distance to opponent's den gives a higher bonus
            distance = abs(piece.x - opp_den[0]) + abs(piece.y - opp_den[1])
            bonus_distance = (MAX_DISTANCE - distance) * factor_distance
            score += effective_value + bonus_distance
        else:
            # For enemy pieces, closeness to our den is more dangerous
            distance = abs(piece.x - own_den[0]) + abs(piece.y - own_den[1])
            bonus_distance = (MAX_DISTANCE - distance) * factor_distance
            score -= effective_value + bonus_distance

    # 2. Mobility: Reward/penalize based on the number of legal moves each piece has
    for piece in game.pieces:
        mobility = len(game.get_valid_moves(piece))
        score += mobility * factor_mobility if piece.player == player else -mobility * factor_mobility

    # 3. Trap Control: Count friendly pieces adjacent to opponent traps and enemy pieces near own traps
    for trap in opp_traps:
        adjacent = get_adjacent_positions(*trap)
        control = sum(1 for pos in adjacent for p in game.pieces if p.player == player and (p.x, p.y) == pos)
        score += control * factor_trap_control

    for trap in own_traps:
        adjacent = get_adjacent_positions(*trap)
        control = sum(1 for pos in adjacent for p in game.pieces if p.player != player and (p.x, p.y) == pos)
        score -= control * factor_trap_control

    # 4. Lair Defense: Apply a penalty based on the minimum distance of enemy pieces to our den
    opp_pieces = [p for p in game.pieces if p.player != player]
    if opp_pieces:
        min_opp_distance = min(abs(p.x - own_den[0]) + abs(p.y - own_den[1]) for p in opp_pieces)
        penalty = (MAX_DISTANCE - min_opp_distance) * factor_lair_defense
        score -= penalty

    # 5. Mouse Positioning: Special bonus/penalty based on the mouse's position in water and its proximity to elephants
    player_mouse = next((p for p in game.pieces if p.player == player and p.name == "mouse"), None)
    if player_mouse:
        if is_water(player_mouse.x, player_mouse.y):
            score += factor_mouse_position
        # Bonus if enemy elephant is immediately adjacent to our mouse
        for p in game.pieces:
            if p.player != player and p.name == "elephant" and abs(p.x - player_mouse.x) + abs(p.y - player_mouse.y) == 1:
                score += factor_mouse_position

    opp_mouse = next((p for p in game.pieces if p.player != player and p.name == "mouse"), None)
    if opp_mouse:
        if is_water(opp_mouse.x, opp_mouse.y):
            score -= factor_mouse_position
        # Penalty if our elephant is adjacent to the enemy mouse
        for p in game.pieces:
            if p.player == player and p.name == "elephant" and abs(p.x - opp_mouse.x) + abs(p.y - opp_mouse.y) == 1:
                score -= factor_mouse_position

    # 6. Piece Protection: Increase score for having friendly pieces nearby, reduce score if enemy pieces are protecting theirs
    for piece in game.pieces:
        adjacent = get_adjacent_positions(piece.x, piece.y)
        protectors = sum(1 for pos in adjacent for p in game.pieces if p.player == piece.player and (p.x, p.y) == pos)
        score += protectors * factor_piece_protection if piece.player == player else -protectors * factor_piece_protection

    # 7. Central Control: Slight bonus/penalty for pieces on central squares (adjacent to water)
    central_squares = [(x, y) for x in range(BOARD_COLS) for y in range(BOARD_ROWS)
                       if not is_water(x, y) and any(is_water(nx, ny) for nx, ny in get_adjacent_positions(x, y))]
    for pos in central_squares:
        for p in game.pieces:
            if (p.x, p.y) == pos:
                score += factor_central_control if p.player == player else -factor_central_control

    return score
