from functools import reduce
from .card import Card
from .deck import Deck
from .message_tracker import MessageTracker

class HandTracker(object):
    """
    A class to handle card dynamics during a game of five card draw poker.

    Attributes
    ----------
        DECK : Deck
            a deck of cards
        hands : dict
            player hand data
        FLUSH_RANKS : dict
            ratings for flush hands
        UNIQUE_5_RANKS : dict
            ratings for hands with 5 unique-valued cards and different suits
        DUPE_RANKS : dict
            ratings for hands with at least one pair of cards with the same card value.

    Methods
    -------
        TrackPlayers :
            Begin tracking players.
        UntrackPlayers :
            Stop tracking players.
        AssignCards :
            Associate cards with a player.
        UnassignCards :
            Stop associating cards with a player.
        DealHand :
            Get top five cards of the deck.
        DealPlayersIn :
            Deal cards to each player being tracked.
        SwapCards :
            Get a list of cards to replace some discarded cards.
        SwapPlayersCards :
            Replace the discarded cards o1f a tracked player.
        AllowDiscards :
            Decide if discarding chosen cards is allowed.
        CollectCards :
            Remove cards from tracked players and return them to the deck.
        ShuffleDeck :
            Shuffles order of remaining cards in deck.
        LoadData :
            Load the ratings for each possible hand in five card draw poker.
        HasFlush :
            Determines if a hand contains a flush.
        HasUnique5 :
            Determines if a hand contains five unique valued cards.
        TwosEncoding :
             Convert hand to a sum of powers of two.
        PrimesEncoding :
             Convert hand to a product of prime numbers.
        EvaluateHand :
            Get the rating of a hand.
        EvaluatePlayersIn :
            Store the rating of each tracked players hand.
        TrackedPlayers :
            Get a list of players being tracked.
        TrackedHand :
            Get a list of cards assigned to a player.

    """

    def __init__(self):
        """Constructs all the necessary attributes for the handtracker object."""
        # create a deck
        self.DECK = Deck()
        # create a state for player hand data
        self.players = {}
        # load data containing ratings of all possible five card hands
        self.LoadData()

    def TrackPlayers(self, names : list[str]):
        """
        Inserts some names into the tracker so the tracker can begin storing data about them.
        
        Parameters
        ----------
            names : the names of players
        
        Side effects
        ------------
            The players attribute gets additional keys.

        """
        # assert player is not being tracked already
        for name in names:
            if name in self.players:
                raise Exception(f"{name} is already being tracked.")
        # begin tracking players
        self.players.update({name : {"cards" : [], "card_images": []} for name in names})

    def UntrackPlayers(self, names : list[str]):
        """
        Removes some names from the tracker.

        Parameters
        ----------
            names : the names of players
        
        Side effects
        ------------
            The players attribute loses some keys.

        """
        for name in names:
            # assert each player was being tracked
            try:
                # stop tracking player
                del self.players[name]
            except KeyError:
                raise KeyError(f"{name} is not being tracked.")

    def AssignCards(self, name : str, cards : list[Card]):
        """
        Allocates additional cards to a player.

        Parameters
        ----------
            name : the name of a player
            cards : cards to assign to the player

        Side effects
        ------------
            The players attribute has some values updated.

        """
        # assert player is being tracked
        try:
            # allocate cards to player
            self.players[name]["cards"].extend(cards)
        except KeyError:
            raise KeyError(f"{name} is not being tracked.")

    def UnassignCards(self, name : str, cards : list[Card]):
        """
        Unallocates specifric cards from a player.

        Parameters
        ----------
            name : the name of a player
            cards : cards to unassign from the player
        
        Side effects
        ------------
            The players attribute has some values updated.

        """
        # assert player is holding all cards
        if set(cards).intersection(self.Hand(name)) != set(cards):
            raise Exception(f"{name} is not holding some of {cards}.")
        
        # assert player is being tracked
        try:
            # unallocate cards from player
            self.players[name]["cards"] = [card for card in self.Hand(name) if card not in cards]
        except KeyError:
            raise KeyError(f"{name} is not being tracked.")

    def DealHand(self) -> list[Card]:
        """
        Provide five cards from the deck.
        
        Side effects
        ------------
            The DECK.t attribute is increased by five.

        """
        # assert enough cards are in the deck to deal
        if 5 > len(self.DECK):
            Exception("There are not enough cards remaining in the deck.")
        
        # return a five card hand
        hand = [next(self.DECK) for _ in range(5)]
        return hand

    def DealPlayersIn(self):
        """
        Provides five cards to all players being tracked.
        
        Side effects
        ------------
            The players attribute has some values updated.

        """
        # determine if enough cards are in the deck to deal everyone hands
        if len(self.players) * 5 > len(self.DECK):
            Exception("There are not enough cards remaining to deal all players hands.")

        # deal hands to tracked players
        for player in self.players:
            hand = self.DealHand()
            self.AssignCards(player, hand)

    def SwapCards(self, discards : list[Card]) -> list[Card]:
        """
        Provides cards to replace some discarded cards.

        Parameters
        ----------
            discards : cards to swap
        
        Side effects
        ------------
            The DECK attribute has the t attribute increased by the amount of cards being discarded.

        """
        # assert enough cards in deck
        if len(self.DECK) < len(discards):
            raise Exception(f"Not enough cards in deck to swap {discards}.")

        # get new cards and return them
        new_cards = [next(self.DECK) for _ in range(len(discards))]
        return new_cards

    def SwapPlayersCards(self, name : str, discards : list[Card]):
        """
        Provides cards to replace some cards discarded by a tracked player.

        Parameters
        ----------
            name : name of tracked player
            discards : cards to swap
        
        Side effects
        ------------
            The DECK attribute has the t attribute increased by the amount of cards being discarded.\n
            The players attribute has some values updated.

        """
        # assert enough cards in deck
        if len(self.DECK) < len(discards):
            raise Exception(f"Not enough cards in deck to swap {discards}.")

        # remove discards from hand
        self.UnassignCards(name, discards)

        # get new cards and assign to player
        new_cards = [next(self.DECK) for _ in range(len(discards))]
        self.AssignCards(name, new_cards)

    def AllowDiscards(self, hand : list[Card], discards : list[Card]) -> bool:
        """
        Decides if discarding a selection of cards from a hand is acceptible in five card draw.

        Parameters
        ----------
            hand : the hand to discard from
            discards : the selection of cards to discard
        
        """
        # assert 5 card hands
        print("DISCARD LIST:", discards)
        if len(hand) != 5 or len(discards) > 5:
            raise Exception("Unknown variant of poker.")
        # the whole hand cannot be discarded
        if len(discards) == 5:
            return False
        # if four cards are discarded the last card must be an ace
        remaining = [card for card in hand if card not in discards]
        # hand will be multiple of 41 if it has an ace, otherwise it will have a remainder 
        if len(discards) == 4 and self.PrimesEncoding(remaining) % 41: 
            return False
        # discard request approved
        return True
    
    def CollectCards(self):
        """
        Puts all cards back in the deck.
        
        Side effects
        ------------
            The deck attribute has the t attribute set to 0. \n
            The players attribute is cleared.

        """
        self.DECK.CollectCards()
        players = self.TrackedPlayers()
        self.UntrackPlayers(players)

    def ShuffleDeck(self):
        """
        Shuffles the remaining cards in the deck .
        
        Side effects
        ------------
            The deck attribute has the state attribute permutated.

        """
        self.DECK.Shuffle()

    def LoadData(self):
        """
        Constructs all the hand ranking attributes for the handtracker object.
        
        Side effects
        ------------
            The FLUSH_RANKS attribute is created. \n
            The UNIQUE5_RANKS attribute is created. \n
            The DUPES_RANKS attribute is created.

        """
        # create ciphers for reading and encoding hands for fast hand ranking
        PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
        DV = {char : 2 ** i for i, char in enumerate("23456789TJQKA")}
        DP = {char : PRIMES[i] for i, char in enumerate("23456789TJQKA")}
        CLASSES = {
            "HC" : "high card", 
            "1P" : "pair", 
            "2P" : "two pair", 
            "3K" : "three of a kind", 
            "SS" : "straight", 
            "FF" : "flush", 
            "FH" : "full house", 
            "4K" : "four of a kind", 
            "SF" : "straight flush",
            "RF" : "royal flush"}

        # store ratings of all hands with flushes
        self.FLUSH_RANKS = {}
        # read data
        with open("data/flushes.txt", "r") as file:
            for line in file:
                # locate and encode hand as sum of powers of two
                hand = reduce(lambda x, y : x+y, map(lambda x : DV[line[int(x)]], "45678"))
                # store hand ratings by integer key 
                self.FLUSH_RANKS[hand] = []
                # store numerical rating
                self.FLUSH_RANKS[hand].append(int(str(line)[11:]))
                # store categorical rating
                self.FLUSH_RANKS[hand].append(CLASSES[str(line[:2])])

        # store ratings of all non-flush hands with 5 unique card values
        self.UNIQUE5_RANKS = {}
        # read data
        with open("data/uniquefive.txt", "r") as file:
            for line in file:
                # locate and encode hand as sum of powers of two
                hand = reduce(lambda x, y : x+y, map(lambda x : DV[line[int(x)]], "45678"))
                # store hand ratings by integer key 
                self.UNIQUE5_RANKS[hand] = []
                # store numerical rating
                self.UNIQUE5_RANKS[hand].append(int(str(line)[11:]))
                # store categorical rating
                self.UNIQUE5_RANKS[hand].append(CLASSES[str(line[:2])])

        # store ratings of all hands with duplicate card values
        self.DUPE_RANKS = {}
        # read data
        with open("data/dupes.txt", "r") as file:
            for line in file:
                # locate and encode hand as product of primes
                hand = reduce(lambda x, y : x*y, map(lambda x : DP[line[int(x)]], "45678"))
                # store hand ratings by integer key 
                self.DUPE_RANKS[hand] = []
                # store numerical rating
                self.DUPE_RANKS[hand].append(int(str(line)[11:]))
                # store categorical rating
                self.DUPE_RANKS[hand].append(CLASSES[str(line[:2])])

    def HasFlush(self, cards : list[Card]) -> bool:
        """
        Check if a hand contains a flush.

        Parameters
        ----------
            cards : hand to check
        
        """
        # look at suit bits of each card
        suit_mask = 15 << 12
        has_flush = reduce(lambda x, y : x&y, map(lambda x : int(x), cards)) & suit_mask
        return bool(has_flush)

    def HasUnique5(self, cards : list[Card]) -> bool:
        """
        Check if a hand contains five unique cards.

        Parameters
        ----------
            cards : hand to check
        
        """
        # look at value bits of each card
        values = reduce(lambda x, y : x|y, map(lambda x : int(x), cards)) >> 16
        has_unique5 = bin(values).count("1") == 5
        return has_unique5

    def TwosEncoding(self, cards : list[Card]) -> int:
        """
        Convert hand to a sum of powers of two.

        Parameters
        ----------
            cards : hand to convert
        
        """
        return reduce(lambda x, y : x|y, map(lambda x : int(x), cards)) >> 16

    def PrimesEncoding(self, cards : list[Card]) -> int:
        """
        Convert hand to a product of primes.

        Parameters
        ----------
            cards : hand to convert
        
        """
        return reduce(lambda x, y : x*y, map(lambda x : int(x) & 255, cards))

    def EvaluateHand(self, hand : list[Card]) -> tuple[int, str]:
        """
        Evaluates a hand both numerically and categorically.

        Parameters
        ----------
            hand : hand to evaluate
        
        """
        # assert 5 card hands
        if len(hand) != 5 :
            raise Exception("Unknown variant of poker.")

        # encode hand as int and use as key to get rank
        if self.HasFlush(hand):
            key = self.TwosEncoding(hand)
            return self.FLUSH_RANKS[key]
        elif self.HasUnique5(hand):
            key = self.TwosEncoding(hand)
            return self.UNIQUE5_RANKS[key]
        else:
            key = self.PrimesEncoding(hand)
            return self.DUPE_RANKS[key]

    def EvaluatePlayersIn(self):
        """
        Evaluates the hands of tracked players.
        
        Side effects
        ------------
            hands : The players attribute has some values updated.

        """
        # evaluate hands of players being tracked and store the info
        for player in self.players:
            hand = self.Hand(player)
            rank_n, rank_c = self.EvaluateHand(hand)
            self.players[player]["rank_n"] = rank_n
            self.players[player]["rank_c"] = rank_c

    def TrackedPlayers(self) -> list:
        """
        Provides the names of players being tracked.
        
        """
        return [*self.players]

    def Hand(self, name : str) -> list[Card]:
        """
        Provides the hand of a player being tracked.
        
        """
        # assert player is being tracked and return hand
        try:
            return self.players[name]["cards"]
        except KeyError:
            raise KeyError(f"{name} is not being tracked.")
        
    def HandImages(self, name: str) -> list[str]:
        """
        Provides the hand images (image names of each card) of a player being tracked.
        """
        try:
            imagehand = self.Hand(name)
            print('************Image Hand:', imagehand)  # Log the hand
            card_images = [card.get_CardImages() for card in imagehand]  # This should already be flat
            print('************Hand images before flattening:', card_images)  # Log the images being returned
            
            # Flatten the list if it is nested
            if card_images and isinstance(card_images[0], list):
                card_images = [img for sublist in card_images for img in sublist]
            
            print('************Hand images after flattening:', card_images)  # Log the images being returned
            return card_images
        except KeyError:
            raise KeyError(f"{name} is not being tracked.")