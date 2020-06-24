import random
from pygame.sprite import Sprite
import pygame


class EnemyBullet(Sprite):

    def __init__(self, sp_settings, screen, enemy_ships):
        super(EnemyBullet, self).__init__()

        self.sp_settings = sp_settings
        self.enemy_bullet_image = pygame.image.load('images/enemy_bomb.png')
        self.rect = self.enemy_bullet_image.get_rect()
        self.enemy_bullet_image = pygame.transform.scale(self.enemy_bullet_image, (40, 40))
        self.rect.width, self.rect.height = 40, 40
        self.screen = screen
        self.enemy_ship = enemy_ships

        self.rect.center = random.choice(list(self.enemy_ship)).rect.center
        self.rect.top = random.choice(list(self.enemy_ship)).rect.top
        self.y = self.rect.y

    def update(self):
        self.y += self.sp_settings.enemy_ship_bullet_speed_factor
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.enemy_bullet_image, self.rect)
