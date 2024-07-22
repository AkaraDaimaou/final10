import pygame
import random

class Pipe:
    def __init__(self, x, y_top, y_bottom, image_up, image_down):
        self.x = x
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.image_up = image_up
        self.image_down = image_down

    def move(self, velocity_x):
        self.x += velocity_x

    @staticmethod
    def create_pipe(window_width, window_height, image_up, image_down):
        gap = random.randint(150, 250)  # Varying pipe gap
        pipe_height = image_up.get_height()
        y_pos = random.randint(int(window_height * 0.3), int(window_height * 0.6))
        return [
            Pipe(window_width, y_pos - pipe_height, y_pos + gap, image_up, image_down),
            Pipe(window_width + window_width / 2, y_pos - pipe_height, y_pos + gap, image_up, image_down)
        ]
