# JT_poker/game_logic/message_tracker.py
import threading

class MessageTracker:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # This ensures thread-safe singleton instantiation
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MessageTracker, cls).__new__(cls)
                cls._instance.messages = []  # Initialize messages here to ensure it's done only once
                cls._instance.messages.append("Message Tracker Class is now running")
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
        self.messages.clear()  # Clear the list in place instead of reassigning

# Example usage
# tracker = MessageTracker.instance()
# tracker.add_message("Test message")
# print(tracker.get_messages())
