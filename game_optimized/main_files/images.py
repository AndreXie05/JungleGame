import pygame
import os
from game_optimized.main_files.config import TILE_SIZE

def load_images(version="v1"):  # Default to v1
    images = {}
    pieces = ["elephant", "lion", "tiger", "leopard", "dog", "wolf", "cat", "mouse"]
    for piece in pieces:
        for player in [1, 2]:
            key = piece + f"_{player}"
            filename = f"{piece}_{player}.png" if version == "v1" else f"{piece}_{player}_v2.png"
            img = pygame.image.load(os.path.join("images", filename))
            images[key] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return images

# Global variable to store the selected version
selected_version = "v2"
images = load_images(selected_version)

def update_images(version):
    global images, selected_version
    selected_version = version
    images = load_images(version)