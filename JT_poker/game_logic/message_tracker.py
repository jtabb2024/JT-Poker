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
            self.card_images = []  # initialize card images list
            self._initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def send_tableview(self, table_view):
        # Game State that will be sent to the poker game window (table view, etc.)
        pass
        
    def send_pot(self, pot_amount):
        # Int representing the amount of chips in the pot for the poker game window
        pass
        
    def send_player_chips(self, name, player_chips):
        # Int representing the amount of chips the player has for the poker game window
        pass

    def send_player_bet(self, name, player_bet):
        # Int representing the amount of chips the player has bet for the poker game window
        pass
        
    def send_player_action(self, name, player_action):
        # String representing the action the player took for the poker game window
        pass
        
    def send_player_hand(self, name, player_hand):
        # List of strings representing the cards the player has for the poker game window
        pass
        
    def send_player_status(self, name, player_status):
        # String representing the status of the player for the poker game window
        pass
        
    def send_player_turn(self, name, player_turn):
        # Boolean representing if it is the player's turn for the poker game window
        pass
        
    def send_player_winner(self, name, player_winner):
        # Boolean representing if the player is the winner for the poker game window
        pass
        
    def send_player_fold(self, name, player_fold):
        # Boolean representing if the player has folded for the poker game window
        pass
        
    def send_player_allin(self, name, player_allin):
        # Boolean representing if the player has gone all in for the poker game window
        pass
        
    def send_player_mincall(self, name, player_mincall):
        # Boolean representing if the player has made the minimum call for the poker game window
        pass
    
    def send_player_raise(self, name, player_raise):
        # Boolean representing if the player has raised for the poker game window
        pass
        
    def send_player_call(self, name, player_call):
        # Boolean representing if the player has called for the poker game window
        pass
        
    def send_player_check(self, name, player_check):
        # Boolean representing if the player has checked for the poker game window
        pass
        
    def send_player_discard(self, name, player_discard):
        # List of strings representing the cards the player has discarded for the poker game window
        pass

    def broadcast_messages(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_messages',
                'message': self.get_messages(),
            }
        )
        
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

    def add_card_images(self, images):  # add card images
        print('************Adding card images:', images)  # Log the images being added
        self.card_images.extend(images)
        self.broadcast_card_images()

    def get_card_images(self):
        return self.card_images

    def clear_card_images(self):  # clear card images
        self.card_images.clear()
        self.broadcast_card_images()

    def broadcast_card_images(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'poker_group',  # Group name
            {
                'type': 'update_card_images',
                'card_images': self.get_card_images(),
            }
        )
        
    def send_player_state(self, player_info):
        for player_name, player_data in player_info.items():
            #if player_name == name:
                self.send_lb_message(f"Processing data for {player_name}")
                #print(f"Processing data for {player_name}")
                #print(player_info)
                seat = player_data['seat']
                stack = player_data['chips']['stack']
                contribution = player_data['chips']['contribution']
                # Need to check if each dictionary item exists before trying to access it
                # cards = player_data['hand']['cards']
                # card_images = player_data['hand']['card_images']
                # rank_n = player_data['hand']['rank_n']
                # rank_c = player_data['hand']['rank_c']
                # status = player_data['status']
                # handimages = player_data['handimages']
                self.send_lb_message(f"Seat: {seat}")
                self.send_lb_message(f"Stack: {stack}")
                self.send_lb_message(f"Contribution: {contribution}")
                # self.send_lb_message(f"Cards: {cards}")
                # self.send_lb_message(f"Card Images: {card_images}")
                # self.send_lb_message(f"Rank N: {rank_n}")
                # self.send_lb_message(f"Rank C: {rank_c}")
                # self.send_lb_message(f"Status: {status}")
                # self.send_lb_message(f"Hand Images: {handimages}")
                #self.broadcast_player_info(f"{player_info}")
        
    def broadcast_player_info(self, player_info):
        # Game State that will be sent to the poker game window (player info, player actions, etc.
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'poker_group',  # Group name
        {
            'type': 'update_player_info',
            'player_info': player_info,
        }
    )