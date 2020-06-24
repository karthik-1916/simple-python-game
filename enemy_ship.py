from pygame.sprite import Sprite
import pygame


class EnemyShip(Sprite):
    """A class to repreasent a single pumpkin in the fleet"""

    def __init__(self, settings, screen):
        """Initialize the enemy_ship and set ites starting position"""
        super(EnemyShip, self).__init__()
        self.screen = screen
        self.settings = settings

        """Load the enemy_ship image and set its rect attributes"""
        self.image = pygame.image.load("images/enemy_ship.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect.width, self.rect.height = 60, 60

        """Start each new ship near the top left of the screen"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """Store the ship's exact position"""
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.enemy_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """Return true if ships is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
