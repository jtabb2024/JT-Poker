import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.test import RequestFactory
from .views.main_view import Start_game

class PokerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        if message['type'] == 'update_messages':
            factory = RequestFactory()
            request = factory.post('/playPoker/', {})
            response = Start_game(request)
            messages = response.context_data.get('messages', [])
            await self.send(text_data=json.dumps({
                'messages': messages
            }))



