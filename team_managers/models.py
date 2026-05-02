from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=200) # team name
    admin = models.ForeignKey(User, related_name='admin_of_team', on_delete=models.CASCADE) # if the admin leaves, the whole team gets deleted. The admin = coach (whoever makes the 'team')
    invite_code = models.CharField(max_length=8, unique=True, blank=True) # Security note: unique= true ensures each team will generate a unique code
    members = models.ManyToManyField(User, related_name='joined_teams', blank=True) 

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = get_random_string(8).upper() # uppercase unique code (8 digits/letters)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name