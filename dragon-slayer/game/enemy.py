import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()
        self.attack_pattern = 1  # Example attack pattern

    def update(self):
        if self.attack_pattern == 1:
            # Implement attack pattern 1 logic
            pass
