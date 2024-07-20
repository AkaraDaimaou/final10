import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_power = 10
        self.gravity = 1
        self.vel_y = 0
        self.on_ground = False
        self.magic_attack_image = pygame.image.load('assets/magic_attack.png').convert_alpha()  # Magic attack image
        self.magic_attack_limit = 3  # Limit of magic attacks
        self.magic_attacks_available = self.magic_attack_limit

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
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # jumping
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def use_magic_attack(self):
        if self.magic_attacks_available > 0:
            # Implement magic attack logic here
            self.magic_attacks_available -= 1
            return pygame.Rect(self.rect.centerx, self.rect.top, self.magic_attack_image.get_width(), self.magic_attack_image.get_height())
        return None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
