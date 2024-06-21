from django.shortcuts import render, redirect
from JT_poker.models import Player
from ..game_logic.message_tracker import MessageTracker

mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker

#def start_game(request):
    #mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker
    #return render(request, 'StartGame.html')

def start_game(request):
    # Check if any player exists
    if Player.objects.exists():
        # Try to get the default player
        default_player = Player.objects.filter(Default_Player=True).first()
        # If no default player is set, just get the first player
        if not default_player:
            default_player = Player.objects.first()
        # Pass the default player to the template
        print(f"Default Player: {default_player}")
        return render(request, 'Startgame.html', {'default_player': default_player})
    else:
        # Redirect to the page to add a player if no players exist
        return redirect('add_player_url')  # Replace 'add_player_url' with the actual URL name for adding a player
