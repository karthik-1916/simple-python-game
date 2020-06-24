import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from background import Background
import game_functions as gf
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button

pygame.init()
pygame.mixer.init()

black = 0, 0, 0

"""Init settings"""
settings = Settings()

"""Set the display"""
screen = pygame.display.set_mode(settings.screen_size)
"""Set the display caption"""
pygame.display.set_caption(settings.screen_caption)

"""Make a ship"""
ship = Ship(settings, screen)

"""Set the background image of the screen"""
background = Background(settings, screen)

"""Create Group object to hold fleet of enemy ship"""
enemy_ships = Group()
gf.create_fleet(enemy_ships, settings, screen)

"""Create the Group object to store player's ship bullet"""
player_bullets = Group()

"""Enemy Bullets"""
enemy_bullets = Group()

"""Game stats"""
stats = GameStats(settings)
"""Scoreboard"""
score_board = Scoreboard(settings, screen, stats)

"""Play Button"""
play_button = Button(settings, screen, "Play")

"""Explosion"""
exp_sprite = Group()


def run_game():
    """Start the main loop for the game"""
    while True:
        gf.listen_events(ship, player_bullets, settings, screen, stats, score_board, play_button, enemy_ships)

        if stats.game_active:
            ship.update()
            gf.update_bullets(player_bullets, enemy_ships, settings, screen,
                              stats, score_board, ship, enemy_bullets, exp_sprite)
            gf.update_enemy_ships(settings, enemy_ships, stats, screen,
                                  score_board, ship, player_bullets, enemy_bullets)
            # gf.random_fire_bullet(settings, screen, enemy_ships, enemy_bullets)
            # gf.update_enemy_bullets(enemy_bullets, settings)
            gf.check_enemy_bullets_ship_collision(settings, stats, screen, score_board,
                                                  ship, enemy_ships, player_bullets,
                                                  enemy_bullets)

        gf.update_screen(screen, background, ship, enemy_ships, stats, play_button,
                         player_bullets, enemy_bullets, score_board, exp_sprite)


run_game()
