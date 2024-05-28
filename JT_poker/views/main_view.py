from django.shortcuts import render
from .play_game import PlayGame
from .spectate_game import SpectateGame
from ..game_logic.message_tracker import MessageTracker

def start_game(request):
    mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker
    mtracker.add_message("main_view.py start_game called")
    return render(request, 'StartGame.html')
    

