from django.urls import path
from . import views

# reinforcing the app name so errors don't occur related to webpage. (Url redirections stuff) 
app_name = 'team_managers'

urlpatterns = [
   path("", views.home, name="home"),
]