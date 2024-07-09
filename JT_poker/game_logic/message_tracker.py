import time
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
            self._initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def send_state_tableview(self, table_view):
        # Game State that will be sent to the poker game window (table view, etc.)
        pass
        
    def send_state_pot(self, pot_amount):
        # Int representing the amount of chips in the pot for the poker game window
        pass
        
    def send_state_player_chips(self, name, player_chips):
        # Int representing the amount of chips the player has for the poker game window
        pass

    def send_state_player_bet(self, name, player_bet):
        # Int representing the amount of chips the player has bet for the poker game window
        pass
        
    def send_state_player_action(self, name, player_action):
        # String representing the action the player took for the poker game window
        pass
        
    def send_state_player_hand(self, name, player_hand):
        # List of strings representing the cards the player has for the poker game window
        pass
        
    def send_state_player_status(self, name, player_status):
        # String representing the status of the player for the poker game window
        pass
        
    def send_state_player_turn(self, name, player_turn):
        # Boolean representing if it is the player's turn for the poker game window
        pass
        
    def send_state_player_winner(self, name, player_winner):
        # Boolean representing if the player is the winner for the poker game window
        pass
        
    def send_state_player_fold(self, name, player_fold):
        # Boolean representing if the player has folded for the poker game window
        pass
        
    def send_state_player_allin(self, name, player_allin):
        # Boolean representing if the player has gone all in for the poker game window
        pass
        
    def send_state_player_mincall(self, name, player_mincall):
        # Boolean representing if the player has made the minimum call for the poker game window
        pass
    
    def send_state_player_raise(self, name, player_raise):
        # Boolean representing if the player has raised for the poker game window
        pass
        
    def send_state_player_call(self, name, player_call):
        # Boolean representing if the player has called for the poker game window
        pass
        
    def send_state_player_check(self, name, player_check):
        # Boolean representing if the player has checked for the poker game window
        pass
        
    def send_state_player_discard(self, name, player_discard):
        # List of strings representing the cards the player has discarded for the poker game window
        pass
        
    def send_lb_message(self, lb_message, player_info=None):
        # Wait for x seconds this is just a test and should be moved elsewhere and time import should be removed
        #time.sleep(1)
        #if player_info:
            #self.send_player_state("Update State:", player_info)
        self.broadcast_lb_message(lb_message)
        
    def broadcast_lb_message(self, lb_message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_lb_message',
                'message': lb_message,
            }
        )
    
    def send_card_images(self, card_images, name):
        # Game State that will be sent to the poker game window card images
        self.broadcast_card_images(card_images, name)

    def broadcast_card_images(self, card_images, name):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_card_images',
                'card_images': card_images,
                'name': name
            }
        )
        
    def send_state_playerinfo(self, player_info): # add update_all=false, name=none, update_item=none
        #update_item can equal (chips, bet, action, hand, status, turn, winner, fold, allin, mincall, raise, call, check, discard)  
        for player_name, player_data in player_info.items():
            #if player_name == name:
                self.send_lb_message(f"Processing data for {player_name}")
                #print(f"Processing data for {player_name}")
                seat = player_data['seat']
                self.send_lb_message(f"Seat: {seat}")
                stack = player_data['chips']['stack']
                self.send_lb_message(f"Stack: {stack}")
                contribution = player_data['chips']['contribution']
                self.send_lb_message(f"Contribution: {contribution}")
                # Need to check if each dictionary item exists before trying to access it
                if 'hand' in player_data:
                    cards = player_data['hand']['cards']
                    card_images = player_data['hand']['card_images']
                    rank_n = player_data['hand']['rank_n']
                    rank_c = player_data['hand']['rank_c']
                    self.send_lb_message(f"Cards: {cards}")
                    self.send_lb_message(f"Card Images: {card_images}")
                    self.send_lb_message(f"Rank N: {rank_n}")
                    self.send_lb_message(f"Rank C: {rank_c}")
                if 'status' in player_data:
                    status = player_data['status']
                    self.send_lb_message(f"Status: {status}")              
                #self.broadcast_player_info(f"{player_info}")
        
    def broadcast_player_info(self, player_info):
        # Game State that will be sent to the poker game window player info
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'poker_group',  # Group name
        {
            'type': 'update_player_info',
            'player_info': player_info,
        }
    )