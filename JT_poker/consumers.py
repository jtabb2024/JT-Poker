import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .game_logic.play_game import PlayGame
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

        if message['type'] == 'start_game':
            asyncio.create_task(self.start_game())

    async def update_messages(self, event):
        messages = event['messages']
        await self.send(text_data=json.dumps({
            'type': 'update_messages',
            'messages': messages
        }))
        
    async def update_lb_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'update_lb_message',
            'message': message
        }))

    async def update_card_images(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_card_images',
            'card_images': event['card_images'],
            'name': event['name']   
        }))
        
    async def start_game(self):
        print("consumer start game started")
        play_game_instance = await sync_to_async(PlayGame)()
        await sync_to_async(play_game_instance.StartGame)()
    
    async def update_player_info(self, event):
        player_info = event['player_info']
        await self.send(text_data=json.dumps({
            'type': 'update_player_info',
            'player_info': player_info
        }))

    async def update_gamepot(self, event):
        pamount = event.get('pot_amount',0)
        print("update_game_pot", pamount)
        await self.send(text_data=json.dumps({
            'type': 'update_gamepot',
            'amount': pamount
        }))