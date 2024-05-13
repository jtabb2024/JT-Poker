class ChipTracker(object):
    def __init__(self):
        # initialise player and rules trackers
        self.gameinfo = {"ante" : 0}
        self.players = {}

    def __abs__(self):
        return sum([self.Contribution(player) + self.Stack(player) for player in self.players])

    def TrackPlayers(self, names):
        # initialise player tracking
        self.players = {name : {"stack" : 0, "contribution" : 0 } for name in names}

    def UntrackPlayers(self, names):
        for name in names:
            # assert each player was being tracked
            try:
                # stop tracking player
                del self.players[name]
            except KeyError:
                raise KeyError(f"{name} is not being tracked.")

    def Reward(self, name, amount):
        # assert player is being tracked
        if name not in self.players:
            raise KeyError(f"{name} is not being tracked.")
        # add chips to players stack
        self.players[name]["stack"] += amount

    def Spend(self, name, amount):
        # assert player has enough chips
        if not self.HasEnough(name, amount):
            raise ValueError(f"{name} doesn't have enough chips to pay {amount} chips.")
        # remove chips from players stack
        self.players[name]["stack"] -= amount

    def HasEnough(self, name, amount):
        # check if player has enough chips
        print("Amount:", amount, "Type:", type(amount))
        print("Stack:", self.players[name]["stack"], "Type:", type(self.players[name]["stack"]))
        return True if amount <= self.players[name]["stack"] else False

    def Bet(self, name, amount):
        # remove chips from player
        self.Spend(name, amount)
        # add chips to pot
        self.players[name]["contribution"] += amount

    def CallAmount(self, name):
        # calculate how many chips a player needs to contribute, to minimum call
        return self.MaxContribution() - self.Contribution(name)

    def BetDetails(self, name, amount):
        # check if bet is players full stack
        has_allin = True if amount == self.Stack(name) else False
        # check if bet is atleast the min call amount
        min_to_call = self.CallAmount(name)
        has_mincalled = True if amount >= min_to_call else False
        if has_mincalled:
            # check if bet is more than the min call amount
            has_raised = True if amount > min_to_call else False
            has_folded = False
        else:
            # check if player didn't bet anything
            has_folded = True if not amount else False
            has_raised = False
        return {"has_raised" : has_raised, "has_allin" : has_allin, "has_mincalled" : has_mincalled, "has_folded" : has_folded}

    def GatherContributions(self, cap):
        contributions = 0
        # check contribution of each player
        for contributor in self.players:
            # take capped contributions
            if not self.Contribution(contributor):
                continue
            if self.Contribution(contributor) > cap:
                contributions += cap
                self.players[contributor]["contribution"] -= cap
            else:
                contributions += self.Contribution(contributor)
                self.players[contributor]["contribution"] = 0
        return contributions

    def SplitContributions(self, names):
        # track rewards
        rewards = {}
        # calculate rewards per player based on contributions
        contributions = 0
        # accomodate side pots
        names.sort(key = lambda x : self.Contribution(x))
        for i, name in enumerate(names):
            # check if total player contribution has been accounted for
            contribution = self.Contribution(name)
            if contribution:
                # account for contribution
                contributions += self.GatherContributions(contribution)
            # split contributions
            split = contributions // (len(names) - i)
            # reward contributions
            self.Reward(name, split)
            contributions -= split
            # track rewards
            rewards[name] = split
        return rewards

    def UpdateAnte(self, amount):
        # update ante amount
        self.gameinfo["ante"] = amount

    def PayAnte(self, player):
        ante = self.Ante()
        stack = self.Stack(player)
        # track payment details
        status = {"bet_all" : False, "bet_something" : False}
        # pay
        if ante >= stack:
            status["bet_all"] = True
            self.Bet(player, stack)
        else:
            status["bet_something"] = True
            self.Bet(player, ante)
        return status

    def TrackedPlayers(self):
        # return all tracked players
        return [*self.players]

    def SkintPlayers(self):
        # return players without chips
        return [player for player in self.players if not self.Stack(player)]

    def Stack(self, name):
        # return player stack
        return self.players[name]["stack"]

    def Contribution(self, name):
        return self.players[name]["contribution"]

    def MaxContribution(self):
        return max([self.players[name]["contribution"] for name in self.players])

    def Ante(self):
        # return ante amount 
        return self.gameinfo["ante"]

    def PotAmount(self):
        # determine and return total amount of chips in pot
        return sum([self.Contribution(name) for name in self.players])
