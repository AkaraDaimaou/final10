import pygame

class Enemy:
    def __init__(self, x, y, behavior='patrol'):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1
        self.behavior = behavior  # Patrol or chase

    def update(self, player):
        if self.behavior == 'patrol':
            self.rect.x += self.speed * self.direction
            if self.rect.right >= 800 or self.rect.left <= 0:
                self.direction *= -1
        elif self.behavior == 'chase':
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.speed
            if player.rect.y > self.rect.y:
                self.rect.y += self.speed
            elif player.rect.y < self.rect.y:
                self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
