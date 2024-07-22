import pygame
import os
import sys

def load_image(image_name, script_dir):
    try:
        image_path = os.path.join(script_dir, "images", image_name)
        return pygame.image.load(image_path)
    except Exception as e:
        print(f"Unable to load image {image_path}: {e}")
        sys.exit(1)

def load_sound(sound_name, script_dir):
    try:
        sound_path = os.path.join(script_dir, "sounds", sound_name)
        return pygame.mixer.Sound(sound_path)
    except Exception as e:
        print(f"Unable to load sound {sound_path}: {e}")
        sys.exit(1)
