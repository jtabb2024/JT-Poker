from django.shortcuts import render
from ..game_logic.message_tracker import MessageTracker

def start_game(request):
    mtracker = MessageTracker.instance()  # get the current instance of Message_Tracker
    return render(request, 'StartGame.html')
    

