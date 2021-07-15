from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('tournament/', views.tournament, name='tournament'),
    # path('tournament/add/', views.add_tournament, name='add_tournament'),
    # path('tournament/update/<str:t>', views.update_tournament, name='update_tournament'),
    # path('tournament/update/', views.update_tournament, name='update_tournament'),
    path('team/detail/', views.team_detail, name='team_detail'),
    path('team/summary/', views.team_summary, name='team_summary'),
    # path('team/update/', views.update_team, name='update_team'),
    # path('session/<str:t>/', views.session, name='session'),
    path('session/detail/', views.session_detail, name='session_detail'),
    path('session/summary/', views.session_summary, name='session_summary'),
    path('matchups/', views.matchups, name='matchups'),
    path('matchups/td-assignment', views.matchups_td_assignment, name='matchups_td_assignment'),
    path('td/', views.td, name='td'),
    path('td/add/', views.add_td, name='add_td'),
    path('faqs/', views.faqs, name='faqs'),
    path('single_tournament_ajax/', views.single_tournament_ajax, name='single_tournament_ajax')
]
