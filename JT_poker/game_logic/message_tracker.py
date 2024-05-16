# JT_poker/game_logic/message_tracker.py
class MessageTracker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MessageTracker, cls).__new__(cls)
            cls._instance.messages = []  # Initialize messages here to ensure it's done only once
        return cls._instance

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
        self.messages = []
