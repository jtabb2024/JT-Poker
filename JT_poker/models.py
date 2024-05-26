from django.db import models

class Player(models.Model):
    Player_ID = models.AutoField(primary_key=True)
    Player_Name = models.CharField(max_length=100)
    Player_Picture = models.ImageField(upload_to='player_pictures/', blank=True, null=True)
    Default_Player = models.BooleanField(default=False)
    Player_Chips = models.IntegerField(default=0)

    def __str__(self):
        return self.Player_Name