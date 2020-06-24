from pygame.sprite import Sprite
import pygame


class Explosion(Sprite):

    def __init__(self, screen, center):
        super(Explosion, self).__init__()

        # Load the image
        self.center = center
        self.screen = screen
        self.image = pygame.image.load('images/explosion.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)
