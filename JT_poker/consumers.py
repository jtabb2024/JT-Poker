import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views.main_view import Start_game
from .game_logic.message_tracker import MessageTracker

class PokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Received message type: {message['type']}")  # Print the message type
        if message['type'] == 'fetch_messages':
            mtracker = MessageTracker.instance()  # Get the singleton instance
            messages = mtracker.get_messages()
            await self.send(text_data=json.dumps({
                'messages': messages
            }))
        elif message['type'] == 'fetch_card_images':
            mtracker = MessageTracker.instance()  # Get the singleton instance
            card_images = mtracker.get_card_images()  # This should be the card data
            await self.send(text_data=json.dumps({
                'card_images': card_images
            }))

