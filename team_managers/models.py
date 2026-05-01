from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=200) # team name
    admin = models.ForeignKey(User, related_name='admin_of_team', on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=10, unique=True) # Security note: unique= true ensures each team will generate a unique code
    members = models.ManyToManyField(User, related_name='joined_teams', blank=True) 

    def __str__(self):
        return self.name