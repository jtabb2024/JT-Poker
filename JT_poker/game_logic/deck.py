from random import shuffle
from .card import Card
from .message_tracker import MessageTracker

class Deck(object):
    """
    A class to represent a deck of cards.

    Attributes
    ----------
        state : list[Card]
            the order of the cards in the deck
        t : int
            the amount of cards no longer in the deck

    Methods
    -------
        Shuffle : 
            Shuffles order of remaining cards in deck.
        CollectCards : 
            Set the amount of cards no longer in the deck to 0.
        DepartedCards : 
            Get a list of the cards no longer in the deck.
        RemainingCards : 
            Get a list of the cards remaining in the deck.

    """

    def __init__(self):
        """Constructs all the necessary attributes for the deck object."""
        # create list of 52 unique cards
        self.state = [Card(v, s) for v in range(13) for s in range(4)]
        # initialise tracking attribute for tracking remaining cards in deck
        self.t = 0

    def __repr__(self):
        """Displays the remaining cards in the deck when the deck object is printed."""
        return str(self.RemainingCards())

    def __str__(self):
        """Converts the deck object to a string displaying the remaining cards in the deck."""
        return str(self.RemainingCards())

    def __iter__(self):
        """Converts the deck object to an iterator providing each card of a 52-card deck."""
        return self.state

    def __next__(self):
        """Provides the top card of the deck."""
        # assert there is a remaining card in deck
        try:
            top_card = self.RemainingCards()[0]
        except IndexError:
            raise StopIteration("No more cards in the deck")

        # return first remaining card as top card and update tracker
        self.t += 1
        return top_card

    def __len__(self):
        """Provides the amount of cards remaining in deck."""
        return 52 - self.t

    def Shuffle(self):
        """
        Shuffles the order of remaining cards in deck.
        
        Side effects
        ------------
            The state attribute is permutated.

        """
        departed_cards = self.DepartedCards()
        remaining_cards = self.RemainingCards()
        shuffle(remaining_cards)
        self.state = departed_cards + remaining_cards

    def CollectCards(self):
        """
        Set the amount of cards no longer in the deck to 0.
        
        Side effects
        ------------
            The t attribute is set to 0.

        """
        self.t = 0

    def DepartedCards(self) -> list[Card]:
        """
        Get a list of the cards no longer in the deck.

        """
        return self.state[:self.t]

    def RemainingCards(self) -> list[Card]:
        """
        Get a list of the cards remaining in the deck.

        """
        return self.state[self.t:]
