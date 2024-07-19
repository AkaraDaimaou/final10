import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('..//assets//boss.png')
        self.rect = self.image.get_rect()
        self.health = 100
        self.damage_after_half_health = True

    def update(self):
        if self.damage_after_half_health and self.health <= 50:
            # Implement damage dealing logic
            pass

    def special_attack(self):
        # Implement special attack pattern
        pass
