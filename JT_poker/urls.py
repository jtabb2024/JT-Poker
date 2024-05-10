# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('play/', views.game_view, name='game'),
    path('playPoker/', views.game_view, name='play_poker'),
]