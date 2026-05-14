from django.urls import path
from . import views

# reinforcing the app name so errors don't occur related to webpage. (Url redirections stuff) 
app_name = 'team_managers'

urlpatterns = [
   path("", views.home, name="home"),
   path("create/", views.create_a_team, name="create_a_team"),
   path("join/", views.join_a_team, name="join_a_team"),
   # path below should create a separate webpage for each team 
   path("team/<int:team_id>/", views.team_details, name="team_details")
]