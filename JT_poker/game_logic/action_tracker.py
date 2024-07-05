from functools import reduce
from itertools import groupby
from math import inf
from random import choice, shuffle
from .chip_tracker import ChipTracker
from .message_tracker import MessageTracker
from .card import Card

class ActionTracker(object):
    def __init__(self):
        # initialise players and species tracker
        self.players = {}
        self.playertype = {"humans" : [], "bots" : []}
        # Get the MessageTracker instance
        self.mtracker = MessageTracker.instance()

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
            self.playertype["humans"].append(name)
    
    def AddBots(self, names):
        # start tracking bots
        for name in names:
            self.playertype["bots"].append(name)

    def KickBot(self, name):
        # stop tracking bot
        self.playertype["bots"].remove(name)
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
        if name in self.playertype["humans"]:
            print(f"[INFO] Your cards are {info['self']['hand']['cards']}")
            self.mtracker.send_lb_message(f"{name}: Your cards are {info['self']['hand']['cards']}")
            print(f"[INFO] There are {info['game']['pot']} chips in the pot.")
            self.mtracker.send_lb_message(f"There are {info['game']['pot']} chips in the pot.")
            print(f"[INFO] You have {info['self']['chips']['stack']} chips remaining.")
            self.mtracker.send_lb_message(f"You have {info['self']['chips']['stack']} chips remaining.")
            print(f"[INFO] The amount to call is {info['game']['call']} chips.")
            self.mtracker.send_lb_message(f"The amount to call is {info['game']['call']} chips.")
            amount = int(input("How much would you like to put in the pot?"))
            self.mtracker.send_lb_message("How much would you like to put in the pot?")
        else:
            #Oringinal code with all-in and raising the amount of the pot, etc. options - this has been replaced with a slower game version only
            #allowing a bot to bet up to 2 * the call amount
            #amount = choice([0, info['self']['chips']['stack'], info['game']['call'], info['game']['pot'], 2*info['game']['pot'], 2*info['game']['call']])
            amount = choice([0, info['game']['call'], 2*info['game']['call']])
        return amount

    def SelectDiscards(self, name, info):
        # determine species to ask for discards from
        if name in self.playertype["humans"]:
            # give info and get user input from human
            print(f"[INFO] Your cards are {info['self']['hand']['cards']}")
            self.mtracker.send_lb_message(f"{name}: Your cards are {info['self']['hand']['cards']}")
            mask = input("Which cards would you like to swap? (00000 for none, 11111 for all)")
            discards =  [info['self']['hand']['cards'][i] for i, v in enumerate(mask) if int(v)]
            self.mtracker.send_lb_message(f"{name}: You discarded {discards}")
        else:
            # get random input from bots
            discards = [info['self']['hand']['cards'][i] for i in range(5) if choice([True,False])]
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
