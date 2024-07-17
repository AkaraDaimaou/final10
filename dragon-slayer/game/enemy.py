import pygame

class Enemy:
    def __init__(self):
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 100
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
