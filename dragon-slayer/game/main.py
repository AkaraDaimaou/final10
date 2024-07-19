import pygame
import time
from player import Player
from enemy import Enemy
from platform import Platform
from powerup import PowerUp
from collectible import Collectible

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/health_potion.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def transition_effect(screen):
    for alpha in range(0, 300):
        screen.fill((0, 0, 0, alpha))
        pygame.display.update()
        time.sleep(0.01)

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Dragon Slayer')

clock = pygame.time.Clock()

# Load images
background = pygame.image.load('assets/background.png')

# Initialize game components
player = Player()
powerups = [PowerUp(300, 450)]
collectibles = [Collectible(200, 400)]
enemies = [Enemy(400, 100, 'patrol')]
platforms = [Platform(200, 500, 400, 20), Platform(100, 400, 200, 20), Platform(400, 300, 200, 20)]
health_potions = [HealthPotion(250, 350)]

running = True
transition_effect(screen)  # Call the transition effect at the start of the game

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    player.update(platforms)
    for powerup in powerups:
        powerup.update(player)
        powerup.draw(screen)
    for collectible in collectibles:
        collectible.update(player, collectibles)
        collectible.draw(screen)
    for enemy in enemies:
        enemy.update(player)
        enemy.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    for health_potion in health_potions:
        screen.blit(health_potion.image, (health_potion.rect.x, health_potion.rect.y))
    
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
