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
    
    def send_player_state(self, player_info):
        self.broadcast_player_info(player_info)

    def clear_card_images(self):  # clear card images
        self.card_images.clear()
        self.broadcast_card_images()
    
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
        
    def send_tableview(self, table_view):
        # Game State that will be sent to the poker game window (table view, etc.)
        pass
        
    def send_lb_message(self, lb_message):
        # Messages that will be sent to the left bar in the poker game window
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
        
    def send_player_showdown(self, name, player_showdown):
        # Boolean representing if the player is in the showdown for the poker game window 
        pass

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