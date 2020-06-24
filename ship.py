import pygame
import os
from pygame.sprite import Sprite


def load_image(name):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error.message:
        print('Cannot load image:', fullname)
        raise SystemExit.message

    return image, image.get_rect()


class Ship(Sprite):

    def __init__(self, ship_setting, screen):
        """Initialize the ship and its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ship_setting = ship_setting

        """Load the ship image and get its rect"""
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.rect.width, self.rect.height = 40, 60
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.screen_rect = self.screen.get_rect()

        """Start each new ship at the bottom center of the screen"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        """Store a decimal value for the ship's center"""
        self.center = float(self.rect.centerx)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position on the movement flag
        Update the ship's center value, not the rect"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += 1.5
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= 1.5

        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
