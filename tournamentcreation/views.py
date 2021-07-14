from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TournamentForm
from .models import Match, Session, Team, Tournament, TD, UserProfile, TeamPlayer, Segment, Session_Segments
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json


def dashboard(request):
    print(request.user.username)
    context = {}
    return render(request, 'tournamentcreation/dashboard.html', context)

def index(request):
    if request.method == 'POST':
        # print('********************************')
        # print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if(user):
            login(request, user)
            return redirect(dashboard)
        else:
            return render(request, 'tournamentcreation/index.html', {'success': False})        
   
    context = {}

    return render(request, 'tournamentcreation/index.html', context)


# def signin(request):
#     if request.method == 'POST':
#         print('********************************')
#         print(request.POST)
#     return render(request, 'tournamentcreation/signin.html')


def signup(request):
    if request.method == 'POST':
        # print('********************************')
        # print(request.POST)
        first_name = request.POST.get('full-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone-number')
        organization = request.POST.get('organization')
        password = request.POST.get('confirm-password')
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        
        UserProfile.objects.create(user=user, phone=phone, organization=organization)
        
        return redirect(index)
        

    context = {}
    
    return render(request, 'tournamentcreation/signup.html', context)


# def tournament(request):
#     tournament_objects = Tournament.object.all()
#     if request.method == 'POST':
#         print('********************************')
#         print(request.POST)

#         title = request.POST['title']
#         global_tds = request.POST['global-tds']
#         print(global_tds)
#         co_ordinator = request.POST['co-ordinator']
#         start_date = request.POST['start-date']
#         end_date = request.POST['end-date']
#         format = request.POST['format']

#         td = TD.objects.get(bbo_username=global_tds)
#         print(td)
#         print('-----------------')
#         # print(td.bbo_username)

#         tournament = Tournament(title=title, global_tds=td, coordinator=co_ordinator,
#                                 start_date=start_date, end_date=end_date, format=format)
#         tournament.save()

#         # for creating global TD/appending into database
#         # td = TD.objects.get(bbo_username=global_tds)
#         # tour_id = tournament.id
#         print('&&&&&&&&&&&&&&&&&&&&&&&&')
#         # print(td)
#         # print(tour_id)

#         update_global_td = GlobalTD(bbo_username=td, tournament_id=tournament)
#         update_global_td.save()

#         return redirect('session', t=tournament.id)

#         # form = TournamentForm(request.POST)

#         # if form.is_valid():
#         #     form.save()

#         #     return redirect('/')

#     # form = TournamentForm()

#     td = TD.objects.all()
#     # format = Tournament.objects.all()
#     # print('$$$$$$$$$$$$$$$$$$$$')
#     # print(format)
#     context = {'td': td, 'tournament_objects': tournament_objects}
#     print(tournament_objects)

#     return render(request, 'tournamentcreation/tournament.html', context)


def single_tournament_ajax(request):
    id = request.GET.get('id')
    s_tour_object = Tournament.objects.filter(pk=id)
    TDs = TD.objects.filter(tournament=Tournament.objects.get(pk=id))
    s_tour_object = json.loads(serializers.serialize('json', s_tour_object))
    TDs = json.loads(serializers.serialize('json', TDs))
    return JsonResponse([s_tour_object, TDs], safe=False)


@login_required(login_url='/')
def tournament(request):
    tournament_objects = Tournament.objects.filter(user=request.user)
    td = TD.objects.all()
    context = {
        'td': td,
        'tournament_objects': tournament_objects
    }
    
    if request.method == 'POST':
        if('logout' in request.POST):
            logout(request)
            return redirect(index)
        
        if('modify-tournament' in request.POST):
            print(request.POST)
            current_focus = request.POST.get('current-focus')
            title = request.POST.get('title')
            is_active = True if request.POST.get('is-active') == 'on' else False
            format = request.POST.get('format')
            start_date = request.POST.get('start-date')
            end_date = request.POST.get('end-date')
            host = request.POST.get('host')
            
            tournament = Tournament.objects.get(pk=current_focus)
            tournament.title = title
            tournament.is_active = is_active
            tournament.format = format
            tournament.start_date = start_date
            tournament.end_date = end_date
            tournament.host = host
            tournament.save()
            
            Global_TDs = []
            Local_TDs = []
            TDs_objects = TD.objects.filter(tournament=tournament)
            for TD_object in TDs_objects:
                if(TD_object.bbo_username in request.POST):
                    Global_TDs.append(TD_object)
                else:
                    Local_TDs.append(TD_object)
                    
            for Global_TD in Global_TDs:
                Global_TD.is_global = True
                Global_TD.save()
                
            for Local_TD in Local_TDs:
                Local_TD.is_global = False
                Local_TD.save()

            return render(request, 'tournamentcreation/tournament.html', context)
        
        if('add-tournament' in request.POST):
            title = request.POST.get('title')
            is_active = True if request.POST.get('is-active') == 'on' else False
            format = request.POST.get('format')
            start_date = request.POST.get('start-date')
            end_date = request.POST.get('end-date')
            host = request.POST.get('host')
            
            Tournament.objects.create(user=request.user, title=title, is_active=is_active, format=format,
                                                        start_date=start_date, end_date=end_date, host=host)
            
            
            return render(request, 'tournamentcreation/tournament.html', context)
    
    print(request.user)
    return render(request, 'tournamentcreation/tournament.html', context)
        
# Shehroz Work
'''
def tournament(request):
    tournament_objects = Tournament.objects.all()
    if request.method == 'POST':
        print('********************************')
        print(request.POST)

        title = request.POST['title']
        global_tds = request.POST['global-tds']
        print(global_tds)
        host = request.POST['host']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        format = request.POST['format']

        td = TD.objects.get(bbo_username=global_tds)
        print(td)
        print('-----------------')
        # print(td.bbo_username)

        tournament = Tournament(title=title, global_tds=td, coordinator=host,
                                start_date=start_date, end_date=end_date, format=format)
        tournament.save()

        # for creating global TD/appending into database
        # td = TD.objects.get(bbo_username=global_tds)
        # tour_id = tournament.id
        print('&&&&&&&&&&&&&&&&&&&&&&&&')
        # print(td)
        # print(tour_id)

        # update_global_td = GlobalTD(bbo_username=td, tournament_id=tournament)
        # update_global_td.save()

        return redirect('session', t=tournament.id)

        # form = TournamentForm(request.POST)

        # if form.is_valid():
        #     form.save()

        #     return redirect('/')

    # form = TournamentForm()

    td = TD.objects.all()
    # format = Tournament.objects.all()
    # print('$$$$$$$$$$$$$$$$$$$$')
    # print(format)
    context = {
        'td': td,
        'tournament_objects': tournament_objects
    }
    print(tournament_objects)

    return render(request, 'tournamentcreation/tournament.html', context)
'''

def team_detail(request):
    tournament_objects = Tournament.objects.filter(user=request.user)
    team_objects = Team.objects.all()
    
    if request.method == 'POST':
        team = Team()
        
        tournament = Tournament.objects.get(pk=request.POST.get('tournament-info'))
        team_number = request.POST.get('team-number')
        is_active = True if request.POST.get('is-active') == 'on' else False
        team_name = request.POST.get('team-name')
        cap_bbo_id = request.POST.get('team-captain-bbo-id')
        cap_name = request.POST.get('team-captain-name')
        cap_email = request.POST.get('team-captain-email')
        cap_number = request.POST.get('team-captain-phone')
        cap_country = request.POST.get('team-captain-country')
        cap_playing = True if request.POST.get('is-captain-player') == 'on' else False
        
        team.tournament = tournament
        team.team_number = team_number
        team.is_active = is_active
        team.team_name = team_name
        team.cap_bbo_id = cap_bbo_id
        team.cap_name = cap_name
        team.cap_email = cap_email
        team.cap_number = cap_number
        team.cap_country = cap_country
        team.cap_playing = cap_playing
        
        for i in range(1,9):
            if('player-' + str(i) + '-bbo-id') in request.POST:
                player = TeamPlayer.objects.create(bbo_username=request.POST.get('player-'+str(i)+'-bbo-id'), full_name=request.POST.get('player-'+str(i)+'-name'))
                if(i == 1):
                    team.player_1 = player
                if(i == 2):
                    team.player_2 = player
                if(i == 3):
                    team.player_3 = player
                if(i == 4):
                    team.player_4 = player
                if(i == 5):
                    team.player_5 = player
                if(i == 6):
                    team.player_6 = player
                if(i == 7):
                    team.player_7 = player
                if(i == 8):
                    team.player_8 = player
                    
        team.save()
        

    context = {
        'tournament_objects': tournament_objects,
        'team_objects': team_objects
    }

    return render(request, 'tournamentcreation/team-detail.html', context)


def team_summary(request):
    tournament_objects = Tournament.objects.all()
    team_objects = Team.objects.all()

    context = {
        'tournament_objects': tournament_objects,
        'team_objects': team_objects
    }

    return render(request, 'tournamentcreation/team-summary.html', context=context)


def session_detail(request):
    tournament_objects = Tournament.objects.all()
    session_objects = Session.objects.all()

    if request.method == 'POST':
        tournament = Tournament.objects.get(pk=request.POST.get('tournament-info'))
        session_name = request.POST.get('session-name')
        format = request.POST.get('format')
        scoring = request.POST.get('scoring')
        host = request.POST.get('host')
        num_teams = request.POST.get('num-of-teams')
        num_segs = request.POST.get('num-of-seg')
        no_invite = True if request.POST.get('no-invite') == 'on' else False
        slow = True if request.POST.get('is-slow') else False
        use_predealt = True if request.POST.get('is-predealt-boards') else False
        barometer = True if request.POST.get('is-barometer') else False
        allow_kibitzers = True if request.POST.get('is-kibitzers') else False
        allow_undos = True if request.POST.get('is-undo') else False
        other_hacks = request.POST.get('other-hacks-inp')
        
        session = Session.objects.create(tournament=tournament, session_name=session_name, format=format, scoring=scoring,
                               host=host, num_teams=num_teams, num_segs=num_segs, no_invite=no_invite,
                               slow=slow, use_predealt=use_predealt, barometer=barometer, 
                               allow_kibitzers=allow_kibitzers, allow_undos=allow_undos, other_hacks=other_hacks)
        
        for i in range(1, int(num_segs) + 1):
            start_time = request.POST.get('start-time-segment-' + str(i))
            number_of_boards = request.POST.get('num-of-boards-' + str(i))
            starting_board_number = request.POST.get('start-board-num-' + str(i))
            segment = Segment.objects.create(start_time=start_time, number_of_boards=number_of_boards, starting_board_number=starting_board_number)
            
            Session_Segments.objects.create(session=session, segment=segment)
            
        context = {
        'tournament_objects': tournament_objects,
        'session_objects': session_objects
        }

        return render(request, 'tournamentcreation/session-detail.html', context)
            

    context = {
        'tournament_objects': tournament_objects,
        'session_objects': session_objects
    }

    return render(request, 'tournamentcreation/session-detail.html', context)


def session_summary(request):
    tournament_objects = Tournament.objects.all()
    session_objects = Session.objects.all()

    context = {
        'tournament_objects': tournament_objects,
        'session_objects': session_objects
    }

    return render(request, 'tournamentcreation/session-summary.html', context)


def matchups(request):
    team_objects = Team.objects.all()

    context = {
        'team_objects': team_objects
    }

    return render(request, 'tournamentcreation/matchups.html', context)


def matchups_td_assignment(request):
    tournament_objects = Tournament.objects.all()
    match_objects = Match.objects.all()
    td_objects = TD.objects.all()

    context = {
        'tournament_objects': tournament_objects,
        'match_objects': match_objects,
        'td_objects': td_objects
    }

    return render(request, 'tournamentcreation/matchups-td-assignment.html', context)


def td(request):
    tournament_objects = Tournament.objects.filter(user=request.user)
    td_objects = TD.objects.all()

    if request.method == 'POST':
        pass

    context = {
        'tournament_objects': tournament_objects,
        'td_objects': td_objects
    }

    return render(request, 'tournamentcreation/td.html', context)


def add_td(request):
    if(request.method == 'POST'):
        tournament = request.POST.get('tournament-info')
        bbo_username = request.POST.get('bbo-username')
        name = request.POST.get('name')
        is_global = True if request.POST.get('is-global') == 'on' else False
        
        TD.objects.create(bbo_username=bbo_username, name=name, is_global=is_global, 
                          tournament = None if tournament == '0' else Tournament.objects.get(pk=tournament) )
        
    tournament_objects = Tournament.objects.filter(user=request.user)

    context = {
        'tournament_objects': tournament_objects
    }

    return render(request, 'tournamentcreation/td-add.html', context)


def faqs(request):
    return render(request, 'tournamentcreation/faqs.html')
