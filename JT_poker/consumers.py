import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .views.main_view import start_game
from .game_logic.message_tracker import MessageTracker

class PokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to a specific group
        self.group_name = 'poker_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"Received message type: {message['type']}")  # Print the message 

        if message['type'] == 'fetch_messages':
            mtracker = MessageTracker.instance()  # Get the singleton instance
            messages = mtracker.get_messages()
            await self.send(text_data=json.dumps({
                'type': 'update_messages',
                'messages': messages
            }))
        elif message['type'] == 'fetch_card_images':
            mtracker = MessageTracker.instance()  # Get the singleton instance
            card_images = mtracker.get_card_images()  # This should be the card data
            await self.send(text_data=json.dumps({
                'type': 'update_card_images',
                'card_images': card_images
            }))

    async def update_messages(self, event):
        messages = event['messages']
        await self.send(text_data=json.dumps({
            'type': 'update_messages',
            'messages': messages
        }))

    async def update_card_images(self, event):
        card_images = event['card_images']
        await self.send(text_data=json.dumps({
            'type': 'update_card_images',
            'card_images': card_images
        }))

