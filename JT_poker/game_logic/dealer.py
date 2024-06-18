import json
from functools import reduce
from itertools import groupby
from math import inf
from random import choice, shuffle
from .hand_tracker import HandTracker
from .seat_tracker import SeatTracker
from .chip_tracker import ChipTracker
from .action_tracker import ActionTracker
from .message_tracker import MessageTracker

class Dealer(object):
    def __init__(self, num_seats=3):
        # initialise trackers
        self.hands = HandTracker()
        self.seats = SeatTracker(num_seats)
        self.chips = ChipTracker()
        self.action = ActionTracker()
        self.mtracker = MessageTracker.instance()
        
    def MoveButton(self):
        # move button to next player and log
        self.seats.MoveButton()
        player = self.seats.button["player"]
        print(f"[BUTTON] The button was given to {player}.") # remove this when ready and all other print statements
        self.mtracker.send_lb_message(f"The button was given to {player}.")

    def ShuffleDeck(self):
        self.hands.ShuffleDeck()
        print(f"[CARDS] The deck has been shuffled.")
        self.mtracker.send_lb_message(f"The deck has been shuffled.")
        
    def DealHands(self):
        # determine players in the round and begin tracking
        names = self.seats.players
        print(f"((((((((SEATS)))))))): {list(self.seats)}")
        seating = self.seats.OccupiedSeats()
        print(f"((((((((SEATING)))))))): {seating}")
        seatmapping = self.seats.GetPlayerSeatMapping()
        print(f"((((((((SEATMAPPING)))))))): {seatmapping}")
        self.hands.TrackPlayers(names)
        # deal and evaluate hands and log
        self.hands.DealPlayersIn()
        self.hands.EvaluatePlayersIn()
        print(f"[HANDS] Hands have been dealt.")
        self.mtracker.send_lb_message(f"Cards have been dealt.")
        for name in names:
            if name in self.action.playertype["humans"]:
                    hand = self.hands.Hand(name)
                    handimages = self.hands.HandImages(name)
                    self.mtracker.send_lb_message(f"This is the DealHands Human player hand: {hand}")
                    self.mtracker.send_lb_message(f"This is the DealHands Human player hand image names: {handimages}")
                    self.mtracker.add_card_images(handimages)
        # initialise player statuses
        self.action.NewRound(names)
        # debug info below only
        print("Player Info: ", self.PlayerInfo())
        # This is where you can actually send all of the player info to the UI and update all items - need to add this logic
        self.mtracker.send_lb_message("DealHands", self.PlayerInfo())
        # self.mtracker.send_player_state(self.PlayerInfo())
        for name in names:
            TableInfo = self.TableView(name)
            print("Table Info: ", TableInfo)
    
    def EditHand(self, name, discards):
        hand = self.hands.Hand(name)
        # act on discard request and return success or not
        if self.hands.AllowDiscards(hand, discards):
            self.hands.SwapPlayersCards(name, discards)
            self.hands.EvaluatePlayersIn()
            # log approved request
            if discards:
                print(f"[HANDS] {name} swapped {len(discards)} cards.")
                self.mtracker.send_lb_message(f"{name} swapped {len(discards)} cards.")
            else:
                print(f"[CARDS] {name} didn't swap any cards.")
                self.mtracker.send_lb_message(f"{name} didn't swap any cards.")
            return True
        return False
        
    def CollectCards(self):
        # collect all cards and log
        self.hands.CollectCards()
        print(f"[CARDS] Cards have been collected.")
        self.mtracker.send_lb_message(f"Cards have been collected.")
        
        
    def TakeAnte(self):
        # take ante from players
        for name in list(self.seats):
            status = self.chips.PayAnte(name)
            amount = self.chips.Contribution(name)
            # log all-in or not
            if status["bet_all"]:
                print(f"[ANTE] The ante forced {name} to go all-in with {amount} chips!")
                self.mtracker.send_lb_message(f"The ante forced {name} to go all-in with {amount} chips!")
                self.action.SetAllIn(name)
            elif status["bet_something"]:
                print(f"[ANTE] {name} paid {amount} chips for the ante.")
                self.mtracker.send_lb_message(f"{name} paid {amount} chips for the ante.")
            self.mtracker.send_lb_message("TakeAnte")
            self.mtracker.send_state_playerinfo(self.PlayerInfo())
    
    def TakeBet(self, name, amount):
        # act on bet request and return success or not
        # check player has enough chips
        if self.chips.HasEnough(name, amount):
            # determine action based on bet amount
            status = self.chips.BetDetails(name, amount)
            # assert action is legal
            if not any([status["has_mincalled"], status["has_allin"], status["has_folded"]]):
                return False
            # log action
            if status["has_raised"] and status["has_allin"]:
                self.action.ExtendRound()
                self.action.SetAllIn(name)
                surplus = amount - self.chips.CallAmount(name) 
                print(f"[ACTION] {name} has raised by {surplus} and gone all-in!")
                self.mtracker.send_lb_message(f"{name} has raised by {surplus} and gone all-in!")
            elif status["has_raised"] and status["has_mincalled"]:
                self.action.ExtendRound()
                self.action.SetMinCalled(name)
                surplus = amount - self.chips.CallAmount(name) 
                print(f"[ACTION] {name} has raised by {surplus}.")
                self.mtracker.send_lb_message(f"{name} has raised by {surplus}.")
            elif status["has_allin"] and status["has_mincalled"]:
                self.action.SetAllIn(name)
                print(f"[ACTION] {name} has gone all-in to call!")
                self.mtracker.send_lb_message(f"{name} has gone all-in to call!")
            elif status["has_mincalled"] and amount == 0:
                self.action.SetMinCalled(name)
                print(f"[ACTION] {name} has checked.")
                self.mtracker.send_lb_message(f"{name} has checked.")
            elif status["has_mincalled"]:
                self.action.SetMinCalled(name)
                print(f"[ACTION] {name} has called.")
                self.mtracker.send_lb_message(f"{name} has called.")
            elif status["has_folded"]:
                self.action.SetFolded(name)
                print(f"[ACTION] {name} has folded.")
                self.mtracker.send_lb_message(f"{name} has folded.")
            elif status["has_allin"]:
                self.action.SetAllIn(name)
                print(f"[ACTION] {name} couldn't call but has gone all-in.")
                self.mtracker.send_lb_message(f"{name} couldn't call but has gone all-in.")
            self.chips.Bet(name, amount)
            return True
        else:
            return False

    def PlayerInfo(self):
        # initialise info tracker and return it
        info = {}
        # add info about each player
        for name in self.seats.players:
            info[name] = {}
            info[name]["seat"] = self.seats.players[name]
            info[name]["chips"] = self.chips.players[name]
            if name in self.hands.players:
                info[name]["hand"] = self.hands.players[name]
                #info[name]["hand"]["cards"] = [str(card) for card in info[name]["hand"]["cards"]] <--- this causes a major bug
            if name in self.action.players:
                info[name]["status"] = self.action.players[name]
                #info[name]["handimages"] = self.hands.HandImages(name)
        # log missing info
        if not self.action.players:
            print(f"[WARNING] Nobody has a status.")
            self.mtracker.send_lb_message(f"[WARNING] Nobody has a status.")
        if not self.hands.players:
            print(f"[WARNING] Nobody has a hand.")
            self.mtracker.send_lb_message(f"[WARNING] Nobody has a hand.")
        return info

    def TableView(self, viewer):
        info = {"self" : {}, "others" : {}, "game" : {}}
        for name in self.seats.players:
            # add info about viewer
            if viewer == name:
                info["self"]["name"] = name
                info["self"]["seat"] = self.seats.players[name]
                info["self"]["chips"] = self.chips.players[name]
                info["self"]["status"] = self.action.players[name]
                info["self"]["hand"] = self.hands.players[name]
                #info["self"]["handimages"] = self.hands.HandImages(name)
                if name in self.action.playertype["humans"]:
                    # Get the 'hand' part of the info dictionary for the viewer
                    viewer_hand = info["self"].get("hand", [])
                    # Add the viewer's hand to the message tracker
                    self.mtracker.send_lb_message(f"This is the Human TableView player hand: {viewer_hand}")
            else:
                # add info about other players
                info["others"][name] = {}
                info["others"][name]["seat"] = self.seats.players[name]
                info["others"][name]["chips"] = self.chips.players[name]
                info["others"][name]["status"] = self.action.players[name]
                #info["others"][name]["hand"] = []
                info["others"][name]["hand"] = self.hands.players[name]
                #info["others"][name]["handimages"] = self.hands.HandImages(name)
        # add info game circumstances
        info["game"]["call"] = self.chips.CallAmount(viewer)
        info["game"]["pot"] = self.chips.PotAmount()
        print("**********TableView**************:", info)
        return info

    def KickPlayers(self, names):
        self.seats.KickPlayers(names)
        self.action.KickPlayers(names)
        self.chips.UntrackPlayers(names)
        for name in names:
            print(f"[PLAYER] {name} is leaving the table.")
            self.mtracker.send_lb_message(f"{name} is leaving the table.")
         

    def CalculateRewards(self, player_info):
        pot = self.chips.PotAmount()
        # initialise rewards tracker
        rewards = {}
        # determine players who have not folded and sort them by hand rank and contribution; ascending 
        candidates = [name for name in player_info.keys() if not player_info[name]["status"]["has_folded"]]
        candidates.sort(key = lambda x : (player_info[x]["hand"]["rank_n"], player_info[x]["chips"]["contribution"]))
        # group players by hand rank
        groups = groupby(candidates, key = lambda x : player_info[x]["hand"]["rank_n"])
        # determine rewards per group
        for rank_n, players in groups:
            splits = self.chips.SplitContributions(list(players))
            rewards.update(splits)
            if sum(rewards.values()) == pot:
                break
        # return rewards tracker
        return rewards

    def Payout(self):
        # get data to determine size of rewards
        info = self.PlayerInfo()
        rewards = self.CalculateRewards(info)
        # get info to determine order to pay rewards
        showdown = self.action.ShowdownPlayers(self.seats)
        # check if hand reveal step can be skipped
        if len(showdown) < 2:
            winner = showdown[0]
            print(f"[SHOWDOWN] {winner} won {rewards[winner]} chips.")
            self.mtracker.send_lb_message(f"[SHOWDOWN!] {winner} won {rewards[winner]} chips.")
            return True
        
        # determine which players should reveal hands
        mucks = set([])
        i, rank_n = 0, inf
        for name in showdown:
            if self.hands.players[name]["rank_n"] <= rank_n:
                hand = self.hands.Hand(name)
                print(f"[SHOWDOWN] {name} is holding {hand}")
                self.mtracker.send_lb_message(f"[SHOWDOWN] {name} is holding {hand}")
                rank_n = self.hands.players[name]["rank_n"]
            else:
                print(f"[SHOWDOWN] {name} mucked.")
                self.mtracker.send_lb_message(f"[SHOWDOWN] {name} mucked.")
                mucks.add(name)
        # reward players
        for name in showdown:
            if name in rewards:
                reward = rewards[name]
                if name not in mucks:
                    hand = self.hands.players[name]["rank_c"]
                    print(f"[REWARDS] {name} won {reward} with a {hand}")
                    self.mtracker.send_lb_message(f"{name} won {reward} with a {hand}")
                else:
                    print(f"[REWARDS] {name} got {reward} chips back.")
                    self.mtracker.send_lb_message(f"{name} got {reward} chips back.")

    def StartingChips(self, amount):
        # give chips to all players
        names = self.TrackedPlayers()
        self.chips.TrackPlayers(names)
        for name in names:
            self.chips.Reward(name, amount)
        print(f"[SETUP] All players have been given {amount} chips.")
        self.mtracker.send_lb_message(f"All players have been given {amount} chips.")

    def UpdateAnte(self, amount):
        # set ante amount
        self.chips.UpdateAnte(amount)
        print(f"[SETUP] The ante has been set to {amount} chips.")
        self.mtracker.send_lb_message(f"The ante has been set to {amount} chips.")

    def TrackedPlayers(self):
        # return all tracked players
        return self.seats.TrackedPlayers()

    def DealingOrder(self):
        # determine order that players should take turns post-draw
        return list(self.seats)

    def PredrawOrder(self):
        # determine order that players should take turns pre-draw
        name = self.DealingOrder()[2 % len(self.TrackedPlayers())]
        seat = self.seats.players[name]
        queue = [name for name in self.seats.seats[seat:] + self.seats.seats[:seat] if name]
        # return order that players should take turns pre-draw
        return queue

    def SkintPlayers(self):
        return self.chips.SkintPlayers()

    def Summary(self):
        # log summary of player chips
        for name in self.TrackedPlayers():
            print(f"[STANDINGS] {name} has got {self.chips.players[name]['stack']} chips remaining.")
            self.mtracker.send_lb_message(f"{name} has got {self.chips.players[name]['stack']} chips remaining.")
    
    def SeatPlayers(self, players):
        self.seats.TrackPlayers(players)
        self.seats.SeatPlayers()

    def InitializeTable(self, humans, bots, starting_chips):
        # seat players
        players = humans + bots
        shuffle(players)
        self.SeatPlayers(players)
        # track species
        self.action.AddHumans(humans)
        self.action.AddBots(bots)
        # give chips to players
        self.StartingChips(starting_chips)