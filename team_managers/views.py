from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team 
from .forms import TeamForms 


@login_required(login_url='users:login')
def home(request):
    manage = Team.objects.filter(admin=request.user)
    join = Team.objects.filter(members=request.user)
    return render(request, "team_managers/home.html", {
        'manage_teams': manage,
        'join_teams': join
        })


@login_required(login_url='users:login')
def create_team(request):
    if request.method == "POST":
        form = TeamForms(request.POST)
        if form.is_valid(): 
            team = form.save(commit=False)
            team.admin= request.user 
            team.save()
            messages.success(request, f'Team "{team.name}" created successfully!')
            return redirect('team_managers:home')
    else:
        form= TeamForms()
    return render(request, "team_managers/create_a_team.html", {'form': form})

@login_required(login_url='users:login')
def team_details(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.admin or request.user in team.members.all():
        return render(request, 'team_managers/team_details.html', {'team': team})
    else: 
        return HttpResponseForbidden("Cannot access this team. Ask your coach for the code.")