from random import shuffle
from .message_tracker import MessageTracker

class SeatTracker(object):
    """
    A class to handle seating dynamics during a game of five card draw poker.

    Attributes
    ----------
        seats : list[str]
            seat vacancies and occupants indexed by seat number
        players : dict
            player seating data
        button : dict
            button assignment data
        L : int
            the maximum player capacity of the tracker

    Methods
    -------
        OccupySeat :
            Assign a player to a seat
        EmptySeat :
            Unassign a player from a seat
        TrackPlayers :
            Begin tracking players
        UntrackPlayers :
            Stop tracking players
        SeatPlayers :
            Assign tracked players to seats
        KickPlayers :
            Unassign tracked players from seats
        MoveButton :
            Move button to next player
        TrackButton :
            Update button data
        TrackedPlayers :
            Get list of tracked players
        AvailableSeats :
            Get list of available seats
        

    """
    def __init__(self, amount_seats : int = 4):
        """
        Constructs all the necessary attributes for the seattracker object.

        Parameters
        ----------
            amount_seats : the maximum player capacity of the game of five card draw
            
        """
        # initialise seat tracking
        self.seats = ["" for _ in range(amount_seats)]
        # initialise player tracking
        self.players = {}
        # initialise button tracking
        self.button = {"seat" : -1, "player" : ""}
        # store input parameters
        self.L = amount_seats

    def __iter__(self):
        """Converts the seatracker object to an iterator providing players in dealing order."""
        b_seat = self.button["seat"]
        return (player for player in self.seats[b_seat+1:] + self.seats[:b_seat+1] if player)

    def __len__(self):
        """Provides the amount of seats being tracked by the tracker."""
        return self.L

    def OccupySeat(self, name : str, seat : int):
        """
        Occupies a seat with a player.

        Parameters
        ----------
            name : player's name
            seat : index of seat to occupy
        
        Side effects
        ------------
            The seats attribute has an item replaced.

        """
        # assert name is unique
        if name in self.seats:
            raise Exception(f"{name} is already occupying a seat.")
        # assert seat at table
        if seat >= len(self) or seat < 0:
            raise IndexError(f"No seat with index {seat}.") 
        # assert seat is empty
        if self.seats[seat]:
            raise Exception(f"The seat is already occupied by {self.seats[seat]}.")
        # occupy seat
        self.seats[seat] = name

    def EmptySeat(self, seat : int):
        """
        Empties a seat occupied by a player.

        Parameters
        ----------
            seat : index of seat to empty
        
        Side effects
        ------------
            The seats attribute has an item replaced.

        """
        # assert seat at table
        if seat >= len(self) or seat < 0:
            raise IndexError(f"No seat with index {seat}.")
        # assert seat is occupied
        if not self.seats[seat]:
            raise Exception(f"The seat {seat} wasn't occupied.")
        # empty seat
        self.seats[seat] = ""
        
    def TrackPlayers(self, names : list[str]):
        """
        Inserts some names into the tracker so the tracker can begin storing data about them.

        Parameters
        ----------
            names : players to track
        
        Side effects
        ------------
            The players attribute gets additional keys.

        """
        for name in names:
            # assert name is unique
            if name in self.players:
                raise Exception(f"{name} is already being tracked.")
            # begin tracking
            self.players.update({name : {}})

    def UntrackPlayers(self, names : list[str]):
        """
        Removes some names from the player tracker.

        Parameters
        ----------
            names : players to stop tracking
        
        Side effects
        ------------
            The players attribute has some keys removed.

        """
        for name in names:
            # assert each player was being tracked
            try:
                # stop tracking player
                del self.players[name]
            except KeyError:
                raise KeyError(f"{names} is not being tracked.")

    def SeatPlayers(self):
        """
        Allocates seats to tracked players.

        Side effects
        ------------
            The seats attribute has items replaced. \n
            The players attribute has some values updated.

        """
        # select seats
        seats = self.AvailableSeats()
        shuffle(seats)
        # get players names to be seated
        players = [name for name in self.players if not self.players[name]]
        # assert enough seats
        if len(players) > len(seats):
            raise Exception(f"There is not enough available seats for {players}.")
        # allocate seats 
        for assignment in zip(players, seats):
            name, empty_seat = assignment
            # update seat tracker
            self.OccupySeat(name, empty_seat)
            # update player tracker
            self.players[name] = empty_seat

    def KickPlayers(self, players : list[str]):
        """
        Removes players from the game.

        Parameters
        ----------
            players : players to kick from seats
        
        Side effects
        ------------
            The seats attribute has items replaced. \n
            The players attribute has some keys deleted.

        """
        # assert players are being tracked
        for name in players:
            if name not in self.players:
                raise KeyError(f"{name} is not being tracked.")
            # update seat tracker 
            seat = self.players[name]
            self.EmptySeat(seat)
        # update player tracker
        self.UntrackPlayers(players)
        
    def TrackButton(self):
        """
        Stores information about the button seat.

        Side effects
        ------------
            The button attribute has a value updated.

        """
        b_seat = self.button["seat"]
        self.button["player"] = self.seats[b_seat]

    def MoveButton(self):
        """
        Moves the button to the next occupied seat if possible, otherwise the next empty one.

        Side effects
        ------------
            The button attribute has both values updated.

        """
        # find player to give button to if possible
        while True:
            # check each seat for a player
            seat = self.button["seat"]
            seat += 1
            seat %= len(self)
            self.button["seat"] = seat
            # stop if player is at seat or there are no seated players
            if self.seats[seat] or not self.players:
                break
        # update button tracker
        self.TrackButton()

    def TrackedPlayers(self) -> list[str]:
        """
        Provides the names of players being tracked.

        """
        return [*self.players]

    def AvailableSeats(self) -> list[int]:
        """
        Provides the seats that are unoccupied.

        """
        return [i for i, occupant in enumerate(self.seats) if not occupant]

    def OccupiedSeats(self) -> list[int]:
        """
        Provides the seats that are occupied.

        """
        return [i for i, occupant in enumerate(self.seats) if occupant]

    def GetPlayerSeatMapping(self, human_name) -> dict[str, int]:
        """
        Provides a mapping of player names to their occupied seats.
        Returns
        -------
        dict[str, int]
        A dictionary where keys are player names and values are their seat numbers.
        """
        # Initialize the seat mapping dictionary
        seatmapping = {}

        # Find the human player's seat number
        human_seat = self.players.get(human_name)

        # Assign the UI_key for the human player and bots
        for name, seat in self.players.items():
            if seat is not None:
                if name == human_name:
                    # Mark the human player
                    seatmapping[name] = {"seat": seat, "UI_key": "HPlayer"}
                else:
                    # Calculate the bot's UI_key based on its seat relative to the human player's seat
                    # Adjust bot_index to start from 1 instead of 0
                    bot_index = ((seat - human_seat - 1) % len(self.players)) + 1
                    seatmapping[name] = {"seat": seat, "UI_key": f"Bot{bot_index}"}

        return seatmapping

