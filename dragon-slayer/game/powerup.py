import pygame

class PowerUp:
    def __init__(self, x, y):
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))  # Blue color for power-up
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player):
        if self.rect.colliderect(player.rect):
            # Example: Increase player speed for 10 seconds
            player.speed *= 2
            pygame.time.set_timer(pygame.USEREVENT, 10000)  # 10 seconds
            self.rect.x, self.rect.y = -100, -100  # Remove power-up from screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)
