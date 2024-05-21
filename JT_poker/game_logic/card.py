from .message_tracker import MessageTracker

class Card(object):
    """
    A class to represent a card.

    Attributes
    ----------
        MASK : str
            a guide for intepreting the binary encoding of the card
        PRIMES : tuple
            a cipher for encoding the card value as a prime
        _prime : int
            the prime encoding of the card value
        _rank : int
            the decimal encoding of the card value
        _suit : int
            the binary, one hot encoding of the card suit
        _value : int
            the binary, one hot encoding of the card value
        b : int
            the binary encoding of the card that combines _prime, _rank, _suit and _value 
        value_r : str
            the str representation of card value
        suit_r : str
            thr str representation of card suit
        value_i : int
            a class parameter for the card value
        suit_i : int
            a class parameter for the card suit
    
    """

    def __init__(self, value : int, suit : int):
        """
        Constructs all the necessary attributes for the card object.

        Parameters
        ----------
            value : card value
            suit : card suit

        """
        # Get the running instance of Message_Tracker
        self.mtracker = MessageTracker.instance()

        # assert acceptable parameters 
        try:
            value %= 13
            suit %= 4
        except TypeError:
            raise TypeError("Card objects only allow integers as arguments.")

        # encode card as integer for fast hand ranking
        self.MASK = "xxxAKQJT98765432♣♢♡♠RRRRxxPPPPPP"
        self.PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
        
        self._prime = self.PRIMES[value]
        self._rank = value << 8
        self._suit = (2 ** suit) << 12
        self._value = (2 ** value) << 16
        
        self.b = self._prime + self._rank + self._suit + self._value
    
        # encode card as string for representation
        self.VALUES = ("2","3","4","5","6","7","8","9","10","J","Q","K","A")
        self.SUITS = "♠♡♢♣"
        self.IMG_SUITS ="SHDC" 

        self.value_r, self.suit_r, self.suit_img_r = self.VALUES[value], self.SUITS[suit], self.IMG_SUITS[suit]
        self.r = self.value_r + self.suit_r
        self.card_images = f"{self.value_r}{self.suit_img_r}.png"

        # store input parameters
        self.value_i, self.suit_i = value, suit
    
    def get_CardImages(self):
        return self.card_images
    
    def __repr__(self):
        """Displays the card value and card suit when the card object is printed."""
        self.mtracker.add_message(f"Card self.r: {self.r}")
        self.mtracker.add_message(f"Value_i, Suit_i: {self.value_i},{self.suit_i}")
        self.mtracker.add_message(self.get_CardImages())
        return self.r

    def __str__(self):
        """Converts the card object to a string dispalying the card value and card suit."""
        return self.r

    def __int__(self):
        """Converts the card object to an integer that encodes the card value and card suit."""
        self.mtracker.add_message(f"Card self.b: {self.b}")
        return self.b

    def __hash__(self):
        """Creates a hash that's derived from the card value and card suit."""
        return hash((self.value_i, self.suit_i, self.b))

    def __eq__(self, other):
        """Compares the hash of the card object with others."""
        return hash(self) == hash(other)
