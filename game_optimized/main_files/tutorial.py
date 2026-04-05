import pygame
import sys
import textwrap
import os

def draw_wrapped_text_centered(surface, text, font, color, rect, line_spacing=1.5, max_chars=45):
    wrapped_lines = textwrap.wrap(text, width=max_chars)
    line_height = font.get_linesize() * line_spacing
    total_text_height = len(wrapped_lines) * line_height
    start_y = rect.centery - total_text_height // 2

    for line in wrapped_lines:
        line_surface = font.render(line, True, color)
        line_width = line_surface.get_width()
        x = rect.centerx - line_width // 2
        surface.blit(line_surface, (x, start_y))
        start_y += line_height

def load_page_images(num_pages):
    images = []
    for i in range(num_pages):
        image_path = f"images/page_{i}.png"
        if os.path.exists(image_path):
            img = pygame.image.load(image_path)
            img = pygame.transform.scale(img, (550, 450))  # imagem maior e mais larga
            images.append(img)
        else:
            images.append(None)
    return images

def tutorial_mode():
    pygame.init()
    screen_width, screen_height = 700, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Jungle Game - Tutorial")

    background_image = pygame.image.load("images/tutorial_image.jpeg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    next_button = pygame.image.load("images/next_button.jpng")
    next_button = pygame.transform.scale(next_button, (50, 50))
    back_button = pygame.image.load("images/back_button.jpng")
    back_button = pygame.transform.scale(back_button, (50, 50))

    next_button_rect = next_button.get_rect(topleft=(screen_width - 80, screen_height - 80))
    back_button_rect = back_button.get_rect(topleft=(30, screen_height - 80))

    title_font = pygame.font.Font(None, 64)
    text_font = pygame.font.Font(None, 36)
    instruction_font = pygame.font.Font(None, 28)

    tutorial_pages = [
        "Welcome to The Jungle Game! In this tutorial you will learn the basic rules for playing.",
        "Objective: Capture the opponent's lair or eliminate all of the opponent's pieces to win.",
        "Hierarchy: Each piece has a value and quality. Pieces of higher value capture pieces of the same value or those of lower value.",
        "Special Rule: The Rat can capture the Elephant, even though it is a piece with a lower hierarchical value.",
        "Special Rule: Both the Tiger and the Lion can make jumps across the water, unless the Rat is blocking the way.",
        "Strategy: The Rat is a very important piece strategically!",
        "Moves: Select an animal and see the valid moves highlighted on the board.",
        "Remember: Strategy and positioning are essential to achieving victory. Have fun!"
        ]

    page_images = load_page_images(len(tutorial_pages))
    current_page = 0
    clock = pygame.time.Clock()

    text_color = (255, 100, 0)

    while True:
        screen.blit(background_image, (0, 0))

        # Título
        title_surface = title_font.render("Tutorial", True, text_color)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 60))
        screen.blit(title_surface, title_rect)

        # Texto do tutorial (reposicionado mais para baixo)
        text_rect = pygame.Rect(50, 130, screen_width - 100, 150)
        draw_wrapped_text_centered(
            screen, tutorial_pages[current_page], text_font,
            text_color, text_rect, line_spacing=1.5, max_chars=50
        )

        # Imagem centralizada e maior
        img = page_images[current_page]
        if img:
            img_rect = img.get_rect(center=(screen_width // 2, 480))  # mais abaixo
            screen.blit(img, img_rect)

        # Instruções reposicionadas na parte inferior
        instruction_rect = pygame.Rect(50, 820, screen_width - 100, 60)
        instructions_text = "ESC: Leave"
        draw_wrapped_text_centered(screen, instructions_text, instruction_font, text_color, instruction_rect, max_chars=60)

        # Botões
        screen.blit(next_button, next_button_rect.topleft)
        screen.blit(back_button, back_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT and current_page < len(tutorial_pages) - 1:
                    current_page += 1
                elif event.key == pygame.K_LEFT and current_page > 0:
                    current_page -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos) and current_page < len(tutorial_pages) - 1:
                    current_page += 1
                elif back_button_rect.collidepoint(event.pos) and current_page > 0:
                    current_page -= 1

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    tutorial_mode()