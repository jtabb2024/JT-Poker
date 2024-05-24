from django.shortcuts import render
from .play_game import PlayGame
from .spectate_game import SpectateGame
from ..game_logic.message_tracker import MessageTracker

def Start_game(request):
    mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker

    if request.method == "POST":
        if 'play' in request.POST:
            game = PlayGame()
            mtracker.add_message("Game initialized with human player.")
        elif 'spectate' in request.POST:
            game = SpectateGame()
            mtracker.add_message("Spectator game initialized.")

    return render(request, 'StartGame.html')
    

