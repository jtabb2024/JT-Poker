from django.shortcuts import render
from JT_poker.game_logic.play_game import PlayGame
from JT_poker.game_logic.spectate_game import SpectateGame

def game_view(request):
    game_output = ""
    if request.method == "POST":
        if 'play' in request.POST:
            game = PlayGame()
            game_output = "Game initialized with human player."
        elif 'spectate' in request.POST:
            game = SpectateGame()
            game_output = "Spectator game initialized."

    context = {
        'game_output': game_output
    }
    return render(request, 'StartGame.html', context)