class Settings:
    """A class to store all the settings of the game"""

    def __init__(self):
        """Initialize the game's screen setting"""
        self.screen_width = 1000
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.bg_color = (0, 0, 0)
        self.screen_caption = "Simple Python Game"

        """Ship Settings"""
        self.ship_speed_factor = 0.1
        self.ship_limit = 3

        """Initialize enemy ship settings"""
        self.enemy_speed_factor = 0.5
        self.fleet_drop_speed = 5
        self.fleet_direction = 1
        self.enemy_ship_bullet_speed_factor = 1

        """Initialize player bullets settings"""
        self.bullet_color = 255, 0, 0
        self.bullet_speed_factor = 3
        self.bullets_allowed = 4

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the enemy_ship point values increase
        self.score_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.enemy_ship_speed_factor = 1

        # Scoring
        self.enemy_ship_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        # self.bullet_speed_factor*=self.speedup_scale
        self.enemy_ship_speed_factor *= self.speedup_scale

        self.enemy_ship_points = int(self.enemy_ship_points * (self.score_scale))

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
