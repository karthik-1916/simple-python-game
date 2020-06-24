import pygame
from pygame.sprite import Sprite


class Bullets(Sprite):
    """Class to manage bullets fired from the ship"""

    def __init__(self, settings, screen, ship):
        """Create a bullet object at the ship's current position"""
        super(Bullets, self).__init__()
        self.screen = screen
        self.settings = settings
        self.bullet_image = pygame.image.load("images/ship_bullet.png")
        self.rect = self.bullet_image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def blitme(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.bullet_image, self.rect)
