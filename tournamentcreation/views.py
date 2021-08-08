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
from django.contrib import auth, messages
from .models import Seating


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
        if (user):
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


def tournament_ajax3(request):
    session_name = request.GET.get('session_name')
    session_object = Session.objects.filter(session_name=session_name)
    session_object = json.loads(serializers.serialize('json', session_object))
    for d in session_object:
        id_session = d['pk']
    segment_object = Session_Segments.objects.filter(session_id=id_session)
    segment_object = json.loads(serializers.serialize('json', segment_object))
    listt = []
    for data in segment_object:
        listt.append(data['fields']['segment'])
    new_list = []
    for each_data in listt:
        segment_new_object = Segment.objects.filter(pk=each_data)
        segment_new_object = json.loads(serializers.serialize('json', segment_new_object))
        new_list.append(segment_new_object[0]['fields'])

    print('------>>>', new_list)
    return JsonResponse([session_object, new_list], safe=False)


def tournament_ajaxajax(request):
    try:
        id = request.GET.get('id')
        session_object = Match.objects.filter(segement_id=id)
        session_object = json.loads(serializers.serialize('json', session_object))
        team1 = session_object[0]['fields']['team1']
        team2 = session_object[0]['fields']['team2']
        teamdata1 = Team.objects.filter(pk=team1)
        teamdata2 = Team.objects.filter(pk=team2)
        teamdata1_data = json.loads(serializers.serialize('json', teamdata1))
        teamdata2_data = json.loads(serializers.serialize('json', teamdata2))
        print(teamdata1_data, teamdata2_data)
        return JsonResponse([teamdata1_data, teamdata2_data], safe=False)
    except Exception as e:
        print(e)


def tournament_ajax(request):
    id = request.GET.get('id')
    tour_object = Team.objects.filter(team_number=id)
    tour_object = json.loads(serializers.serialize('json', tour_object))
    try:
        search_team_player1 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_1'])
        search_team_player2 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_2'])
        search_team_player3 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_3'])
        search_team_player4 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_4'])
        search_team_player5 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_5'])
        search_team_player6 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_6'])
        search_team_player7 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_7'])
        search_team_player8 = TeamPlayer.objects.filter(bbo_username=tour_object[0]['fields']['player_8'])

    except:
        print('nothing')
    try:
        dictplayer = {}
        dictplayer['player_1'] = (json.loads(serializers.serialize('json', search_team_player1))[0])['fields'][
            'full_name']
        dictplayer['player_2'] = (json.loads(serializers.serialize('json', search_team_player2))[0])['fields'][
            'full_name']
        dictplayer['player_3'] = (json.loads(serializers.serialize('json', search_team_player3))[0])['fields'][
            'full_name']
        dictplayer['player_4'] = (json.loads(serializers.serialize('json', search_team_player4))[0])['fields'][
            'full_name']
        dictplayer['player_5'] = (json.loads(serializers.serialize('json', search_team_player5))[0])['fields'][
            'full_name']
        dictplayer['player_6'] = (json.loads(serializers.serialize('json', search_team_player6))[0])['fields'][
            'full_name']
        dictplayer['player_7'] = (json.loads(serializers.serialize('json', search_team_player7))[0])['fields'][
            'full_name']
        dictplayer['player_8'] = (json.loads(serializers.serialize('json', search_team_player8))[0])['fields'][
            'full_name']
    except:
        pass
    tour_object.append(dictplayer)

    return JsonResponse([tour_object], safe=False)


@login_required(login_url='/')
def tournament(request):
    tournament_objects = Tournament.objects.filter(user=request.user)
    td = TD.objects.all()
    context = {
        'td': td,
        'tournament_objects': tournament_objects
    }

    if request.method == 'POST':
        if ('logout' in request.POST):
            logout(request)
            return redirect(index)

        if ('modify-tournament' in request.POST):
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
                if (TD_object.bbo_username in request.POST):
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

        if ('add-tournament' in request.POST):
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
    ts_tour_object = json.loads(serializers.serialize('json', tournament_objects))
    team_objects = Team.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', team_objects))
    newlist = {}
    for data in ts_tour_object:

        dictt = []
        for each_data in s_tour_object:
            if data['pk'] == each_data['fields']['tournament']:
                dictt.append(each_data['fields'])
            else:
                pass

        newlist[data['fields']['title']] = (dictt)
    print(',,.,.,.,,.>>>>>>>>>')
    print('-------->', newlist)
    # try:
    if request.POST.get('secondsubmit'):
        team_number = request.POST.get('teamphencho')
        print('------------->>>>>>>', team_number)
        team_number = Team.objects.get(team_number=request.POST.get('teamphencho'))
        north = request.POST.get('north')
        print(request.POST.get('north'))
        west = request.POST.get('west')
        east = request.POST.get('east')
        south = request.POST.get('south')
        seat = Seating.objects.create(north=north, south=south, east=east, west=west, team_id=team_number)
        seat.save()
    if request.POST.get('button3'):
        try:
            print('-------sunnat')
            team = Team()
            tournament = Tournament.objects.get(title=request.POST.get('tournament-info'))
            team_number = request.POST.get('team-number')
            is_active = True if request.POST.get('is-active') == 'on' else False
            team_name = request.POST.get('team-name')
            cap_bbo_id = request.POST.get('team-captain-bbo-id')
            cap_name = request.POST.get('team-captain-name')
            cap_email = request.POST.get('team-captain-email')
            cap_number = request.POST.get('team-captain-phone')
            cap_country = request.POST.get('team-captain-country')
            cap_playing = True if request.POST.get('is-captain-player') == 'on' else False
            print('------------->>>>>>>', team_number)

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

            for i in range(1, 9):
                if ('player-' + str(i) + '-bbo-id') in request.POST:

                    player = TeamPlayer(bbo_username=request.POST.get('player-' + str(i) + '-bbo-id'),
                                        full_name=request.POST.get('player-' + str(i) + '-name'))
                    player.save()
                    if (i == 1):
                        team.player_1 = player
                    if (i == 2):
                        team.player_2 = player
                    if (i == 3):
                        team.player_3 = player
                    if (i == 4):
                        team.player_4 = player
                    if (i == 5):
                        team.player_5 = player
                    if (i == 6):
                        team.player_6 = player
                    if (i == 7):
                        team.player_7 = player
                    if (i == 8):
                        team.player_8 = player
            team.save()

        except Exception as e:
            response = {
                'message': str(e)

            }
            return render(request, 'tournamentcreation/team-detail.html', response)

    if request.POST.get('firstsubmit'):
        try:
            print('firstsubmittt')
            print('-----------', request.POST.get('team-info'))
            team = Team.objects.get(team_number=request.POST.get('team-info'))
            tournament = Tournament.objects.get(title=request.POST.get('tournament-info'))
            team_number = request.POST.get('team-number')
            is_active = True if request.POST.get('is-active') == 'on' else False
            team_name = request.POST.get('team-name')
            cap_bbo_id = request.POST.get('team-captain-bbo-id')
            cap_name = request.POST.get('team-captain-name')
            cap_email = request.POST.get('team-captain-email')
            cap_number = request.POST.get('team-captain-phone')
            cap_country = request.POST.get('team-captain-country')
            cap_playing = True if request.POST.get('is-captain-player') == 'on' else False
            print('------------->>>>>>>', team_number)

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

            for i in range(1, 9):
                if ('player-' + str(i) + '-bbo-id') in request.POST:

                    player = TeamPlayer(bbo_username=request.POST.get('player-' + str(i) + '-bbo-id'),
                                        full_name=request.POST.get('player-' + str(i) + '-name'))
                    player.save()
                    if (i == 1):
                        team.player_1 = player
                    if (i == 2):
                        team.player_2 = player
                    if (i == 3):
                        team.player_3 = player
                    if (i == 4):
                        team.player_4 = player
                    if (i == 5):
                        team.player_5 = player
                    if (i == 6):
                        team.player_6 = player
                    if (i == 7):
                        team.player_7 = player
                    if (i == 8):
                        team.player_8 = player
            team.save()
        except Exception as e:
            response = {
                'message': str(e)

            }
            return render(request, 'tournamentcreation/team-detail.html', response)
    context = {
        'tournament_objects': tournament_objects,
        'team_objects': team_objects,
        'newlist': newlist,

    }

    return render(request, 'tournamentcreation/team-detail.html', context)


# def seating(request):
#     if request.method='POST':

def team_summary(request):
    tournament_objects = Tournament.objects.all()
    # team_objects = Team.objects.all()

    context = {
        'tournament_objects': tournament_objects,
        # 'team_objects': team_objects
    }

    return render(request, 'tournamentcreation/team-summary.html', context=context)


def session_detail(request):
    try:
        tournament_objects = Tournament.objects.all()
        session_objects = Session.objects.all()
        if request.POST.get('modify-session'):
            print('----->>',request.POST.get("session-info"))
            session = Session.objects.get(session_name=request.POST.get("session-info"))
            tournament = Tournament.objects.get(title=request.POST.get('tournament-info'))
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

            session.tournament = tournament
            session.session_name = session_name
            session.format = format
            session.scoring = scoring
            session.host = host
            session.num_teams = num_teams
            session.num_segs = num_segs
            session.no_invite = no_invite
            session.slow = slow
            session.use_predealt = use_predealt
            session.barometer = barometer
            session.allow_kibitzers = allow_kibitzers
            session.allow_undos = allow_undos
            session.other_hacks = other_hacks
            session.save()
            # for i in range(1, int(num_segs) + 1):
            #     start_time = request.POST.get('start-time-segment-' + str(i))
            #     number_of_boards = request.POST.get('num-of-boards-' + str(i))
            #     starting_board_number = request.POST.get('start-board-num-' + str(i))
            #     segment = Segment(start_time=start_time, number_of_boards=number_of_boards,
            #                                      starting_board_number=starting_board_number)
            #
            #     Session_Segments(session=session, segment=segment)


        if request.POST.get('submitbutton'):
            tournament = Tournament.objects.get(title=request.POST.get('tournament-info'))
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

            session = Session.objects.create(tournament=tournament, session_name=session_name, format=format,
                                             scoring=scoring,
                                             host=host, num_teams=num_teams, num_segs=num_segs, no_invite=no_invite,
                                             slow=slow, use_predealt=use_predealt, barometer=barometer,
                                             allow_kibitzers=allow_kibitzers, allow_undos=allow_undos,
                                             other_hacks=other_hacks)

            for i in range(1, int(num_segs) + 1):
                start_time = request.POST.get('start-time-segment-' + str(i))
                number_of_boards = request.POST.get('num-of-boards-' + str(i))
                starting_board_number = request.POST.get('start-board-num-' + str(i))
                segment = Segment.objects.create(start_time=start_time, number_of_boards=number_of_boards,
                                                 starting_board_number=starting_board_number)

                Session_Segments.objects.create(session=session, segment=segment)

    except:
        pass
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
    # session_objects = Session.objects.filter()

    context = {
        'tournament_objects': tournament_objects,
        # 'session_objects': session_objects
    }

    return render(request, 'tournamentcreation/session-summary.html', context)


def ajax_sessionsummary(request):
    id = request.GET.get('id')
    s_tour_object = Session.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', s_tour_object))
    newlist = []
    for data in s_tour_object:
        if data['fields']['tournament'] == int(id):
            newlist.append(data)
        else:
            pass

    return JsonResponse([newlist], safe=False)


def newajax_sessionsummary(request):
    id = request.GET.get('id')
    s_tour_object = TD.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', s_tour_object))
    newlist = []
    for data in s_tour_object:
        if data['fields']['tournament'] == int(id):
            newlist.append(data)
        else:
            pass
    print('------->', newlist)
    return JsonResponse([newlist], safe=False)


def matchesajaxcall(request):
    id = request.GET.get('id')
    print('-id', id)
    s_tour_object1 = Match.objects.filter(segement_id=id).all()
    s_tour_object11 = json.loads(serializers.serialize('json', s_tour_object1))

    listt = []
    for each_data in s_tour_object11:
        dictt = {}
        dictt['team1'] = each_data['fields']['team1']
        dictt['team2'] = each_data['fields']['team2']
        listt.append(dictt)

    list2 = []
    for each in listt:
        dict2 = {}
        data1 = each['team1']
        data2 = each['team2']
        dada1 = Team.objects.filter(id=data1)
        team_num1 = json.loads(serializers.serialize('json', dada1))
        dada2 = Team.objects.filter(id=data2)
        team_num2 = json.loads(serializers.serialize('json', dada2))
        for each_data in team_num1:
            dict2['team_number1'] = each_data['fields']['team_number']

        for each_data2 in team_num2:
            dict2['team_number2'] = each_data2['fields']['team_number']
        list2.append(dict2)

    newlist = []
    for datadata in list2:
        newdict = {}
        t1 = datadata['team_number1']
        t2 = datadata['team_number2']
        datat1 = Seating.objects.filter(team_id=t1)
        datas1 = json.loads(serializers.serialize('json', datat1))
        datat2 = Seating.objects.filter(team_id=t2)
        datas2 = json.loads(serializers.serialize('json', datat2))
        for data_in_t1 in datas1:
            newdict['t1north'] = data_in_t1['fields']['north']
            newdict['t1west'] = data_in_t1['fields']['west']
            newdict['t1south'] = data_in_t1['fields']['south']
            newdict['t1east'] = data_in_t1['fields']['east']
        for data_in_t2 in datas2:
            print('in loop')
            newdict['t2north'] = data_in_t2['fields']['north']
            newdict['t2west'] = data_in_t2['fields']['west']
            newdict['t2south'] = data_in_t2['fields']['south']
            newdict['t2east'] = data_in_t2['fields']['east']
        newlist.append(newdict)
    print('-------------------------------------->>>>>>>>>', newlist)
    return JsonResponse(newlist, safe=False)


def ajax_teamsummary(request):
    id = request.GET.get('id')

    s_tour_object = Team.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', s_tour_object))
    newlist = []
    for data in s_tour_object:
        if data['fields']['tournament'] == int(id):
            newlist.append(data)
        else:
            pass
    print(newlist)

    return JsonResponse([newlist], safe=False)


def matchups(request):
    match_objects = Match.objects.all()
    team_objects = Team.objects.all()
    tournament_objects = Tournament.objects.all()
    if request.method == 'POST':
        # session_id = Session.objects.get(pk=request.POST.get('session-info'))
        team_1 = Team.objects.get(pk=request.POST.get('team-1'))
        team_2 = Team.objects.get(pk=request.POST.get('team-2'))
        segmentnumber = Segment.objects.get(id=request.POST.get('match-info'))
        if team_1 != team_2:
            Match.objects.create(team1=team_1, team2=team_2, segement_id=segmentnumber)

        else:
            messages.error(request, 'Both teams  should not be same')

    context = {
        'match_objects': match_objects,
        'team_objects': team_objects,
        'tournament_objects': tournament_objects
    }

    return render(request, 'tournamentcreation/matchups.html', context)


def ajaxcall_team_details(request):
    id = request.GET.get('id')
    tournament_objects = Tournament.objects.filter(user=request.user).filter(title=id)
    ts_tour_object = json.loads(serializers.serialize('json', tournament_objects))
    team_objects = Team.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', team_objects))
    newlist = {}
    print('->>>>>>>>', s_tour_object)
    print('->>>>>>>>', ts_tour_object)
    for data in ts_tour_object:

        dictt = []
        for each_data in s_tour_object:
            if data['pk'] == each_data['fields']['tournament']:
                dictt.append(each_data['fields'])
            else:
                pass

        newlist[data['fields']['title']] = (dictt)
    print('->>>', id)
    print('->>>>>>..newlist', newlist)

    return JsonResponse([newlist], safe=False)


def ajax_session_new(request):
    id = request.GET.get('id')
    tournament_objects = Tournament.objects.filter(user=request.user).filter(title=id)
    ts_tour_object = json.loads(serializers.serialize('json', tournament_objects))
    session_objects = Session.objects.all()
    s_tour_object = json.loads(serializers.serialize('json', session_objects))
    newlist = {}
    for data in ts_tour_object:
        dictt = []
        for each_data in s_tour_object:
            if data['pk'] == each_data['fields']['tournament']:
                dictt.append(each_data['fields'])
            else:
                pass
        newlist[data['fields']['title']] = (dictt)
    print('->>>', id)
    print('->newlist', newlist)
    return JsonResponse([newlist], safe=False)


def ajax_call_new(request):
    id = request.GET.get('id')
    tournament_objects = Tournament.objects.filter(user=request.user)
    ts_tour_object = json.loads(serializers.serialize('json', tournament_objects))
    team_objects = Team.objects.filter(tournament=id).all()
    team_tour_ob = json.loads(serializers.serialize('json', team_objects))
    listnn = []
    for dd in team_tour_ob:
        listnn.append(dd['pk'])
    session_objects = Session.objects.filter(tournament=id).all()
    s_tour_object = json.loads(serializers.serialize('json', session_objects))
    session_segment_objects = Session_Segments.objects.all()
    ss_tour_object = json.loads(serializers.serialize('json', session_segment_objects))
    new_list = {}
    for each_data1 in s_tour_object:
        dictt = []
        for each_data2 in ss_tour_object:
            if each_data1['pk'] == each_data2['fields']['session']:
                dictt.append(each_data2['fields']['segment'])
                print('in if')
            else:
                print('in else')
        new_list[each_data1['fields']['session_name']] = (dictt)
    print(new_list)
    listt = []
    for data in new_list:
        for each_data in new_list[data]:
            listt.append(each_data)
    print('->>>>', listt)
    return JsonResponse([listt, listnn], safe=False)


def ajax_call_tournament_tomatch(request):
    id = request.GET.get('id')
    td_data = TD.objects.filter(is_global=False).filter(tournament=id)
    td_tour_object = json.loads(serializers.serialize('json', td_data))
    tournament_objects = Tournament.objects.filter(user=request.user)
    ts_tour_object = json.loads(serializers.serialize('json', tournament_objects))
    session_objects = Session.objects.filter(tournament=id).all()
    s_tour_object = json.loads(serializers.serialize('json', session_objects))
    session_segment_objects = Session_Segments.objects.all()
    ss_tour_object = json.loads(serializers.serialize('json', session_segment_objects))
    match_objects = Match.objects.all()
    ms_tour_object = json.loads(serializers.serialize('json', match_objects))
    new_list = {}
    for each_data1 in s_tour_object:
        dictt = []
        for each_data2 in ss_tour_object:
            if each_data1['pk'] == each_data2['fields']['session']:
                dictt.append(each_data2['fields']['segment'])
                print('in if')
            else:
                print('in else')
        new_list[each_data1['fields']['session_name']] = (dictt)
    print(new_list)
    listt = []
    for data in new_list:
        for each_data in new_list[data]:
            listt.append(each_data)
    print('->>>>', listt)
    list2 = []
    for eacdata1 in ms_tour_object:
        for eachdata in listt:
            if eachdata == eacdata1['fields']['segement_id']:
                list2.append(eacdata1['pk'])
    print('__-->lest new', list2)
    list_td = []
    for data_td in td_tour_object:
        list_td.append(data_td['pk'])
    return JsonResponse([list2, list_td], safe=False)


def ajaxcall(request):
    id = request.GET.get('id')
    s_tour_object = Match.objects.filter(pk=id)

    s_tour_object = json.loads(serializers.serialize('json', s_tour_object))
    team1 = s_tour_object[0]['fields']['team1']
    team2 = s_tour_object[0]['fields']['team2']
    team1_data = Team.objects.filter(pk=team1)
    team2_data = Team.objects.filter(pk=team2)
    team1_data_res = json.loads(serializers.serialize('json', team1_data))
    team2_data_res = json.loads(serializers.serialize('json', team2_data))

    return JsonResponse([s_tour_object, team2_data_res, team1_data_res], safe=False)


# def td_function(request):
#     try:
#         tournament = request.POST.get('tournament-info')
#
#     except :
#         pass

def matches(request):
    tournament_objects = Tournament.objects.all()

    # s_tour_object = json.loads(serializers.serialize('json', match_objects))
    # print('---->>>>>',s_tour_object)

    context = {
        'tournament_objects': tournament_objects,

    }

    return render(request, 'tournamentcreation/matchess.html', context)


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


def ajaxcall_td_function(request, **kwargs):
    match_id = kwargs["match"]
    td_name = kwargs['td']
    print(type(match_id))
    print(type(td_name))
    print('------>td>>>>>>>>>>>>')
    td = TD.objects.filter(bbo_username=td_name)
    td.update(match=match_id)
    return JsonResponse(td_name, safe=False)


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

    # def seating(request):
    #
    #     if (request.method == 'POST'):
    #
    #
    #
    #     context = {
    #         'tournament_objects': tournament_objects
    #     }

    return render(request, 'tournamentcreation/td-add.html', context)


def add_td(request):
    if (request.method == 'POST'):
        tournament = request.POST.get('tournament-info')
        bbo_username = request.POST.get('bbo-username')
        name = request.POST.get('name')
        is_global = True if request.POST.get('is-global') == 'on' else False

        TD.objects.create(bbo_username=bbo_username, name=name, is_global=is_global,
                          tournament=None if tournament == '0' else Tournament.objects.get(pk=tournament))

    tournament_objects = Tournament.objects.filter(user=request.user)

    context = {
        'tournament_objects': tournament_objects
    }

    return render(request, 'tournamentcreation/td-add.html', context)


def faqs(request):
    return render(request, 'tournamentcreation/faqs.html')
