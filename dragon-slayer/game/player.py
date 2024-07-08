import pygame

class Player:
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.speed = 5
        self.jump_power = 10
        self.gravity = 1
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.check_collision(platforms)

    def check_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
