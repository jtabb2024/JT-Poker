# JT_poker/game_logic/message_tracker.py
class MessageTracker:
    _instance = None
    instance_count = 0  # Class variable to track the number of instances

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.messages = []
            MessageTracker.instance_count += 1
            self.messages.append(f"Message Tracker Class is now running: {MessageTracker.instance_count}")
            self._initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages.clear()
        
    def send_card_data(self, card_data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "poker_game",  # This is the name of the group you'll set up in your consumer
            {
                "type": "card.data",  # This is the type of the message
                "card_data": card_data,  # This is the card data
            },
        )
