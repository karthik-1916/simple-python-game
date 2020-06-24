import pygame


class Background:
    """Class to create background screen"""

    def __init__(self, screen_settings, screen):

        self.screen = screen

        """Load background image"""
        self.background_image = pygame.image.load("images/space.png")

        """Resizing image to match screen resolution"""
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (screen_settings.screen_width,
                                                        screen_settings.screen_height)
                                                       )
        self.rect = self.background_image.get_rect()
        self.background_imageY1 = 0
        self.background_imageX1 = 0

        self.background_imageY2 = self.background_image.get_height()
        self.background_imageX2 = 0

        self.moving_speed = 0.3

    def update(self):
        self.background_imageY1 -= self.moving_speed
        self.background_imageY2 -= self.moving_speed
        if self.background_imageY1 <= -self.rect.height:
            self.background_imageY1 = self.rect.height
        if self.background_imageY2 <= -self.rect.height:
            self.background_imageY2 = self.rect.height

    def blitme(self):
        self.screen.blit(self.background_image, (0, self.background_imageY1))
        self.screen.blit(self.background_image, (0, self.background_imageY2))
