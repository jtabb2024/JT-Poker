import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.test import RequestFactory
from .views.main_view import Start_game
from .game_logic.message_tracker import MessageTracker

class PokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        if message['type'] == 'fetch_messages':
            tracker = MessageTracker.instance()  # Get the singleton instance
            messages = tracker.get_messages()
            await self.send(text_data=json.dumps({
                'messages': messages
            }))



