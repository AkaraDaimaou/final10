import pygame
from player import Player
from enemy import Enemy
from platform import Platform
from powerup import PowerUp
from collectible import Collectible

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Dragon Slayer')

clock = pygame.time.Clock()

# Load images
background = pygame.image.load('assets/images/background.png')

# Initialize game components
player = Player()
powerups = [PowerUp(300, 450)]
collectibles = [Collectible(200, 400)]
enemies = [Enemy(400, 100, 'patrol')]
platforms = [Platform(200, 500, 400, 20), Platform(100, 400, 200, 20), Platform(400, 300, 200, 20)]

running = True
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
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
