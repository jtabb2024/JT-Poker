# main_view.py
from django.shortcuts import render
from .play_game import PlayGame
from .spectate_game import SpectateGame
from ..game_logic.message_tracker import MessageTracker

def Start_game(request):
    mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker
    game_output = ""
    messages = []

    if request.method == "POST":
        if 'play' in request.POST:
            game = PlayGame()
            game_output = "Game initialized with human player."
            mtracker.add_message(game_output)
        elif 'spectate' in request.POST:
            game = SpectateGame()
            game_output = "Spectator game initialized."
            mtracker.add_message(game_output)

        # Retrieve updated messages from MessageTracker
        messages = mtracker.get_messages()

    context = {
        'game_output': game_output,
        'messages': messages,
    }

    return render(request, 'StartGame.html', context)
    

