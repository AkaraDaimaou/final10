# enemy.py
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, behavior):
        super().__init__()
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.behavior = behavior
        self.direction = 1
        self.speed = 2

    def update(self, player=None):
        if self.behavior == 'patrol':
            self.patrol()
        elif self.behavior == 'follow' and player:
            self.follow(player)

    def patrol(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > 800:
            self.direction *= -1

    def follow(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        elif player.rect.x < self.rect.x:
            self.rect.x -= self.speed
