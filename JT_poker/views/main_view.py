from django.shortcuts import render
from .play_game import PlayGame
from .spectate_game import SpectateGame
from ..game_logic.message_tracker import MessageTracker

def Start_game(request):
    game_output = ""
    messages = []

    tracker = MessageTracker()  # Create a singleton instance of MessageTracker

    if request.method == "POST":
        print("Form submitted")  # Debug print
        if 'play' in request.POST:
            game = PlayGame(message_tracker=tracker)  # Pass the tracker to PlayGame
            game_output = "Game initialized with human player."
            print("Play game initialized")  # Debug print
        elif 'spectate' in request.POST:
            game = SpectateGame(message_tracker=tracker)  # Pass the tracker to SpectateGame (if needed)
            game_output = "Spectator game initialized."
            print("Spectate game initialized")  # Debug print

        # Retrieve messages from MessageTracker
        messages = tracker.get_messages()

    context = {
        'game_output': game_output,
        'messages': messages,
    }

    return render(request, 'StartGame.html', context)
    

