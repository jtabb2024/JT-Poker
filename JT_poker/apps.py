from django.apps import AppConfig
from .game_logic.message_tracker import MessageTracker

class JtPokerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'JT_poker'

    def ready(self):
        # This method will be called when Django starts up
        # Initialize your singleton here
        MessageTracker.instance()