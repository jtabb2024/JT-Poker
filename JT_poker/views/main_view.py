from django.shortcuts import render
from .play_game import PlayGame
from .spectate_game import SpectateGame
from ..game_logic.message_tracker import MessageTracker

def Start_game(request):
    tracker = MessageTracker.instance() # get the curent instance of Message_Tracker
    tracker.add_message("PlayGame is executing...")
    game_output = ""
    messages = []

    if request.method == "POST":
        print("Form submitted")  # Debug print
        if 'play' in request.POST:
            game = PlayGame()
            game_output = "Game initialized with human player."
            print("Play game initialized")  # Debug print
        elif 'spectate' in request.POST:
            game = SpectateGame()
            game_output = "Spectator game initialized."
            print("Spectate game initialized")  # Debug print

        # Retrieve messages from MessageTracker
        messages = tracker.get_messages()

    context = {
        'game_output': game_output,
        'messages': messages,
    }

    return render(request, 'StartGame.html', context)
    

