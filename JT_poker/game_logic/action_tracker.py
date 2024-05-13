from functools import reduce
from itertools import groupby
from math import inf
from random import choice, shuffle
from .chip_tracker import ChipTracker
from .card import Card

class ActionTracker(object):
    def __init__(self):
        # initialise players and species tracker
        self.players = {}
        self.beings = {"humans" : [], "bots" : []}

    def UntrackPlayers(self, names):
        for name in names:
            # assert each player was being tracked
            try:
                # stop tracking player
                del self.players[name]
            except KeyError:
                raise KeyError(f"{name} is not being tracked.")

    def NewRound(self, names):
        # set players statuses to false
        for name in names:
            self.players[name] = {"has_allin" : False, "has_mincalled" : False, "has_folded" : False}

    def ExtendRound(self):
        # set players statuses to have not mincalled
        for name in self.players.keys():
            self.players[name]["has_mincalled"] = False

    def AddHumans(self, names):
        # start tracking humans
        for name in names:
            self.beings["humans"].append(name)
    
    def AddBots(self, names):
        # start tracking bots
        for name in names:
            self.beings["bots"].append(name)

    def KickBot(self, name):
        # stop tracking bot
        self.beings["bots"].remove(name)
        if name in self.players:
            del self.players[name]

    def KickPlayers(self, names):
        for name in names:
            # assert player is seated
            if name not in self.players:
                raise KeyError(f"{name} wasn't being tracked.")
            # kick bot
            self.KickBot(name)

    def SelectAmount(self, name, info):
        # determine species and get a bet amount request
        if name in self.beings["humans"]:
            return {
                "info": {
                    "cards": info['self']['hand']['cards'],
                    "pot": info['game']['pot'],
                    "chips_left": info['self']['chips']['stack'],
                    "call_amount": info['game']['call']
                },
                "prompt": "How much would you like to put in the pot?"
            }
        else:
            amount = choice([0, info['self']['chips']['stack'], info['game']['call'], info['game']['pot'], 2*info['game']['pot'], 2*info['game']['call']])
            return {"amount": amount}

    def SelectDiscards(self, name, info, mask=None):
        # Determine species to ask for discards from
        # Human Players: When a human player is playing, the method initially checks if a mask has been provided
        # If the mask is already provided (from the frontend), it uses this mask to compute the cards to discard.
        # If no mask is provided, it sends back the current cards with a prompt asking for the mask.
        # Bot Players: For bots, it continues to randomly choose discards as it did before.
        # Implementation Notes:
        # Frontend Responsibility: Your web interface needs to handle displaying the cards and collecting the mask as user input, then sending this mask back to the server.
        # Enforce that discard selection is always 5 characters/integers long and only has 0's or 1's with 1's being the card to discard
        # Backend Processing: Upon receiving the mask, your backend will call this method again, passing the received mask to actually compute the discards.
        # Need to use view to code the input "prompt": "Which cards would you like to swap? (00000 for none, 11111 for all)"  only if a human player cna you self.beings to check
        # If human then send Mask if not then send no mask

        if name in self.beings["humans"]:
            if mask is None:
                # In a real application, you might handle this case differently,
                # possibly raising an error or logging a warning because a mask
                # is required for human players to specify discards.
                raise ValueError("A mask must be provided for human players.")
            # Compute which cards to discard based on the mask provided by the frontend.
            # need place to grab this data print(f"[INFO] Your cards are {info['self']['hand']['cards']}")
            discards = [info['self']['hand']['cards'][i] for i, v in enumerate(mask) if int(v)]
        else:
            # Randomly decide discards for bots
            discards = [info['self']['hand']['cards'][i] for i in range(5) if choice([True, False])]
        return discards

    def SetAllIn(self, name):
        # record player has gone all in
        self.players[name]["has_allin"] = True

    def SetMinCalled(self, name):
        # record player has min called
        self.players[name]["has_mincalled"] = True

    def SetFolded(self, name):
        # record player has folded
        self.players[name]["has_folded"] = True

    def PlayerHasActed(self, name):
        # determine if player needs to take an action
        return any(self.players[name].values())

    def ShowdownPlayers(self, dealing_order):
        # return players who have not folded
        return [name for name in dealing_order if name and not self.players[name]["has_folded"]]

    def ActingPlayers(self, action_order):
        # return players who have not folded or gone all in
        return [name for name in action_order if name and not self.players[name]["has_folded"] and not self.players[name]["has_allin"]]

    def TrackedPlayers(self):
        return [*self.players]
