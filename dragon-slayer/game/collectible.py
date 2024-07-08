import pygame

class Collectible:
    def __init__(self, x, y):
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow color for collectibles
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player, collectibles):
        if self.rect.colliderect(player.rect):
            # Add points to player
            player.score += 10
            collectibles.remove(self)  # Remove collectible from the list

    def draw(self, screen):
        screen.blit(self.image, self.rect)
