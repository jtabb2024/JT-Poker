# urls.py

from django.urls import path
from .views.main_view import start_game

urlpatterns = [
    path('playPoker/', start_game, name='start_game'),
]

