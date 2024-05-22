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
            self.card_images = [] # initialize card images list
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
        
    def add_card_images(self, images):  # add card images
        print('************Adding card images:', images)  # Log the images being added
        self.card_images.append(images)

    def get_card_images(self):
        card_images = self.card_images
        self.card_images = []  # Clear the card images after they are fetched
        print('************Getting card images:', card_images)  # Log the images being returned
        return card_images

    def clear_card_images(self):  # clear card images
        self.card_images.clear()