from random import shuffle
from .dealer import Dealer
from .play_game import PlayGame

class SpectateGame(PlayGame):
    def __init__(self):
        # initialise humanless game
        super().__init__()
    
    def Configuration(self):
        # configure game
        self.dealer = Dealer(len(self.OPPONENTS))
        humans = []
        self.dealer.InitializeTable(humans, self.OPPONENTS, self.CHIPS)
        self.dealer.UpdateAnte(self.ANTE)
        self.HUMAN = None
    
    def NewHand(self):
        # kick bots with few chips
        self.dealer.KickPlayers(self.dealer.SkintPlayers())

        # check amount of players remaining
        if len(self.dealer.TrackedPlayers()) < 2:
            print(f"[END] {self.dealer.TrackedPlayers()[0]} has won!")
            return False
        

        # begin new round
        print(f"\n[NEW ROUND]")
        self.dealer.MoveButton()
        self.dealer.TakeAnte()
        self.dealer.DealHands()
        return True

if __name__ == "__main__":
    prompt = "Press 1 to play, or 0 to spectate."
    answer = input(prompt)
    if int(answer):
        PlayGame()
    else:
        SpectateGame()