import pygame
import sys
import importlib
import game_optimized.AI.ai_vs_p_main as ai_vs_player

# Import WIDTH and HEIGHT from the configuration module.
# These values define the dimensions of the game window.
from game_optimized.main_files.config import WIDTH, HEIGHT

# Initialize the pygame library so that we can start using its functions.
pygame.init()

# Create the game window using the imported WIDTH and HEIGHT,
# and set the title of the window to "Jungle Game".
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Game")

# Define commonly used colors (RGB format).
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Set up the fonts for the title and buttons.
# 'None' uses the default font; larger sizes are used for titles.
title_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 36)

# Try to load the background image for the lobby, and scale it to the screen dimensions.
# If the image fails to load, print an error and set background_image to None.
try:
    background_image = pygame.image.load("images/lobby_background.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Error loading background image: {e}")
    background_image = None

# Options for different game modes along with the paths to their respective modules.
# Each tuple contains the text to display and the module path that should be loaded.
options = [
    ("Player vs Player", "game_optimized.Player's.p_vs_p_main"),
    ("Random vs Player", "game_optimized.Random.p_vs_rand_main"),
    ("Random vs Random", "game_optimized.Random.rand_vs_rand_main"),
    ("Ai vs Player", "game_optimized.AI.ai_vs_p_main"),  # Default module for minimax AI
    ("Ai vs Ai", "game_optimized.AI.ai_vs_ai_main"),
    ("Tutorial", "game_optimized.main_files.Tutorial")
]

# -------------------------
# Main Menu Layout Settings
# -------------------------
# Calculate the size and position for each menu button.
button_width = 400     # Width of each button
button_height = 60     # Height of each button
button_margin = 30     # Space between buttons
start_y = 200          # Vertical starting position for the first button

# Create a list to store button rectangles along with their display text and associated module path.
buttons = []
for idx, (text, module_path) in enumerate(options):
    x = (WIDTH - button_width) // 2  # Center the button horizontally
    y = start_y + idx * (button_height + button_margin)  # Distribute buttons vertically
    rect = pygame.Rect(x, y, button_width, button_height)
    buttons.append((rect, text, module_path))

# Define a global rectangle for the Config button in the lower right corner.
CONFIG_BUTTON_RECT = pygame.Rect(WIDTH - 120 - 20, HEIGHT - 40 - 40, 120, 40)

def draw_menu():
    """
    Renders the main menu screen.
    Draws the background (or white fill if no image),
    adds a semi-transparent overlay to soften the background,
    renders the title and each menu button, including a separate Config button.
    """
    # Display background image if available, otherwise fill the screen with white.
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)
    
    # Create and apply a translucent white overlay over the background.
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(WHITE)
    screen.blit(overlay, (0, 0))
    
    # Draw the title of the game, centered at the top.
    title_text = title_font.render("Welcome to the Jungle Game!", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_text, title_rect)
    
    # Draw each of the buttons defined in the "buttons" list.
    for rect, text, _ in buttons:
        pygame.draw.rect(screen, LIGHT_BLUE, rect)  # Draw button background
        pygame.draw.rect(screen, BLACK, rect, 2)     # Draw button border
        text_surface = button_font.render(text, True, BLACK)  # Render button text
        text_rect = text_surface.get_rect(center=rect.center)  # Center text on button
        screen.blit(text_surface, text_rect)
    
    # Draw the Config button in the lower right using the global variable.
    pygame.draw.rect(screen, LIGHT_BLUE, CONFIG_BUTTON_RECT)
    pygame.draw.rect(screen, BLACK, CONFIG_BUTTON_RECT, 2)
    config_text = button_font.render("Config", True, BLACK)
    config_text_rect = config_text.get_rect(center=CONFIG_BUTTON_RECT.center)
    screen.blit(config_text, config_text_rect)
    
    # Update the display to show all drawn elements.
    pygame.display.flip()

# ------------------------------
# Image Selection Menu Setup
# ------------------------------
def image_selection_menu():
    """
    Displays an image selection menu that allows the player
    to choose between two different sets of images ("v1" or "v2").
    If preview images cannot be loaded, an error is printed.
    """
    from game_optimized.main_files.images import update_images

    try:
        # Load preview images for selection.
        img_v1 = pygame.image.load("images/images_v1.png")
        img_v2 = pygame.image.load("images/images_v2.png")
    except Exception as e:
        print(f"Error loading preview images: {e}")
        return

    preview_width = 900
    # Determine background dimensions. If no background image, use screen dimensions.
    bg_width = background_image.get_width() if background_image else WIDTH
    bg_height = background_image.get_height() if background_image else HEIGHT
    preview_height = int(preview_width * bg_height / bg_width)
    
    # Scale the preview images to calculated dimensions.
    img_v1 = pygame.transform.scale(img_v1, (preview_width, preview_height))
    img_v2 = pygame.transform.scale(img_v2, (preview_width, preview_height))
    
    # Position the preview images in the left and right thirds of the screen.
    img_v1_rect = img_v1.get_rect(center=(WIDTH // 3, HEIGHT // 2))
    img_v2_rect = img_v2.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))
    
    # Determine a dividing vertical line between the two images.
    dividing_x = (img_v1_rect.centerx + img_v2_rect.centerx) // 2
    
    # Set up clickable areas for each preview.
    v1_select_rect = pygame.Rect(
        img_v1_rect.left, img_v1_rect.top,
        dividing_x - img_v1_rect.left, img_v1_rect.height
    )
    v2_select_rect = pygame.Rect(
        dividing_x, img_v2_rect.top,
        img_v2_rect.right - dividing_x, img_v2_rect.height
    )
    
    # Create a Back button centered at the bottom of the screen.
    back_rect = pygame.Rect((WIDTH - 250) // 2, HEIGHT - 100, 250, 60)
    
    selecting = True
    while selecting:
        # Render the background and overlay.
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        # Display the title for this menu.
        title = title_font.render("Select Your Animals", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Draw both preview images on the screen.
        screen.blit(img_v1, img_v1_rect)
        screen.blit(img_v2, img_v2_rect)
        
        # Draw the Back button.
        pygame.draw.rect(screen, LIGHT_BLUE, back_rect)
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        back_text = button_font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        
        # Check for user events like quitting the game or clicking on a selection.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the left mouse button is clicked...
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Check if image v1 area was clicked.
                if v1_select_rect.collidepoint(mouse_pos):
                    update_images("v1")
                    print("Selected Images v1")
                    selecting = False
                # Check if image v2 area was clicked.
                elif v2_select_rect.collidepoint(mouse_pos):
                    update_images("v2")
                    print("Selected Images v2")
                    selecting = False
                # If Back button is clicked, exit image selection.
                elif back_rect.collidepoint(mouse_pos):
                    selecting = False

# ---------------------------
# Configuration Menu Setup
# ---------------------------
def configuration_menu():
    """
    Opens the configuration menu where users can change settings
    like image selection, volume adjustment, and toggling sound on/off.
    """
    config_running = True
    btn_width = 250
    btn_height = 60
    btn_margin = 25
    
    # Define rectangles for buttons. These are centered horizontally.
    images_rect = pygame.Rect((WIDTH - btn_width) // 2, 140, btn_width, btn_height)
    volume_title_pos = (WIDTH // 2, 230)  # Position for volume title text

    # Set up volume control buttons (minus and plus) for decreasing/increasing volume.
    vol_btn_size = 60
    vol_minus_rect = pygame.Rect(WIDTH // 2 - 90, 280, vol_btn_size, vol_btn_size)
    vol_plus_rect = pygame.Rect(WIDTH // 2 + 30, 280, vol_btn_size, vol_btn_size)

    # Define a button to toggle sound on/off.
    sound_button_rect = pygame.Rect((WIDTH - btn_width) // 2, 360, btn_width, btn_height)
    
    sound_on = True  # Initial state: sound is enabled

    # Set up a Back button to exit the configuration menu.
    back_rect = pygame.Rect((WIDTH - btn_width) // 2, 440, btn_width, btn_height)

    while config_running:
        # Display the background and overlay for the menu.
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        # Render the title "Configuration" at the top.
        config_title = title_font.render("Configuration", True, BLACK)
        config_title_rect = config_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(config_title, config_title_rect)

        # Render the Images button.
        pygame.draw.rect(screen, LIGHT_BLUE, images_rect)
        pygame.draw.rect(screen, BLACK, images_rect, 2)
        images_text = button_font.render("Images", True, BLACK)
        images_text_rect = images_text.get_rect(center=images_rect.center)
        screen.blit(images_text, images_text_rect)

        # Display the volume label.
        vol_title = button_font.render("Volume", True, BLACK)
        vol_title_rect = vol_title.get_rect(center=volume_title_pos)
        screen.blit(vol_title, vol_title_rect)

        # Render the minus button for volume decrease.
        pygame.draw.rect(screen, LIGHT_BLUE, vol_minus_rect)
        pygame.draw.rect(screen, BLACK, vol_minus_rect, 2)
        minus_text = button_font.render("-", True, BLACK)
        minus_rect = minus_text.get_rect(center=vol_minus_rect.center)
        screen.blit(minus_text, minus_rect)

        # Render the plus button for volume increase.
        pygame.draw.rect(screen, LIGHT_BLUE, vol_plus_rect)
        pygame.draw.rect(screen, BLACK, vol_plus_rect, 2)
        plus_text = button_font.render("+", True, BLACK)
        plus_rect = plus_text.get_rect(center=vol_plus_rect.center)
        screen.blit(plus_text, plus_rect)

        # Display the current volume percentage.
        current_volume = pygame.mixer.music.get_volume()
        vol_value_text = button_font.render(f"{int(current_volume * 100)}%", True, BLACK)
        vol_value_rect = vol_value_text.get_rect(center=(WIDTH // 2, 330))
        screen.blit(vol_value_text, vol_value_rect)

        # Render the sound on/off button with its current state.
        sound_text = "Sound: ON" if sound_on else "Sound: OFF"
        pygame.draw.rect(screen, LIGHT_BLUE, sound_button_rect)
        pygame.draw.rect(screen, BLACK, sound_button_rect, 2)
        sound_text_surface = button_font.render(sound_text, True, BLACK)
        sound_text_rect = sound_text_surface.get_rect(center=sound_button_rect.center)
        screen.blit(sound_text_surface, sound_text_rect)

        # Draw the Back button to exit to the previous menu.
        pygame.draw.rect(screen, LIGHT_BLUE, back_rect)
        pygame.draw.rect(screen, BLACK, back_rect, 2)
        back_text = button_font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        
        # Process user events for configuration options.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # If Images button is clicked, open image selection menu.
                if images_rect.collidepoint(mouse_pos):
                    image_selection_menu()
                # If volume minus is clicked, lower the volume.
                elif vol_minus_rect.collidepoint(mouse_pos):
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = max(0.0, round(current_volume - 0.05, 2))
                    pygame.mixer.music.set_volume(new_volume)
                # If volume plus is clicked, increase the volume.
                elif vol_plus_rect.collidepoint(mouse_pos):
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = min(1.0, round(current_volume + 0.05, 2))
                    pygame.mixer.music.set_volume(new_volume)
                # Toggle sound state when clicking the sound button.
                elif sound_button_rect.collidepoint(mouse_pos):
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                # Exit configuration if Back is clicked.
                elif back_rect.collidepoint(mouse_pos):
                    config_running = False

# ---------------------------
# Difficulty Selection Menu Setup
# ---------------------------
def difficulty_menu():
    """
    Presents a menu that lets the player choose between various difficulty levels.
    Returns the string corresponding to the chosen difficulty.
    """
    difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Impossible", "impossible")]
    diff_button_width = 300
    diff_button_height = 60
    diff_button_margin = 30
    diff_start_y = 200

    # Build a list of buttons for each difficulty level.
    diff_buttons = []
    for idx, (text, level) in enumerate(difficulties):
        x = (WIDTH - diff_button_width) // 2
        y = diff_start_y + idx * (diff_button_height + diff_button_margin)
        rect = pygame.Rect(x, y, diff_button_width, diff_button_height)
        diff_buttons.append((rect, text, level))
    
    selecting = True
    while selecting:
        # Redraw background and overlay for each frame.
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        # Display the "Select Difficulty" title.
        diff_title = title_font.render("Select Difficulty", True, BLACK)
        diff_title_rect = diff_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(diff_title, diff_title_rect)
        
        # Draw each difficulty button.
        for rect, text, _ in diff_buttons:
            pygame.draw.rect(screen, LIGHT_BLUE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text_surface = button_font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        # Process mouse events to determine if a button is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for rect, text, level in diff_buttons:
                    if rect.collidepoint(mouse_pos):
                        return level  # Return the chosen difficulty level.
    return None

# ---------------------------
# Algorithm Selection Menu Setup
# ---------------------------
def algorithm_selection_menu(chosen_eval):
    """
    Opens a menu that lets the player choose the algorithm for AI.
    The player can choose between Minimax (default) and Negamax.
    The chosen evaluation function is passed along to the game module.
    """
    algo_running = True
    algo_button_width = 300
    algo_button_height = 60
    algo_button_margin = 30
    algo_start_y = 200

    # Create button rectangles for both algorithm options.
    minimax_rect = pygame.Rect((WIDTH - algo_button_width) // 2, algo_start_y, algo_button_width, algo_button_height)
    negamax_rect = pygame.Rect((WIDTH - algo_button_width) // 2, algo_start_y + algo_button_height + algo_button_margin, algo_button_width, algo_button_height)

    while algo_running:
        # Render the menu background.
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))
        
        # Display the title for algorithm selection.
        algo_title = title_font.render("Select Algorithm", True, BLACK)
        algo_title_rect = algo_title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(algo_title, algo_title_rect)
        
        # Draw the Minimax button.
        pygame.draw.rect(screen, LIGHT_BLUE, minimax_rect)
        pygame.draw.rect(screen, BLACK, minimax_rect, 2)
        minimax_text = button_font.render("Minimax", True, BLACK)
        minimax_text_rect = minimax_text.get_rect(center=minimax_rect.center)
        screen.blit(minimax_text, minimax_text_rect)
        
        # Draw the Negamax button.
        pygame.draw.rect(screen, LIGHT_BLUE, negamax_rect)
        pygame.draw.rect(screen, BLACK, negamax_rect, 2)
        negamax_text = button_font.render("Negamax", True, BLACK)
        negamax_text_rect = negamax_text.get_rect(center=negamax_rect.center)
        screen.blit(negamax_text, negamax_text_rect)
        
        pygame.display.flip()
        
        # Process events for algorithm selection.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if minimax_rect.collidepoint(mouse_pos):
                    try:
                        # If Minimax is selected, import the corresponding function and call game main.
                        from game_optimized.AI.minimax_rand import get_best_move
                        ai_vs_player.main(chosen_eval, get_best_move)
                    except ImportError as e:
                        print(f"Error importing minimax module: {e}")
                    algo_running = False
                elif negamax_rect.collidepoint(mouse_pos):
                    try:
                        # If Negamax is selected, import the corresponding function and call game main.
                        from game_optimized.AI.negamax import get_best_move
                        ai_vs_player.main(chosen_eval, get_best_move)
                    except ImportError as e:
                        print(f"Error importing negamax module: {e}")
                    algo_running = False

def launch_game(module_path, difficulty=None):
    """
    Launches the selected game mode by:
    - Stopping any existing music
    - Loading the game's music
    - Importing the game module dynamically based on module_path and starting the main function.
    """
    try:
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load("sounds/game_sound.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop the music indefinitely
        except Exception as music_err:
            print(f"Error loading gameplay music: {music_err}")

        # Dynamically import the module for the chosen game mode.
        game_module = importlib.import_module(module_path)
        if hasattr(game_module, "main"):
            # Pass the selected difficulty (if any) to the game module.
            if difficulty is not None:
                game_module.main(difficulty)
            else:
                game_module.main()
        else:
            print(f"No 'main' function found in module {module_path}")
    except ImportError as e:
        print(f"Error importing module {module_path}: {e}")

def main_menu():
    """
    Displays the main menu loop that:
    - Draws the menu
    - Detects clicks on game mode buttons or the config button
    - Launches the corresponding game mode or configuration screen
    """
    running = True
    clock = pygame.time.Clock()
    while running:
        draw_menu()
        # Check for user events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If left mouse button is clicked:
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # First check if the Config button was clicked.
                if CONFIG_BUTTON_RECT.collidepoint(event.pos):
                    configuration_menu()
                    continue

                # Check which game mode button was clicked.
                for rect, text, module_path in buttons:
                    if rect.collidepoint(event.pos):
                        if text == "Tutorial":
                            # Open the tutorial mode.
                            import game_optimized.main_files.tutorial as tutorial
                            tutorial.tutorial_mode()
                        elif text == "Ai vs Player":
                            # For the "Ai vs Player" option, show the difficulty menu first.
                            difficulty = difficulty_menu()
                            if difficulty not in ("easy", "medium", "hard", "impossible"):
                                print("Invalid difficulty selected.")
                                continue
                            # Based on the chosen difficulty, select the corresponding evaluation function.
                            if difficulty == "easy":
                                from game_optimized.AI.eval_easy import evaluate_easy as chosen_eval
                            elif difficulty == "medium":
                                from game_optimized.AI.eval_medium import evaluate_medium as chosen_eval
                            elif difficulty == "hard":
                                from game_optimized.AI.eval_hard import evaluate_hard as chosen_eval
                            elif difficulty == "impossible":
                                from game_optimized.AI.eval_impossible import evaluate_impossible as chosen_eval
                            
                            # Open the algorithm selection menu so the user can choose between Minimax and Negamax.
                            algorithm_selection_menu(chosen_eval)
                        else:
                            # For all other modes, launch the game with the module path.
                            launch_game(module_path)
        clock.tick(60)  # Limit the loop to 60 frames per second.

if __name__ == "__main__":
    # Initialize the mixer for playing sound effects and background music.
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/home_screen_sound.mp3")
        pygame.mixer.music.set_volume(0.31)
        pygame.mixer.music.play(-1)  # Play the home screen music in a loop.
    except Exception as e:
        print(f"Error loading background music: {e}")

    # Enter the main menu loop when the script is run directly.
    main_menu()
