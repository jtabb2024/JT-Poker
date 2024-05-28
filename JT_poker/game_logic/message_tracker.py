from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class MessageTracker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MessageTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.messages = []
            self.card_images = []  # initialize card images list
            self._initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_message(self, message):
        self.messages.append(message)
        self.broadcast_messages()

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages.clear()
        self.broadcast_messages()

    def add_card_images(self, images):  # add card images
        print('************Adding card images:', images)  # Log the images being added
        self.card_images.extend(images)
        self.broadcast_card_images()

    def get_card_images(self):
        return self.card_images

    def clear_card_images(self):  # clear card images
        self.card_images.clear()
        self.broadcast_card_images()

    def broadcast_messages(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_messages',
                'messages': self.get_messages(),
            }
        )

    def broadcast_card_images(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_card_images',
                'card_images': self.get_card_images(),
            }
        )