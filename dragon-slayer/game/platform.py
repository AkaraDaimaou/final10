import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load('assets/platform.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
