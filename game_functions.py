import sys
import pygame
from bullets import Bullets
from enemy_ship import EnemyShip
import random
from enemy_bullet import EnemyBullet
from time import sleep
from explosion import Explosion
import logging


# noinspection PyUnreachableCode
def listen_events(ship, bullets, settings, screen, stats,
                  scoreboard, play_button, enemy_ships):
    """Listen to key presses"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            """Listen to keydown presses"""
        elif event.type == pygame.KEYDOWN:
            listen_keydown_event(event, ship, bullets, settings, screen)

            """Listen to keyup presses"""
        elif event.type == pygame.KEYUP:
            listen_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, scoreboard,
                              play_button, ship, enemy_ships, bullets,
                              mouse_x, mouse_y)


def listen_keydown_event(event, ship, bullets, settings, screen):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, settings, screen, ship)


def listen_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(bullets, enemy_ships, settings, screen,
                   stats, scoreboard, ship, enemy_bullets, exp_sprite):
    """Update the position of the bullet and
    remove from the sprite as soon it looses focus"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Check for any bullet that have hit enemy_ships.
    # If so, get rid of the bullet and enemy_ship.
    check_bullet_enemy_ship_collisions(settings, screen, stats, scoreboard, ship,
                                       enemy_ships, bullets, enemy_bullets,
                                       exp_sprite)


def check_bullet_enemy_ship_collisions(settings, screen, stats, scoreboard,
                                       ship, enemy_ships, bullets, enemy_bullets,
                                       exp_sprite):
    """Respond to bullet-enemy_ship collisions."""
    # Remove any bullets and enemy_ship that have collected.
    collision = pygame.sprite.groupcollide(bullets, enemy_ships, True, True)
    if collision:
        for enemy_ship in collision.values():
            stats.score += settings.enemy_ship_points * len(enemy_ship)
            for al in enemy_ship:
                exp = Explosion(screen, al.rect.center)
                exp_sprite.add(exp)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(enemy_ships) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        enemy_bullets.empty()
        settings.increase_speed()

        # Increase the level
        stats.level += 1
        scoreboard.prep_level()

        create_fleet(enemy_ships, settings, screen)


def update_screen(screen, background, ship, enemy_ships, stats,
                  play_button, bullets, enemy_bullets, scoreboard, exp_sprite):
    # screen.fill(black)
    """Update the background"""
    background.update()
    background.blitme()

    """Redraw all bullets behind ship and enemy_ships"""
    for bullet in bullets.sprites():
        bullet.blitme()

    for en_bullet in enemy_bullets.sprites():
        en_bullet.blitme()

    for exp in exp_sprite:
        exp.blitme()

    exp_sprite.empty()

    """Update the ship"""
    ship.blitme()

    """Draw enemy_ships"""
    enemy_ships.draw(screen)

    """Draw score"""
    scoreboard.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        enemy_bullets.empty()
        play_button.draw_button()

    """Make the most recently drawn screen visible"""
    pygame.display.flip()


def fire_bullet(bullets, settings, screen, ship):
    """Function to fire bullet when player presses space button"""
    if len(bullets) < settings.bullets_allowed:
        new_player_bullet = Bullets(settings, screen, ship)
        bullets.add(new_player_bullet)


def update_enemy_ships(settings, enemy_ships, stats, screen,
                       scoreboard, ship, bullets, enemy_bullets):
    """Update the position of all ships in fleet"""
    """Check if the fleet is at the edge,
    and the update the position of all enemy_ships in the fleet"""
    check_fleet_edges(settings, enemy_ships)
    enemy_ships.update()

    check_enemy_ships_bottom(settings, stats, screen, scoreboard,
                             ship, enemy_ships, bullets, enemy_bullets)


def check_enemy_ships_bottom(sp_settings, stats, screen, sb, ship,
                             enemy_ships, bullets, enemy_bullets):
    """Check if any enemy_ships have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for enemy_ship in enemy_ships.sprites():
        if enemy_ship.rect.bottom >= screen_rect.bottom:
            ship_hit(sp_settings, stats, screen, sb, ship,
                     enemy_ships, bullets, enemy_bullets)
            break


def check_fleet_edges(settings, enemy_ships):
    """Respond Appropriately if any ship have reached an edge"""
    for ship in enemy_ships.sprites():
        if ship.check_edge():
            change_fleet_direction(settings, enemy_ships)
            break


def change_fleet_direction(settings, enemy_ships):
    for ship in enemy_ships.sprites():
        ship.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def create_fleet(enemy_ships, settings, screen):
    """Create a full fleet of ships"""
    enemy_ship = EnemyShip(settings, screen)
    number_ship_x = get_number_ship_x(settings, enemy_ship.rect.width)
    number_ship_y = get_number_ship_y(settings, enemy_ship.rect.height)

    for row_number in range(number_ship_y):
        for ship_number in range(number_ship_x):
            ship = EnemyShip(settings, screen)
            ship_width = ship.rect.width
            ship.x = ship_width + 2 * ship_width * ship_number
            ship.rect.x = ship.x
            ship.rect.y = ship.rect.height + 2 * ship.rect.height * row_number
            enemy_ships.add(ship)


def get_number_ship_x(settings, enemy_ship_width):
    available_space_x = settings.screen_width - (2 * enemy_ship_width)
    return int(available_space_x / (2 * enemy_ship_width))


def get_number_ship_y(settings, enemy_ship_height):
    available_ship_y = (settings.screen_height - (3 * enemy_ship_height) - enemy_ship_height)
    return int(available_ship_y / (2 * enemy_ship_height))


def check_play_button(settings, screen, stats, sb, play_button, ship, enemy_ships, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        settings.initialize_dynamic_settings()

        # Hide the mouse curser
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard image.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of enemy_ships and bullets.
        enemy_ships.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(enemy_ships, settings, screen)
        ship.center_ship()


def random_fire_bullet(settings, screen, enemy_ships, enemy_bullets):
    dt = 5
    timer = random.randint(2, 300)

    if len(enemy_ships) <= 15:
        timer = random.randint(2, 500)

    if len(enemy_ships) <= 10:
        timer = random.randint(2, 700)

    if len(enemy_ships) < 5:
        timer = random.randint(2, 1000)
    timer -= dt
    if timer <= 0:
        fire_enemy_bullets(settings, screen, enemy_ships, enemy_bullets)


def fire_enemy_bullets(settings, screen, enemy_ships, enemy_bullets):
    # Firing enemy bullet
    en_bullet = EnemyBullet(settings, screen, enemy_ships)
    enemy_bullets.add(en_bullet)


def update_enemy_bullets(enemy_bullets, settings):
    enemy_bullets.update()

    for bullet in enemy_bullets.copy():
        if bullet.rect.bottom >= settings.screen_height:
            enemy_bullets.remove(bullet)


def check_enemy_bullets_ship_collision(settings, stats, screen, sb, ship, enemy_ships, bullets, enemy_bullets):
    if pygame.sprite.spritecollideany(ship, enemy_bullets):
        ship_hit(settings, stats, screen, sb, ship, enemy_ships, bullets, enemy_bullets)


def ship_hit(settings, stats, screen, sb, ship, enemy_ships, bullets, enemy_bullets):
    """Respond to ship being hit by enemy_ship."""
    if stats.ships_left > 0:
        # Decrement ship_left.
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()
        # Empty the list of enemy_ships and bullets.
        enemy_ships.empty()
        bullets.empty()
        enemy_bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(enemy_ships, settings, screen)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, scoreboard):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
