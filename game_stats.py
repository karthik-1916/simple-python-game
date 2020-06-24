class GameStats():
    """Track statisticss for Scary Pumpkin."""

    def __init__(self, sp_settings):
        """Initialize statistics."""
        self.sp_settings = sp_settings
        self.reset_stats()

        # High score should be reset.
        self.high_score = 0

        # Start Scary Pumpkin in an active state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.sp_settings.ship_limit
        self.score = 0
        self.level = 1
