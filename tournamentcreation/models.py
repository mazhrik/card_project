from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.conf import settings


# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email', max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     full_name = models.CharField(max_length=30)
#     phone_no = models.CharField(max_length=30)
#     organization = models.CharField(max_length=30, null=True)
#     date_joined = models.DateTimeField(
#         verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FILED = 'email'
#     REQUIRED_FIELDS = ['username', 'full_name', 'phone_no']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True


class User(models.Model):
    # bbo_username = models.CharField(primary_key=True, max_length=20)
    # name = models.CharField(max_length=50, null=True)
    # email = models.CharField(max_length=50, null=True)
    # password = models.
    pass


# class Format(models.Model):
#     format_id = models.IntegerField(primary_key=True)
#     usage = models.CharField(max_length=255)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username


class Tournament(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    FORMAT = (
        ('Knockout', 'Knockout'),
        ('Mixed', 'Mixed'),
        ('Round Robin', 'Round Robin'),
        ('Swiss', 'Swiss')
    )

    # global_tds = models.ForeignKey(
    #     TD, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=255, null=True)
    start_date = models.CharField(max_length=12, null=True)
    end_date = models.CharField(max_length=12, null=True)
    # format = models.ForeignKey(Format, on_delete=models.CASCADE)
    format = models.CharField(max_length=15, null=True, choices=FORMAT)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return self.title
    
    
class TD(models.Model):
    bbo_username = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, null=True)
    is_global = models.BooleanField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    

# class TournamentTD(models.Model):
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     td = models.ForeignKey(TD, on_delete=models.CASCADE)
#     is_global = models.BooleanField(default=False)


# class Scoring(models.Model):
#     scoring_id = models.IntegerField(primary_key=True)

class Segment(models.Model):
    start_time = models.CharField(max_length=100, null=True)
    number_of_boards = models.CharField(max_length=50, null=True)
    starting_board_number = models.CharField(max_length=50, null=True) 

class Session(models.Model):
    # FORMAT = (
    #     ('Knockout', 'Knockout'),
    #     ('Mixed', 'Mixed'),
    #     ('Round Robin', 'Round Robin'),
    #     ('Swiss', 'Swiss')
    # )

    # SCORING = (
    #     ('BAM', 'BAM'),
    #     ('IMPs', 'IMPs'),
    #     ('TotalPoints', 'TotalPoints')
    # )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=255, null=True)
    # format = models.ForeignKey(Format, on_delete=models.CASCADE)
    format = models.CharField(max_length=15, null=True)
    # scoring = models.ForeignKey(Scoring, on_delete=models.CASCADE)
    scoring = models.CharField(max_length=15, null=True)
    # session_num = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=255, null=True)
    num_teams = models.CharField(max_length=255, null=True)
    num_segs = models.CharField(max_length=255, null=True)
    no_invite = models.BooleanField(default=False)
    slow = models.BooleanField(default=False)
    use_predealt = models.BooleanField(default=False)
    barometer = models.BooleanField(default=False)
    allow_kibitzers = models.BooleanField(default=False)
    allow_undos = models.BooleanField(default=False)
    other_hacks = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.session_name


class Session_Segments(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)


class TeamPlayer(models.Model):
    bbo_username = models.CharField(primary_key=True, max_length=50)
    full_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.full_name


class Team(models.Model):
    tournament = models.ForeignKey(
        Tournament, null=True, on_delete=models.SET_NULL)
    team_number = models.CharField(max_length=100, null=True)
    team_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField()
    cap_name = models.CharField(max_length=255, null=True)
    cap_email = models.EmailField(max_length=50)
    cap_bbo_id = models.CharField(max_length=255)
    cap_number = models.CharField(max_length=255, null=True)
    cap_country = models.CharField(max_length=255, null=True)
    cap_playing = models.BooleanField()
    player_1 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_1', null=True)
    player_2 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_2', null=True)
    player_3 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_3', null=True)
    player_4 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_4', null=True)
    player_5 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_5', null=True)
    player_6 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_6', null=True)
    player_7 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_7', null=True)
    player_8 = models.ForeignKey(
        TeamPlayer, on_delete=models.CASCADE, related_name='player_8', null=True)

    def __str__(self):
        return self.team_name


class Match(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    # segment
    match_num = models.IntegerField(unique=True, null=True)
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team2')
    # seating_rights

    def __str__(self):
        return str(self.match_num)


# class GlobalTD(models.Model):
#     bbo_username = models.ForeignKey(TD, on_delete=models.CASCADE)
#     tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)

#     # def __str__(self):
#     #     return self.bbo_username


# class LocalTD(models.Model):
#     bbo_username = models.ForeignKey(TD, on_delete=models.CASCADE)
#     match_id = models.ForeignKey(Match, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.bbo_username


class Seating(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    segment_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    north = models.ForeignKey(TeamPlayer, on_delete=models.CASCADE,related_name="north",default=None)
    south = models.ForeignKey(TeamPlayer, on_delete=models.CASCADE,related_name="south",default=None)
    east = models.ForeignKey(TeamPlayer, on_delete=models.CASCADE,related_name="east",default=None)
    west = models.ForeignKey(TeamPlayer, on_delete=models.CASCADE,related_name="west",default=None)
