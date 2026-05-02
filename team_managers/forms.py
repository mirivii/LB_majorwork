from django import forms 
from .models import Team

class TeamForms(forms.ModelForm): # creating the team 
    class Meta: 
        model = Team 
        fields = ['name'] 

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        team = super().save(commit=False)
        team.admin = self.user
        if commit:
            team.save()
        return team