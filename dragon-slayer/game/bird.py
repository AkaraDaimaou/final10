import pygame

class Bird:
    def __init__(self, x, y, image, flap_sound):
        self.x = x
        self.y = y
        self.image = image
        self.flap_sound = flap_sound
        self.velocity_y = 0
        self.gravity = 0.5
        self.flap_power = -10

    def flap(self):
        self.velocity_y = self.flap_power
        self.flap_sound.play()

    def move(self, ground):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.y = min(self.y, ground)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
