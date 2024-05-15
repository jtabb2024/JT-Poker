# urls.py

from django.urls import path
from .views.main_view import Start_game

urlpatterns = [
    path('playPoker/', Start_game, name='start_game'),
]